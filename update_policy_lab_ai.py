#!/usr/bin/env python3
import pathlib, re

path = pathlib.Path('policy-lab.html')
html = path.read_text()

# ── FIX 1: Replace placeholder text ──
old_placeholder = '''<span class="placeholder">Click "Interpret this scenario" for a rule-based analysis.</span>
          <div style="margin-top:0.4rem; font-size:0.65rem; color:var(--text-muted); opacity:0.6;">Rule-based interpretation. LLM worker not yet connected.</div>'''

new_placeholder = '''<span class="placeholder">Click "Interpret this scenario" for AI-powered analysis.</span>
          <div style="margin-top:0.4rem; font-size:0.65rem; color:var(--text-muted); opacity:0.6;">⚠️ AI can make mistakes. Verify with your own research.</div>'''

if old_placeholder in html:
    html = html.replace(old_placeholder, new_placeholder)
    print("✅ Placeholder text updated")
else:
    print("⚠️ Placeholder not matched exactly - trying regex fallback")
    pattern = r'<span class="placeholder">Click "Interpret this scenario"[^<]*</span>\s*<div[^>]*>Rule-based interpretation[^<]*</div>'
    if re.search(pattern, html):
        html = re.sub(pattern, 
            '<span class="placeholder">Click "Interpret this scenario" for AI-powered analysis.</span>\n          <div style="margin-top:0.4rem; font-size:0.65rem; color:var(--text-muted); opacity:0.6;">⚠️ AI can make mistakes. Verify with your own research.</div>',
            html)
        print("✅ Placeholder updated via regex")
    else:
        print("❌ Placeholder not found")

# ── FIX 2: Replace generateAI function ──
func_start = html.find("async function generateAI(){")
init_marker = html.find("// ============================================================\n// INIT", func_start)

if func_start == -1 or init_marker == -1:
    print("❌ Cannot locate generateAI function boundaries")
    print(f"   func_start: {func_start}, init_marker: {init_marker}")
else:
    new_func = '''async function generateAI(){
  if(!lastResult){toast('Run analysis first.');return;}
  const btn=document.getElementById('aiButton');
  const status=document.getElementById('aiStatus');
  const out=document.getElementById('aiOutput');
  btn.disabled=true;
  status.textContent='\\u23f3 Thinking\\u2026';
  out.innerHTML='<span style="opacity:0.6;">Analyzing scenario via AI\\u2026</span>';

  const{p,conv,prod,port}=lastResult;
  const ilb = lastResult.ilb || null;
  const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
  const distDiff=prod.distressProb-conv.distressProb;

  let verdictText='';
  if (conv.distressProb > 0.5) verdictText='Unsustainable baseline (>50% distress).';
  else if (saving < -2 && distDiff <= 0.02) verdictText='Clear win (cheaper, no worse distress).';
  else if (saving < -2 && distDiff > 0.05) verdictText='Trade-off (cheaper but riskier).';
  else verdictText='Neutral or worse.';

  // Slim payload - do not send full matrices
  const payload = {
    scenario: {
      debtGDP: p.debtGDP,
      muY: p.muY, muPi: p.muPi, muN: p.muN,
      couponConv: p.couponConv,
      alphaN: p.alphaN, cap: p.cap,
      thetaAI: p.thetaAI, share: p.share, pam: p.pam
    },
    conventional: {
      cost: conv.expectedCost,
      distress: conv.distressProb,
      welfare: conv.welfare
    },
    productivity: {
      cost: prod.expectedCost,
      distress: prod.distressProb,
      welfare: prod.welfare
    },
    ilb: ilb ? { cost: ilb.expectedCost, distress: ilb.distressProb } : null,
    optimalShare: port.optimal.share,
    verdict: verdictText
  };

  try {
    // Try the Cloudflare Worker
    const response = await fetch('https://ai-policy.traffictorch.workers.dev', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error('Worker HTTP ' + response.status);
    const result = await response.json();
    if (result.error) throw new Error(result.error);

    let html = '';
    if (result.summary) html += '<div class="summary">\\ud83d\\udccc ' + result.summary + '</div>';
    if (result.advice) html += '<div class="advice">\\u2705 ' + result.advice + '</div>';
    html += '<div style="margin-top:0.5rem;font-size:0.6rem;color:var(--text-muted);opacity:0.6;">\\u26a0\\ufe0f AI-generated analysis. Verify with your own research.</div>';

    out.innerHTML = html;
    status.textContent = '\\u2705 Done';

  } catch (error) {
    // Fallback to rule-based
    console.warn('AI Worker failed, using rule-based fallback:', error);
    let summary='\\ud83d\\udccc ', advice='';

    if (conv.distressProb > 0.5) {
      summary='\\u26a0\\ufe0f The sovereign is already in a high-distress regime (>50%).';
      advice='\\u2705 Policy recommendation: focus on primary balance before issuing new bond structures.';
    } else if (saving < -2 && distDiff <= 0.02) {
      summary='\\u2705 The productivity bond is a clear win: cheaper ('+saving.toFixed(2)+'%).';
      advice='\\u2705 Policy recommendation: proceed with a pilot issuance at ~'+(port.optimal.share*100).toFixed(0)+'% of new debt.';
    } else if (saving < -2 && distDiff > 0.05) {
      summary='\\u26a0\\ufe0f Trade-off: the bond is cheaper ('+saving.toFixed(2)+'%), but significantly riskier (+'+(distDiff*100).toFixed(1)+'pp).';
      advice='\\u2705 Policy recommendation: '+(p.pam?'PAM is enabled, but further adjustment may be needed.':'Enable PAM to mitigate the feedback loop.');
    } else {
      summary='\\ud83d\\udcca Neutral outcome: saving is '+saving.toFixed(2)+'%, distress change is +'+(distDiff*100).toFixed(1)+'pp.';
      advice='\\u2705 Policy recommendation: the instrument does not materially improve this scenario.';
    }
    out.innerHTML='<div class="summary">'+summary+'</div><div class="advice" style="margin-top:0.5rem;">'+advice+'</div><div style="margin-top:0.5rem;font-size:0.6rem;color:var(--text-muted);opacity:0.6;">\\u26a0\\ufe0f Offline rule-based analysis (worker unavailable).</div>';
    status.textContent = '\\u2705 Done (Offline)';
  } finally {
    btn.disabled=false;
  }
}

'''
    html = html[:func_start] + new_func + html[init_marker:]
    print("✅ generateAI function replaced with worker + fallback")

# Save
path.write_text(html)
print("File saved.")

# Verification
html_check = path.read_text()
checks = {
    "Old dev note gone": "LLM worker not yet connected" not in html_check,
    "New placeholder present": "AI-powered analysis" in html_check,
    "Worker URL present": "ai-policy.traffictorch.workers.dev" in html_check,
    "Fallback present": "Offline rule-based analysis" in html_check,
    "Slim payload used": "optimalShare: port.optimal.share" in html_check
}
print("\nVerification:")
for name, ok in checks.items():
    print(f"  {'✅' if ok else '❌'} {name}")
