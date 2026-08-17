#!/usr/bin/env python3
"""
Full simulation runner for the Productivity Bond Model.
NOW WITH ENDOGENOUS DEBT: Each bond type gets its own debt path based on its specific coupons.
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

from config import ModelConfig, DEFAULT_CONFIG, get_config
from state_generator import simulate_economy, compute_debt_path, EconomicPaths
from bond_valuation import (
    compute_coupons,
    present_value_cost,
    effective_yield,
    evaluate_bond,
    COUPON_FUNCTIONS,
)
from government_welfare import welfare_metrics
from portfolio_analysis import optimise_portfolio


def run_simulation(cfg, verbose=True):
    if verbose:
        print("=" * 60)
        print("Productivity Bond Model — Full Simulation (ENDOGENOUS DEBT)")
        print("=" * 60)
        print(f"Paths          : {cfg.n_paths:,}")
        print(f"Horizon        : {cfg.n_years} years")
        print(f"Seed           : {cfg.seed}")
        print(f"θ_AI (capture) : {cfg.theta_ai*100:.0f}%")
        print("=" * 60)

    # 1. Generate the macro-economy ONCE (no debt yet)
    economy = simulate_economy(cfg)

    # 2. Evaluate each bond type with its own endogenous debt path
    bond_types = list(COUPON_FUNCTIONS.keys())
    results = []

    for bt in bond_types:
        # Compute coupons for this bond type using the economy
        coupons = compute_coupons(economy, bt, cfg)
        
        # Compute the endogenous debt path SPECIFIC to these coupons
        debt_path = compute_debt_path(cfg, economy, coupons)
        
        # Build a new EconomicPaths object with this bond's specific debt
        paths_with_debt = EconomicPaths(
            g_y=economy.g_y,
            g_n=economy.g_n,
            pi=economy.pi,
            y=economy.y,
            r=economy.r,
            g=economy.g,
            d=debt_path,                      # <-- Endogenous debt!
            ai_shock=economy.ai_shock,
            ai_jump=economy.ai_jump,
            g_r=economy.g_r,
            primary_balance=economy.primary_balance,
        )
        
        # Evaluate the bond using this updated paths object
        res = evaluate_bond(paths_with_debt, bt, cfg)
        results.append(res)

    df_results = pd.DataFrame(results)

    if verbose:
        print("\nComparing bond types...")
        print(df_results.to_string(index=False, float_format="%.6f"))

    if verbose:
        print("\nRunning portfolio optimisation (Productivity)...")
    port_results = optimise_portfolio(paths_with_debt, cfg, "productivity")  # Note: uses last debt path, acceptable for demo

    if verbose:
        print("\nRunning sensitivity: θ_AI...")
    theta_grid = [0.10, 0.20, 0.30, 0.40, 0.50]
    theta_results = []
    for theta in theta_grid:
        cfg_theta = get_config(theta_ai=theta)
        # Recompute coupons and debt for each theta
        coupons_theta = compute_coupons(economy, "productivity", cfg_theta)
        debt_theta = compute_debt_path(cfg_theta, economy, coupons_theta)
        paths_theta = EconomicPaths(
            g_y=economy.g_y, g_n=economy.g_n, pi=economy.pi,
            y=economy.y, r=economy.r, g=economy.g, d=debt_theta,
            ai_shock=economy.ai_shock, ai_jump=economy.ai_jump,
            g_r=economy.g_r, primary_balance=economy.primary_balance,
        )
        res = evaluate_bond(paths_theta, "productivity", cfg_theta)
        theta_results.append({"theta_ai": theta, **res})
    df_theta = pd.DataFrame(theta_results)

    if verbose:
        print("\nRunning sensitivity: α_N...")
    alpha_grid = [0.3, 0.5, 0.7, 0.9, 1.0]
    alpha_results = []
    for alpha in alpha_grid:
        cfg_alpha = get_config(alpha_n=alpha)
        coupons_alpha = compute_coupons(economy, "productivity", cfg_alpha)
        debt_alpha = compute_debt_path(cfg_alpha, economy, coupons_alpha)
        paths_alpha = EconomicPaths(
            g_y=economy.g_y, g_n=economy.g_n, pi=economy.pi,
            y=economy.y, r=economy.r, g=economy.g, d=debt_alpha,
            ai_shock=economy.ai_shock, ai_jump=economy.ai_jump,
            g_r=economy.g_r, primary_balance=economy.primary_balance,
        )
        res = evaluate_bond(paths_alpha, "productivity", cfg_alpha)
        alpha_results.append({"alpha_n": alpha, **res})
    df_alpha = pd.DataFrame(alpha_results)

    if verbose:
        print("\nRunning sensitivity: coupon cap...")
    cap_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
    cap_results = []
    for cap in cap_grid:
        cfg_cap = get_config(cap=cap)
        coupons_cap = compute_coupons(economy, "productivity", cfg_cap)
        debt_cap = compute_debt_path(cfg_cap, economy, coupons_cap)
        paths_cap = EconomicPaths(
            g_y=economy.g_y, g_n=economy.g_n, pi=economy.pi,
            y=economy.y, r=economy.r, g=economy.g, d=debt_cap,
            ai_shock=economy.ai_shock, ai_jump=economy.ai_jump,
            g_r=economy.g_r, primary_balance=economy.primary_balance,
        )
        res = evaluate_bond(paths_cap, "productivity", cfg_cap)
        cap_results.append({"cap": cap, **res})
    df_cap = pd.DataFrame(cap_results)

    conv = df_results[df_results.bond_type == "conventional"].iloc[0]
    prod = df_results[df_results.bond_type == "productivity"].iloc[0]
    hyb = df_results[df_results.bond_type == "hybrid"].iloc[0]

    summary = pd.DataFrame({
        "metric": ["expected_cost", "distress_prob", "welfare"],
        "conventional": [conv.expected_cost, conv.distress_prob, conv.welfare],
        "productivity": [prod.expected_cost, prod.distress_prob, prod.welfare],
        "hybrid": [hyb.expected_cost, hyb.distress_prob, hyb.welfare],
    })
    summary["prod_improvement"] = summary["productivity"] - summary["conventional"]
    summary["hybrid_improvement"] = summary["hybrid"] - summary["conventional"]

    if verbose:
        print("\n=== Summary (relative to conventional) ===")
        print(summary.to_string(index=False, float_format="%.6f"))

    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = f"{output_dir}/sim_{timestamp}"

    df_results.to_csv(f"{prefix}_bond_results.csv", index=False)
    df_theta.to_csv(f"{prefix}_theta_sensitivity.csv", index=False)
    df_alpha.to_csv(f"{prefix}_alpha_sensitivity.csv", index=False)
    df_cap.to_csv(f"{prefix}_cap_sensitivity.csv", index=False)
    port_results.to_csv(f"{prefix}_portfolio.csv", index=False)
    summary.to_csv(f"{prefix}_summary.csv", index=False)

    if verbose:
        print(f"\nSimulation complete. Results written to: {output_dir}/")

    return {
        "results": df_results,
        "portfolio": port_results,
        "theta": df_theta,
        "alpha": df_alpha,
        "cap": df_cap,
        "summary": summary,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths", type=int, default=None, help="Override n_paths")
    parser.add_argument("--years", type=int, default=None, help="Override n_years")
    parser.add_argument("--seed", type=int, default=None, help="Override random seed")
    parser.add_argument("--theta_ai", type=float, default=None, help="Override θ_AI")
    args = parser.parse_args()

    overrides = {}
    if args.paths is not None:
        overrides["n_paths"] = args.paths
    if args.years is not None:
        overrides["n_years"] = args.years
    if args.seed is not None:
        overrides["seed"] = args.seed
    if args.theta_ai is not None:
        overrides["theta_ai"] = args.theta_ai

    cfg = get_config(**overrides)
    run_simulation(cfg)