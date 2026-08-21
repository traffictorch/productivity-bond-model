# Changelog

All notable changes to the Productivity Bond Model and this website.

## [0.8.0] – 2026-08-22

### Added
- Endogenous debt feedback loop in Monte Carlo simulator.
- AI‑powered Economic Interpretation Engine (GLM/Google/Llama).
- Shared navigation and footer components for all pages (`nav.html`, `footer.html`).
- Auto‑fetching changelog from GitHub.
- **Starfield overlay** – epic static star background with subtle twinkling effect on page load.
- **News/Blog system** – JSON‑powered blog with individual post pages (`news.html`, `post.html`, `posts.json`).
- **PDF.js self‑hosted viewer** – full control over PDF display, centred on all devices.
- **Book page** – comprehensive layout with cover image, metadata, key features, and results cards.
- **Mobile menu vertical scrolling** – menu scrolls independently of page on mobile.
- **Custom 404 page** – branded error page with helpful navigation links.
- **About, Contact, Privacy, Terms pages** – complete set of legal and informational pages.

### Fixed
- Distress probability calculations – now correctly shows 77.2pp increase for Productivity bonds.
- Theme toggle consistency across all pages – now uses event delegation for dynamic nav.
- Mobile hamburger menu and dropdown toggling – fully functional on all devices.
- **Mobile menu alignment** – proper font sizes, spacing, and dropdown indentation.
- **PDF centering on iPhone** – Google Docs viewer replaced with self‑hosted PDF.js.
- **Manifest.json syntax** – missing comma fixed (no more "Unexpected token" errors).
- **Plotly errors on non‑home pages** – chart rendering now checks for container existence.
- **Hero background** – now off‑white in light mode, dark grey in dark mode (no more purple glow).
- **Day/night mode** – persists correctly across all pages using localStorage.

### Changed
- Updated sensitivity charts with new data.
- Refactored site structure: all pages now use `nav.html` and `footer.html`.
- **Mobile nav font size** – increased from 0.85rem to 1.2rem for better readability.
- **Mobile nav layout** – cleaner spacing, full‑width touch targets, scrollable menu.
- **Hero progressive reveal** – smoother fade‑in timing for badges, title, and buttons.
- **PDF viewer** – replaced Google Docs embed with self‑hosted PDF.js for full control and mobile centering.
- **Simulator auto‑scroll** – on mobile, results scroll into view after simulation completes (button‑click only).

## [0.7.0] – 2026-07-15

### Added
- Happiness Curve and Bond Strength dashboard.
- Dark/light theme toggle persists across pages.

### Improved
- Bar chart visualisation in the simulator.
- Responsive layout for mobile devices.

## [0.6.0] – 2026-06-01

### Added
- Initial public release of the canonical website.
- Full model definition, interactive simulator, and adoption scenarios.
- PWA support and offline reading.
- Monte Carlo simulation (10,000 paths, 10‑year horizon).
- Portfolio optimisation table.

---

_This changelog is automatically displayed on the [changelog page](https://traffictorch.github.io/productivity-bond-model/changelog.html)._