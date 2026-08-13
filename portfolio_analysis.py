"""
Portfolio optimisation for the Productivity Bond Model.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Optional, List

from config import ModelConfig, DEFAULT_CONFIG, get_config
from state_generator import EconomicPaths
from bond_valuation import (
    compute_coupons,
    present_value_cost,
    evaluate_bond,
)


def optimise_portfolio(
    paths: EconomicPaths,
    cfg: Optional[ModelConfig] = None,
    bond_type: str = "productivity",
) -> pd.DataFrame:
    """
    Find the optimal mix of conventional debt and a state-contingent bond.
    """
    if cfg is None:
        cfg = DEFAULT_CONFIG

    conv_coupons = compute_coupons(paths, "conventional", cfg)
    pb_coupons = compute_coupons(paths, bond_type, cfg)
    debt = paths.d  # <-- FIXED: Use the same debt path for all bonds

    results = []
    for share in cfg.share_grid:
        weighted_coupons = (1 - share) * conv_coupons + share * pb_coupons

        pv_cost = present_value_cost(weighted_coupons, cfg, paths)
        expected_cost = float(np.mean(pv_cost))
        cost_vol = float(np.std(pv_cost))

        debt_service = weighted_coupons * debt
        distress_ratio = debt_service / paths.r
        distress_bool = distress_ratio > cfg.distress_threshold
        distress_prob = float(np.mean(np.any(distress_bool, axis=1)))

        welfare = expected_cost + cfg.kappa * (cost_vol ** 2) + cfg.eta * distress_prob
        eff_yield = float(np.mean(weighted_coupons))

        results.append({
            "share": share,
            "expected_cost": expected_cost,
            "cost_volatility": cost_vol,
            "distress_prob": distress_prob,
            "welfare": welfare,
            "effective_yield": eff_yield,
        })

    return pd.DataFrame(results)


def optimise_portfolio_with_theta(
    paths: EconomicPaths,
    cfg: Optional[ModelConfig] = None,
    bond_type: str = "productivity",
    theta_grid: Optional[List[float]] = None,
) -> pd.DataFrame:
    if cfg is None:
        cfg = DEFAULT_CONFIG
    if theta_grid is None:
        theta_grid = [0.10, 0.20, 0.30, 0.40, 0.50]

    results = []
    for theta in theta_grid:
        cfg_theta = get_config(theta_ai=theta)
        df_port = optimise_portfolio(paths, cfg_theta, bond_type)
        best_idx = df_port["welfare"].idxmin()
        best_row = df_port.loc[best_idx]
        results.append({
            "theta_ai": theta,
            "optimal_share": best_row["share"],
            "min_welfare": best_row["welfare"],
            "expected_cost": best_row["expected_cost"],
            "distress_prob": best_row["distress_prob"],
        })

    return pd.DataFrame(results)


def portfolio_summary(
    paths: EconomicPaths,
    cfg: Optional[ModelConfig] = None,
) -> pd.DataFrame:
    if cfg is None:
        cfg = DEFAULT_CONFIG

    conv_metrics = evaluate_bond(paths, "conventional", cfg)
    conv_cost = conv_metrics["expected_cost"]
    conv_distress = conv_metrics["distress_prob"]
    conv_welfare = conv_metrics["welfare"]

    df_opt = optimise_portfolio(paths, cfg, "productivity")
    best_idx = df_opt["welfare"].idxmin()
    best = df_opt.loc[best_idx]
    opt_share = best["share"]
    opt_cost = best["expected_cost"]
    opt_distress = best["distress_prob"]
    opt_welfare = best["welfare"]

    prod_metrics = evaluate_bond(paths, "productivity", cfg)
    prod_cost = prod_metrics["expected_cost"]
    prod_distress = prod_metrics["distress_prob"]
    prod_welfare = prod_metrics["welfare"]

    summary = pd.DataFrame({
        "strategy": ["Conventional Only", "Optimal Portfolio", "Productivity Only"],
        "share": [0.0, opt_share, 1.0],
        "expected_cost": [conv_cost, opt_cost, prod_cost],
        "distress_prob": [conv_distress, opt_distress, prod_distress],
        "welfare": [conv_welfare, opt_welfare, prod_welfare],
    })

    summary["cost_improvement"] = summary["expected_cost"] - conv_cost
    summary["distress_improvement"] = summary["distress_prob"] - conv_distress
    summary["welfare_improvement"] = summary["welfare"] - conv_welfare

    return summary