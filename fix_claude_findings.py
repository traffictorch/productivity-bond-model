#!/usr/bin/env python3
import pathlib, re, sys

path = pathlib.Path('policy-lab.html')
if not path.exists():
    print("ERROR: policy-lab.html not found")
    sys.exit(1)

html = path.read_text()

if '/* ACCORDION FIXED */' in html:
    print("Already patched. Nothing to do.")
    sys.exit(0)

fixes = []

# FIX 1: Remove the duplicate accordion listener (the regression)
fixes.append((
    "Fix duplicate accordion toggle",
    """  // Ensure accordions toggle even if an earlier JS error occurred
  document.querySelectorAll('.accordion-toggle').forEach(function(el){
    el.addEventListener('click', function(e){
      e.preventDefault();
      const content = this.nextElementSibling;
      const arrow = this.querySelector('.arrow');
      if(content){
        content.classList.toggle('open');
        this.classList.toggle('open');
        if(arrow) arrow.classList.toggle('open');
      }
    });
  });""",
    "  /* ACCORDION FIXED */"
))

# FIX 2: Remove GDP from readInputs
fixes.append((
    "Remove GDP from readInputs",
    "    gdp: parseNum('gdp', 250),\n",
    ""
))

# FIX 3: Remove GDP from Copy Summary
fixes.append((
    "Remove GDP from Copy Summary",
    "text+='Sovereign: GDP $'+p.gdp+'B, debt/GDP '+(p.debtGDP)+'%, growth '+",
    "text+='Sovereign: debt/GDP '+(p.debtGDP)+'%, growth '+"
))

# FIX 4: Fix the "see verdict below" text
fixes.append((
    "Fix share note text",
    "At your chosen <strong><span id=\"shareDisplay\">30</span>% share</strong>, blended results differ — see verdict below.",
    "At your chosen <strong><span id=\"shareDisplay\">30</span>% share</strong>, the actual blended results would be between these and conventional."
))

# FIX 5: Fix the mobile CSS target
fixes.append((
    "Fix mobile CSS target",
    ".presets { display: grid; grid-template-columns: 1fr 1fr; }\n      .presets button { width: 100%; margin: 0; font-size: 0.75rem; }",
    ".mode-selector { display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; }\n      .mode-selector .mode-btn { width: 100%; margin: 0; font-size: 0.75rem; text-align: center; }"
))

# FIX 6: Fix the verdict logic (absolute guards + fall-throughs)
fixes.append((
    "Fix verdict logic",
    """  if (saving < -2 && distressDiff < 0.05) {
    parts.push('✅ <strong>Clear win.</strong> The bond is cheaper ('+saving.toFixed(2)+'%) AND has similar or lower distress.');
  } else if (saving < -2 && distressDiff > 0.10) {
    parts.push('⚠️ <strong>Trade-off.</strong> The bond is cheaper ('+saving.toFixed(2)+'%), but carries significantly higher distress (+'+(distressDiff*100).toFixed(1)+'pp). This is the feedback loop in action.');
  } else if (saving > 1) {
    parts.push('❌ <strong>Does not outperform.</strong> The bond is more expensive (+'+saving.toFixed(2)+'%) and riskier.');
  } else {
    parts.push('📊 <strong>Neutral.</strong> The bond is roughly cost-equivalent to conventional debt, but changes the risk profile.');
  }""",
    """  if (conv.distressProb > 0.5) {
    parts.push('⚠️ <strong>Unsustainable baseline.</strong> Conventional distress is already above 50%. Changing the bond structure won\\'t fix a structural deficit — look at primary balances.');
  } else if (saving < -2 && distressDiff <= 0.02) {
    parts.push('✅ <strong>Clear win.</strong> The bond is cheaper ('+saving.toFixed(2)+'%) AND has similar or lower distress.');
  } else if (saving < -2 && distressDiff > 0.05) {
    parts.push('⚠️ <strong>Trade-off.</strong> The bond is cheaper ('+saving.toFixed(2)+'%), but carries significantly higher distress (+'+(distressDiff*100).toFixed(1)+'pp). This is the feedback loop in action.');
  } else if (saving > 1) {
    parts.push('❌ <strong>Does not outperform.</strong> The bond is more expensive (+'+saving.toFixed(2)+'%).');
  } else if (saving < -2 && distressDiff > 0.02 && distressDiff <= 0.05) {
    parts.push('📊 <strong>Mixed result.</strong> Cheaper ('+saving.toFixed(2)+'%), but slightly riskier (+'+(distressDiff*100).toFixed(1)+'pp distress).');
  } else {
    parts.push('📊 <strong>Neutral.</strong> The bond is roughly cost-equivalent to conventional debt.');
  }"""
))

# FIX 7: Fix the Interpret this scenario logic to match the new verdict
fixes.append((
    "Fix generateAI logic",
    """    let summary='📌 ',advice='';
    if(p.thetaAI<0.15){
      summary='⚠️ θ_AI is below the 0.15 critical threshold. The productivity bond barely outperforms conventional debt in this scenario.';
      advice='✅ Policy recommendation: prioritize policies that capture AI gains (taxes, royalties, sovereign equity) before issuing Productivity Bonds. Without these, the instrument cannot deliver its promised cost reduction.';
    }else if(p.thetaAI>0.30){
      summary='✅ θ_AI is above 0.30 — the bond is structurally viable. Expected cost saving: '+saving.toFixed(2)+'%.';
      advice='✅ Policy recommendation: proceed with a pilot issuance at ~'+(port.optimal.share*100).toFixed(0)+'% of new debt. '+(p.pam?'PAM enabled provides additional distress protection.':'Consider enabling PAM to mitigate the feedback loop.');
    }else{
      summary='📊 θ_AI = '+p.thetaAI.toFixed(2)+' sits between the failure threshold and the outperformance threshold. Modest advantage only.';
      advice='✅ Policy recommendation: test with a small pilot first. Strengthen AI capture mechanisms to move θ_AI above 0.30.';
    }
    if(distDiff>0.05&&!p.pam){
      advice+=' Note: distress probability rises '+(distDiff*100).toFixed(1)+'pp vs conventional — enable PAM to mitigate.';
    }""",
    """    let summary='📌 ',advice='';
    const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
    const distDiff=prod.distressProb-conv.distressProb;
    
    if (conv.distressProb > 0.5) {
      summary='⚠️ The sovereign is already in a high-distress regime (>50%). Bond structure changes alone will not fix this.';
      advice='✅ Policy recommendation: focus on primary balance and fiscal consolidation before issuing new bond structures.';
    } else if (saving < -2 && distDiff <= 0.02) {
      summary='✅ The productivity bond is a clear win: cheaper ('+saving.toFixed(2)+'%) and no worse on distress.';
      advice='✅ Policy recommendation: proceed with a pilot issuance at ~'+(port.optimal.share*100).toFixed(0)+'% of new debt.';
    } else if (saving < -2 && distDiff > 0.05) {
      summary='⚠️ Trade-off: the bond is cheaper ('+saving.toFixed(2)+'%), but significantly riskier (+'+(distDiff*100).toFixed(1)+'pp distress).';
      advice='✅ Policy recommendation: '+(p.pam?'PAM is enabled, which helps, but further principal adjustment may be needed.':'Enable PAM or add a debt ceiling. Without safeguards, the feedback loop dominates.');
    } else {
      summary='📊 Neutral outcome: saving is '+saving.toFixed(2)+'%, distress change is +'+(distDiff*100).toFixed(1)+'pp.';
      advice='✅ Policy recommendation: the instrument doesn\\'t materially improve this specific scenario. Review debt baseline and coupon design.';
    }"""
))

# FIX 8: Fix the PAM FAQ text
fixes.append((
    "Fix PAM FAQ text",
    """<p style="color:var(--text-secondary); margin-top:0.5rem;">The PAM is a rule that automatically reduces outstanding principal when DSR exceeds a threshold (default 15%). When you turn it on, you'll see distress probability drop significantly — at the cost of a small hit to investor returns.</p>
            <p style="color:var(--text-secondary); margin-top:0.5rem;">This is the model's most important design refinement. Without PAM, variable coupons may not reduce distress even though they reduce expected cost.</p>""",
    """<p style="color:var(--text-secondary); margin-top:0.5rem;">The PAM is a rule that automatically reduces outstanding principal when DSR exceeds a threshold (default 15%). When you turn it on, the debt/GDP ratio drops (e.g., from 107% to 94%), which improves long-run sustainability.</p>
            <p style="color:var(--text-secondary); margin-top:0.5rem;"><strong>Note on distress metrics:</strong> The PAM lowers debt/GDP, but the binary "ever above 15%" distress metric may not change much if the baseline deficit is large. This is a known limitation of binary distress metrics in highly stressed scenarios.</p>"""
))

# FIX 9: Fix duplicate Chart.js options object (Trajectory)
fixes.append((
    "Fix duplicate plugins: Trajectory",
    """    options:{
      responsive:true,maintainAspectRatio:true,plugins:{legend:{labels:{color:textColor,boxWidth:12,padding:12,font:{size:11}}},tooltip:{backgroundColor:'rgba(12,15,25,0.9)'}},backgroundColor:'transparent',
      plugins:{legend:{labels:{color:textColor,boxWidth:12,padding:12,font:{size:11}}}},
      scales:{
        x:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}}},
        y:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10},callback:v=>(v*100).toFixed(0)+'%'}}
      }
    }""",
    """    options:{
      responsive:true,maintainAspectRatio:true,
      plugins:{legend:{labels:{color:textColor,boxWidth:12,padding:12,font:{size:11}}},tooltip:{backgroundColor:'rgba(12,15,25,0.9)'}},
      scales:{
        x:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}}},
        y:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10},callback:v=>(v*100).toFixed(0)+'%'}}
      }
    }"""
))

# FIX 10: Fix duplicate Chart.js options object (DSR)
fixes.append((
    "Fix duplicate plugins: DSR",
    """    options:{
      responsive:true,maintainAspectRatio:true,plugins:{legend:{labels:{color:textColor,boxWidth:12,padding:12,font:{size:11}}},tooltip:{backgroundColor:'rgba(12,15,25,0.9)'}},backgroundColor:'transparent',
      plugins:{legend:{labels:{color:textColor,boxWidth:12,padding:12,font:{size:11}}}},
      scales:{
        x:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}}},
        y:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10},callback:v=>(v*100).toFixed(0)+'%'}}
      }
    }""",
    """    options:{
      responsive:true,maintainAspectRatio:true,
      plugins:{legend:{labels:{color:textColor,boxWidth:12,padding:12,font:{size:11}}},tooltip:{backgroundColor:'rgba(12,15,25,0.9)'}},
      scales:{
        x:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}}},
        y:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10},callback:v=>(v*100).toFixed(0)+'%'}}
      }
    }"""
))

print("Applying final fixes based on Claude's review...")
ok = 0
skipped = 0
for name, find, replace in fixes:
    if find in html:
        html = html.replace(find, replace, 1)
        print("  OK  " + name)
        ok += 1
    else:
        print("  MISS  " + name)
        skipped += 1

path.write_text(html)
print("\n" + str(ok) + " applied, " + str(skipped) + " skipped.")
