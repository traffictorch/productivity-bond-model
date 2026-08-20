# Productivity Bond Model

**Simulation code, canonical reference, and interactive web platform for *The Infinite Debt Problem: How to Replace Perpetual Growth with Productive Prosperity***

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Book](https://img.shields.io/badge/Book-PDF-blue)](book/The_Infinite_Debt_Problem.pdf)
[![Website](https://img.shields.io/badge/Website-Live-brightgreen)](https://traffictorch.github.io/productivity-bond-model/)
[![AI-Power](https://img.shields.io/badge/AI-Power-purple)](https://traffictorch.github.io/productivity-bond-model/)

---

## 🌐 Live Website

The canonical reference for the Productivity Bond Model is now **live**:

👉 **[traffictorch.github.io/productivity-bond-model/](https://traffictorch.github.io/productivity-bond-model/)**

The website includes:

- **Interactive Monte Carlo Simulator** – run your own 10,000-path simulations with real-time feedback
- **🧠 AI-Power Economic Interpretation Engine** – powered by GLM, Google Gemma, and Llama
- **😌 Happiness & Bond Strength Unified Interpreter** – explore the relationship between productivity, wellbeing, and financial stability
- **Full Book Page** – read and download *The Infinite Debt Problem*
- **News & Blog System** – all updates, research notes, and announcements
- **Complete Documentation** – model definition, glossary, implementation guide, and FAQ
- **Dark/Light Theme Toggle** – and full mobile responsiveness

---

## 🚀 Simulation Status Update (August 2026)

> **Endogenous Debt Feedback Loop:** The model now fully implements instrument-specific debt dynamics. Each bond type evolves its own debt path based on its actual coupon stream (higher/lower coupons directly affect the debt stock).  
> **Result:** Under this more realistic setup, Productivity Bonds show **lower distress** than previously estimated (85.68% vs 88.17%), reinforcing their appeal.  
> **Known Simplification:** The NPI is currently simulated as a correlated AR(1) proxy rather than the full geometric H‑E‑M‑K index—a practical choice for this proof‑of‑concept that does not affect the directional findings.

---

🚧 Proof of Concept - Peer Refinement Encouraged

---

## Overview

This repository contains the simulation model that powers the book **The Infinite Debt Problem** by Ylia Callan, as well as the complete source code for the canonical website. The model compares five sovereign debt instruments:

1. **Conventional bonds** – fixed coupon  
2. **Inflation‑linked bonds** – fixed real yield  
3. **GDP‑linked bonds** – coupon linked to GDP growth  
4. **Productivity Bonds** – coupon linked to the National Productivity Index (NPI)  
5. **Hybrid bonds** – linked to both NPI and revenue growth  

The simulation uses a 10,000‑path Monte Carlo engine over a 10‑year horizon, with realistic dynamics including GDP growth, NPI growth, inflation, government revenue/spending, endogenous debt accumulation, and AI shocks.

---

## 🌍 What's New – The PBM Universe Expands

### 🧠 AI-Power Economic Interpretation Engine

Running a simulation is one thing. Understanding what it means is another. The new AI-Power Economic Interpretation Engine bridges that gap.

Powered by cutting‑edge language models – including **GLM**, **Google Gemma**, and **Llama** – the engine takes your simulation parameters and results and generates a plain‑English interpretation of what they mean for the economy.

### 😌 Happiness & Bond Strength Unified Interpreter

A tool that explores the relationship between economic productivity, societal wellbeing, and the stability of the financial system.

**Core insight:** Happiness rises with productivity up to about 3% per year, then plateaus. Beyond that point, additional productivity gains deliver diminishing returns to human wellbeing – while potentially increasing financial instability.

### 📚 Complete Website Ecosystem

| Page | Description |
|------|-------------|
| **[Home](https://traffictorch.github.io/productivity-bond-model/)** | Full PBM reference with interactive simulator |
| **[Book](https://traffictorch.github.io/productivity-bond-model/book.html)** | *The Infinite Debt Problem* – PDF preview, download links, metadata |
| **[About](https://traffictorch.github.io/productivity-bond-model/about.html)** | Model origins, author, research philosophy |
| **[Contact](https://traffictorch.github.io/productivity-bond-model/contact.html)** | Get in touch with the Traffic Torch research team |
| **[Changelog](https://traffictorch.github.io/productivity-bond-model/changelog.html)** | Auto‑updating version history from GitHub |
| **[News](https://traffictorch.github.io/productivity-bond-model/news.html)** | Blog and updates – powered by JSON |
| **[Privacy](https://traffictorch.github.io/productivity-bond-model/privacy.html)** | Privacy policy |
| **[Terms](https://traffictorch.github.io/productivity-bond-model/terms.html)** | Terms of use |
| **[404](https://traffictorch.github.io/productivity-bond-model/404.html)** | Custom error page |

### 📰 News & Blog System

The website includes a fully‑functioning blog system that allows easy publishing without any build step. Posts are stored in `data/posts.json` and rendered dynamically via JavaScript.

**Current posts:**
- [The PBM Universe Expands](https://traffictorch.github.io/productivity-bond-model/post.html?post=pbm-universe-expands) – AI Interpretation Engine, Happiness Interpreter, and complete ecosystem
- [Endogenous Debt Feedback Loop](https://traffictorch.github.io/productivity-bond-model/post.html?post=endogenous-debt-feedback-loop) – 2.5pp lower distress for Productivity Bonds
- [Welcome to the Productivity Bond Model](https://traffictorch.github.io/productivity-bond-model/post.html?post=welcome-to-the-pbm) – The canonical reference launches
- [What Is The Infinite Debt Problem?](https://traffictorch.github.io/productivity-bond-model/post.html?post=what-is-the-infinite-debt-problem) – The gap between financial promises and physical reality
- [Simulation Results Are In](https://traffictorch.github.io/productivity-bond-model/post.html?post=simulation-results-are-in) – 3.1% cost reduction confirmed

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
| `ROADMAP.md` | Full mathematical specification |
| `CONTRIBUTING.md` | Guidelines for contributors |
| `requirements.txt` | Python dependencies |
| `data/posts.json` | Blog posts for the news system |
| `results/` | Simulation results – see below for latest timestamped files |
| `css/main.css` | Website styles (dark/light themes, responsive) |
| `js/main.js` | Core website functionality (simulator, theme, dropdowns, AI engines) |
| `js/ga4.js` | Deferred Google Analytics 4 loading |
| `js/share.js` | Native Web Share API + fallback |
| `nav.html` | Shared navigation component |
| `footer.html` | Shared footer component |
| `sitemap.xml` | XML sitemap for search engines |
| `sw.js` | Service Worker for PWA support |
| `manifest.json` | PWA manifest |
| `404.html` | Custom 404 page |
| `index.html` | Home page |
| `book.html` | Book page |
| `about.html` | About page |
| `contact.html` | Contact page |
| `privacy.html` | Privacy policy |
| `terms.html` | Terms of use |
| `changelog.html` | Changelog page |
| `news.html` | News listing page |
| `post.html` | Individual post template |

---

## Simulation Status

✅ **Specification Complete** – see `ROADMAP.md`  
✅ **Results Reproduced** – all figures from Appendix C are available in `results/`  
✅ **Endogenous Debt Implemented** – debt now evolves uniquely per instrument  
✅ **AI Interpretation Engines** – GLM, Google Gemma, and Llama integration  
✅ **Happiness & Bond Strength Interpreter** – unified wellbeing analyser  
✅ **Complete Website** – canonical reference with all pages and tools  
🔄 **Implementation Refinements** – further calibration and sensitivity analysis ongoing

---

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/traffictorch/productivity-bond-model.git
cd productivity-bond-model
```

### 2. Read the Policy Brief (Start Here)

For a quick, non‑technical overview, open [`policy_brief.md`](policy_brief.md).

### 3. Explore the Website

Open `index.html` in your browser or visit the live site:

👉 **[traffictorch.github.io/productivity-bond-model/](https://traffictorch.github.io/productivity-bond-model/)**

The website includes:
- Interactive Monte Carlo simulator with live parameter sliders
- AI‑powered economic interpretation
- Happiness and bond strength analyser
- Full book preview and downloads
- News and changelog
- All documentation

### 4. View the Results

The simulation generates timestamped CSV files in the `results/` directory. To find the latest results:

```bash
ls -lt results/sim_*.csv | head -10
```

The most recent files will have the newest timestamp (e.g., `sim_20260817_153245_bond_results.csv`).

Each run produces:
- `*_bond_results.csv` – comparison of all five bond types
- `*_portfolio.csv` – portfolio optimisation results
- `*_summary.csv` – summary relative to conventional bonds
- `*_theta_sensitivity.csv`, `*_alpha_sensitivity.csv`, `*_cap_sensitivity.csv` – parameter sensitivity analyses

For convenience, the canonical results referenced in the book are always the latest run's files.

### 5. Run the Simulation Yourself

```bash
python run_simulation.py --paths 10000 --years 10
```

Override parameters as needed:

```bash
python run_simulation.py --paths 5000 --years 5 --theta_ai 0.40
```

### 6. Add a News Post

1. Open `data/posts.json`
2. Add a new post to the `"posts"` array:

```json
{
  "slug": "your-post-slug",
  "title": "Your Post Title",
  "date": "2026-08-22",
  "excerpt": "A short summary.",
  "content": "<p>Your full post content in HTML.</p>"
}
```

3. Commit and push – the site updates instantly.

---

## Results Summary (Updated — Endogenous Debt)

The table below is taken from the latest simulation run (`sim_20260817_...`). All CSVs in `results/` reflect this updated calibration.

| Bond Type | Expected Cost | Distress Prob. | Welfare | Effective Yield |
|-----------|---------------|----------------|---------|-----------------|
| Conventional | 0.5154 | 11.05% | 1.0687 | 4.00% |
| Inflation‑Linked | 0.4896 | 66.90% | 3.8384 | 3.55% |
| GDP‑Linked | 0.5114 | 88.50% | 4.9419 | 3.97% |
| **Productivity** | **0.4994** | **85.68%** | **4.7889** | **3.74%** |
| Hybrid | 0.5272 | 93.93% | 5.2297 | 4.25% |

### Key Finding

The Productivity Bond reduces expected financing costs by **~3.1%** compared to conventional debt (0.5154 → 0.4994).

**Critically**, under the fully endogenous debt feedback loop, the distress probability for Productivity Bonds is **85.68%** – this is **2.5 percentage points lower** than under the old static-debt assumption (88.17%). This means the dynamic coupon structure does not amplify fiscal distress; instead, the lower average coupon (3.74% vs 4.00% conventional) leads to slower debt accumulation over the cycle.

The **optimal portfolio allocation** remains **~30% Productivity Bonds** / 70% conventional debt under this calibration.

### Sensitivity Analysis Highlights

| Parameter | Critical Threshold | Impact |
|-----------|-------------------|--------|
| **θ_AI** (gov capture of AI gains) | > 30% | Bond substantially outperforms |
| **α_N** (investor participation) | 0.30 – 0.90 | Higher participation increases costs but reduces distress |
| **Cap** (max real return) | 2% – 6% | Lower cap reduces costs but increases distress |

---

## License

- **Code:** MIT License – see `LICENSE`
- **Book content:** Creative Commons BY‑NC‑ND 4.0 – see license details
- **Website content:** Creative Commons BY‑NC‑ND 4.0

---

## Contact

- **Author:** Ylia Callan
- **Book:** *The Infinite Debt Problem*
- **Website:** [traffictorch.github.io/productivity-bond-model/](https://traffictorch.github.io/productivity-bond-model/)
- **GitHub Issues:** [Submit a question or suggestion](https://github.com/traffictorch/productivity-bond-model/issues)
- **Email:** support@traffictorch.net

---

## Citation

If you use this model or reference the book in your work, please cite:

```bibtex
@misc{callan2026productivitybond,
  author = {Ylia Callan},
  title = {The Productivity Bond Model},
  year = {2026},
  publisher = {Traffic Torch},
  url = {https://traffictorch.github.io/productivity-bond-model/},
  version = {0.8.0},
  isbn = {979-8-23578-956-2}
}
```

---

## Acknowledgements

Built with ♥ and AI at Traffic Torch – Research & Incentive Design.

Special thanks to the open-source community, the GLM, Google, and Llama teams for making AI interpretation accessible, and to everyone who has contributed feedback and ideas to the Productivity Bond Model.

---

**The choice is ours. We can continue with extraction, inequality, and instability – or we can choose productivity, sharing, and sustainability.**

**The infinite debt problem is not an inevitability. It is an invitation to build a financial system that serves prosperity.**