#!/usr/bin/env python3
import pathlib, sys, re

# ── PART 1: FIX POLICY LAB VERDICT LOGIC ──
path = pathlib.Path('policy-lab.html')
if path.exists():
    html = path.read_text()
    
    # Fix verdict logic to read actual numbers, not just theta
    old_verdict = """  if(p.thetaAI<0.15){
    parts.push('⚠️ θ_AI = '+p.thetaAI.toFixed(2)+' is <strong>below the critical threshold (0.15)</strong>. The bond will barely outperform conventional debt — prioritize policies that capture AI gains before issuing.');
  }else if(p.thetaAI>0.30){
    parts.push('✅ θ_AI = '+p.thetaAI.toFixed(2)+' is <strong>above 0.30</strong> — the bond outperforms conventional debt. The government captures enough AI gains to make the instrument viable.');
  }else{
    parts.push('📊 θ_AI = '+p.thetaAI.toFixed(2)+' is <strong>between 0.15 and 0.30</strong>. The bond has modest advantages but is sensitive to capture policies.');
  }
  const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
  parts.push('Expected cost: <strong>'+prod.expectedCost.toFixed(3)+'</strong> vs conventional <strong>'+conv.expectedCost.toFixed(3)+'</strong> ('+saving.toFixed(2)+'%).');
  parts.push('Distress probability: <strong>'+(prod.distressProb*100).toFixed(1)+'%</strong> vs <strong>'+(conv.distressProb*100).toFixed(1)+'%</strong> conventional.');"""
    
    new_verdict = """  const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
  const distressDiff=prod.distressProb-conv.distressProb;
  
  if (saving < -2 && distressDiff < 0.05) {
    parts.push('✅ <strong>Clear win.</strong> The bond is cheaper ('+saving.toFixed(2)+'%) AND has similar or lower distress.');
  } else if (saving < -2 && distressDiff > 0.10) {
    parts.push('⚠️ <strong>Trade-off.</strong> The bond is cheaper ('+saving.toFixed(2)+'%), but carries significantly higher distress (+'+(distressDiff*100).toFixed(1)+'pp). This is the feedback loop in action.');
  } else if (saving > 1) {
    parts.push('❌ <strong>Does not outperform.</strong> The bond is more expensive (+'+saving.toFixed(2)+'%) and riskier.');
  } else {
    parts.push('📊 <strong>Neutral.</strong> The bond is roughly cost-equivalent to conventional debt, but changes the risk profile.');
  }
  
  if(p.thetaAI<0.15){
    parts.push('⚠️ θ_AI = '+p.thetaAI.toFixed(2)+' is below 0.15. Government capture is very weak.');
  }else if(p.thetaAI>0.30){
    parts.push('✅ θ_AI = '+p.thetaAI.toFixed(2)+' is above 0.30. Strong capture supports the instrument.');
  }else{
    parts.push('📊 θ_AI = '+p.thetaAI.toFixed(2)+' is between 0.15 and 0.30. Moderate capture.');
  }
  
  parts.push('Expected cost: <strong>'+prod.expectedCost.toFixed(3)+'</strong> vs conventional <strong>'+conv.expectedCost.toFixed(3)+'</strong> ('+saving.toFixed(2)+'%).');
  parts.push('Distress probability: <strong>'+(prod.distressProb*100).toFixed(1)+'%</strong> vs <strong>'+(conv.distressProb*100).toFixed(1)+'%</strong> conventional.');"""

    if old_verdict in html:
        html = html.replace(old_verdict, new_verdict)
        print("  OK  Fixed verdict logic (reads actual numbers)")
    else:
        print("  MISS  Verdict logic (might already be patched)")

    # Fix chart white background
    html = html.replace("responsive:true,maintainAspectRatio:true,", "responsive:true,maintainAspectRatio:true,plugins:{legend:{labels:{color:textColor,boxWidth:12,padding:12,font:{size:11}}},tooltip:{backgroundColor:'rgba(12,15,25,0.9)'}},backgroundColor:'transparent',")
    
    path.write_text(html)
    print("  OK  Fixed chart backgrounds")
else:
    print("  ERROR: policy-lab.html not found")

# ── PART 2: SITE INTEGRATION (NAV + TOOLS PAGE) ──
print("\nUpdating site navigation and tools page...")

nav_target = '<li><a href="global-vitals-dashboard.html">🌍 Global Vitals</a></li>'
nav_replace = '<li><a href="global-vitals-dashboard.html">🌍 Global Vitals</a></li>\n        <li><a href="policy-lab.html">🏛️ Policy Lab</a></li>'

updated_files = 0
for f in pathlib.Path('.').glob('*.html'):
    if 'index-backup' in f.name or 'index-beta' in f.name or '404' in f.name:
        continue
    content = f.read_text()
    if nav_target in content and 'href="policy-lab.html">🏛️ Policy Lab' not in content:
        content = content.replace(nav_target, nav_replace)
        f.write_text(content)
        updated_files += 1

print(f"  OK  Added Policy Lab to nav in {updated_files} HTML files")

# Update tools.html count and add card
tools_path = pathlib.Path('tools.html')
if tools_path.exists():
    tools = tools_path.read_text()
    
    # Update text count
    tools = tools.replace("6+ powerful tools", "7 interactive tools")
    
    # Add Policy Lab card if missing
    if 'policy-lab.html" class="btn-primary"' not in tools and 'policy-lab.html" class="btn-secondary"' not in tools:
        new_card = """
    <!-- Policy Lab -->
    <div class="tool-card" style="border-color:rgba(79,70,229,0.4);">
      <div class="tool-card-icon">🏛️</div>
      <h3 class="tool-card-title">Policy Lab</h3>
      <p class="tool-card-desc">Model sovereign debt trajectories under conventional vs productivity-linked issuance.</p>
      <a href="policy-lab.html" class="btn-primary" style="width:100%; text-align:center; padding:0.6rem 1.5rem; font-size:0.85rem;">Try It →</a>
    </div>
"""
        tools = tools.replace('<div class="tool-cards-grid">', '<div class="tool-cards-grid">\n' + new_card)
        
    tools_path.write_text(tools)
    print("  OK  Updated tools.html (added Policy Lab card, changed count to 7)")

print("\nAll patches applied successfully.")
