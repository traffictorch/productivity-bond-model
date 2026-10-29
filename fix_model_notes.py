#!/usr/bin/env python3
import pathlib, re

p = pathlib.Path('model-notes.html')
if not p.exists():
    print("ERROR: model-notes.html not found")
    exit(1)

h = p.read_text()

# ── FIX 1: Remove inline onclick (stops double-toggle with core.min.js) ──
count = h.count(' onclick="toggleAccordion(this)"')
h = h.replace(' onclick="toggleAccordion(this)"', '')
print(f"✅ Removed {count} inline onclick handlers (fixes double-toggle)")

# ── FIX 2: Replace the page's accordion script with isolated listener ──
old_script = '''<script>
// Accordion wiring
window.toggleAccordion=function(el){
  var content=el.nextElementSibling;
  var arrow=el.querySelector('.arrow');
  if(content){
    content.classList.toggle('open');
    el.classList.toggle('open');
    if(arrow)arrow.classList.toggle('open');
  }
};

// Keyboard accessibility
window.addEventListener('load',function(){
  document.documentElement.classList.add('loaded');
  document.querySelectorAll('.accordion-toggle').forEach(function(el){
    el.setAttribute('role','button');
    el.setAttribute('tabindex','0');
    el.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();el.click();}
    });
  });
});
</script>'''

new_script = '''<script>
// Page visibility
window.addEventListener('load', function(){
  document.documentElement.classList.add('loaded');
});

// Isolated accordion handler — clones nodes to strip core.min.js listeners
document.addEventListener('DOMContentLoaded', function(){
  setTimeout(function(){
    document.querySelectorAll('.accordion-toggle').forEach(function(el){
      var newEl = el.cloneNode(true);
      el.parentNode.replaceChild(newEl, el);
      newEl.setAttribute('role', 'button');
      newEl.setAttribute('tabindex', '0');
      newEl.addEventListener('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        var content = this.nextElementSibling;
        var arrow = this.querySelector('.arrow');
        if (content) {
          content.classList.toggle('open');
          this.classList.toggle('open');
          if (arrow) arrow.classList.toggle('open');
        }
      });
      newEl.addEventListener('keydown', function(e){
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this.click(); }
      });
    });
  }, 50);
});
</script>'''

if old_script in h:
    h = h.replace(old_script, new_script)
    print("✅ Replaced accordion script with isolated listener")
else:
    print("⚠️  Script anchor not found — check manually")

# ── FIX 3: Repair broken Related Pages links ──
base = "https://traffictorch.github.io/productivity-bond-model/"
broken = [
    ("https://traffictorch.github.io/policy-lab.html", base + "policy-lab.html"),
    ("https://traffictorch.github.io/index.html#simulator", base + "index.html#simulator"),
    ("https://traffictorch.github.io/appendix.html", base + "appendix.html"),
    ("https://traffictorch.github.io/book.html", base + "book.html"),
    ("https://traffictorch.github.io/changelog.html", base + "changelog.html"),
]
fixed = 0
for old, new in broken:
    if old in h:
        h = h.replace(old, new)
        fixed += 1
print(f"✅ Fixed {fixed} broken Related Pages links")

# ── FIX 4: Correct the 88.17% framing to acknowledge the book's PAM ──
old_claim = '''<div class="callout warn">
        <strong>⚠️ Productivity distress (88.17%)</strong> — The v1.1 number is 85.68%, not 88.17%. The book's number was from the fixed-debt model, which overstates the effect because it doesn't let the debt stock adjust per bond type. The v1.1 number is more realistic.
      </div>'''

new_claim = '''<div class="callout warn">
        <strong>⚠️ Productivity distress (88.17%)</strong> — The v1.1 number is 85.68%, not 88.17%. <strong>Both are pre-PAM figures.</strong> The book identifies 88.17% as the unacceptable baseline and argues in Chapter 14 that the Principal-Adjustment Mechanism is <em>"not an optional refinement. It is part of the architecture."</em> The v1.1 figure is slightly lower because the endogenous model lets each bond type roll its own debt path. The conclusion is unchanged: without PAM, variable coupons are not viable.
      </div>'''

if old_claim in h:
    h = h.replace(old_claim, new_claim)
    print("✅ Updated 88.17% paragraph to acknowledge book's PAM")
else:
    print("⚠️  88.17% callout anchor not found")

# ── FIX 5: Correct the optimal share row ──
h = h.replace(
    '<td>Scenario-dependent (30–45%)</td>',
    '<td>0–45% (regime-dependent)</td>'
)
print("✅ Corrected optimal portfolio share row")

p.write_text(h)
print("\nFile saved.")
