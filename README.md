# Productivity Bond Model

**Simulation code for *The Infinite Debt Problem: How to Replace Perpetual Growth with Productive Prosperity***

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Book](https://img.shields.io/badge/Book-PDF-blue)](book/The_Infinite_Debt_Problem.pdf)
[![Policy Brief](https://img.shields.io/badge/Policy-Brief-green)](policy_brief.md)

---

##DEMO CAVEATS

⚠️ Proof-of-Concept Notice: This simulation holds the debt path constant across instruments to isolate coupon effects. It does not yet implement endogenous debt feedback (higher coupons → higher borrowing). The NPI is currently simulated as a correlated proxy rather than the full geometric H-E-M-K index. Results are directional/illustrative, not actuarial.

## Overview

This repository contains the simulation model that powers the book **The Infinite Debt Problem** by Ylia Callan. The model compares five sovereign debt instruments:

1. **Conventional bonds** – fixed coupon  
2. **Inflation‑linked bonds** – fixed real yield  
3. **GDP‑linked bonds** – coupon linked to GDP growth  
4. **Productivity Bonds** – coupon linked to the National Productivity Index (NPI)  
5. **Hybrid bonds** – linked to both NPI and revenue growth  

The simulation uses a 10,000‑path Monte Carlo engine over a 10‑year horizon, with realistic dynamics including GDP growth, NPI growth, inflation, employment, government revenue/spending, debt accumulation, and AI shocks.

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
🔄 **Implementation In Progress** – we welcome contributions to complete the full Python simulation engine

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
Results Summary (from Appendix C)
Bond Type	Expected Cost	Distress Prob.	Welfare	Effective Yield
Conventional	0.5154	11.05%	1.0687	4.00%
Inflation‑Linked	0.4896	70.22%	4.0044	3.55%
GDP‑Linked	0.5114	90.32%	5.0329	3.97%
Productivity	0.4994	88.17%	4.9134	3.74%
Hybrid	0.5272	94.63%	5.2647	4.25%

    Key Finding: The Productivity Bond reduces expected financing costs by ~3.1% compared to conventional debt. However, the dynamic feedback loop between higher coupons in good years and debt accumulation means that distress probability can increase unless a principal‑adjustment mechanism is included. The optimal portfolio allocation is 30% Productivity Bonds / 70% conventional debt.

License

    Code: MIT License – see LICENSE

    Book content: Creative Commons BY‑NC‑ND 4.0 – see license details

Contact

    Author: Ylia Callan

    Book: The Infinite Debt Problem

    GitHub Issues: Submit a question or suggestion
    
    
