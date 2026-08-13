"""
Bond coupon formulas and valuation.
"""

from __future__ import annotations

import numpy as np
from typing import Optional

from config import ModelConfig, DEFAULT_CONFIG
from state_generator import EconomicPaths


def coupon_conventional(paths, cfg):
    return np.full_like(paths.g_y, cfg.conventional_coupon)


def coupon_inflation_linked(paths, cfg):
    return (1.0 + paths.pi) * (1.0 + cfg.inflation_real_spread) - 1.0


def coupon_gdp_linked(paths, cfg):
    real_part = np.clip(cfg.alpha_g * paths.g_y, cfg.floor, cfg.cap)
    return (1.0 + paths.pi) * (1.0 + real_part) - 1.0


def coupon_productivity(paths, cfg):
    real_part = np.clip(cfg.alpha_n * paths.g_n, cfg.floor, cfg.cap)
    return (1.0 + paths.pi) * (1.0 + real_part) - 1.0


def coupon_hybrid(paths, cfg):
    real_part = np.clip(
        cfg.alpha_n * paths.g_n + cfg.alpha_f * paths.g_r, cfg.floor, cfg.cap
    )
    return (1.0 + paths.pi) * (1.0 + real_part) - 1.0


COUPON_FUNCTIONS = {
    "conventional": coupon_conventional,
    "inflation_linked": coupon_inflation_linked,
    "gdp_linked": coupon_gdp_linked,
    "productivity": coupon_productivity,
    "hybrid": coupon_hybrid,
}


def compute_coupons(paths, bond_type, cfg=None):
    if cfg is None:
        cfg = DEFAULT_CONFIG
    if bond_type not in COUPON_FUNCTIONS:
        raise ValueError(f"Unknown bond type: {bond_type}")
    return COUPON_FUNCTIONS[bond_type](paths, cfg)


def present_value_cost(coupons, cfg, paths, face=1.0):
    """
    Compute the present value of debt service using risk-adjusted discounting.
    """
    n_paths, n_years = coupons.shape
    t = np.arange(1, n_years + 1, dtype=float)

    eps_y = paths.g_y - cfg.mu_y
    cum_eps_y = np.cumsum(eps_y, axis=1)

    df = np.exp(
        -cfg.r_f * t
        - cfg.gamma_risk * cum_eps_y
        - cfg.lambda_ai_risk * t
    )

    pv_coupons = (coupons * df).sum(axis=1)
    pv_principal = df[:, -1] * face

    return pv_coupons + pv_principal


def effective_yield(coupons):
    return float(np.mean(coupons))


def evaluate_bond(paths, bond_type, cfg):
    """Return metrics for a single bond type."""
    coupons = compute_coupons(paths, bond_type, cfg)
    debt = paths.d  # <-- FIXED: Use the same debt path for all bond types
    
    pv_cost = present_value_cost(coupons, cfg, paths)
    expected_cost = float(np.mean(pv_cost))
    cost_vol = float(np.std(pv_cost))

    debt_service = coupons * debt
    distress_ratio = debt_service / paths.r
    
    # DEBUG: Print distribution for conventional bond
    if bond_type == "conventional":
        print(f"\n=== DEBUG: {bond_type.capitalize()} Bond ===")
        print(f"distress_ratio stats - min: {distress_ratio.min():.4f}, "
              f"mean: {distress_ratio.mean():.4f}, max: {distress_ratio.max():.4f}")
        print(f"debt stats (final year) - min: {debt[:,-1].min():.2f}, "
              f"mean: {debt[:,-1].mean():.2f}, max: {debt[:,-1].max():.2f}")
        print(f"revenue stats (final year) - min: {paths.r[:,-1].min():.2f}, "
              f"mean: {paths.r[:,-1].mean():.2f}")
        print(f"debt service stats (final year) - min: {debt_service[:,-1].min():.2f}, "
              f"mean: {debt_service[:,-1].mean():.2f}")
        pct_above = (distress_ratio > cfg.distress_threshold).any(axis=1).mean()
        print(f"distress_prob: {pct_above*100:.2f}%")
    
    distress_bool = distress_ratio > cfg.distress_threshold
    distress_prob = float(np.mean(np.any(distress_bool, axis=1)))

    welfare = expected_cost + cfg.kappa * (cost_vol ** 2) + cfg.eta * distress_prob
    eff_yield = effective_yield(coupons)
    price = float(np.mean(present_value_cost(coupons, cfg, paths, face=1.0)))

    return {
        "bond_type": bond_type,
        "expected_cost": expected_cost,
        "cost_volatility": cost_vol,
        "distress_prob": distress_prob,
        "welfare": welfare,
        "effective_yield": eff_yield,
        "price": price,
    }