#!/usr/bin/env python3
import pathlib, sys

path = pathlib.Path('policy-lab.html')
if not path.exists():
    print("ERROR: policy-lab.html not found")
    sys.exit(1)

html = path.read_text()

if 'function parseNum(' in html:
    print("Already patched. Nothing to do.")
    sys.exit(0)

fixes = []

fixes.append((
    "Share link unit round-trip",
    """function buildShareUrl(){
  const p=readInputs();
  const base=window.location.href.split('?')[0];
  const params=new URLSearchParams();
  for(const k of ['gdp','debtGDP','muY','muPi','muN','couponConv','alphaN','cap','thetaAI','share'])params.set(k,p[k]);
  params.set('pam',p.pam?'1':'0');
  return base+'?'+params.toString();
}""",
    """function buildShareUrl(){
  const base=window.location.href.split('?')[0];
  const params=new URLSearchParams();
  ['gdp','debtGDP','muY','muPi','muN','couponConv','alphaN','cap','thetaAI','share'].forEach(function(k){
    const el=document.getElementById(k);
    if(el)params.set(k,el.value);
  });
  params.set('pam',document.getElementById('pam').checked?'1':'0');
  return base+'?'+params.toString();
}"""
))

fixes.append((
    "Zero-value input handling",
    """function readInputs(){
  return{
    gdp:parseFloat(document.getElementById('gdp').value)||250,
    debtGDP:parseFloat(document.getElementById('debtGDP').value)||60,
    muY:(parseFloat(document.getElementById('muY').value)||2.5)/100,
    muPi:(parseFloat(document.getElementById('muPi').value)||2.0)/100,
    muN:(parseFloat(document.getElementById('muN').value)||2.0)/100,
    couponConv:(parseFloat(document.getElementById('couponConv').value)||4.0)/100,
    alphaN:parseFloat(document.getElementById('alphaN').value)||0.7,
    cap:(parseFloat(document.getElementById('cap').value)||4.0)/100,
    thetaAI:parseFloat(document.getElementById('thetaAI').value)||0.3,
    share:(parseFloat(document.getElementById('share').value)||30)/100,
    pam:document.getElementById('pam').checked
  };
}""",
    """function parseNum(id, fallback) {
  const el = document.getElementById(id);
  if (!el) return fallback;
  const v = parseFloat(el.value);
  return isNaN(v) ? fallback : v;
}

function readInputs(){
  return{
    gdp: parseNum('gdp', 250),
    debtGDP: parseNum('debtGDP', 60),
    muY: parseNum('muY', 2.5)/100,
    muPi: parseNum('muPi', 2.0)/100,
    muN: parseNum('muN', 2.0)/100,
    couponConv: parseNum('couponConv', 4.0)/100,
    alphaN: parseNum('alphaN', 0.7),
    cap: parseNum('cap', 4.0)/100,
    thetaAI: parseNum('thetaAI', 0.3),
    share: parseNum('share', 30)/100,
    pam: document.getElementById('pam').checked
  };
}"""
))

fixes.append((
    "Card label: cost",
    '<div class="lbl">Expected cost (bond price)</div>',
    '<div class="lbl">Expected cost (100% prod issuance)</div>'
))

fixes.append((
    "Card label: distress",
    '<div class="lbl">Distress probability</div>',
    '<div class="lbl">Distress (100% prod issuance)</div>'
))

fixes.append((
    "Card: saving color hook",
    """<div class="stat-card green">
            <div class="num" id="statSaving">—</div>
            <div class="lbl">Cost saving vs conventional</div>
          </div>""",
    """<div class="stat-card" id="statSavingCard">
            <div class="num" id="statSaving">—</div>
            <div class="lbl">Saving vs conventional (100% prod)</div>
          </div>"""
))

fixes.append((
    "Note under stat grid",
    """<div class="lbl">Recommended portfolio share</div>
          </div>
        </div>""",
    """<div class="lbl">Recommended portfolio share</div>
          </div>
        </div>
        <div style="font-size:0.75rem;color:var(--text-muted);margin-top:-0.4rem;margin-bottom:1rem;">
          Cards above show <strong>100% productivity issuance</strong>. At your chosen <strong><span id="shareDisplay">30</span>% share</strong>, blended results differ — see verdict below.
        </div>"""
))

fixes.append((
    "Remove unused GDP input",
    """        <label>GDP (billions)
          <input type="number" id="gdp" value="250" step="10" min="10" />
        </label>
""",
    ""
))

fixes.append((
    "Failure preset fix",
    "failure:{gdp:500,debtGDP:80,muY:2.0,muPi:2.0,muN:2.0,couponConv:5.0,alphaN:0.80,cap:4.0,thetaAI:0.10,share:50,pam:false,label:'⚠️ Failure Case — θ_AI = 0.10, below threshold'}",
    "failure:{gdp:500,debtGDP:80,muY:2.0,muPi:2.0,muN:2.0,couponConv:4.0,alphaN:0.80,cap:4.0,thetaAI:0.05,share:50,pam:false,label:'⚠️ Failure Case — θ_AI = 0.05, far below threshold'}"
))

fixes.append((
    "AI button label",
    '<button class="btn-secondary" id="aiButton" onclick="generateAI()">🧠 Generate AI Analysis</button>',
    '<button class="btn-secondary" id="aiButton" onclick="generateAI()">📝 Interpret this scenario</button>'
))

fixes.append((
    "AI placeholder text",
    """<span class="placeholder">Click "Generate AI Analysis" for detailed interpretation.</span>
          <div style="margin-top:0.4rem; font-size:0.65rem; color:var(--text-muted); opacity:0.6;">⚠️ AI can make mistakes. Verify with your own research.</div>""",
    """<span class="placeholder">Click "Interpret this scenario" for a rule-based analysis.</span>
          <div style="margin-top:0.4rem; font-size:0.65rem; color:var(--text-muted); opacity:0.6;">Rule-based interpretation. LLM worker not yet connected.</div>"""
))

fixes.append((
    "Noscript visibility",
    """  <link rel="stylesheet" href="css/core.min.css" />

  <style>
    html { opacity: 0; transition: opacity 0.12s ease; }""",
    """  <link rel="stylesheet" href="css/core.min.css" />
  <noscript><style>html{opacity:1!important}</style></noscript>

  <style>
    html { opacity: 0; transition: opacity 0.12s ease; }"""
))

fixes.append((
    "Load-timeout failsafe",
    '  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js" defer></script>',
    """  <script>setTimeout(function(){document.documentElement.classList.add('loaded');},2000);</script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js" defer></script>"""
))

fixes.append((
    "Saving card color logic",
    """  const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
  document.getElementById('statSaving').textContent=saving.toFixed(2)+'%';
  document.getElementById('statOptimal').textContent=(port.optimal.share*100).toFixed(0)+'%';""",
    """  const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
  document.getElementById('statSaving').textContent=saving.toFixed(2)+'%';
  const savingCard=document.getElementById('statSavingCard');
  if(savingCard)savingCard.className='stat-card '+(saving<0?'green':'red');
  document.getElementById('statOptimal').textContent=(port.optimal.share*100).toFixed(0)+'%';
  const sd=document.getElementById('shareDisplay');
  if(sd)sd.textContent=(p.share*100).toFixed(0);"""
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
print("")
print(str(ok) + " applied, " + str(skipped) + " skipped.")
