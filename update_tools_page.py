#!/usr/bin/env python3
import pathlib

path = pathlib.Path('tools.html')
if not path.exists():
    print("ERROR: tools.html not found")
    exit(1)

html = path.read_text()

# 1. Update Meta Description and Hero text to 6 tools
html = html.replace('content="7 interactive tools', 'content="6 interactive tools')
html = html.replace('>7 interactive tools', '>6 interactive tools')

# 2. Update JSON-LD Schema
html = html.replace('"name": "PBM Productivity Lab – 3 Tools"', '"name": "PBM Productivity Lab – 6 Tools"')
html = html.replace('"name": "PBM Productivity Lab"', '"name": "PBM Productivity Lab"') # Just in case
html = html.replace('"description": "A suite of 3 interactive web tools', '"description": "A suite of 6 interactive web tools')

# 3. Add Policy Lab to the Hero Tabs
tabs_target = """  <button class="hero-tab-btn" onclick="location.href='global-vitals-dashboard.html'" style="background:#4f46e5; border:1px solid #4f46e5; border-radius:30px; padding:0.4rem 1.2rem; font-size:0.85rem; color:#fff; cursor:pointer; transition:0.2s; font-weight:500;">🌍 5. Global Dashboard</button>"""
tabs_replace = tabs_target + """
  <button class="hero-tab-btn" onclick="location.href='policy-lab.html'" style="background:var(--bg-input); border:1px solid var(--border-divider); border-radius:30px; padding:0.4rem 1.2rem; font-size:0.85rem; color:var(--text-primary); cursor:pointer; transition:0.2s; font-weight:500;">🏛️ 6. Policy Lab</button>"""

if '6. Policy Lab' not in html:
    html = html.replace(tabs_target, tabs_replace)
    print("✅ Added Policy Lab to Hero Tabs")
else:
    print("✅ Policy Lab already in Hero Tabs")

# 4. Add Policy Lab to the bottom Card Grid
grid_target = """    <div class="tool-cards-grid">"""
grid_replace = """    <div class="tool-cards-grid">
      <div class="tool-card" style="border-color:rgba(79,70,229,0.4);">
        <div class="tool-card-icon">🏛️</div>
        <h3 class="tool-card-title">Policy Lab</h3>
        <p class="tool-card-desc">Model sovereign debt trajectories under conventional vs productivity-linked issuance with endogenous feedback loops.</p>
        <a href="policy-lab.html" class="btn-primary" style="width:100%; text-align:center; padding:0.6rem 1.5rem; font-size:0.85rem;">Try It →</a>
      </div>"""

if 'Policy Lab' not in html.split('tool-cards-grid')[1]:
    html = html.replace(grid_target, grid_replace)
    print("✅ Added Policy Lab to Card Grid")
else:
    print("✅ Policy Lab already in Card Grid")

# 5. Add Policy Lab to the noscript section
noscript_target = """          <strong>📈 Compound Curve</strong> – projects how annual debt grows exponentially and shows how small reductions bend the curve downward.
        </li>"""
noscript_replace = """          <strong>📈 Compound Curve</strong> – projects how annual debt grows exponentially and shows how small reductions bend the curve downward.
        </li>
        <li>
          <strong>🏛️ Policy Lab</strong> – a sovereign debt scenario builder that models conventional vs productivity-linked bond trajectories.
        </li>"""

if '🏛️ Policy Lab' not in html.split('<noscript>')[1]:
    html = html.replace(noscript_target, noscript_replace)
    print("✅ Added Policy Lab to Noscript fallback")

path.write_text(html)
print("File saved.")
