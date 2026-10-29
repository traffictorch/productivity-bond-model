#!/usr/bin/env python3
import pathlib
path = pathlib.Path('policy-lab.html')
html = path.read_text()

old = "}else if(p.thetaAI>0.30){"
new = "}else if(p.thetaAI>=0.30){"

if old in html:
    html = html.replace(old, new, 1)
    path.write_text(html)
    print("✅ Fixed θ_AI boundary: > 0.30 → >= 0.30")
elif new in html:
    print("✅ Already >= 0.30")
else:
    print("⚠️ Could not find the boundary check")
