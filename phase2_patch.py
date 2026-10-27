#!/usr/bin/env python3
import pathlib, sys

path = pathlib.Path('policy-lab.html')
if not path.exists():
    print("ERROR: policy-lab.html not found")
    sys.exit(1)

html = path.read_text()

if 'inflation_linked' in html and 'ILB dominates' in html:
    print("Already patched. Nothing to do.")
    sys.exit(0)

fixes = []

# ── FIX 1: Add inflation_linked case to computeCoupons ──
fixes.append((
    "Add inflation_linked bond case",
    """switch(bondType){
      case'conventional':c=cfg.conventional_coupon;break;
      case'gdp_linked':c=(1+pi)*(1+clamp(cfg.alpha_g*gY,cfg.floor,cfg.cap))-1;break;""",
    """switch(bondType){
      case'conventional':c=cfg.conventional_coupon;break;
      case'inflation_linked':c=(1+pi)*(1+cfg.inflation_real_spread)-1;break;
      case'gdp_linked':c=(1+pi)*(1+clamp(cfg.alpha_g*gY,cfg.floor,cfg.cap))-1;break;"""
))

# ── FIX 2: Scope PAM to productivity + hybrid only ──
fixes.append((
    "PAM applies only to productivity/hybrid",
    """function computeDebtPath(cfg,economy,coupons){
  const nP=coupons.length,nY=coupons[0].length;
  const d=zeros(nP,nY);
  const initialDebt=cfg.d0_over_y0*cfg.y0;
  for(let p=0;p<nP;p++){
    let d_prev=initialDebt;
    for(let t=0;t<nY;t++){
      const c=coupons[p][t];
      const ds=d_prev*c;
      const rev=economy.r[p][t];
      let dNew=d_prev*(1+c)-economy.primary_balance[p][t];
      if(cfg.pam_enabled&&rev>0&&ds/rev>cfg.pam_trigger)dNew*=(1-cfg.pam_factor);""",
    """function computeDebtPath(cfg,economy,coupons,bondType){
  const nP=coupons.length,nY=coupons[0].length;
  const d=zeros(nP,nY);
  const initialDebt=cfg.d0_over_y0*cfg.y0;
  const pamApplies=(bondType==='productivity'||bondType==='hybrid')&&cfg.pam_enabled;
  for(let p=0;p<nP;p++){
    let d_prev=initialDebt;
    for(let t=0;t<nY;t++){
      const c=coupons[p][t];
      const ds=d_prev*c;
      const rev=economy.r[p][t];
      let dNew=d_prev*(1+c)-economy.primary_balance[p][t];
      if(pamApplies&&rev>0&&ds/rev>cfg.pam_trigger)dNew*=(1-cfg.pam_factor);"""
))

fixes.append((
    "Update computeDebtPath call site with bondType",
    "const debt=computeDebtPath(cfg,economy,coupons);",
    "const debt=computeDebtPath(cfg,economy,coupons,bondType);"
))

# ── FIX 3: Compute ILB in runAnalysis ──
fixes.append((
    "Compute ILB in runAnalysis",
    """const port=computePortfolio(econ,cfg,[0,0.1,0.2,0.3,0.4,0.5,0.75,1.0]);
      lastResult={p,cfg,conv,prod,port};
      renderResults(p,conv,prod,port);""",
    """const ilb=evaluateBond(econ,'inflation_linked',cfg);
      const port=computePortfolio(econ,cfg,[0,0.1,0.2,0.3,0.4,0.5,0.75,1.0]);
      lastResult={p,cfg,conv,prod,port,ilb};
      renderResults(p,conv,prod,port,ilb);"""
))

# ── FIX 4: renderResults signature + pass ILB to charts ──
fixes.append((
    "renderResults accepts ilb",
    "function renderResults(p,conv,prod,port){",
    "function renderResults(p,conv,prod,port,ilb){"
))

fixes.append((
    "renderResults passes ilb to charts and verdict",
    """  drawTrajectory(conv,prod);
  drawDSR(conv,prod);
  renderVerdict(p,conv,prod,port);""",
    """  drawTrajectory(conv,prod,ilb);
  drawDSR(conv,prod,ilb);
  renderVerdict(p,conv,prod,port,ilb);"""
))

# ── FIX 5: drawTrajectory with ILB dataset ──
fixes.append((
    "drawTrajectory signature accepts ilb",
    "function drawTrajectory(conv,prod){",
    "function drawTrajectory(conv,prod,ilb){"
))

fixes.append((
    "drawTrajectory ILB dataset",
    """        {label:'Conventional',data:conv.trajectory.meanDebtToGDP,borderColor:'#f87171',backgroundColor:'rgba(248,113,113,0.1)',fill:true,tension:0.3,pointRadius:3},
        {label:'Productivity',data:prod.trajectory.meanDebtToGDP,borderColor:'#4f46e5',backgroundColor:'rgba(79,70,229,0.1)',fill:true,tension:0.3,pointRadius:3}""",
    """        {label:'Conventional',data:conv.trajectory.meanDebtToGDP,borderColor:'#f87171',backgroundColor:'rgba(248,113,113,0.1)',fill:true,tension:0.3,pointRadius:3},
        {label:'Productivity',data:prod.trajectory.meanDebtToGDP,borderColor:'#4f46e5',backgroundColor:'rgba(79,70,229,0.1)',fill:true,tension:0.3,pointRadius:3},
        {label:'Inflation-linked',data:(ilb&&ilb.trajectory)?ilb.trajectory.meanDebtToGDP:null,borderColor:'#34d399',backgroundColor:'transparent',fill:false,tension:0.3,pointRadius:3,borderDash:[6,3]}"""
))

# ── FIX 6: drawDSR with ILB dataset ──
fixes.append((
    "drawDSR signature accepts ilb",
    "function drawDSR(conv,prod){",
    "function drawDSR(conv,prod,ilb){"
))

fixes.append((
    "drawDSR ILB dataset",
    """        {label:'Conventional DSR',data:conv.trajectory.meanDSR,borderColor:'#f87171',tension:0.3,pointRadius:3},
        {label:'Productivity DSR',data:prod.trajectory.meanDSR,borderColor:'#4f46e5',tension:0.3,pointRadius:3},""",
    """        {label:'Conventional DSR',data:conv.trajectory.meanDSR,borderColor:'#f87171',tension:0.3,pointRadius:3},
        {label:'Productivity DSR',data:prod.trajectory.meanDSR,borderColor:'#4f46e5',tension:0.3,pointRadius:3},
        {label:'Inflation-linked DSR',data:(ilb&&ilb.trajectory)?ilb.trajectory.meanDSR:null,borderColor:'#34d399',tension:0.3,pointRadius:3,borderDash:[6,3]},"""
))

# ── FIX 7: renderVerdict signature + ILB dominance + theta note ──
fixes.append((
    "renderVerdict accepts ilb",
    "function renderVerdict(p,conv,prod,port){",
    "function renderVerdict(p,conv,prod,port,ilb){"
))

fixes.append((
    "renderVerdict adds ILB dominance + theta note",
    """  sol.innerHTML=parts.join('<br>');
  act.textContent='Model: endogenous debt · '+(currentScenario?'θ_AI='+p.thetaAI.toFixed(2)+', α_N='+p.alphaN.toFixed(2)+', cap='+(p.cap*100).toFixed(1)+'%':'');""",
    """  if(ilb && ilb.expectedCost < prod.expectedCost && ilb.distressProb < prod.distressProb){
    parts.push('<div style="margin-top:0.6rem;padding:0.7rem 1rem;background:rgba(251,191,36,0.15);border-left:3px solid #f59e0b;border-radius:4px;"><strong>⚠️ Inflation-linked comparison:</strong> Under these parameters, an ILB would be both cheaper (cost '+ilb.expectedCost.toFixed(3)+') and less distress-prone ('+(ilb.distressProb*100).toFixed(1)+'%) than a productivity bond. The case for the productivity bond rests on alignment with efficiency metrics, not cost minimisation.</div>');
  }
  parts.push('<div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.6rem;padding-top:0.5rem;border-top:1px solid var(--border-divider);"><strong>Note:</strong> θ_AI affects outcomes primarily through rare AI shocks in this calibration. The 0.15 / 0.30 thresholds are from the book\\'s analytical framework, not this simulation.</div>');
  sol.innerHTML=parts.join('<br>');
  act.textContent='Model: endogenous debt · '+(currentScenario?'θ_AI='+p.thetaAI.toFixed(2)+', α_N='+p.alphaN.toFixed(2)+', cap='+(p.cap*100).toFixed(1)+'%':'');"""
))

# ── FIX 8: Version banner upgrade ──
fixes.append((
    "Version banner points to model-notes",
    """      <div class="warn-banner">
        ⚠️ <strong>Model version note:</strong> These results use the <strong>endogenous-debt model (v1.1)</strong>. The book's Appendix C used an older fixed-debt calibration — numbers may differ. See <a href="changelog.html" style="color:#f59e0b; text-decoration:underline;">CHANGELOG</a>.
      </div>""",
    """      <div class="warn-banner">
        ⚠️ <strong>Model v1.1 (endogenous debt).</strong> Book Appendix C uses v1.0 (fixed debt). Numbers differ by design. <a href="model-notes.html" style="color:#f59e0b;text-decoration:underline;font-weight:600;">Full model notes →</a>
      </div>"""
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
