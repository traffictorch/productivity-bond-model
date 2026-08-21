// ============================================================
// HOME.JS – Full home‑page functionality
// ============================================================

(function() {
  'use strict';

  console.log('🏠 home.js loaded');

  // ---------- DOM helpers ----------
  function getEl(id) { return document.getElementById(id); }
  function qs(sel) { return document.querySelector(sel); }
  function qsa(sel) { return document.querySelectorAll(sel); }

  // ---------- LAZY LOAD PLOTLY ----------
  let plotlyLoaded = false;
  let plotlyLoading = false;
  let plotlyQueue = [];

  function loadPlotly() {
    return new Promise((resolve, reject) => {
      if (plotlyLoaded) { resolve(); return; }
      if (plotlyLoading) {
        plotlyQueue.push(resolve);
        return;
      }
      plotlyLoading = true;
      console.log('📦 Loading Plotly...');
      const script = document.createElement('script');
      script.src = 'https://cdn.plot.ly/plotly-2.27.1.min.js';
      script.async = true;
      script.onload = () => {
        plotlyLoaded = true;
        plotlyLoading = false;
        plotlyQueue.forEach(r => r());
        plotlyQueue = [];
        console.log('✅ Plotly loaded');
        resolve();
        renderAllCharts();
      };
      script.onerror = () => {
        plotlyLoading = false;
        console.error('❌ Plotly load failed');
        reject(new Error('Plotly load failed'));
      };
      document.body.appendChild(script);
    });
  }

  // ---------- DIVERGENCE CHART ----------
  function renderDivergenceChart() {
    const div = getEl('chart-divergence');
    if (!div || typeof Plotly === 'undefined') {
      setTimeout(renderDivergenceChart, 300);
      return;
    }

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#eef2f8' : '#0f111a';
    const gridColor = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';

    const years = Array.from({ length: 46 }, (_, i) => 1980 + i);
    const financial = years.map((_, i) => {
      const t = i / 45;
      const target = 50 + (250 * Math.pow(t, 1.8));
      return Math.min(target, 320);
    });
    financial[0] = 50;
    financial[45] = 305;

    const resources = years.map((_, i) => {
      const t = i / 45;
      const rise = 50 + 32 * (1 - Math.exp(-5 * t));
      const decline = Math.max(0, (i - 30) * 0.8);
      const plateau = rise - decline * 0.12;
      return Math.max(48, Math.min(plateau, 85));
    });
    resources[0] = 50;
    resources[45] = 58;

    const gapTrace = {
      x: years.concat(years.slice().reverse()),
      y: financial.concat(resources.slice().reverse()),
      fill: 'toself',
      fillcolor: 'rgba(248,113,113,0.15)',
      line: { color: 'transparent' },
      name: 'The Gap',
      hoverinfo: 'skip',
      showlegend: true
    };

    const traceFinancial = {
      x: years,
      y: financial,
      name: 'Financial Obligations (Debt)',
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: '#4f46e5', width: 3 },
      marker: { color: '#4f46e5', size: 4 },
      hovertemplate: '%{x}: $%{y:.0f}T<extra>Debt</extra>'
    };

    const traceResources = {
      x: years,
      y: resources,
      name: 'Resource Extraction',
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: '#34d399', width: 3 },
      marker: { color: '#34d399', size: 4 },
      hovertemplate: '%{x}: %{y:.0f}<extra>Resources</extra>'
    };

    const annotations = [
      { x: 1985, y: 58, text: '📈 Debt: $50T (1980)', showarrow: true, arrowhead: 2, ax: 0, ay: -35, font: { size: 10, color: textColor } },
      { x: 1995, y: 110, text: '💳 Debt accelerates', showarrow: true, arrowhead: 2, ax: -40, ay: -25, font: { size: 10, color: textColor } },
      { x: 2008, y: 175, text: '📉 2008 Financial Crisis', showarrow: true, arrowhead: 2, ax: 50, ay: -20, font: { size: 10, color: textColor } },
      { x: 2015, y: 220, text: '⚠️ The Gap Widens', showarrow: true, arrowhead: 2, ax: -50, ay: -30, font: { size: 11, color: '#f87171', weight: 'bold' } },
      { x: 2005, y: 82, text: '🌍 Resource extraction peaks', showarrow: true, arrowhead: 2, ax: 40, ay: 30, font: { size: 10, color: textColor } },
      { x: 2025, y: 305, text: '❓ $300T+ in debt', showarrow: true, arrowhead: 2, ax: 0, ay: -40, font: { size: 11, color: '#f87171', weight: 'bold' } }
    ];

    const layout = {
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: { color: textColor, family: 'Inter' },
      margin: { l: 60, r: 30, t: 30, b: 50 },
      xaxis: { title: 'Year', gridcolor: gridColor, range: [1978, 2027], tickmode: 'linear', dtick: 5 },
      yaxis: { title: 'Index (1980 = 50)', gridcolor: gridColor, range: [0, 350], tickformat: '.0f' },
      legend: { orientation: 'h', x: 0.5, y: 1.08, xanchor: 'center', font: { size: 11 } },
      annotations,
      displayModeBar: false,
      hovermode: 'x unified'
    };

    Plotly.newPlot('chart-divergence', [gapTrace, traceFinancial, traceResources], layout, {
      responsive: true,
      displayModeBar: false
    });
    console.log('📈 Divergence chart rendered');
  }

  // ---------- RENDER ALL CHARTS ----------
  function renderAllCharts() {
    if (typeof Plotly === 'undefined') {
      setTimeout(renderAllCharts, 500);
      return;
    }

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#eef2f8' : '#0f111a';
    const gridColor = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';

    // Chart 1: Cost vs θ_AI
    const costTheta = document.getElementById('chart-cost-theta');
    if (costTheta) {
      const thetaValues = [0.10, 0.20, 0.30, 0.40, 0.50];
      const costConv = [0.5154, 0.5154, 0.5154, 0.5154, 0.5154];
      const costProd = [0.5079, 0.5035, 0.4994, 0.4959, 0.4923];
      const layout1 = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: textColor, family: 'Inter' },
        margin: { l: 40, r: 20, t: 20, b: 40 },
        xaxis: { title: 'θ_AI', gridcolor: gridColor },
        yaxis: { title: 'Expected Cost', gridcolor: gridColor },
        legend: { orientation: 'h', x: 0, y: 1.05 },
        displayModeBar: false
      };
      Plotly.newPlot('chart-cost-theta', [
        { x: thetaValues, y: costConv, name: 'Conventional', type: 'scatter', mode: 'lines+markers', line: { color: '#4b5563', width: 2 }, marker: { color: '#4b5563' } },
        { x: thetaValues, y: costProd, name: 'Productivity Bond', type: 'scatter', mode: 'lines+markers', line: { color: '#a78bfa', width: 3 }, marker: { color: '#a78bfa', size: 8 } }
      ], layout1, { responsive: true });
      console.log('📈 Cost vs θ_AI chart rendered');
    }

    // Chart 2: Distress vs α_N
    const distressAlpha = document.getElementById('chart-distress-alpha');
    if (distressAlpha) {
      const alphaValues = [0.30, 0.50, 0.70, 0.90, 1.00];
      const distressValues = [82.5, 85.8, 88.17, 89.6, 90.1];
      const layout2 = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: textColor, family: 'Inter' },
        margin: { l: 40, r: 20, t: 20, b: 40 },
        xaxis: { title: 'α_N (participation)', gridcolor: gridColor },
        yaxis: { title: 'Distress Probability (%)', gridcolor: gridColor },
        legend: { orientation: 'h', x: 0, y: 1.05 },
        displayModeBar: false
      };
      Plotly.newPlot('chart-distress-alpha', [
        { x: alphaValues, y: distressValues, name: 'Distress Probability', type: 'scatter', mode: 'lines+markers', line: { color: '#f87171', width: 3 }, marker: { color: '#f87171', size: 8 } }
      ], layout2, { responsive: true });
      console.log('📈 Distress vs α_N chart rendered');
    }

    // Chart 3: Happiness Curve (initial)
    const happinessDiv = document.getElementById('chart-happiness');
    if (happinessDiv) {
      const gNpiValues = Array.from({ length: 61 }, (_, i) => i * 0.001);
      const happinessValues = gNpiValues.map(g => 1 / (1 + Math.exp(-80 * (g - 0.03))));
      const layoutH = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: textColor, family: 'Inter' },
        margin: { l: 40, r: 20, t: 20, b: 40 },
        xaxis: { title: 'Productivity Growth (g_NPI)', gridcolor: gridColor, tickformat: '.0%' },
        yaxis: { title: 'Happiness Index', gridcolor: gridColor, range: [0, 1.1], tickformat: '.0%' },
        displayModeBar: false
      };
      Plotly.newPlot('chart-happiness', [
        { x: gNpiValues, y: happinessValues, type: 'scatter', mode: 'lines', line: { color: '#f472b6', width: 3 }, name: 'Happiness Curve' }
      ], layoutH, { responsive: true });
      console.log('📈 Happiness curve chart rendered');
    }

    // Divergence chart (already rendered separately)
    renderDivergenceChart();
  }

  // ---------- SIMULATOR ENGINE ----------
  function initSimulator() {
    const thetaSlider = getEl('theta-slider');
    const alphaSlider = getEl('alpha-slider');
    const capSlider = getEl('cap-slider');
    const runBtn = getEl('run-btn');
    const progressBar = getEl('progress-bar');
    const statusText = getEl('status-text');
    const pathCounter = getEl('path-counter');

    const costConv = getEl('cost-conv');
    const costProd = getEl('cost-prod');
    const distressConv = getEl('distress-conv');
    const distressProd = getEl('distress-prod');
    const headlineCost = getEl('headline-cost');
    const headlineDistress = getEl('headline-distress');

    const barConv = getEl('bar-conv');
    const barProd = getEl('bar-prod');
    const barIlb = getEl('bar-ilb');
    const barGdp = getEl('bar-gdp');
    const barHybrid = getEl('bar-hybrid');
    const barConvVal = getEl('bar-conv-val');
    const barProdVal = getEl('bar-prod-val');
    const barIlbVal = getEl('bar-ilb-val');
    const barGdpVal = getEl('bar-gdp-val');
    const barHybridVal = getEl('bar-hybrid-val');

    const ltConvCost = getEl('lt-conv-cost');
    const ltProdCost = getEl('lt-prod-cost');
    const ltConvDist = getEl('lt-conv-dist');
    const ltProdDist = getEl('lt-prod-dist');
    const ltSaving = getEl('lt-saving');
    const ltDistInc = getEl('lt-dist-inc');

    if (!thetaSlider || !alphaSlider || !capSlider) return;

    function updateLabels() {
      const thetaLabel = getEl('theta-label');
      const alphaLabel = getEl('alpha-label');
      const capLabel = getEl('cap-label');
      if (thetaLabel) thetaLabel.textContent = thetaSlider.value;
      if (alphaLabel) alphaLabel.textContent = alphaSlider.value;
      if (capLabel) capLabel.textContent = (parseFloat(capSlider.value) * 100).toFixed(1) + '%';
    }

    thetaSlider.addEventListener('input', updateLabels);
    alphaSlider.addEventListener('input', updateLabels);
    capSlider.addEventListener('input', updateLabels);
    updateLabels();

    function normalRandom(mean, std) {
      mean = mean || 0;
      std = std || 1;
      let u = 0, v = 0;
      while (u === 0) u = Math.random();
      while (v === 0) v = Math.random();
      return mean + std * Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    }

    function runPath(thetaAI, alpha, cap, years) {
      years = years || 10;
      let debt = 100;
      let revenue = 30;
      let cost = 0;
      let distress = false;
      let inflation = 0.02;
      for (let y = 0; y < years; y++) {
        const gdpGrowth = normalRandom(0.025, 0.02);
        const npiBase = normalRandom(0.02, 0.025);
        const aiBoost = Math.max(0, gdpGrowth) * thetaAI * 0.5;
        const npiGrowth = npiBase + aiBoost;
        const realReturn = Math.min(Math.max(alpha * npiGrowth, 0), cap);
        const coupon = (1 + inflation) * (1 + realReturn) - 1;
        const debtService = debt * coupon;
        cost += debtService / Math.pow(1 + 0.03, y);
        revenue = revenue * (1 + gdpGrowth * 0.7);
        if (debtService / revenue > 0.15) distress = true;
        const spending = 36 + (gdpGrowth > 0 ? -0.05 * debt : 0.05 * debt);
        debt = debt + (spending - revenue) + debtService;
        if (debt < 0) debt = 0;
      }
      return { cost, distress };
    }

    function runSimulation() {
      const thetaAI = parseFloat(thetaSlider.value);
      const alpha = parseFloat(alphaSlider.value);
      const cap = parseFloat(capSlider.value);
      const totalPaths = 10000;
      let completed = 0;
      let convCostSum = 0, prodCostSum = 0;
      let convDistress = 0, prodDistress = 0;

      if (statusText) statusText.textContent = 'Simulating...';
      if (runBtn) {
        runBtn.disabled = true;
        runBtn.textContent = '⏳ Running...';
      }

      const batchSize = 100;
      let currentBatch = 0;

      function processBatch() {
        const end = Math.min(currentBatch + batchSize, totalPaths);
        for (let i = currentBatch; i < end; i++) {
          // Conventional
          let debtC = 100, revC = 30, costC = 0, distressC = false;
          for (let y = 0; y < 10; y++) {
            const gdpG = normalRandom(0.025, 0.02);
            const debtService = debtC * 0.04;
            costC += debtService / Math.pow(1 + 0.03, y);
            revC = revC * (1 + gdpG * 0.7);
            if (debtService / revC > 0.15) distressC = true;
            const spend = 36 + (gdpG > 0 ? -0.05 * debtC : 0.05 * debtC);
            debtC = debtC + (spend - revC) + debtService;
            if (debtC < 0) debtC = 0;
          }
          convCostSum += costC;
          if (distressC) convDistress++;

          // Productivity bond
          const prod = runPath(thetaAI, alpha, cap, 10);
          prodCostSum += prod.cost;
          if (prod.distress) prodDistress++;
        }

        completed = end;
        const pct = (completed / totalPaths) * 100;
        if (progressBar) progressBar.style.width = pct + '%';
        if (pathCounter) pathCounter.textContent = completed + ' / ' + totalPaths;

        if (completed < totalPaths) {
          currentBatch = end;
          updateMetrics(completed);
          setTimeout(processBatch, 0);
        } else {
          updateMetrics(totalPaths);
          if (statusText) statusText.textContent = '✅ Done!';
          if (runBtn) {
            runBtn.disabled = false;
            runBtn.textContent = '▶ Run Simulation';
          }
        }
      }

function updateMetrics(count) {
  if (count === 0) return;
  const cCost = convCostSum / count;
  const pCost = prodCostSum / count;
  const cDist = (convDistress / count) * 100;
  const pDist = (prodDistress / count) * 100;

  if (costConv) costConv.textContent = cCost.toFixed(3);
  if (costProd) costProd.textContent = pCost.toFixed(3);
  if (distressConv) distressConv.textContent = cDist.toFixed(1) + '%';
  if (distressProd) distressProd.textContent = pDist.toFixed(1) + '%';

  const costSave = ((cCost - pCost) / cCost * 100);
  const distDiff = pDist - cDist;
  if (headlineCost) headlineCost.textContent = costSave.toFixed(1) + '%';
  if (headlineDistress) headlineDistress.textContent = (distDiff > 0 ? '+' : '') + distDiff.toFixed(1) + 'pp';

  // Update bars – set height directly (no transform)
  const maxBarHeight = 120;
  const maxCost = 0.55;
  const scale = maxBarHeight / maxCost;

  const setBarHeight = (el, val) => {
    if (el) {
      const height = Math.min(maxBarHeight, Math.max(6, val * scale));
      el.style.height = height + 'px';
    }
  };

  requestAnimationFrame(() => {
    setBarHeight(barConv, cCost);
    setBarHeight(barProd, pCost);
    setBarHeight(barIlb, 0.489);
    setBarHeight(barGdp, 0.511);
    setBarHeight(barHybrid, 0.527);

    if (barConvVal) barConvVal.textContent = cCost.toFixed(3);
    if (barProdVal) barProdVal.textContent = pCost.toFixed(3);
    if (barIlbVal) barIlbVal.textContent = '0.489';
    if (barGdpVal) barGdpVal.textContent = '0.511';
    if (barHybridVal) barHybridVal.textContent = '0.527';

    if (ltConvCost) ltConvCost.textContent = cCost.toFixed(3);
    if (ltProdCost) ltProdCost.textContent = pCost.toFixed(3);
    if (ltConvDist) ltConvDist.textContent = cDist.toFixed(1) + '%';
    if (ltProdDist) ltProdDist.textContent = pDist.toFixed(1) + '%';
    if (ltSaving) ltSaving.textContent = costSave.toFixed(1) + '%';
    if (ltDistInc) ltDistInc.textContent = (distDiff > 0 ? '+' : '') + distDiff.toFixed(1) + 'pp';

    const prodBox = getEl('cost-prod-box');
    if (prodBox) prodBox.className = 'metric-box' + (pCost < cCost ? ' better' : ' worse');
    const distBox = getEl('distress-prod-box');
    if (distBox) distBox.className = 'metric-box' + (pDist < cDist ? ' better' : ' worse');
  });
}

      convCostSum = 0; prodCostSum = 0; convDistress = 0; prodDistress = 0;
      completed = 0; currentBatch = 0;
      if (progressBar) progressBar.style.width = '0%';
      if (pathCounter) pathCounter.textContent = '0 / 10000';
      if (statusText) statusText.textContent = 'Running...';

      processBatch();
    }

    if (runBtn) runBtn.addEventListener('click', runSimulation);

    // CSV download
    const downloadBtn = getEl('download-csv-btn');
    if (downloadBtn) {
      downloadBtn.addEventListener('click', function() {
        const convCost = getEl('cost-conv')?.textContent || '0';
        const prodCost = getEl('cost-prod')?.textContent || '0';
        const convDist = getEl('distress-conv')?.textContent.replace('%', '') || '0';
        const prodDist = getEl('distress-prod')?.textContent.replace('%', '') || '0';
        const theta = thetaSlider.value;
        const alpha = alphaSlider.value;
        const cap = capSlider.value;

        const csvRows = [
          ['Metric', 'Value'],
          ['Theta_AI', theta],
          ['Alpha_N', alpha],
          ['Cap', cap],
          ['Conv_Cost', convCost],
          ['Prod_Cost', prodCost],
          ['Conv_Distress_Pct', convDist],
          ['Prod_Distress_Pct', prodDist],
          ['Cost_Saving_Pct', ((parseFloat(convCost) - parseFloat(prodCost)) / parseFloat(convCost) * 100).toFixed(2)]
        ];
        const csvContent = csvRows.map(row => row.join(',')).join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'productivity_bond_results_' + new Date().toISOString().slice(0, 10) + '.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }

    // Adoption presets
    qsa('.btn-preset').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const card = this.closest('.scenario-card');
        if (!card) return;
        const theta = parseFloat(card.dataset.theta);
        const alpha = parseFloat(card.dataset.alpha);
        const cap = parseFloat(card.dataset.cap);
        thetaSlider.value = theta;
        alphaSlider.value = alpha;
        capSlider.value = cap;
        updateLabels();
        qsa('.scenario-card').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        runSimulation();
      });
    });

    qsa('.scenario-card').forEach(card => {
      card.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-preset')) return;
        this.classList.toggle('active');
      });
    });

    setTimeout(runSimulation, 500);
    console.log('⚡ Simulator initialised');
  }

  // ---------- HAPPINESS SLIDER ----------
  function initHappinessSlider() {
    const happinessSlider = getEl('happiness-slider');
    const happinessLabel = getEl('happiness-label');
    const happinessVal = getEl('happiness-val');
    const bondStrengthVal = getEl('bond-strength-val');

    if (!happinessSlider) return;

    let raf = null;

    function updateHappiness() {
      if (raf) cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const gNPI = parseFloat(happinessSlider.value);
        const happiness = 1 / (1 + Math.exp(-80 * (gNPI - 0.03)));
        const bondStrength = Math.min(1, Math.max(0, (gNPI - 0.01) / 0.04));

        if (happinessLabel) happinessLabel.textContent = (gNPI * 100).toFixed(1) + '%';
        if (happinessVal) happinessVal.textContent = (happiness * 100).toFixed(1) + '%';
        if (bondStrengthVal) bondStrengthVal.textContent = (bondStrength * 100).toFixed(1) + '%';

        // Update happiness chart if Plotly is loaded
        if (typeof Plotly !== 'undefined') {
          const chartDiv = getEl('chart-happiness');
          if (chartDiv) {
            const xRange = Array.from({ length: 61 }, (_, i) => i * 0.001);
            const yRange = xRange.map(g => 1 / (1 + Math.exp(-80 * (g - 0.03))));
            const traceLine = {
              x: xRange,
              y: yRange,
              type: 'scatter',
              mode: 'lines',
              line: { color: '#f472b6', width: 3 },
              name: 'Happiness Curve',
              showlegend: true
            };
            const tracePoint = {
              x: [gNPI],
              y: [happiness],
              type: 'scatter',
              mode: 'markers',
              marker: { color: '#ffffff', size: 12, line: { color: '#f472b6', width: 3 } },
              name: 'Current',
              showlegend: true
            };
            const currentLayout = chartDiv.layout || { displayModeBar: false };
            Plotly.react('chart-happiness', [traceLine, tracePoint], { ...currentLayout,
              displayModeBar: false }, { responsive: true });
          }
        }
        raf = null;
      });
    }

    happinessSlider.addEventListener('input', updateHappiness);
    setTimeout(updateHappiness, 300);
    console.log('😌 Happiness slider initialised');
  }

  // ---------- AI PREDICTION ENGINES ----------
  function initPredictionEngines() {
    // Economic Interpretation
    (function() {
      const btn = getEl('predict-btn');
      const output = getEl('prediction-output');
      const status = getEl('prediction-status');
      let fetching = false;

      async function generate() {
        if (fetching) return;
        const theta = parseFloat(getEl('theta-slider')?.value || 0.15);
        const alpha = parseFloat(getEl('alpha-slider')?.value || 0.55);
        const cap = parseFloat(getEl('cap-slider')?.value || 0.02);
        const convCost = parseFloat(getEl('cost-conv')?.textContent || 0.515);
        const prodCost = parseFloat(getEl('cost-prod')?.textContent || 0.499);
        const convDistress = parseFloat(getEl('distress-conv')?.textContent.replace('%', '') || 11.0);
        const prodDistress = parseFloat(getEl('distress-prod')?.textContent.replace('%', '') || 88.2);

        const payload = {
          theta_ai: theta,
          alpha_n: alpha,
          cap,
          conv_cost: convCost,
          prod_cost: prodCost,
          conv_distress: convDistress,
          prod_distress: prodDistress
        };

        fetching = true;
        if (btn) btn.disabled = true;
        if (status) status.textContent = '⏳ Generating...';
        if (output) output.innerHTML = '<span style="opacity:0.5;">Thinking...</span>';

        try {
          const resp = await fetch('https://productivity-interpretation.traffictorch.workers.dev/?_=' + Date.now(), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const data = await resp.json();
          if (!resp.ok) throw new Error(data.error || 'HTTP error');
          if (output) {
            if (data.paragraphs) {
              output.innerHTML = data.paragraphs.map(p => `<p style="margin-bottom:0.6rem;">${p}</p>`).join('');
            } else {
              output.innerHTML = data.interpretation || 'No interpretation.';
            }
            if (status) status.textContent = '✅ Done';
          }
        } catch (err) {
          if (output) output.innerHTML = `⚠️ Error: ${err.message}`;
          if (status) status.textContent = '❌ Error';
        } finally {
          fetching = false;
          if (btn) btn.disabled = false;
        }
      }

      if (btn) btn.addEventListener('click', generate);
    })();

    // Happiness Interpretation
    (function() {
      const btn = getEl('happiness-predict-btn');
      const output = getEl('happiness-output');

      async function generateHappiness() {
        const gNPI = parseFloat(getEl('happiness-slider')?.value || 0.03);
        const happiness = parseFloat(getEl('happiness-val')?.textContent.replace('%', '') || 50) / 100;
        const bondStrength = parseFloat(getEl('bond-strength-val')?.textContent.replace('%', '') || 75) / 100;
        const theta_ai = parseFloat(getEl('theta-slider')?.value || 0.15);
        const alpha_n = parseFloat(getEl('alpha-slider')?.value || 0.55);
        const cap = parseFloat(getEl('cap-slider')?.value || 0.02);
        const convCost = parseFloat(getEl('cost-conv')?.textContent || 0.515);
        const prodCost = parseFloat(getEl('cost-prod')?.textContent || 0.499);
        const convDistress = parseFloat(getEl('distress-conv')?.textContent.replace('%', '') || 11.0);
        const prodDistress = parseFloat(getEl('distress-prod')?.textContent.replace('%', '') || 88.2);

        const payload = {
          productivityGrowth: gNPI,
          happiness,
          bondStrength,
          theta_ai,
          alpha_n,
          cap,
          convCost,
          prodCost,
          convDistress,
          prodDistress
        };

        if (output) output.innerHTML = '<span style="opacity:0.5;">Thinking...</span>';
        try {
          const resp = await fetch('https://happiness-bs-interpretation.traffictorch.workers.dev/?_=' + Date.now(), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const data = await resp.json();
          if (!resp.ok) throw new Error(data.error || 'HTTP error');
          if (output) {
            if (data.paragraphs) {
              output.innerHTML = data.paragraphs.map(p => `<p style="margin-bottom:0.6rem;">${p}</p>`).join('');
            } else {
              output.innerHTML = data.interpretation || 'No interpretation.';
            }
          }
        } catch (err) {
          if (output) output.innerHTML = `⚠️ Error: ${err.message}`;
        }
      }

      if (btn) btn.addEventListener('click', generateHappiness);
    })();
    console.log('🧠 Prediction engines initialised');
  }

  // ---------- INIT HOME PAGE ----------
  function initHomePage() {
    console.log('🚀 initHomePage called');
    // Load Plotly and render charts
    loadPlotly().catch(console.error);

    // Initialise interactive components
    initSimulator();
    initHappinessSlider();
    initPredictionEngines();
  }

  // ---------- AUTO‑RUN ----------
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHomePage);
  } else {
    initHomePage();
  }

  window.initHomePage = initHomePage;
  window.renderAllCharts = renderAllCharts;
})();