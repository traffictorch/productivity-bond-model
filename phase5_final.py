#!/usr/bin/env python3
import pathlib, re

print("Running final cleanup (Sitemap, Changelog, FAQ, Widgets)...")

# ── 1. Update Sitemap ──
sitemap_path = pathlib.Path('sitemap.xml')
if sitemap_path.exists():
    sitemap = sitemap_path.read_text()
    if 'policy-lab.html' not in sitemap:
        new_url = """  <url>
    <loc>https://traffictorch.github.io/productivity-bond-model/policy-lab.html</loc>
    <priority>0.9</priority>
    <changefreq>weekly</changefreq>
  </url>
</urlset>"""
        sitemap = sitemap.replace('</urlset>', new_url)
        sitemap_path.write_text(sitemap)
        print("  OK  sitemap.xml updated with Policy Lab")
    else:
        print("  OK  sitemap.xml already contains Policy Lab")

# ── 2. Update Changelog ──
changelog_path = pathlib.Path('changelog.html')
if changelog_path.exists():
    changelog = changelog_path.read_text()
    if 'Policy Lab' not in changelog:
        # Find the first entry and insert above it
        anchor = re.search(r'<h2[^>]*>.*?</h2>', changelog)
        if anchor:
            new_entry = """<div class="changelog-entry" style="margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid var(--border-divider);">
  <h2 style="font-size:1.4rem; color:var(--text-primary);">v1.2.0 — Policy Lab & Site Integration</h2>
  <p style="color:var(--text-muted); font-size:0.85rem; margin-bottom:0.5rem;">October 27, 2026</p>
  <ul style="color:var(--text-secondary); margin-left:1.5rem; line-height:1.8;">
    <li>Added <a href="policy-lab.html" style="color:#b388ff;">Policy Lab</a> — sovereign debt scenario builder.</li>
    <li>Upgraded to endogenous-debt model (v1.1) across all tools.</li>
    <li>Added <a href="model-notes.html" style="color:#b388ff;">Model Notes</a> explaining v1.0 vs v1.1 differences.</li>
    <li>Fixed share link bugs, zero-value input handling, and async UI freezing.</li>
    <li>Added Inflation-Linked Bond comparison to Policy Lab charts.</li>
  </ul>
</div>\n\n"""
            changelog = changelog.replace(anchor.group(0), new_entry + anchor.group(0), 1)
            changelog_path.write_text(changelog)
            print("  OK  changelog.html updated with v1.2.0 entry")
    else:
        print("  OK  changelog.html already mentions Policy Lab")

# ── 3. Update Policy Lab FAQ (remove old misleading theta claim) ──
policy_path = pathlib.Path('policy-lab.html')
if policy_path.exists():
    html = policy_path.read_text()
    
    # Fix the FAQ item about theta_AI
    old_faq = """<p style="color:var(--text-secondary);"><strong>θ_AI</strong> is the fraction of AI-driven productivity gains that the government captures through taxes, royalties, or sovereign equity. It's the single most important parameter in the model.</p>
            <p style="color:var(--text-secondary); margin-top:0.5rem;">The empirical evidence is clear:</p>
            <ul style="color:var(--text-secondary); margin-left:1.5rem; line-height:1.8;">
              <li>If <strong>θ_AI &lt; 0.15</strong>, the Productivity Bond barely outperforms conventional debt</li>
              <li>If <strong>θ_AI &gt; 0.30</strong>, it substantially outperforms</li>
            </ul>
            <p style="color:var(--text-secondary); margin-top:0.5rem;">This is why the verdict warns you when θ_AI is too low — the instrument only works if the gains it's linked to actually reach the public balance sheet.</p>"""
    
    new_faq = """<p style="color:var(--text-secondary);"><strong>θ_AI</strong> is the fraction of AI-driven productivity gains that the government captures through taxes, royalties, or sovereign equity.</p>
            <p style="color:var(--text-secondary); margin-top:0.5rem;">In the book's analytical framework, θ_AI is a critical threshold: below 0.15 the bond barely works, above 0.30 it substantially outperforms. However, in the current simulation (v1.1), AI shocks are rare (5% per year) and modest, so θ_AI affects outcomes primarily through those shocks.</p>
            <p style="color:var(--text-secondary); margin-top:0.5rem;">This means the thresholds are a theoretical guideline, not a guaranteed simulation result. <a href="model-notes.html" style="color:#b388ff;">See Model Notes for the full explanation.</a></p>"""
    
    if old_faq in html:
        html = html.replace(old_faq, new_faq)
        print("  OK  Fixed theta_AI FAQ claim")
    else:
        print("  MISS  theta_AI FAQ anchor not found (might be partially patched)")

    # Add Governance Widget and PWA install button
    if '<div id="gov-widget"></div>' not in html:
        widget_html = """
<div id="gov-widget"></div>
<script src="js/governance-widget.js" defer></script>

<button id="pwaInstallBtn" class="pwa-install-btn">
  <span class="icon">📱</span>
  <span class="btn-text">Install Apps</span>
  <span class="icon">💻</span>
</button>
<div id="pwaIosOverlay" class="pwa-ios-overlay">
  <div class="pwa-ios-modal">
    <h3>Install on iPhone</h3>
    <p>To add this app to your home screen:</p>
    <div class="step"><span>1.</span><span class="step-icon">⬆️</span><span>In <strong>Safari</strong> tap the <strong>Share</strong> button.</span></div>
    <div class="step"><span>2.</span><span class="step-icon">➕</span><span>Scroll down and tap <strong>"Add to Home Screen"</strong>.</span></div>
    <button id="pwaCloseIosModal" class="close-btn">Got it</button>
  </div>
</div>
"""
        html = html.replace('</main>', widget_html + '\n</main>')
        print("  OK  Added Governance widget and PWA install button to Policy Lab")

    policy_path.write_text(html)

print("\n🎉 All remaining phases complete!")
