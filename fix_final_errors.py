#!/usr/bin/env python3
import pathlib, subprocess, sys

path = pathlib.Path('policy-lab.html')
html = path.read_text()

# FIX 1: Restore the missing variables in renderVerdict
v_search = "  const parts=[];\n  if (conv.distressProb > 0.5) {"
v_replace = "  const parts=[];\n  const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);\n  const distressDiff=prod.distressProb-conv.distressProb;\n  if (conv.distressProb > 0.5) {"

if v_search in html:
    html = html.replace(v_search, v_replace)
    print("✅ Fixed missing variables in renderVerdict")
elif "const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);\n  const distressDiff" in html:
    print("✅ renderVerdict is already fixed")
else:
    print("⚠️ renderVerdict: target not found")

# FIX 2: Remove the duplicate variables in generateAI
a_search = """        let summary='📌 ',advice='';
        const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
        const distDiff=prod.distressProb-conv.distressProb;
        
        if (conv.distressProb > 0.5) {"""
a_replace = """        let summary='📌 ',advice='';
        
        if (conv.distressProb > 0.5) {"""

if a_search in html:
    html = html.replace(a_search, a_replace)
    print("✅ Fixed duplicate variables in generateAI")
else:
    # Try a more flexible regex if the exact string doesn't match
    import re
    pattern = r"let summary='📌 ',advice='';\s*const saving=\(\(prod\.expectedCost-conv\.expectedCost\)/conv\.expectedCost\*100\);\s*const distDiff=prod\.distressProb-conv\.distressProb;\s*if \(conv\.distressProb > 0\.5\)"
    if re.search(pattern, html):
        html = re.sub(pattern, "let summary='📌 ',advice='';\n        if (conv.distressProb > 0.5)", html)
        print("✅ Fixed duplicate variables in generateAI (via regex)")
    else:
        print("✅ generateAI is already clean")

path.write_text(html)
print("File saved.")
