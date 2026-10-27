#!/usr/bin/env python3
import re
import pathlib

path = pathlib.Path('policy-lab.html')
html = path.read_text()

# ── FIX 1: renderVerdict missing saving and distressDiff ──
rv_start = html.find('function renderVerdict')
if rv_start == -1:
    print("ERROR: renderVerdict not found")
else:
    # Find "const parts=[];" within renderVerdict and insert declarations right after
    parts_idx = html.find('const parts=[];', rv_start)
    if parts_idx == -1:
        print("ERROR: const parts=[] not found in renderVerdict")
    else:
        insert_pos = parts_idx + len('const parts=[];')
        decl = "\n  const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);\n  const distressDiff=prod.distressProb-conv.distressProb;"
        # Check if already present
        after_parts = html[insert_pos:insert_pos+200]
        if 'const saving' in after_parts:
            print("OK: renderVerdict already has saving/distressDiff")
        else:
            html = html[:insert_pos] + decl + html[insert_pos:]
            print("FIXED: Inserted saving and distressDiff into renderVerdict")

# ── FIX 2: generateAI duplicate declarations ──
pattern = r"(let summary='📌 ',advice='';\s*)const saving=\(\(prod\.expectedCost-conv\.expectedCost\)/conv\.expectedCost\*100\);\s*const distDiff=prod\.distressProb-conv\.distressProb;\s*"
matches = list(re.finditer(pattern, html))
print(f"Found {len(matches)} duplicate declaration block(s) after 'let summary' in generateAI")

if matches:
    html = re.sub(pattern, r"\1\n        ", html, count=1)
    print("FIXED: Removed duplicate declarations from generateAI")

path.write_text(html)
print("File saved.")

# ── VERIFY: extract the renderVerdict block for inspection ──
rv_start2 = html.find('function renderVerdict')
rv_end = html.find('\nfunction ', rv_start2 + 100)
if rv_end == -1:
    rv_end = html.find('// =====', rv_start2 + 100)
block = html[rv_start2:rv_start2+600]
print("\n--- renderVerdict (first 600 chars) ---")
print(block)
