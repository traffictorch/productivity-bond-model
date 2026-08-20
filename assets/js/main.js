        (function() {
            'use strict';

            // ---------- THEME TOGGLE ----------
            const themeToggle = document.getElementById('themeToggle');
            const themeIcon = document.getElementById('themeIcon');
            const html = document.documentElement;

            function setTheme(theme) {
                html.setAttribute('data-theme', theme);
                localStorage.setItem('theme', theme);
                const isDark = theme === 'dark';
                themeIcon.textContent = isDark ? '🌙' : '☀️';
                themeToggle.setAttribute('aria-pressed', isDark ? 'false' : 'true');
            }

            function getPreferredTheme() {
                const stored = localStorage.getItem('theme');
                if (stored) return stored;
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
                    return 'light';
                }
                return 'dark';
            }

            setTheme(getPreferredTheme());

            themeToggle.addEventListener('click', function() {
                const current = html.getAttribute('data-theme');
                const next = current === 'dark' ? 'light' : 'dark';
                setTheme(next);
                if (typeof Plotly !== 'undefined') {
                    setTimeout(renderAllCharts, 200);
                }
            });

            const systemMedia = window.matchMedia('(prefers-color-scheme: light)');
            systemMedia.addEventListener('change', function(e) {
                if (!localStorage.getItem('theme')) {
                    const newTheme = e.matches ? 'light' : 'dark';
                    setTheme(newTheme);
                }
            });

            // ---------- ACCORDION TOGGLE ----------
            window.toggleAccordion = function(el) {
                const content = el.nextElementSibling;
                const arrow = el.querySelector('.arrow');
                if (content) {
                    content.classList.toggle('open');
                    el.classList.toggle('open');
                    if (arrow) arrow.classList.toggle('open');
                }
            };

            // ---------- HAMBURGER NAV TOGGLE ----------
            const hamburgerBtn = document.getElementById('hamburgerBtn');
            const navLinks = document.getElementById('navLinks');

            if (hamburgerBtn && navLinks) {
                hamburgerBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    navLinks.classList.toggle('open');
                    hamburgerBtn.classList.toggle('open');
                });

                navLinks.querySelectorAll('a').forEach(function(link) {
                    link.addEventListener('click', function() {
                        navLinks.classList.remove('open');
                        hamburgerBtn.classList.remove('open');
                    });
                });

                document.addEventListener('click', function(e) {
                    if (!e.target.closest('.sticky-nav')) {
                        navLinks.classList.remove('open');
                        hamburgerBtn.classList.remove('open');
                    }
                });
            }

            // ---------- FLOATING RETURN TO TOP ----------
            const floatingReturnTop = document.getElementById('floatingReturnTop');
            if (floatingReturnTop) {
                floatingReturnTop.addEventListener('click', function() {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
            }

            // ---------- SHARING ----------
            function sharePage() {
                const url = window.location.href;
                const title = document.title;
                const text = 'Check out the ' + title + ' model:';

                if (navigator.share) {
                    navigator.share({
                        title: title,
                        text: text,
                        url: url
                    }).catch((err) => {
                        if (err.name !== 'AbortError') console.error('Share failed:', err);
                    });
                } else if (navigator.clipboard) {
                    navigator.clipboard.writeText(url).then(() => {
                        alert('Link copied to clipboard!');
                    }).catch(() => {
                        prompt("Copy this link manually:", url);
                    });
                } else {
                    prompt("Copy this link manually:", url);
                }
            }

            document.querySelectorAll('.share-btn').forEach(btn => {
                btn.addEventListener('click', sharePage);
            });

            // ---------- PWA INSTALL ----------
            const installBtn = document.getElementById('pwaInstallBtn');
            const iosOverlay = document.getElementById('pwaIosOverlay');
            const closeIosBtn = document.getElementById('pwaCloseIosModal');
            let deferredPrompt = null;

            if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
                installBtn.style.display = 'none';
            }

            window.addEventListener('beforeinstallprompt', (e) => {
                e.preventDefault();
                deferredPrompt = e;
            });

            window.addEventListener('appinstalled', () => {
                installBtn.style.display = 'none';
                console.log('PWA installed successfully.');
            });

            setTimeout(() => {
                if (installBtn.style.display !== 'none') {
                    installBtn.style.display = 'flex';
                }
            }, 12000);

            installBtn.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    console.log(`User responded to PWA install: ${outcome}`);
                    deferredPrompt = null;
                } else if (/iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase())) {
                    iosOverlay.style.display = 'flex';
                } else {
                    alert("To install this app, look for 'Install' or 'Add to Home Screen' in your browser's menu.");
                }
            });

            closeIosBtn.addEventListener('click', () => {
                iosOverlay.style.display = 'none';
            });

            iosOverlay.addEventListener('click', (e) => {
                if (e.target === e.currentTarget) {
                    iosOverlay.style.display = 'none';
                }
            });

            // ---------- PRINT POLICY BRIEF ----------
            document.getElementById('print-policy-btn').addEventListener('click', function() {
                window.print();
            });

            // ---------- RETURN TO TOP BUTTON (in-page) ----------
            const backToTopBtn = document.getElementById('backToTopBtn');
            if (backToTopBtn) {
                backToTopBtn.addEventListener('click', function() {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
            }

            // ----------------------------------------------------------
            // DEFERRED HEAVY WORK
            // ----------------------------------------------------------

            function scheduleHeavyWork() {
                if ('requestIdleCallback' in window) {
                    requestIdleCallback(function() {
                        initSimulator();
                        initHappinessSlider();
                        waitForPlotlyAndRender();
                    }, { timeout: 2000 });
                } else {
                    setTimeout(function() {
                        initSimulator();
                        initHappinessSlider();
                        waitForPlotlyAndRender();
                    }, 500);
                }
            }

            function waitForPlotlyAndRender() {
                if (typeof Plotly !== 'undefined') {
                    renderAllCharts();
                } else {
                    setTimeout(function() {
                        if (typeof Plotly !== 'undefined') {
                            renderAllCharts();
                        } else {
                            window.addEventListener('load', function() {
                                if (typeof Plotly !== 'undefined') {
                                    renderAllCharts();
                                } else {
                                    document.querySelectorAll('.plot-container').forEach(el => {
                                        el.innerHTML +=
                                            '<p style="text-align:center;opacity:0.5;">Plotly could not load. Please try again later.</p>';
                                    });
                                }
                            });
                        }
                    }, 300);
                }
            }

            // ----------------------------------------------------------
            // SIMULATOR ENGINE
            // ----------------------------------------------------------
            function initSimulator() {
                const thetaSlider = document.getElementById('theta-slider');
                const alphaSlider = document.getElementById('alpha-slider');
                const capSlider = document.getElementById('cap-slider');
                const runBtn = document.getElementById('run-btn');
                const progressBar = document.getElementById('progress-bar');
                const statusText = document.getElementById('status-text');
                const pathCounter = document.getElementById('path-counter');

                const costConv = document.getElementById('cost-conv');
                const costProd = document.getElementById('cost-prod');
                const distressConv = document.getElementById('distress-conv');
                const distressProd = document.getElementById('distress-prod');
                const headlineCost = document.getElementById('headline-cost');
                const headlineDistress = document.getElementById('headline-distress');

                const barConv = document.getElementById('bar-conv');
                const barProd = document.getElementById('bar-prod');
                const barIlb = document.getElementById('bar-ilb');
                const barGdp = document.getElementById('bar-gdp');
                const barHybrid = document.getElementById('bar-hybrid');
                const barConvVal = document.getElementById('bar-conv-val');
                const barProdVal = document.getElementById('bar-prod-val');
                const barIlbVal = document.getElementById('bar-ilb-val');
                const barGdpVal = document.getElementById('bar-gdp-val');
                const barHybridVal = document.getElementById('bar-hybrid-val');

                const ltConvCost = document.getElementById('lt-conv-cost');
                const ltProdCost = document.getElementById('lt-prod-cost');
                const ltConvDist = document.getElementById('lt-conv-dist');
                const ltProdDist = document.getElementById('lt-prod-dist');
                const ltSaving = document.getElementById('lt-saving');
                const ltDistInc = document.getElementById('lt-dist-inc');

                function updateLabels() {
                    document.getElementById('theta-label').textContent = thetaSlider.value;
                    document.getElementById('alpha-label').textContent = alphaSlider.value;
                    document.getElementById('cap-label').textContent = (parseFloat(capSlider.value) * 100).toFixed(1) + '%';
                }
                thetaSlider.addEventListener('input', updateLabels);
                alphaSlider.addEventListener('input', updateLabels);
                capSlider.addEventListener('input', updateLabels);
                updateLabels();

                function normalRandom(mean, std) {
                    mean = mean || 0;
                    std = std || 1;
                    let u = 0,
                        v = 0;
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
                    return { cost: cost, distress: distress };
                }

                function runSimulation() {
                    const thetaAI = parseFloat(thetaSlider.value);
                    const alpha = parseFloat(alphaSlider.value);
                    const cap = parseFloat(capSlider.value);
                    const totalPaths = 10000;
                    let completed = 0;
                    let convCostSum = 0,
                        prodCostSum = 0;
                    let convDistress = 0,
                        prodDistress = 0;

                    statusText.textContent = 'Simulating...';
                    runBtn.disabled = true;
                    runBtn.textContent = '⏳ Running...';

                    const batchSize = 100;
                    let currentBatch = 0;

                    function processBatch() {
                        const end = Math.min(currentBatch + batchSize, totalPaths);
                        for (let i = currentBatch; i < end; i++) {
                            let debtC = 100,
                                revC = 30,
                                costC = 0,
                                distressC = false;
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

                            const prod = runPath(thetaAI, alpha, cap, 10);
                            prodCostSum += prod.cost;
                            if (prod.distress) prodDistress++;
                        }

                        completed = end;
                        const pct = (completed / totalPaths) * 100;
                        progressBar.style.width = pct + '%';
                        pathCounter.textContent = completed + ' / ' + totalPaths;

                        if (completed < totalPaths) {
                            currentBatch = end;
                            updateMetrics(completed);
                            setTimeout(processBatch, 0);
                        } else {
                            updateMetrics(totalPaths);
                            statusText.textContent = '✅ Done!';
                            runBtn.disabled = false;
                            runBtn.textContent = '▶ Run Simulation';
                        }
                    }

                    function updateMetrics(count) {
                        if (count === 0) return;
                        const cCost = convCostSum / count;
                        const pCost = prodCostSum / count;
                        const cDist = (convDistress / count) * 100;
                        const pDist = (prodDistress / count) * 100;

                        costConv.textContent = cCost.toFixed(3);
                        costProd.textContent = pCost.toFixed(3);
                        distressConv.textContent = cDist.toFixed(1) + '%';
                        distressProd.textContent = pDist.toFixed(1) + '%';

                        const costSave = ((cCost - pCost) / cCost * 100);
                        const distDiff = pDist - cDist;
                        headlineCost.textContent = costSave.toFixed(1) + '%';
                        headlineDistress.textContent = (distDiff > 0 ? '+' : '') + distDiff.toFixed(1) + 'pp';

                        const maxCost = 0.55;
                        const scale = 140 / maxCost;
                        barConv.style.height = Math.max(10, cCost * scale) + 'px';
                        barProd.style.height = Math.max(10, pCost * scale) + 'px';
                        barIlb.style.height = Math.max(10, 0.489 * scale) + 'px';
                        barGdp.style.height = Math.max(10, 0.511 * scale) + 'px';
                        barHybrid.style.height = Math.max(10, 0.527 * scale) + 'px';

                        barConvVal.textContent = cCost.toFixed(3);
                        barProdVal.textContent = pCost.toFixed(3);
                        barIlbVal.textContent = '0.489';
                        barGdpVal.textContent = '0.511';
                        barHybridVal.textContent = '0.527';

                        ltConvCost.textContent = cCost.toFixed(3);
                        ltProdCost.textContent = pCost.toFixed(3);
                        ltConvDist.textContent = cDist.toFixed(1) + '%';
                        ltProdDist.textContent = pDist.toFixed(1) + '%';
                        ltSaving.textContent = costSave.toFixed(1) + '%';
                        ltDistInc.textContent = (distDiff > 0 ? '+' : '') + distDiff.toFixed(1) + 'pp';

                        const prodBox = document.getElementById('cost-prod-box');
                        if (pCost < cCost) {
                            prodBox.className = 'metric-box better';
                        } else {
                            prodBox.className = 'metric-box worse';
                        }
                        const distBox = document.getElementById('distress-prod-box');
                        if (pDist < cDist) {
                            distBox.className = 'metric-box better';
                        } else {
                            distBox.className = 'metric-box worse';
                        }
                    }

                    convCostSum = 0;
                    prodCostSum = 0;
                    convDistress = 0;
                    prodDistress = 0;
                    completed = 0;
                    currentBatch = 0;
                    progressBar.style.width = '0%';
                    pathCounter.textContent = '0 / 10000';
                    statusText.textContent = 'Running...';

                    processBatch();
                }

                runBtn.addEventListener('click', runSimulation);

                // CSV DOWNLOAD
                document.getElementById('download-csv-btn').addEventListener('click', function() {
                    const convCost = document.getElementById('cost-conv').textContent;
                    const prodCost = document.getElementById('cost-prod').textContent;
                    const convDist = document.getElementById('distress-conv').textContent.replace('%', '');
                    const prodDist = document.getElementById('distress-prod').textContent.replace('%', '');
                    const theta = document.getElementById('theta-slider').value;
                    const alpha = document.getElementById('alpha-slider').value;
                    const cap = document.getElementById('cap-slider').value;

                    const csvRows = [
                        ['Metric', 'Value'],
                        ['Theta_AI', theta],
                        ['Alpha_N', alpha],
                        ['Cap', cap],
                        ['Conv_Cost', convCost],
                        ['Prod_Cost', prodCost],
                        ['Conv_Distress_Pct', convDist],
                        ['Prod_Distress_Pct', prodDist],
                        ['Cost_Saving_Pct', ((parseFloat(convCost) - parseFloat(prodCost)) / parseFloat(convCost) *
                            100).toFixed(2)]
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

                // ADOPTION PRESETS
                document.querySelectorAll('.btn-preset').forEach(btn => {
                    btn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        const card = this.closest('.scenario-card');
                        const theta = parseFloat(card.dataset.theta);
                        const alpha = parseFloat(card.dataset.alpha);
                        const cap = parseFloat(card.dataset.cap);
                        thetaSlider.value = theta;
                        alphaSlider.value = alpha;
                        capSlider.value = cap;
                        updateLabels();
                        document.querySelectorAll('.scenario-card').forEach(c => c.classList.remove('active'));
                        card.classList.add('active');
                        runSimulation();
                    });
                });
                document.querySelectorAll('.scenario-card').forEach(card => {
                    card.addEventListener('click', function(e) {
                        if (e.target.classList.contains('btn-preset')) return;
                        this.classList.toggle('active');
                    });
                });

                setTimeout(runSimulation, 500);
            }         
            
// ---------- AI Economic PREDICTION Interpretation ----------
(function() {
  const predictBtn = document.getElementById('predict-btn');
  const outputDiv = document.getElementById('prediction-output');
  const statusSpan = document.getElementById('prediction-status');

  let isFetching = false;

  function getCurrentResults() {
    // Read simulation values from DOM
    const theta = parseFloat(document.getElementById('theta-slider').value);
    const alpha = parseFloat(document.getElementById('alpha-slider').value);
    const cap = parseFloat(document.getElementById('cap-slider').value);
    const convCost = parseFloat(document.getElementById('cost-conv').textContent);
    const prodCost = parseFloat(document.getElementById('cost-prod').textContent);
    const convDistress = parseFloat(document.getElementById('distress-conv').textContent.replace('%', ''));
    const prodDistress = parseFloat(document.getElementById('distress-prod').textContent.replace('%', ''));

    return { theta, alpha, cap, convCost, prodCost, convDistress, prodDistress };
  }

  async function generateInterpretation() {
    if (isFetching) return;

    const current = getCurrentResults();

    isFetching = true;
    predictBtn.disabled = true;
    statusSpan.textContent = '⏳ Generating...';
    outputDiv.innerHTML = '<span style="opacity:0.5;">Thinking...</span>';

    try {
      // Build payload with snake_case field names expected by the worker
      const payload = {
        theta_ai: current.theta,
        alpha_n: current.alpha,
        cap: current.cap,
        conv_cost: current.convCost,
        prod_cost: current.prodCost,
        conv_distress: current.convDistress,
        prod_distress: current.prodDistress
      };

      const url = `https://productivity-interpretation.traffictorch.workers.dev/?_=${Date.now()}`;

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error ${response.status}`);
      }

      if (data.interpretation) {
        let html = '';
        if (data.paragraphs && data.paragraphs.length) {
          html = data.paragraphs.map(p => `<p style="margin-bottom: 0.6rem;">${p}</p>`).join('');
        } else {
          const paras = data.interpretation.split(/\n\s*\n/);
          html = paras.map(p => `<p style="margin-bottom: 0.6rem;">${p.trim()}</p>`).join('');
        }
        outputDiv.innerHTML = html;
        statusSpan.textContent = '✅ Done';
      } else {
        outputDiv.innerHTML = `⚠️ No interpretation returned. Raw response: <pre>${JSON.stringify(data, null, 2)}</pre>`;
        statusSpan.textContent = '❌ No content';
      }
    } catch (error) {
      console.error('Prediction Engine error:', error);
      outputDiv.innerHTML = `⚠️ Error: ${error.message}`;
      statusSpan.textContent = '❌ Error';
    } finally {
      isFetching = false;
      predictBtn.disabled = false;
    }
  }

  predictBtn.addEventListener('click', generateInterpretation);
})();

            // ----------------------------------------------------------
            // HAPPINESS SLIDER
            // ----------------------------------------------------------
            function initHappinessSlider() {
                const happinessSlider = document.getElementById('happiness-slider');
                const happinessLabel = document.getElementById('happiness-label');
                const happinessVal = document.getElementById('happiness-val');
                const bondStrengthVal = document.getElementById('bond-strength-val');

                let happinessRAF = null;

                function updateHappinessMetrics() {
                    if (happinessRAF) {
                        cancelAnimationFrame(happinessRAF);
                        happinessRAF = null;
                    }
                    happinessRAF = requestAnimationFrame(function() {
                        const gNPI = parseFloat(happinessSlider.value);
                        const happiness = 1 / (1 + Math.exp(-80 * (gNPI - 0.03)));
                        const bondStrength = Math.min(1, Math.max(0, (gNPI - 0.01) / 0.04));

                        happinessLabel.textContent = (gNPI * 100).toFixed(1) + '%';
                        happinessVal.textContent = (happiness * 100).toFixed(1) + '%';
                        bondStrengthVal.textContent = (bondStrength * 100).toFixed(1) + '%';

                        if (typeof Plotly !== 'undefined') {
                            const chartDiv = document.getElementById('chart-happiness');
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
                                    marker: { color: '#ffffff', size: 12, line: { color: '#f472b6',
                                            width: 3 } },
                                    name: 'Current',
                                    showlegend: true
                                };
                                const currentLayout = chartDiv.layout || { displayModeBar: false };
                                Plotly.react('chart-happiness', [traceLine, tracePoint], { ...currentLayout,
                                    displayModeBar: false }, { responsive: true });
                            }
                        }
                        happinessRAF = null;
                    });
                }

                happinessSlider.addEventListener('input', updateHappinessMetrics);
                setTimeout(updateHappinessMetrics, 300);
            }
            
// Happiness Prediction Engine
(function() {
  const btn = document.getElementById('happiness-predict-btn');
  const output = document.getElementById('happiness-output');

  async function generateHappinessInterpretation() {
    // Always read fresh values from the DOM
    const gNPI = parseFloat(document.getElementById('happiness-slider').value);
    const happiness = parseFloat(document.getElementById('happiness-val').textContent.replace('%', '')) / 100;
    const bondStrength = parseFloat(document.getElementById('bond-strength-val').textContent.replace('%', '')) / 100;

    // Read simulation metrics (if available)
    const theta_ai = parseFloat(document.getElementById('theta-slider').value);
    const alpha_n = parseFloat(document.getElementById('alpha-slider').value);
    const cap = parseFloat(document.getElementById('cap-slider').value);
    const convCost = parseFloat(document.getElementById('cost-conv').textContent);
    const prodCost = parseFloat(document.getElementById('cost-prod').textContent);
    const convDistress = parseFloat(document.getElementById('distress-conv').textContent.replace('%', ''));
    const prodDistress = parseFloat(document.getElementById('distress-prod').textContent.replace('%', ''));

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

    output.innerHTML = '<span style="opacity:0.5;">Thinking...</span>';
    try {
      const response = await fetch('https://happiness-bs-interpretation.traffictorch.workers.dev/?_=' + Date.now(), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'HTTP error');
      if (data.paragraphs) {
        output.innerHTML = data.paragraphs.map(p => `<p style="margin-bottom:0.6rem;">${p}</p>`).join('');
      } else {
        output.innerHTML = data.interpretation || 'No interpretation.';
      }
    } catch (err) {
      output.innerHTML = `⚠️ Error: ${err.message}`;
    }
  }

  btn.addEventListener('click', generateHappinessInterpretation);
})();

 // ============================================================
// PLOTLY CHARTS (including Divergence)
// ============================================================
function renderAllCharts() {
  if (typeof Plotly === 'undefined') return;

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const textColor = isDark ? '#eef2f8' : '#0f111a';
  const gridColor = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';

  // --- Chart 1: Cost vs θ_AI ---
  const thetaValues = [0.10, 0.20, 0.30, 0.40, 0.50];
  const costConv = [0.5154, 0.5154, 0.5154, 0.5154, 0.5154];
  const costProd = [0.5079, 0.5035, 0.4994, 0.4959, 0.4923];
  const trace1 = {
    x: thetaValues, y: costConv, name: 'Conventional', type: 'scatter',
    mode: 'lines+markers', line: { color: '#4b5563', width: 2 }, marker: { color: '#4b5563' }
  };
  const trace2 = {
    x: thetaValues, y: costProd, name: 'Productivity Bond', type: 'scatter',
    mode: 'lines+markers', line: { color: '#a78bfa', width: 3 }, marker: { color: '#a78bfa', size: 8 }
  };
  const layout1 = {
    paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: textColor, family: 'Inter' }, margin: { l: 40, r: 20, t: 20, b: 40 },
    xaxis: { title: 'θ_AI', gridcolor: gridColor }, yaxis: { title: 'Expected Cost', gridcolor: gridColor },
    legend: { orientation: 'h', x: 0, y: 1.05 }, displayModeBar: false
  };
  Plotly.newPlot('chart-cost-theta', [trace1, trace2], layout1, { responsive: true });

  // --- Chart 2: Distress vs α_N ---
  const alphaValues = [0.30, 0.50, 0.70, 0.90, 1.00];
  const distressAlpha = [82.5, 85.8, 88.17, 89.6, 90.1];
  const trace3 = {
    x: alphaValues, y: distressAlpha, name: 'Distress Probability', type: 'scatter',
    mode: 'lines+markers', line: { color: '#f87171', width: 3 }, marker: { color: '#f87171', size: 8 }
  };
  const layout2 = {
    paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: textColor, family: 'Inter' }, margin: { l: 40, r: 20, t: 20, b: 40 },
    xaxis: { title: 'α_N (participation)', gridcolor: gridColor }, yaxis: { title: 'Distress Probability (%)', gridcolor: gridColor },
    legend: { orientation: 'h', x: 0, y: 1.05 }, displayModeBar: false
  };
  Plotly.newPlot('chart-distress-alpha', [trace3], layout2, { responsive: true });

  // --- Chart 3: Happiness curve (initial) ---
  const happinessDiv = document.getElementById('chart-happiness');
  if (happinessDiv) {
    const gNpiValues = Array.from({ length: 61 }, (_, i) => i * 0.001);
    const happinessValues = gNpiValues.map(g => 1 / (1 + Math.exp(-80 * (g - 0.03))));
    const traceH = {
      x: gNpiValues, y: happinessValues, type: 'scatter', mode: 'lines',
      line: { color: '#f472b6', width: 3 }, name: 'Happiness Curve'
    };
    const layoutH = {
      paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      font: { color: textColor, family: 'Inter' }, margin: { l: 40, r: 20, t: 20, b: 40 },
      xaxis: { title: 'Productivity Growth (g_NPI)', gridcolor: gridColor, tickformat: '.0%' },
      yaxis: { title: 'Happiness Index', gridcolor: gridColor, range: [0, 1.1], tickformat: '.0%' },
      displayModeBar: false
    };
    Plotly.newPlot('chart-happiness', [traceH], layoutH, { responsive: true });
  }

  // --- Update happiness slider point (and keep it interactive) ---
  const hSlider = document.getElementById('happiness-slider');
  if (hSlider && typeof Plotly !== 'undefined') {
    const gNPI = parseFloat(hSlider.value);
    const happiness = 1 / (1 + Math.exp(-80 * (gNPI - 0.03)));
    const xRange = Array.from({ length: 61 }, (_, i) => i * 0.001);
    const yRange = xRange.map(g => 1 / (1 + Math.exp(-80 * (g - 0.03))));
    const traceLine = {
      x: xRange, y: yRange, type: 'scatter', mode: 'lines',
      line: { color: '#f472b6', width: 3 }, name: 'Happiness Curve', showlegend: true
    };
    const tracePoint = {
      x: [gNPI], y: [happiness], type: 'scatter', mode: 'markers',
      marker: { color: '#ffffff', size: 12, line: { color: '#f472b6', width: 3 } }, name: 'Current', showlegend: true
    };
    const currentLayout = happinessDiv.layout || { displayModeBar: false };
    Plotly.react('chart-happiness', [traceLine, tracePoint], { ...currentLayout, displayModeBar: false }, { responsive: true });
  }

  // --- FINALLY, render the divergence chart ---
  renderDivergenceChart();
}

// ============================================================
// DIVERGENCE CHART (Growth vs Resources)
// ============================================================
function renderDivergenceChart() {
  const div = document.getElementById('chart-divergence');
  if (!div) {
    // Retry if container not ready
    setTimeout(renderDivergenceChart, 300);
    return;
  }
  if (typeof Plotly === 'undefined') {
    setTimeout(renderDivergenceChart, 300);
    return;
  }

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const textColor = isDark ? '#eef2f8' : '#0f111a';
  const gridColor = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';

  // Data generation (your existing code)
  const years = Array.from({ length: 46 }, (_, i) => 1980 + i);
  const financial = years.map((y, i) => {
    const t = i / 45;
    const target = 50 + (250 * Math.pow(t, 1.8));
    return Math.min(target, 320);
  });
  financial[0] = 50;
  financial[45] = 305;

  const resources = years.map((y, i) => {
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
    x: years, y: financial, name: 'Financial Obligations (Debt)', type: 'scatter',
    mode: 'lines+markers', line: { color: '#4f46e5', width: 3 }, marker: { color: '#4f46e5', size: 4 },
    hovertemplate: '%{x}: $%{y:.0f}T<extra>Debt</extra>'
  };

  const traceResources = {
    x: years, y: resources, name: 'Resource Extraction', type: 'scatter',
    mode: 'lines+markers', line: { color: '#34d399', width: 3 }, marker: { color: '#34d399', size: 4 },
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
    annotations: annotations,
    displayModeBar: false,
    hovermode: 'x unified'
  };

  Plotly.newPlot('chart-divergence', [gapTrace, traceFinancial, traceResources], layout, {
    responsive: true,
    displayModeBar: false
  });
}

            // ----------------------------------------------------------
            // FOOTER LAST UPDATED
            // ----------------------------------------------------------
            document.getElementById('last-updated').textContent = 'Last updated: ' + new Date().toLocaleString();

            // ----------------------------------------------------------
            // KICK OFF
            // ----------------------------------------------------------
            if (document.readyState === 'complete') {
                scheduleHeavyWork();
            } else {
                window.addEventListener('load', scheduleHeavyWork);
            }

        })();

        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/productivity-bond-model/sw.js')
                .then(registration => {
                    console.log('Service Worker registered successfully:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        }
        
// ----- HERO PROGRESSIVE REVEAL -----
(function() {
    const heroRevealElements = document.querySelectorAll('.hero .fade-step');
    const aiWrapper = document.querySelector('.ai-power-wrapper');

    // 1. Reveal hero elements after 1 seconds
    setTimeout(() => {
        heroRevealElements.forEach(el => el.classList.add('reveal'));
    }, 500);

    // 2. AI‑Experiment button – reveal when scrolled into view
    if (aiWrapper && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    aiWrapper.classList.add('visible');
                    observer.unobserve(aiWrapper);
                }
            });
        }, { threshold: 0.9 });
        observer.observe(aiWrapper);
    } else if (aiWrapper) {
        // Fallback: show after 5 seconds if no IntersectionObserver
        setTimeout(() => aiWrapper.classList.add('visible'), 5000);
    }
})();