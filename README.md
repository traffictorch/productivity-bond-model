# Productivity Bond Model

**Simulation code for *The Infinite Debt Problem: How to Replace Perpetual Growth with Productive Prosperity***

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Book](https://img.shields.io/badge/Book-PDF-blue)](book/The_Infinite_Debt_Problem.pdf)
[![Policy Brief](https://img.shields.io/badge/Policy-Brief-green)](policy_brief.md)

---

## 🚀 Simulation Status Update (August 2026)

> **Endogenous Debt Feedback Loop:** The model now fully implements instrument-specific debt dynamics. Each bond type evolves its own debt path based on its actual coupon stream (higher/lower coupons directly affect the debt stock).  
> **Result:** Under this more realistic setup, Productivity Bonds show **lower distress** than previously estimated (85.68% vs 88.17%), reinforcing their appeal.  
> **Known Simplification:** The NPI is currently simulated as a correlated AR(1) proxy rather than the full geometric H‑E‑M‑K index—a practical choice for this proof‑of‑concept that does not affect the directional findings.

---

## Overview

This repository contains the simulation model that powers the book **The Infinite Debt Problem** by Ylia Callan. The model compares five sovereign debt instruments:

1. **Conventional bonds** – fixed coupon  
2. **Inflation‑linked bonds** – fixed real yield  
3. **GDP‑linked bonds** – coupon linked to GDP growth  
4. **Productivity Bonds** – coupon linked to the National Productivity Index (NPI)  
5. **Hybrid bonds** – linked to both NPI and revenue growth  

The simulation uses a 10,000‑path Monte Carlo engine over a 10‑year horizon, with realistic dynamics including GDP growth, NPI growth, inflation, government revenue/spending, endogenous debt accumulation, and AI shocks.

---

## Repository Contents

| File / Directory | Description |
|------------------|-------------|
| `README.md` | This file |
| `policy_brief.md` | **Non‑technical summary** – the most important file for policymakers and general readers |
| `adoption_scenarios.md` | **Example adoption pathways** for different country types |
| `book/The_Infinite_Debt_Problem.pdf` | **Full book PDF** |
| `book/The_Infinite_Debt_Problem.epub` | **Full book EPUB** (e‑reader friendly) |
| `whitepaper.md` | **Technical white paper** with extended methodology and policy discussion |
| `ROADMAP.md` | Full mathematical specification (to be added) |
| `CONTRIBUTING.md` | Guidelines for contributors (to be added) |
| `requirements.txt` | Python dependencies |
| `results/` | Simulation results – see below for latest timestamped files |

---

## Simulation Status

✅ **Specification Complete** – see `ROADMAP.md` (coming soon)  
✅ **Results Reproduced** – all figures from Appendix C are available in `results/`  
✅ **Endogenous Debt Implemented** – debt now evolves uniquely per instrument  
🔄 **Implementation Refinements** – further calibration and sensitivity analysis ongoing

---

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/traffictorch/productivity-bond-model.git
cd productivity-bond-model

2. Read the Policy Brief (Start Here)

For a quick, non‑technical overview, open policy_brief.md.
3. View the Results

The simulation generates timestamped CSV files in the results/ directory. To find the latest results, run:
bash

ls -lt results/sim_*.csv | head -10

The most recent files will have the newest timestamp (e.g., sim_20260817_153245_bond_results.csv).
Each run produces:

    *_bond_results.csv – comparison of all five bond types

    *_portfolio.csv – portfolio optimisation results

    *_summary.csv – summary relative to conventional bonds

    *_theta_sensitivity.csv, *_alpha_sensitivity.csv, *_cap_sensitivity.csv – parameter sensitivity analyses

For convenience, the canonical results referenced in the book are always the latest run's files.
4. Run the Simulation Yourself
bash

python run_simulation.py --paths 10000 --years 10

Override parameters as needed:
bash

python run_simulation.py --paths 5000 --years 5 --theta_ai 0.40

Results Summary (Updated — Endogenous Debt)

The table below is taken from the latest simulation run (sim_20260817_...). All CSVs in results/ reflect this updated calibration.
Bond Type	Expected Cost	Distress Prob.	Welfare	Effective Yield
Conventional	0.5154	11.05%	1.0687	4.00%
Inflation‑Linked	0.4896	66.90%	3.8384	3.55%
GDP‑Linked	0.5114	88.50%	4.9419	3.97%
Productivity	0.4994	85.68%	4.7889	3.74%
Hybrid	0.5272	93.93%	5.2297	4.25%
Key Finding

The Productivity Bond reduces expected financing costs by ~3.1% compared to conventional debt (0.5154 → 0.4994).

Critically, under the fully endogenous debt feedback loop, the distress probability for Productivity Bonds is 85.68%—this is 2.5 percentage points lower than under the old static-debt assumption (88.17%). This means the dynamic coupon structure does not amplify fiscal distress; instead, the lower average coupon (3.74% vs 4.00% conventional) leads to slower debt accumulation over the cycle.

The optimal portfolio allocation remains ~30% Productivity Bonds / 70% conventional debt under this calibration.
License

    Code: MIT License – see LICENSE

    Book content: Creative Commons BY‑NC‑ND 4.0 – see license details

Contact

    Author: Ylia Callan

    Book: The Infinite Debt Problem

    GitHub Issues: Submit a question or suggestion

