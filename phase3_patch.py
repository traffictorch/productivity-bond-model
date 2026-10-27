#!/usr/bin/env python3
import pathlib, sys

path = pathlib.Path('policy-lab.html')
if not path.exists():
    print("ERROR: policy-lab.html not found")
    sys.exit(1)

html = path.read_text()

if 'simulateEconomyAsync' in html:
    print("Already patched. Nothing to do.")
    sys.exit(0)

fixes = []

# FIX 1: Add simulateEconomyAsync (chunked, yields to UI)
fixes.append((
    "Add async chunked engine",
    """  return{g_y,g_n,pi,y,r,g:gS,g_r,primary_balance:pb,config:cfg};
}

function computeCoupons(economy,bondType,config){""",
    """  return{g_y,g_n,pi,y,r,g:gS,g_r,primary_balance:pb,config:cfg};
}

// Async chunked engine — yields to UI between batches
function simulateEconomyAsync(config, onProgress) {
  return new Promise(function(resolve) {
    const cfg = Object.assign({}, DEFAULTS, config);
    const nP = cfg.n_paths, nY = cfg.n_years;
    const rng = createRNG(cfg.seed);
    const g_y = zeros(nP, nY), g_n = zeros(nP, nY), pi = zeros(nP, nY);
    const y = zeros(nP, nY), r = zeros(nP, nY), gS = zeros(nP, nY);
    const g_r = zeros(nP, nY), pb = zeros(nP, nY);
    const ai_jump = zeros(nP, nY);
    for (let p = 0; p < nP; p++) for (let t = 0; t < nY; t++) if (rng() < cfg.lambda_ai) ai_jump[p][t] = gamma(rng, cfg.ai_shape, cfg.ai_scale);
    const sqrtRho = Math.sqrt(Math.max(0, 1 - cfg.rho_ny * cfg.rho_ny));
    let pIdx = 0;
    const chunkSize = Math.max(200, Math.floor(nP / 20));
    function processChunk() {
      const end = Math.min(pIdx + chunkSize, nP);
      for (; pIdx < end; pIdx++) {
        const pp = pIdx;
        let g_y_prev = cfg.mu_y, g_n_prev = cfg.mu_n, pi_prev = cfg.mu_pi, y_prev = cfg.y0, r_prev = cfg.tau * cfg.y0;
        for (let t = 0; t < nY; t++) {
          const z_y = normal(rng), z_n_indep = normal(rng), z_pi = normal(rng);
          const z_n = cfg.rho_ny * z_y + sqrtRho * z_n_indep;
          const aiG = cfg.ai_gdp_mult * ai_jump[pp][t], aiN = cfg.ai_npi_mult * ai_jump[pp][t], aiP = cfg.ai_pi_mult * ai_jump[pp][t];
          g_y[pp][t] = cfg.mu_y + cfg.rho_y * (g_y_prev - cfg.mu_y) + cfg.sigma_y * z_y + aiG;
          g_n[pp][t] = cfg.mu_n + cfg.rho_n * (g_n_prev - cfg.mu_n) + cfg.sigma_n * z_n + aiN;
          pi[pp][t] = cfg.mu_pi + cfg.rho_pi * (pi_prev - cfg.mu_pi) + cfg.sigma_pi * z_pi + cfg.gamma_y * (g_y[pp][t] - cfg.mu_y) + aiP;
          y[pp][t] = y_prev * (1 + g_y[pp][t]);
          const aiGain = Math.max(y_prev * aiG, 0);
          r[pp][t] = cfg.tau * y[pp][t] + cfg.theta_ai * aiGain;
          g_r[pp][t] = r_prev > 1e-8 ? r[pp][t] / r_prev - 1 : 0;
          const autoStab = -0.05 * (g_y[pp][t] - cfg.mu_y) * y[pp][t];
          gS[pp][t] = Math.max(cfg.g0_over_y0 * y[pp][t] * (1 + 0.3 * (g_y[pp][t] - cfg.mu_y)) + autoStab, 0.10 * y[pp][t]);
          pb[pp][t] = r[pp][t] - gS[pp][t];
          g_y_prev = g_y[pp][t]; g_n_prev = g_n[pp][t]; pi_prev = pi[pp][t]; y_prev = y[pp][t]; r_prev = r[pp][t];
        }
      }
      if (onProgress) onProgress(pIdx, nP);
      if (pIdx < nP) setTimeout(processChunk, 0);
      else resolve({g_y, g_n, pi, y, r, g: gS, g_r, primary_balance: pb, config: cfg});
    }
    processChunk();
  });
}

function computeCoupons(economy,bondType,config){"""
))

# FIX 2: Button IDs and onclick
fixes.append((
    "Button: Run Analysis",
    '<button class="btn-primary" onclick="runAnalysis(2000)" style="padding:0.7rem 1.8rem;">▶ Run Analysis</button>',
    '<button class="btn-primary" id="runBtn" onclick="runAnalysisAsync(2000)" style="padding:0.7rem 1.8rem;">▶ Run Analysis</button>'
))

fixes.append((
    "Button: Full Monte Carlo",
    '<button class="btn-secondary" onclick="runAnalysis(10000)" style="padding:0.7rem 1.8rem;">⚡ Full Monte Carlo (10k paths)</button>',
    '<button class="btn-secondary" id="mcBtn" onclick="runAnalysisAsync(10000)" style="padding:0.7rem 1.8rem;">⚡ Full Monte Carlo (10k paths)</button>'
))

# FIX 3: Stale banner
fixes.append((
    "Stale results banner",
    '<div id="results" class="result-box" style="display:none;">',
    """<div id="staleBanner" style="display:none;margin-bottom:1rem;padding:0.6rem 1rem;background:rgba(251,191,36,0.12);border-left:3px solid #f59e0b;border-radius:4px;font-size:0.85rem;color:var(--text-secondary);">⚠️ Inputs changed since last run — click Run Analysis to update.</div>
      <div id="results" class="result-box" style="display:none;">"""
))

# FIX 4: runAnalysisAsync
fixes.append((
    "Add runAnalysisAsync",
    "function renderResults(p,conv,prod,port,ilb){",
    """async function runAnalysisAsync(nPaths){
  nPaths=nPaths||2000;
  const runBtn=document.getElementById('runBtn');
  const mcBtn=document.getElementById('mcBtn');
  if(runBtn)runBtn.disabled=true;
  if(mcBtn)mcBtn.disabled=true;
  const status=document.getElementById('status');
  try{
    const p=readInputs();
    const cfg=buildConfig(p,nPaths);
    currentScenario=p;
    if(status)status.textContent='Running 0 / '+nPaths.toLocaleString()+' paths…';
    const econ=await simulateEconomyAsync(cfg,function(done,total){
      if(status)status.textContent='Running '+done.toLocaleString()+' / '+total.toLocaleString()+' paths…';
    });
    const conv=evaluateBond(econ,'conventional',cfg);
    const prod=evaluateBond(econ,'productivity',cfg);
    const ilb=evaluateBond(econ,'inflation_linked',cfg);
    const port=computePortfolio(econ,cfg,[0,0.1,0.2,0.3,0.4,0.5,0.75,1.0]);
    lastResult={p,cfg,conv,prod,port,ilb};
    renderResults(p,conv,prod,port,ilb);
    if(status)status.textContent='✅ Done — '+nPaths.toLocaleString()+' paths';
    const sb=document.getElementById('staleBanner');
    if(sb)sb.style.display='none';
  }catch(e){
    console.error(e);
    if(status)status.textContent='❌ '+e.message;
  }finally{
    if(runBtn)runBtn.disabled=false;
    if(mcBtn)mcBtn.disabled=false;
  }
}

function renderResults(p,conv,prod,port,ilb){"""
))

# FIX 5: Toast function
fixes.append((
    "Add toast function",
    "function buildShareUrl(){",
    """function toast(msg){
  let t=document.getElementById('pbm-toast');
  if(!t){
    t=document.createElement('div');
    t.id='pbm-toast';
    t.style.cssText='position:fixed;bottom:2rem;right:2rem;background:rgba(12,15,25,0.95);color:#eef2f8;padding:0.7rem 1.2rem;border-radius:8px;border:1px solid rgba(255,255,255,0.1);box-shadow:0 8px 24px rgba(0,0,0,0.4);z-index:99999;font-size:0.85rem;font-weight:500;opacity:0;transition:opacity 0.2s,transform 0.2s;transform:translateY(10px);pointer-events:none;';
    document.body.appendChild(t);
  }
  t.textContent=msg;
  requestAnimationFrame(function(){t.style.opacity='1';t.style.transform='translateY(0)';});
  clearTimeout(t._timer);
  t._timer=setTimeout(function(){t.style.opacity='0';t.style.transform='translateY(10px)';},2000);
}

function buildShareUrl(){"""
))

# FIX 6: Specific alert→toast
fixes.append((
    "Alert: share link",
    "alert('Share link copied! It reproduces this exact scenario.')",
    "toast('Share link copied')"
))

fixes.append((
    "Alert: summary copied",
    "alert('Summary copied!')",
    "toast('Summary copied')"
))

# FIX 7: Replace exportCSV
fixes.append((
    "Rewrite exportCSV",
    """function exportCSV(){
  if(!lastResult){alert('Run analysis first.');return;}
  const{p,conv,prod}=lastResult;
  let csv='Year,Conv_Coupon,Prod_Coupon,Conv_Debt_to_GDP,Prod_Debt_to_GDP,Conv_DSR,Prod_DSR\\n';
  for(let i=0;i<10;i++){
    csv+=(i+1)+',';
    csv+=conv.raw.coupons[0][i].toFixed(4)+',';
    csv+=prod.raw.coupons[0][i].toFixed(4)+',';
    csv+=conv.trajectory.meanDebtToGDP[i].toFixed(4)+',';
    csv+=prod.trajectory.meanDebtToGDP[i].toFixed(4)+',';
    csv+=conv.trajectory.meanDSR[i].toFixed(4)+',';
    csv+=prod.trajectory.meanDSR[i].toFixed(4)+'\\n';
  }
  const blob=new Blob([csv],{type:'text/csv'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url;
  a.download='policy-lab-scenario.csv';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  URL.revokeObjectURL(url);
}""",
    """function exportCSV(){
  if(!lastResult){toast('Run analysis first.');return;}
  const{p,conv,prod,ilb,port}=lastResult;
  let csv='Policy Lab Export,'+new Date().toISOString().slice(0,10)+'\\n\\n';
  csv+='INPUTS\\n';
  csv+='Debt/GDP,'+p.debtGDP+'%\\n';
  csv+='Nominal growth,'+(p.muY*100).toFixed(2)+'%\\n';
  csv+='Inflation,'+(p.muPi*100).toFixed(2)+'%\\n';
  csv+='NPI growth,'+(p.muN*100).toFixed(2)+'%\\n';
  csv+='Coupon conv,'+(p.couponConv*100).toFixed(2)+'%\\n';
  csv+='alpha_N,'+p.alphaN+'\\n';
  csv+='Cap,'+(p.cap*100).toFixed(2)+'%\\n';
  csv+='theta_AI,'+p.thetaAI+'\\n';
  csv+='Share,'+(p.share*100).toFixed(0)+'%\\n';
  csv+='PAM,'+(p.pam?'on':'off')+'\\n\\n';
  csv+='SUMMARY\\nMetric,Conventional,Productivity,Inflation-Linked\\n';
  csv+='Expected cost,'+conv.expectedCost.toFixed(4)+','+prod.expectedCost.toFixed(4)+','+(ilb?ilb.expectedCost.toFixed(4):'')+'\\n';
  csv+='Distress prob,'+(conv.distressProb*100).toFixed(2)+'%,'+(prod.distressProb*100).toFixed(2)+'%,'+(ilb?(ilb.distressProb*100).toFixed(2):'')+'%\\n';
  csv+='Welfare,'+conv.welfare.toFixed(4)+','+prod.welfare.toFixed(4)+','+(ilb?ilb.welfare.toFixed(4):'')+'\\n';
  csv+='Optimal portfolio share,'+(port.optimal.share*100).toFixed(0)+'%\\n\\n';
  csv+='TRAJECTORY (mean across paths)\\n';
  csv+='Year,Conv_Debt/GDP,Prod_Debt/GDP,ILB_Debt/GDP,Conv_DSR,Prod_DSR,ILB_DSR\\n';
  for(let i=0;i<10;i++){
    csv+=(i+1)+',';
    csv+=conv.trajectory.meanDebtToGDP[i].toFixed(4)+',';
    csv+=prod.trajectory.meanDebtToGDP[i].toFixed(4)+',';
    csv+=(ilb?ilb.trajectory.meanDebtToGDP[i].toFixed(4):'')+',';
    csv+=conv.trajectory.meanDSR[i].toFixed(4)+',';
    csv+=prod.trajectory.meanDSR[i].toFixed(4)+',';
    csv+=(ilb?ilb.trajectory.meanDSR[i].toFixed(4):'')+'\\n';
  }
  const blob=new Blob([csv],{type:'text/csv'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url;
  a.download='policy-lab-'+new Date().toISOString().slice(0,10)+'.csv';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  URL.revokeObjectURL(url);
  toast('CSV exported');
}"""
))

# FIX 8: Init listeners + keyboard
fixes.append((
    "Init: stale listeners + keyboard",
    """window.addEventListener('load',function(){
  document.documentElement.classList.add('loaded');""",
    """window.addEventListener('load',function(){
  document.documentElement.classList.add('loaded');
  ['debtGDP','muY','muPi','muN','couponConv','alphaN','cap','thetaAI','share','pam'].forEach(function(id){
    const el=document.getElementById(id);
    if(el)el.addEventListener('change',function(){
      const sb=document.getElementById('staleBanner');
      if(sb&&lastResult)sb.style.display='block';
    });
  });
  document.querySelectorAll('.accordion-toggle').forEach(function(el){
    el.setAttribute('role','button');
    el.setAttribute('tabindex','0');
    el.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();el.click();}
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

# Post-pass: replace any remaining alert('Run analysis first.') with toast
remaining = html.count("alert('Run analysis first.')")
if remaining > 0:
    html = html.replace("alert('Run analysis first.')", "toast('Run analysis first.')")
    print("  OK  Cleanup: " + str(remaining) + " remaining alert('Run analysis first.') -> toast")

path.write_text(html)
print("")
print(str(ok) + " applied, " + str(skipped) + " skipped.")
