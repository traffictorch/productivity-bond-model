"""
Government welfare, fiscal distress and cost metrics.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, List, Optional

from config import ModelConfig, DEFAULT_CONFIG
from state_generator import EconomicPaths
from bond_valuation import compute_coupons, present_value_cost, effective_yield


def debt_service_ratio(coupons, paths):
    service = coupons * paths.d
    return service / np.maximum(paths.r, 1e-8)


def fiscal_distress(coupons, paths, cfg):
    ratio = debt_service_ratio(coupons, paths)
    return ratio > cfg.distress_threshold


def welfare_metrics(paths, bond_type, cfg=None):
    if cfg is None:
        cfg = DEFAULT_CONFIG

    coupons = compute_coupons(paths, bond_type, cfg)
    pv_cost = present_value_cost(coupons, cfg, paths)

    expected_cost = float(np.mean(pv_cost))
    cost_vol = float(np.std(pv_cost, ddof=1))
    var_cost = float(np.var(pv_cost, ddof=1))

    distress = fiscal_distress(coupons, paths, cfg)
    distress_prob = float(np.mean(distress.any(axis=1)))
    avg_years_in_distress = float(np.mean(distress))

    welfare = expected_cost + cfg.kappa * var_cost + cfg.eta * distress_prob

    return {
        "bond_type": bond_type,
        "expected_cost": expected_cost,
        "cost_volatility": cost_vol,
        "distress_prob": distress_prob,
        "avg_years_distress": avg_years_in_distress,
        "welfare": welfare,
        "effective_yield": effective_yield(coupons),
        "price": expected_cost,
    }


def compare_all_bonds(paths, cfg=None):
    if cfg is None:
        cfg = DEFAULT_CONFIG
    bond_types = [
        "conventional",
        "inflation_linked",
        "gdp_linked",
        "productivity",
        "hybrid",
    ]
    return [welfare_metrics(paths, bt, cfg) for bt in bond_types]
