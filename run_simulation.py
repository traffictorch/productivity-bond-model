#!/usr/bin/env python3
"""Entry point for the Productivity Bond Model simulation."""

from __future__ import annotations

import argparse
from pathlib import Path

from config import get_config
from simulation_engine import run_full_simulation


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Productivity Bond Monte Carlo simulation")
    parser.add_argument("--paths", type=int, default=10_000)
    parser.add_argument("--years", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--theta", type=float, default=0.30)
    parser.add_argument("--output", type=str, default="results")
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = get_config(
        n_paths=args.paths,
        n_years=args.years,
        seed=args.seed,
        theta_ai=args.theta,
    )
    print("=" * 60)
    print("Productivity Bond Model — Full Simulation")
    print("=" * 60)
    print(f"Paths          : {cfg.n_paths:,}")
    print(f"Horizon        : {cfg.n_years} years")
    print(f"Seed           : {cfg.seed}")
    print(f"θ_AI (capture) : {cfg.theta_ai:.0%}")
    print(f"Output dir     : {args.output}")
    print("=" * 60)
    run_full_simulation(output_dir=args.output, cfg=cfg)
    print("\nSimulation complete. Results written to:", Path(args.output).resolve())


if __name__ == "__main__":
    main()
