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


def physical_discount_factors(n_years, r_f):
    t = np.arange(1, n_years + 1, dtype=float)
    return 1.0 / (1.0 + r_f) ** t


def present_value_cost(coupons, cfg, face=1.0):
    n_paths, n_years = coupons.shape
    df = physical_discount_factors(n_years, cfg.r_f)
    pv_coupons = (coupons * df).sum(axis=1)
    pv_principal = df[-1] * face
    return pv_coupons + pv_principal


def effective_yield(coupons):
    return float(np.mean(coupons))
