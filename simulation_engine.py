"""
Main simulation engine.
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Dict, Optional

from config import ModelConfig, DEFAULT_CONFIG, get_config
from state_generator import simulate_paths
from government_welfare import compare_all_bonds, welfare_metrics
from portfolio_analysis import optimise_portfolio


def run_bond_comparison(cfg=None):
    if cfg is None:
        cfg = DEFAULT_CONFIG
    paths = simulate_paths(cfg)
    results = compare_all_bonds(paths, cfg)
    df = pd.DataFrame(results)
    cols = [
        "bond_type", "expected_cost", "cost_volatility",
        "distress_prob", "welfare", "effective_yield", "price",
    ]
    return df[cols]


def run_sensitivity_theta(theta_values=None, base_cfg=None):
    if base_cfg is None:
        base_cfg = DEFAULT_CONFIG
    if theta_values is None:
        theta_values = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    rows = []
    for theta in theta_values:
        cfg = get_config(theta_ai=theta, seed=base_cfg.seed, n_paths=base_cfg.n_paths)
        paths = simulate_paths(cfg)
        m_conv = welfare_metrics(paths, "conventional", cfg)
        m_prod = welfare_metrics(paths, "productivity", cfg)
        rows.append({
            "theta_ai": theta,
            "conv_expected_cost": m_conv["expected_cost"],
            "prod_expected_cost": m_prod["expected_cost"],
            "cost_improvement": (m_prod["expected_cost"] - m_conv["expected_cost"]) / m_conv["expected_cost"],
            "conv_distress": m_conv["distress_prob"],
            "prod_distress": m_prod["distress_prob"],
            "distress_improvement": (m_prod["distress_prob"] - m_conv["distress_prob"]) / max(m_conv["distress_prob"], 1e-8),
        })
    return pd.DataFrame(rows)


def run_sensitivity_alpha(alpha_values=None, base_cfg=None):
    if base_cfg is None:
        base_cfg = DEFAULT_CONFIG
    if alpha_values is None:
        alpha_values = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
    rows = []
    for alpha in alpha_values:
        cfg = get_config(alpha_n=alpha, seed=base_cfg.seed, n_paths=base_cfg.n_paths)
        paths = simulate_paths(cfg)
        m = welfare_metrics(paths, "productivity", cfg)
        rows.append({
            "alpha_n": alpha,
            "expected_cost": m["expected_cost"],
            "distress_prob": m["distress_prob"],
            "welfare": m["welfare"],
            "effective_yield": m["effective_yield"],
        })
    return pd.DataFrame(rows)


def run_sensitivity_cap(cap_values=None, base_cfg=None):
    if base_cfg is None:
        base_cfg = DEFAULT_CONFIG
    if cap_values is None:
        cap_values = [0.03, 0.04, 0.05, 0.06, 0.07, 0.08]
    rows = []
    for cap in cap_values:
        cfg = get_config(cap=cap, seed=base_cfg.seed, n_paths=base_cfg.n_paths)
        paths = simulate_paths(cfg)
        m = welfare_metrics(paths, "productivity", cfg)
        rows.append({
            "cap": cap,
            "expected_cost": m["expected_cost"],
            "distress_prob": m["distress_prob"],
            "welfare": m["welfare"],
            "effective_yield": m["effective_yield"],
        })
    return pd.DataFrame(rows)


def run_full_simulation(output_dir="results", cfg=None):
    if cfg is None:
        cfg = DEFAULT_CONFIG
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating economic paths...")
    paths = simulate_paths(cfg)

    print("Comparing bond types...")
    bond_df = pd.DataFrame(compare_all_bonds(paths, cfg))
    cols = [
        "bond_type", "expected_cost", "cost_volatility",
        "distress_prob", "welfare", "effective_yield", "price",
    ]
    bond_df = bond_df[cols]
    bond_df.to_csv(output_dir / "bond_comparison.csv", index=False)
    print(bond_df.to_string(index=False))

    print("\nRunning portfolio optimisation (Productivity)...")
    port_df = optimise_portfolio(paths, cfg, prod_type="productivity")
    port_df.to_csv(output_dir / "portfolio_results.csv", index=False)

    print("Running sensitivity: θ_AI...")
    sens_theta = run_sensitivity_theta(base_cfg=cfg)
    sens_theta.to_csv(output_dir / "sensitivity_theta.csv", index=False)

    print("Running sensitivity: α_N...")
    sens_alpha = run_sensitivity_alpha(base_cfg=cfg)
    sens_alpha.to_csv(output_dir / "sensitivity_alpha.csv", index=False)

    print("Running sensitivity: coupon cap...")
    sens_cap = run_sensitivity_cap(base_cfg=cfg)
    sens_cap.to_csv(output_dir / "sensitivity_cap.csv", index=False)

    conv = bond_df.loc[bond_df["bond_type"] == "conventional"].iloc[0]
    prod = bond_df.loc[bond_df["bond_type"] == "productivity"].iloc[0]
    hybrid = bond_df.loc[bond_df["bond_type"] == "hybrid"].iloc[0]

    summary = pd.DataFrame([
        {
            "metric": "expected_cost",
            "conventional": conv["expected_cost"],
            "productivity": prod["expected_cost"],
            "hybrid": hybrid["expected_cost"],
            "prod_improvement": (prod["expected_cost"] - conv["expected_cost"]) / conv["expected_cost"],
            "hybrid_improvement": (hybrid["expected_cost"] - conv["expected_cost"]) / conv["expected_cost"],
        },
        {
            "metric": "distress_prob",
            "conventional": conv["distress_prob"],
            "productivity": prod["distress_prob"],
            "hybrid": hybrid["distress_prob"],
            "prod_improvement": (prod["distress_prob"] - conv["distress_prob"]) / max(conv["distress_prob"], 1e-8),
            "hybrid_improvement": (hybrid["distress_prob"] - conv["distress_prob"]) / max(conv["distress_prob"], 1e-8),
        },
        {
            "metric": "welfare",
            "conventional": conv["welfare"],
            "productivity": prod["welfare"],
            "hybrid": hybrid["welfare"],
            "prod_improvement": (prod["welfare"] - conv["welfare"]) / conv["welfare"],
            "hybrid_improvement": (hybrid["welfare"] - conv["welfare"]) / conv["welfare"],
        },
    ])
    summary.to_csv(output_dir / "summary_statistics.csv", index=False)

    print("\n=== Summary (relative to conventional) ===")
    print(summary.to_string(index=False))

    return {
        "bond_comparison": bond_df,
        "portfolio": port_df,
        "sensitivity_theta": sens_theta,
        "sensitivity_alpha": sens_alpha,
        "sensitivity_cap": sens_cap,
        "summary": summary,
    }
