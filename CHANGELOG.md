# Changelog

All notable changes to the Productivity Bond Model and this website.

## [0.8.0] – 2026-08-25

### Added – NPI Index Tracker (Tool #4)

#### Backend Infrastructure
- **Cloudflare D1 Database** – `npi-db` with 47 countries and 34 years (1990–2023) of productivity data.
- **Cloudflare Worker API** – `npi-api` providing two endpoints:
  - `/api/countries` – returns list of available countries
  - `/api/npi` – returns time-series data (GDP, Hours, Energy, Materials, Capital) for a given country and year range
- **Data sources** – compiled from World Bank (GDP), ILO/OECD (Hours), IEA (Energy), UNEP (Materials), and OECD/Penn World Table (Capital).
- **Sample data** – pre-populated with realistic historical data for testing and validation.

#### Frontend Tool – NPI Index Tracker
- **National Productivity Index (NPI) calculation** – implements the book's formula: `NPI = GDP ÷ (Labour^0.40 × Energy^0.25 × Materials^0.20 × Capital^0.15)`.
- **Country selection** – dropdown populated dynamically from the Worker API, supporting 47 countries.
- **Year range slider** – interactive range selector (1990–2023) with live numeric display.
- **Three weight modes**:
  - 📘 **Book NPI** – fixed weights (40/25/20/15) as defined in the book
  - 🌍 **Country Preset** – auto-applies weights based on economic category (Tech, Resource, Manufacturing, Developing, Service, Mixed)
  - ⚙️ **Custom** – user-adjustable sliders with automatic rebalancing to sum to 100%
- **Interactive charts** (Chart.js):
  - Main NPI line chart (base year = 100)
  - Component breakdown bar chart (average annual growth of GDP, Labour, Energy, Materials, Capital)
- **Prescription box** – auto-generated diagnosis with actionable recommendations based on component performance.
- **Data quality notice** – transparent disclaimer about data sources and estimation methods.

#### Additional Features
- **📥 Export CSV** – downloads the current chart data (Year, GDP, Hours, Energy, Materials, Capital, NPI) as a CSV file.
- **📋 Shareable links** – encodes country, year range, weight mode, and custom weights in the URL for easy sharing.
- **🤖 AI Analysis** – Cloudflare Worker (`ai-npi`) providing rule-based productivity insights with:
  - Country-specific economic context (e.g., UK productivity puzzle, Australia's resource economy)
  - Best/worst component identification
  - Category-specific advice (Tech, Resource, Developing, Manufacturing, Mixed)
  - Markdown-to-HTML rendering for bold text formatting
  - AI-generated analysis disclaimer

#### Country Presets
Added country-specific weight presets based on economic categories:

- **Tech-Driven** (USA, KOR, SGP, ISR, CHE, FIN, SWE, DNK) – 30/15/15/40
- **Resource-Based** (AUS, RUS, CAN, SAU, NOR, ZAF, CHL, PER, COL, NGA) – 25/35/30/10
- **Manufacturing** (DEU, JPN, ITA, CHN, POL, CZE, HUN) – 35/25/20/20
- **Service-Based** (GBR, FRA, ESP, NLD, BEL, PRT, GRC) – 35/15/10/40
- **Developing** (IND, BRA, MEX, IDN, TUR, ARG, PHL, VNM, KEN, EGY, THA, MYS) – 55/15/15/15
- **Mixed** (default fallback) – 40/25/20/15

#### Documentation
- **FAQ section** – comprehensive questions and answers about the NPI, weight modes, data sources, and missing data.
- **Data source attribution** – clearly lists World Bank, ILO, IEA, UNEP, and OECD as data providers.
- **Limitations disclaimer** – notes that capital stock data is estimated and the NPI is an empirical proxy.

### Changed
- **tools.html** – added NPI Index Tracker card to the tools grid.
- **index.html** – added NPI Index Tracker feature section on the homepage.
- **Navigation** – updated all pages to include NPI Index in the Tools dropdown.

### Fixed
- **CORS headers** – updated Worker to allow cross-origin requests (`Access-Control-Allow-Origin: *`).
- **Bold text rendering** – added `markdownToHtml()` helper to convert `**bold**` to `<strong>` tags in AI output.
- **AI warning** – added "AI can make mistakes ⚠️" disclaimer to the AI output section.

### Technical Notes
- **Deployment** – Worker deployed to Cloudflare Workers (`npi-api.traffictorch.workers.dev` and `ai-npi.traffictorch.workers.dev`).
- **Database** – D1 database `npi-db` with 47 countries × 34 years = 1,598 rows of data.
- **Frontend** – single-page HTML with inline JavaScript, Chart.js for visualisations, and `core.min.css` for styling.
- **File size** – `npi-index.html` is ~1,500 lines including all JavaScript logic.


## [0.7.0] – 2026-08-24

### Added
- **PBM Productivity Lab** – a central `tools.html` page housing all three interactive tools with tabbed navigation and consistent glass‑morphism design.
- **Wellbeing Index tool** – interactive calculator that measures work‑life balance, mental health, sleep, resilience, and productivity, generating a 0–100 wellbeing score with radar chart and 10‑year projection.
- **Debt Reality tool** – debt payoff calculator that shows time to freedom, total interest paid, debt‑to‑income ratio, and includes an extra payment slider with stacked bar chart visualisation.
- **Compound Curve tool** – debt projection tool that visualises how debt compounds over time, with a reduction slider showing savings from cutting annual debt.
- **AI advisors** – each tool includes a personalised AI advisor (powered by GLM/Llama) that generates custom recommendations based on user inputs.
- **Tool cards row** – reusable 3‑card grid (stacking on mobile) for promoting tools across all pages, with interchangeable cards for each tool.

### Fixed
- **Accordion toggles** – added `onclick="toggleAccordion(this)"` to all accordion items, ensuring they work reliably on dynamically shown panels (tools page).
- **Accordion stuck open** – added `!important` to `max-height` to prevent content being stuck open when panels are shown/hidden.
- **Auto‑scroll on page load** – tools page now stays at the top on load; hash‑based scrolling only triggers when a user clicks a tab.
- **Mobile return‑to‑top** – explicitly hidden on mobile with `display: none !important` to prevent layout issues.
- **Font loading** – switched from async (`display=swap`) to synchronous (`display=block`) to eliminate FOUT (flash of unstyled text).
- **CSS loading** – switched from async (`media="print"`) to synchronous to eliminate FOUC (flash of unstyled content).
- **Duplicated CSS** – removed all duplicated theme, navigation, footer, accordion, dropdown, and PWA styles from tool pages; now rely entirely on `core.min.css`.
- **Duplicated JavaScript** – removed all duplicated theme, hamburger, dropdown, accordion, and PWA logic from tool pages; now rely entirely on `core.min.js`.

### Changed
- **Tools page architecture** – now loads `core.min.css` synchronously, fonts synchronously, with only tool‑specific overrides in inline CSS.
- **All tool pages** – Wellbeing Index, Debt Reality, and Compound Curve now share the same architecture: synchronous CSS/fonts, minimal inline overrides, and `core.min.js` handling all shared functionality.
- **Tab switching** – `switchTab()` now accepts an `updateHash` parameter to control whether the URL hash is updated (prevents unwanted scrolling on load).
- **Accordion behaviour** – all accordions now use direct `onclick` handlers for reliability across dynamically shown content.

### Removed
- All async CSS loading from tool pages (`media="print"` trick removed in favour of synchronous loading).
- All async font loading from tool pages (`display=swap` removed in favour of `display=block`).
- Duplicated accordion initialisation logic from page‑specific scripts (now handled by `core.min.js` or direct `onclick`).

## [0.6.0] – 2026-08-21

### Added
- **Endogenous debt feedback loop** – Monte Carlo simulator now models the full debt dynamics, revealing 77.2pp distress increase for Productivity bonds (raw model).
- **AI‑powered Economic Interpretation Engine** – generates plain‑English economic interpretations using GLM, Google, and Llama models.
- **Shared navigation & footer components** – initially via `nav.html` / `footer.html`, later inlined for performance.
- **Auto‑fetching changelog** – from GitHub `CHANGELOG.md` using `marked.js`.
- **Starfield overlay** – epic static star background with subtle twinkling on page load.
- **News/Blog system** – JSON‑powered blog with `news.html`, `post.html`, and `posts.json`.
- **PDF.js self‑hosted viewer** – full control over PDF display, centred on all devices.
- **Book page** – comprehensive layout with cover image, metadata, key features, and results cards.
- **Mobile menu vertical scrolling** – menu scrolls independently of page on mobile.
- **Custom 404 page** – branded error page with helpful navigation links.
- **About, Contact, Privacy, Terms pages** – complete set of legal and informational pages.
- **Performance optimisation** – CSS and JS split into core (site‑wide) and page‑specific files (`core.min.css`, `core.min.js`, `home.css`, `home.js`).
- **Lazy loading** – `home.js` loads only when the user scrolls to the simulator or charts (Intersection Observer).
- **Fade‑in trick** – `html { opacity: 0; }` with 0.12s transition to eliminate black flash on page load.
- **Inline critical CSS** – reduced render‑blocking resources; full CSS loads asynchronously.
- **Collapsible sections** – Quick Reference (open by default), Model Definition, and Glossary (closed by default) to reduce scrolling.
- **Bar chart height control** – bars now use `height` (pixels) instead of `transform: scaleY()` for reliable sizing.

### Fixed
- Distress probability calculations – now correctly shows 77.2pp increase for Productivity bonds.
- Theme toggle consistency across all pages – uses event delegation for dynamic nav.
- Mobile hamburger menu and dropdown toggling – fully functional on all devices.
- Mobile menu alignment – proper font sizes, spacing, and dropdown indentation.
- PDF centering on iPhone – replaced Google Docs viewer with self‑hosted PDF.js.
- `manifest.json` syntax – missing comma fixed (no more "Unexpected token" errors).
- Plotly errors on non‑home pages – chart rendering now checks for container existence.
- Hero background – now off‑white in light mode, dark grey in dark mode (no more purple glow).
- Day/night mode – persists correctly across all pages using localStorage.
- **PWA Install button** – now shows correctly with text (fixed `core.min.js` minification).
- **Accordion toggles** – removed inline `onclick`; now uses event listeners in `core.js` (no more `nextElementSibling` errors).
- **Bar chart clipping** – numbers now positioned above bars; container height increased to 200px.
- **Hero fade classes** – removed `fade-step` and `delay-*` classes; hero now loads instantly (no layout shift).
- **Theme persistence** – inline script applies saved theme before page renders, eliminating flash.
- **Nav & footer inlined** – removed external fetches; now inlined for speed and stability.
- **All pages updated** – About, Changelog, Privacy, Terms, Contact, News, Post, Book – all now use the new architecture.

### Changed
- Updated sensitivity charts with new data.
- Refactored site structure – all pages now use the split CSS/JS architecture.
- Mobile nav font size – increased from 0.85rem to 1.2rem for better readability.
- Mobile nav layout – cleaner spacing, full‑width touch targets, scrollable menu.
- Hero progressive reveal – smoother fade‑in timing for badges, title, and buttons.
- PDF viewer – replaced Google Docs embed with self‑hosted PDF.js for full control and mobile centering.
- Simulator auto‑scroll – on mobile, results scroll into view after simulation completes (button‑click only).
- **File structure** – `core.min.css`, `core.min.js` for site‑wide; `home.css`, `home.js` for home‑page only.
- **HTML template** – all pages now use inlined nav/footer, critical CSS, and `core.min.js`.
- **Performance** – reduced unused CSS/JS; Plotly loaded only on home page when needed.

### Removed
- `nav.html` and `footer.html` component loader (replaced with inlined HTML for performance).
- `fade-step` and `delay-*` hero animation (replaced with instant render).
- `main.js` (split into `core.min.js` and `home.js`).
- `main.css` (split into `core.min.css` and `home.css`).

## [0.5.0] – 2026-08-20

### Added
- Happiness Curve and Bond Strength dashboard.
- Dark/light theme toggle persists across pages.

### Improved
- Bar chart visualisation in the simulator.
- Responsive layout for mobile devices.

## [0.4.0] – 2026-08-19

### Added
- Initial public release of the canonical website.
- Full model definition, interactive simulator, and adoption scenarios.
- PWA support and offline reading.
- Monte Carlo simulation (10,000 paths, 10‑year horizon).
- Portfolio optimisation table.

---

_This changelog is automatically displayed on the [changelog page](https://traffictorch.github.io/productivity-bond-model/changelog.html)._