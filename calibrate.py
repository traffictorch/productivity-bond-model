#!/usr/bin/env python3
"""
Calibration search to match the book's distress probabilities.
"""

import numpy as np
import pandas as pd
from config import get_config
from state_generator import simulate_paths
from bond_valuation import evaluate_bond

def run_calibration(g0, threshold, n_paths=2000, n_years=10, seed=42):
    """Run a single calibration point with its own paths."""
    cfg = get_config(
        n_paths=n_paths,
        n_years=n_years,
        seed=seed,
        g0_over_y0=g0,
        distress_threshold=threshold
    )
    paths = simulate_paths(cfg)
    conv = evaluate_bond(paths, "conventional", cfg)
    prod = evaluate_bond(paths, "productivity", cfg)
    hybrid = evaluate_bond(paths, "hybrid", cfg)
    return {
        "g0_over_y0": g0,
        "threshold": threshold,
        "conv_distress": conv["distress_prob"],
        "prod_distress": prod["distress_prob"],
        "hybrid_distress": hybrid["distress_prob"],
        "conv_cost": conv["expected_cost"],
        "prod_cost": prod["expected_cost"],
        "conv_debt": conv.get("debt_mean", None),  # if added to evaluate_bond
    }

if __name__ == "__main__":
    # Grid search
    results = []
    for g0 in [0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36]:
        for threshold in [0.12, 0.13, 0.14, 0.15, 0.16, 0.18]:
            res = run_calibration(g0, threshold)
            results.append(res)
            print(f"g0={g0:.2f}, thresh={threshold:.2f}: "
                  f"conv={res['conv_distress']*100:.1f}%, "
                  f"prod={res['prod_distress']*100:.1f}%")
    
    # Save results
    df = pd.DataFrame(results)
    df.to_csv("calibration_results_fixed.csv", index=False)
    print("\nResults saved to calibration_results_fixed.csv")
    
    # Show best match to book targets
    target_conv = 0.1832
    target_prod = 0.1421
    df['conv_error'] = (df['conv_distress'] - target_conv).abs()
    df['prod_error'] = (df['prod_distress'] - target_prod).abs()
    df['total_error'] = df['conv_error'] + df['prod_error']
    best = df.loc[df['total_error'].idxmin()]
    print("\nBest match to book targets:")
    print(f"g0_over_y0 = {best['g0_over_y0']:.2f}")
    print(f"distress_threshold = {best['threshold']:.2f}")
    print(f"conv_distress = {best['conv_distress']*100:.2f}% (target: 18.32%)")
    print(f"prod_distress = {best['prod_distress']*100:.2f}% (target: 14.21%)")