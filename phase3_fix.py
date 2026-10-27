#!/usr/bin/env python3
import pathlib, sys

path = pathlib.Path('policy-lab.html')
if not path.exists():
    print("ERROR: policy-lab.html not found")
    sys.exit(1)

html = path.read_text()

if '/* MOBILE FIX */' in html:
    print("Already patched. Nothing to do.")
    sys.exit(0)

fixes = []

# FIX 1: Remove the gdp reference that causes the preset error
fixes.append((
    "Fix loadPreset error (remove gdp)",
    """function loadPreset(name){
  const p=PRESETS[name];
  if(!p)return;
  document.getElementById('gdp').value=p.gdp;
  document.getElementById('debtGDP').value=p.debtGDP;""",
    """function loadPreset(name){
  const p=PRESETS[name];
  if(!p)return;
  document.getElementById('debtGDP').value=p.debtGDP;"""
))

# FIX 2: Update loadPreset to use runAnalysisAsync instead of runAnalysis
fixes.append((
    "Preset uses runAnalysisAsync",
    "document.querySelectorAll('#presetSelector .mode-btn').forEach(b=>b.classList.toggle('active',b.dataset.preset===name));\n  runAnalysis(2000);",
    "document.querySelectorAll('#presetSelector .mode-btn').forEach(b=>b.classList.toggle('active',b.dataset.preset===name));\n  runAnalysisAsync(2000);"
))

# FIX 3: Add mobile CSS + accordion fix right before </style>
fixes.append((
    "Add mobile responsiveness CSS",
    """    @media (max-width: 768px) {
      .floating-return-top { display: none !important; }
      .stat-grid { grid-template-columns: 1fr 1fr; }
    }
  </style>""",
    """    @media (max-width: 768px) {
      .floating-return-top { display: none !important; }
      .stat-grid { grid-template-columns: 1fr !important; }
      .input-group label { flex: 1 1 100% !important; width: 100%; }
      .input-group input[type="number"] { width: 100%; }
      .chart-container { max-height: 250px !important; height: 250px !important; overflow: hidden; width: 100%; }
      .stat-card .num { font-size: 1.4rem; }
      .presets { display: grid; grid-template-columns: 1fr 1fr; }
      .presets button { width: 100%; margin: 0; font-size: 0.75rem; }
      canvas { max-width: 100% !important; height: auto !important; }
    }
    /* MOBILE FIX */
  </style>"""
))

# FIX 4: Make accordion JS more robust
fixes.append((
    "Fix accordion binding",
    """document.addEventListener('DOMContentLoaded',function(){
  if(typeof initFeedbackForm==='function'){
    initFeedbackForm('feedback-container');
  }
});""",
    """document.addEventListener('DOMContentLoaded',function(){
  if(typeof initFeedbackForm==='function'){
    initFeedbackForm('feedback-container');
  }
  // Ensure accordions toggle even if an earlier JS error occurred
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
  });
});"""
))

print("Patching " + path.name + " ...")
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
