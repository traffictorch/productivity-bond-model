#!/usr/bin/env python3
import pathlib, re

path = pathlib.Path('policy-lab.html')
html = path.read_text()

# 1. Remove the inline onclick from all accordion toggles
html = html.replace(' onclick="toggleAccordion(this)"', '')

# 2. Replace the old toggle function with a robust isolated listener
old_js = """window.toggleAccordion=function(el){
  var content=el.nextElementSibling;
  var arrow=el.querySelector('.arrow');
  if(content){
    content.classList.toggle('open');
    el.classList.toggle('open');
    if(arrow)arrow.classList.toggle('open');
  }
};"""

new_js = """document.addEventListener('DOMContentLoaded', function() {
  // Find all toggles
  document.querySelectorAll('.accordion-toggle').forEach(function(el) {
    // Clone the node to strip any conflicting event listeners from core.min.js
    var newEl = el.cloneNode(true);
    el.parentNode.replaceChild(newEl, el);
    
    newEl.setAttribute('role', 'button');
    newEl.setAttribute('tabindex', '0');
    
    // Add our clean, isolated listener
    newEl.addEventListener('click', function(e) {
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

    newEl.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      }
    });
  });
});"""

if old_js in html:
    html = html.replace(old_js, new_js)
    print("✅ Replaced toggle function with isolated listener")
else:
    # If the old function was formatted slightly differently, try a regex catch
    if 'window.toggleAccordion' in html:
        html = re.sub(r'window\.toggleAccordion\s*=\s*function[\s\S]*?\};', new_js, html)
        print("✅ Replaced toggle function via regex")
    else:
        print("⚠️ Could not find old toggle function")

path.write_text(html)
print("File saved.")
