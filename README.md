# Productivity Bond Model

**Simulation code for *The Infinite Debt Problem: How to Replace Perpetual Growth with Productive Prosperity***

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Book](https://img.shields.io/badge/Book-PDF-blue)](book/The_Infinite_Debt_Problem.pdf)
[![Policy Brief](https://img.shields.io/badge/Policy-Brief-green)](policy_brief.md)

---

## 🚀 Simulation Status Update (August 2026)

> **Endogenous Debt Feedback Loop:** The model now fully implements instrument-specific debt dynamics. Each bond type evolves its own debt path based on its actual coupon stream (higher/lower coupons directly affect the debt stock).  
> **Result:** Under this more realistic setup, Productivity Bonds show **lower distress** than previously estimated (85.7% vs 88.2%), reinforcing their appeal.  
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
| `results/` | Simulation results from the book (CSV format) |

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

The results CSV files are in the results/ directory:

    bond_comparison.csv – comparison of all five bond types

    portfolio_results.csv – portfolio optimisation results

    sensitivity_*.csv – parameter sensitivity analysis

4. Build the Simulation

Follow the specification in ROADMAP.md. The simulation engine is under active development – see CONTRIBUTING.md if you'd like to help.
Results Summary (Updated — Endogenous Debt)
Bond Type	Expected Cost	Distress Prob.	Welfare	Effective Yield
Conventional	0.5154	11.05%	1.0687	4.00%
Inflation‑Linked	0.4896	66.90%	3.8384	3.55%
GDP‑Linked	0.5114	88.50%	4.9419	3.97%
Productivity	0.4994	85.68%	4.7889	3.74%
Hybrid	0.5272	93.93%	5.2297	4.25%
Key Finding

The Productivity Bond reduces expected financing costs by ~3.1% compared to conventional debt (0.5154 → 0.4994).

Critically, under the fully endogenous debt feedback loop, the distress probability for Productivity Bonds is 85.7%—this is 2.5 percentage points lower than under the old static-debt assumption (88.2%). This means the dynamic coupon structure does not amplify fiscal distress; instead, the lower average coupon (3.74% vs 4.00% conventional) leads to slower debt accumulation over the cycle.

The optimal portfolio allocation remains ~30% Productivity Bonds / 70% conventional debt under this calibration.
License

    Code: MIT License – see LICENSE

    Book content: Creative Commons BY‑NC‑ND 4.0 – see license details

Contact

    Author: Ylia Callan

    Book: The Infinite Debt Problem

    GitHub Issues: Submit a question or suggestion