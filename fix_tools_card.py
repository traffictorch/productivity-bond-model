#!/usr/bin/env python3
import pathlib

path = pathlib.Path('tools.html')
if not path.exists():
    print("ERROR: tools.html not found")
    exit(1)

html = path.read_text()

# Check if Policy Lab card already exists
if 'policy-lab.html' in html and '🏛️' in html:
    print("✅ Policy Lab already in tools.html — nothing to do")
    exit(0)

# Find the Wellbeing card (first one) and insert Policy Lab card before it
# The Wellbeing card looks like: <div class="tool-card">\n        <div class="tool-card-icon">🌿</div>
wellbeing_anchor = '''      <div class="tool-card">
        <div class="tool-card-icon">🌿</div>'''

policy_card = '''      <div class="tool-card" style="border-color:rgba(79,70,229,0.4);">
        <div class="tool-card-icon">🏛️</div>
        <h3 class="tool-card-title">Policy Lab</h3>
        <p class="tool-card-desc">Model sovereign debt trajectories under conventional vs productivity-linked issuance with endogenous feedback loops.</p>
        <a href="policy-lab.html" class="btn-primary" style="width:100%; text-align:center; padding:0.6rem 1.5rem; font-size:0.85rem;">Try It →</a>
      </div>
'''

if wellbeing_anchor in html:
    html = html.replace(wellbeing_anchor, policy_card + wellbeing_anchor, 1)
    print("✅ Inserted Policy Lab card before Wellbeing card")
else:
    print("⚠️ Wellbeing card anchor not found. Searching for alternate...")
    # Try alternate spacing
    alt_anchor = '<div class="tool-card-icon">🌿</div>'
    if alt_anchor in html:
        idx = html.find(alt_anchor)
        card_start = html.rfind('<div class="tool-card">', 0, idx)
        if card_start != -1:
            html = html[:card_start] + policy_card + html[card_start:]
            print("✅ Inserted Policy Lab card using flexible anchor")
        else:
            print("❌ Could not find card container")
    else:
        print("❌ Could not find Wellbeing card at all")

# Also add to noscript fallback if not there
if '🏛️ Policy Lab</strong>' not in html:
    noscript_anchor = '<strong>📈 Compound Curve</strong>'
    if noscript_anchor in html:
        idx = html.find(noscript_anchor)
        li_start = html.rfind('<li>', 0, idx)
        if li_start != -1:
            new_li = '''<li>
          <strong>🏛️ Policy Lab</strong> – a sovereign debt scenario builder that models conventional vs productivity-linked bond trajectories.
        </li>
        '''
            html = html[:li_start] + new_li + html[li_start:]
            print("✅ Added Policy Lab to noscript fallback")

path.write_text(html)
print("File saved.")
