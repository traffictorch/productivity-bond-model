/**
 * Governance Widget — Round Table CTA
 * Safe to include on any page. Does nothing if #gov-widget placeholder is absent.
 * Usage: add <div id="gov-widget"></div> where you want the widget, then:
 *   <script src="js/governance-widget.js" defer></script>
 * Idempotent — will not duplicate if script runs twice.
 */
(function () {
  'use strict';

  function buildWidget() {
    return [
      '<div class="glass-card" style="border-color:rgba(167,139,250,0.25); margin-top:2.5rem;">',
      '  <div style="display:flex; align-items:center; gap:0.8rem; flex-wrap:wrap; margin-bottom:0.8rem;">',
      '    <span class="badge-glow" style="background:rgba(167,139,250,0.15); color:#a78bfa; border-color:rgba(167,139,250,0.15);">🗳️ Community Governance</span>',
      '    <span style="font-size:0.7rem; color:var(--text-muted);">Equal authority · No admins · Every decision on the record</span>',
      '  </div>',
      '  <h2 style="font-size:clamp(1.4rem,2.5vw,1.8rem); font-weight:700; margin-bottom:0.5rem; color:var(--text-primary);">Help shape the future</h2>',
      '  <p style="color:var(--text-secondary); margin-bottom:1.2rem; max-width:780px; font-size:0.95rem; line-height:1.65;">',
      '    The Productivity Bond Model lives inside a decentralized governance system called <strong style="color:var(--text-primary);">the Round Table</strong>. Every entity has equal voice. Every decision is tamper-evident and reversible. No admins. No override. Proposals, discussion, and consensus voting — all public, all on the audit chain.',
      '  </p>',
      '  <div style="display:flex; flex-wrap:wrap; gap:0.6rem;">',
      '    <a href="https://traffictorch.net/community/round-table/" class="btn-primary" style="padding:0.6rem 1.7rem; font-size:0.9rem;">Enter the Round Table →</a>',
      '    <a href="https://traffictorch.net/community/round-table/simulator/" class="btn-secondary" style="padding:0.6rem 1.7rem; font-size:0.9rem;">🎬 Watch the simulator</a>',
      '    <a href="https://traffictorch.net/community/round-table/constitution/" class="btn-secondary" style="padding:0.6rem 1.7rem; font-size:0.9rem;">📜 Read the Constitution</a>',
      '    <a href="https://traffictorch.net/community/" class="btn-secondary" style="padding:0.6rem 1.7rem; font-size:0.9rem;">🤝 Community</a>',
      '  </div>',
      '  <p style="font-size:0.75rem; color:var(--text-muted); margin-top:1rem;">',
      '    Part of the <a href="https://traffictorch.net" target="_blank" rel="noopener noreferrer" style="color:#a78bfa; text-decoration:underline;">Traffic Torch</a> platform. Free, open source, no paywalls.',
      '  </p>',
      '</div>'
    ].join('\n');
  }

  function init() {
    var placeholder = document.getElementById('gov-widget');
    if (!placeholder) return;
    if (placeholder.dataset.govRendered === '1') return;
    placeholder.innerHTML = buildWidget();
    placeholder.dataset.govRendered = '1';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
