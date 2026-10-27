#!/usr/bin/env python3
import pathlib

path = pathlib.Path('policy-lab.html')
if not path.exists():
    print("ERROR: policy-lab.html not found")
    exit(1)

html = path.read_text()

# The exact duplicate block causing the SyntaxError
find_str = """            let summary='📌 ',advice='';
            const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
            const distDiff=prod.distressProb-conv.distressProb;"""

replace_str = """            let summary='📌 ',advice='';"""

if find_str in html:
    html = html.replace(find_str, replace_str)
    path.write_text(html)
    print("✅ Fixed duplicate const SyntaxError.")
else:
    print("⚠️ Could not find the exact duplicate block. Checking if already fixed...")
    if "const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);\n            const distDiff=prod.distressProb-conv.distressProb;\n            let summary" in html:
        print("✅ Looks like it's already fixed.")
    else:
        print("❌ Please check the generateAI function manually.")
