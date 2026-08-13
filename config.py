"""
Configuration and parameters for the Productivity Bond Model.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ModelConfig:
    """Core simulation parameters."""

    # Simulation settings
    n_paths: int = 10_000
    n_years: int = 10
    seed: int = 42

    # GDP growth process
    mu_y: float = 0.025
    sigma_y: float = 0.020
    rho_y: float = 0.30

    # NPI growth process
    mu_n: float = 0.020
    sigma_n: float = 0.025
    rho_n: float = 0.20
    rho_ny: float = 0.60

    # Inflation process
    mu_pi: float = 0.020
    sigma_pi: float = 0.015
    rho_pi: float = 0.40
    gamma_y: float = 0.25

    # Fiscal parameters
    tau: float = 0.32
    theta_ai: float = 0.30
    phi: float = 0.70
    g0_over_y0: float = 0.30
    d0_over_y0: float = 0.60
    y0: float = 100.0

    # AI shock structure
    lambda_ai: float = 0.05
    ai_shape: float = 2.0
    ai_scale: float = 0.03
    ai_npi_mult: float = 1.0
    ai_gdp_mult: float = 0.7
    ai_emp_mult: float = -0.5
    ai_pi_mult: float = -0.2

    # Bond coupon parameters
    conventional_coupon: float = 0.04
    inflation_real_spread: float = 0.015
    alpha_n: float = 0.70
    alpha_g: float = 0.70
    alpha_f: float = 0.30
    floor: float = 0.00
    cap: float = 0.05

    # Pricing
    r_f: float = 0.02
    gamma_risk: float = 0.50
    lambda_ai_risk: float = 0.10

    # Government welfare
    kappa: float = 2.0
    eta: float = 5.0
    distress_threshold: float = 0.15

    # Portfolio optimisation
    share_grid: Tuple[float, ...] = (
        0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50
    )


DEFAULT_CONFIG = ModelConfig()


def get_config(**overrides) -> ModelConfig:
    """Return a ModelConfig with optional overrides."""
    if not overrides:
        return DEFAULT_CONFIG
    base = DEFAULT_CONFIG.__dict__.copy()
    base.update(overrides)
    return ModelConfig(**base)
