"""
State variable generation for the Productivity Bond Model.
Now supports endogenous debt: debt path is computed separately for each coupon series.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Optional, Dict, Any

from config import ModelConfig, DEFAULT_CONFIG


@dataclass
class EconomicPaths:
    """Container for all simulated state variables (shape: n_paths × n_years)."""

    g_y: np.ndarray
    g_n: np.ndarray
    pi: np.ndarray
    y: np.ndarray
    r: np.ndarray          # Revenue
    g: np.ndarray          # Government spending
    d: np.ndarray          # Debt (will be filled later per bond type)
    ai_shock: np.ndarray
    ai_jump: np.ndarray
    g_r: np.ndarray        # Revenue growth
    primary_balance: np.ndarray


def generate_shocks(n_paths, n_years, rho_ny, rng):
    z_y = rng.standard_normal((n_paths, n_years))
    z_n_indep = rng.standard_normal((n_paths, n_years))
    z_pi = rng.standard_normal((n_paths, n_years))
    z_n = rho_ny * z_y + np.sqrt(max(0.0, 1.0 - rho_ny**2)) * z_n_indep
    return z_y, z_n, z_pi


def generate_ai_shocks(n_paths, n_years, lambda_ai, shape, scale, rng):
    shock = rng.random((n_paths, n_years)) < lambda_ai
    jump = np.zeros((n_paths, n_years))
    n_shocks = int(shock.sum())
    if n_shocks > 0:
        jump[shock] = rng.gamma(shape, scale, size=n_shocks)
    return shock.astype(float), jump


def simulate_economy(cfg: Optional[ModelConfig] = None) -> EconomicPaths:
    """
    Simulate the macroeconomic variables (GDP, inflation, revenue, primary balance).
    Debt (d) is initialized to zero here - it will be overridden by compute_debt_path().
    """
    if cfg is None:
        cfg = DEFAULT_CONFIG

    rng = np.random.default_rng(cfg.seed)
    n_paths = cfg.n_paths
    n_years = cfg.n_years

    z_y, z_n, z_pi = generate_shocks(n_paths, n_years, cfg.rho_ny, rng)
    ai_shock, ai_jump = generate_ai_shocks(
        n_paths, n_years, cfg.lambda_ai, cfg.ai_shape, cfg.ai_scale, rng
    )

    g_y = np.zeros((n_paths, n_years))
    g_n = np.zeros((n_paths, n_years))
    pi = np.zeros((n_paths, n_years))
    y = np.zeros((n_paths, n_years))
    r = np.zeros((n_paths, n_years))
    g_spend = np.zeros((n_paths, n_years))
    g_r = np.zeros((n_paths, n_years))
    primary_balance = np.zeros((n_paths, n_years))

    g_y_prev = np.full(n_paths, cfg.mu_y)
    g_n_prev = np.full(n_paths, cfg.mu_n)
    pi_prev = np.full(n_paths, cfg.mu_pi)
    y_prev = np.full(n_paths, cfg.y0)
    r_prev = cfg.tau * cfg.y0

    for t in range(n_years):
        ai_gdp = cfg.ai_gdp_mult * ai_jump[:, t]
        ai_npi = cfg.ai_npi_mult * ai_jump[:, t]
        ai_pi = cfg.ai_pi_mult * ai_jump[:, t]

        g_y[:, t] = (
            cfg.mu_y
            + cfg.rho_y * (g_y_prev - cfg.mu_y)
            + cfg.sigma_y * z_y[:, t]
            + ai_gdp
        )
        g_n[:, t] = (
            cfg.mu_n
            + cfg.rho_n * (g_n_prev - cfg.mu_n)
            + cfg.sigma_n * z_n[:, t]
            + ai_npi
        )
        pi[:, t] = (
            cfg.mu_pi
            + cfg.rho_pi * (pi_prev - cfg.mu_pi)
            + cfg.sigma_pi * z_pi[:, t]
            + cfg.gamma_y * (g_y[:, t] - cfg.mu_y)
            + ai_pi
        )

        y[:, t] = y_prev * (1.0 + g_y[:, t])
        ai_gain = np.maximum(y_prev * ai_gdp, 0.0)

        r[:, t] = cfg.tau * y[:, t] + cfg.theta_ai * ai_gain
        g_r[:, t] = np.where(r_prev > 1e-8, (r[:, t] / r_prev) - 1.0, 0.0)

        # Spending: baseline + automatic stabilizer (countercyclical)
        auto_stab = -0.05 * (g_y[:, t] - cfg.mu_y) * y[:, t]
        g_spend[:, t] = (
            cfg.g0_over_y0 * y[:, t] * (1.0 + 0.3 * (g_y[:, t] - cfg.mu_y))
            + auto_stab
        )
        g_spend[:, t] = np.maximum(g_spend[:, t], 0.10 * y[:, t])

        # Primary balance = revenue - spending
        primary_balance[:, t] = r[:, t] - g_spend[:, t]

        # Update previous values for next iteration
        g_y_prev = g_y[:, t]
        g_n_prev = g_n[:, t]
        pi_prev = pi[:, t]
        y_prev = y[:, t]
        r_prev = r[:, t]

    # Debt is set to zero here. It will be computed later via compute_debt_path().
    d = np.zeros((n_paths, n_years))

    return EconomicPaths(
        g_y=g_y,
        g_n=g_n,
        pi=pi,
        y=y,
        r=r,
        g=g_spend,
        d=d,
        ai_shock=ai_shock,
        ai_jump=ai_jump,
        g_r=g_r,
        primary_balance=primary_balance,
    )


def compute_debt_path(
    cfg: ModelConfig,
    economy: EconomicPaths,
    coupon_series: np.ndarray
) -> np.ndarray:
    """
    Roll forward the debt stock using the given coupon series (endogenous).
    
    Args:
        cfg: Model configuration
        economy: EconomicPaths containing primary_balance, etc.
        coupon_series: Shape (n_paths, n_years) - the specific coupons for this bond type.
    
    Returns:
        d: Shape (n_paths, n_years) - the debt path for this specific bond type.
    """
    n_paths, n_years = coupon_series.shape
    d = np.zeros((n_paths, n_years))
    
    # Initial debt
    d_prev = np.full(n_paths, cfg.d0_over_y0 * cfg.y0)
    
    for t in range(n_years):
        # Use the specific coupon for this bond type at time t
        current_coupon = coupon_series[:, t]
        
        # Debt rollover: d_t = d_{t-1} * (1 + coupon_t) - primary_balance_t
        d[:, t] = d_prev * (1.0 + current_coupon) - economy.primary_balance[:, t]
        d[:, t] = np.maximum(d[:, t], 0.0)  # Debt cannot be negative
        
        d_prev = d[:, t]
    
    return d


# Legacy alias for backward compatibility (deprecated, but prevents crashes)
def simulate_paths(cfg: Optional[ModelConfig] = None) -> EconomicPaths:
    """
    DEPRECATED: Kept for backward compatibility.
    This now returns the economy with zero debt.
    Use simulate_economy() + compute_debt_path() instead.
    """
    return simulate_economy(cfg)