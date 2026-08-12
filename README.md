# Productivity Bond Model

**Simulation code for "The Infinite Debt Problem"**

[![License: 
MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

This repository contains the simulation model for the book **The Infinite 
Debt Problem: How to Replace Perpetual Growth with Productive 
Prosperity**.

The model compares five sovereign debt instruments:
1. Conventional bonds
2. Inflation-linked bonds
3. GDP-linked bonds
4. Productivity Bonds (NPI-linked)
5. Hybrid bonds (NPI + revenue growth)

---

## Status

🟡 **Specification Complete — Implementation Needed**

The mathematical specification is fully documented in 
[ROADMAP.md](ROADMAP.md). The results from the book are available in the 
`results/` directory.

**We welcome contributions to implement the full simulation model.**

---

## Repository Contents

| File/Directory | Description |
|----------------|-------------|
| `ROADMAP.md` | Full mathematical specification |
| `CONTRIBUTING.md` | Guidelines for contributors |
| `requirements.txt` | Python dependencies |
| `results/` | Results from the book (CSV format) |

---

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/traffictorch/productivity-bond-model.git
cd productivity-bond-model

2. View the Results

The results CSV files are in the results/ directory:

    bond_comparison.csv — Comparison of all bond types

    portfolio_results.csv — Portfolio optimization results

    sensitivity_*.csv — Parameter sensitivity analysis

3. Build the Simulation

Follow the specification in ROADMAP.md.
Results Summary
Bond Type	Expected Cost	Distress Prob	Welfare	Effective Yield
Conventional	0.4521	18.32%	0.8954	4.00%
Inflation-Linked	0.4387	17.15%	0.8645	3.85%
GDP-Linked	0.4213	15.63%	0.8264	3.62%
Productivity	0.4056	14.21%	0.7889	3.48%
Hybrid	0.3987	13.56%	0.7712	3.39%
License

MIT License — see LICENSE
Contact

Author: Ylia Callan
Book: The Infinite Debt Problem
