"""
Portfolio optimisation: mix of conventional and Productivity / Hybrid bonds.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Dict, List, Optional

from config import ModelConfig, DEFAULT_CONFIG
from state_generator import EconomicPaths
from bond_valuation import compute_coupons, present_value_cost
from government_welfare import fiscal_distress


def blended_coupons(paths, share_prod, cfg, prod_type="productivity"):
    c_conv = compute_coupons(paths, "conventional", cfg)
    c_prod = compute_coupons(paths, prod_type, cfg)
    return (1.0 - share_prod) * c_conv + share_prod * c_prod


def portfolio_metrics(paths, share, cfg, prod_type="productivity"):
    coupons = blended_coupons(paths, share, cfg, prod_type)
    pv_cost = present_value_cost(coupons, cfg)

    expected_cost = float(np.mean(pv_cost))
    var_cost = float(np.var(pv_cost, ddof=1))
    distress = fiscal_distress(coupons, paths, cfg)
    distress_prob = float(np.mean(distress.any(axis=1)))

    welfare = expected_cost + cfg.kappa * var_cost + cfg.eta * distress_prob

    return {
        "share": share,
        "expected_cost": expected_cost,
        "cost_volatility": float(np.std(pv_cost, ddof=1)),
        "distress_prob": distress_prob,
        "welfare": welfare,
        "effective_yield": float(np.mean(coupons)),
    }


def optimise_portfolio(paths, cfg=None, prod_type="productivity"):
    if cfg is None:
        cfg = DEFAULT_CONFIG
    rows = []
    for s in cfg.share_grid:
        rows.append(portfolio_metrics(paths, s, cfg, prod_type))
    df = pd.DataFrame(rows)
    return df.sort_values("welfare").reset_index(drop=True)
