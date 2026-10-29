#!/usr/bin/env python3
import pathlib

path = pathlib.Path('policy-lab.html')
if not path.exists():
    print("ERROR: policy-lab.html not found")
    exit(1)

html = path.read_text()

# Find the specific block in generateAI where saving/distDiff need to be declared
old_block = """  setTimeout(()=>{
    const{p,conv,prod,port}=lastResult;
    let summary='📌 ',advice='';
    
    if (conv.distressProb > 0.5) {"""

new_block = """  setTimeout(()=>{
    const{p,conv,prod,port}=lastResult;
    let summary='📌 ',advice='';
    const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);
    const distDiff=prod.distressProb-conv.distressProb;
    
    if (conv.distressProb > 0.5) {"""

if old_block in html:
    html = html.replace(old_block, new_block)
    print("✅ Injected saving and distDiff declarations into generateAI")
elif "const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);\n    const distDiff" in html:
    print("✅ generateAI already has the declarations")
else:
    print("❌ Could not find the target block. Searching alternatives...")
    # Fallback: try to find within generateAI function specifically
    start = html.find('async function generateAI')
    end = html.find('\n}', start) + 2
    ai_block = html[start:end]
    
    if 'const saving=' in ai_block:
        print("✅ generateAI already contains 'const saving'")
    else:
        # Insert right after the "let summary" line
        target = "let summary='📌 ',advice='';"
        if target in ai_block:
            new_ai_block = ai_block.replace(
                target,
                target + "\n    const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);\n    const distDiff=prod.distressProb-conv.distressProb;",
                1
            )
            html = html[:start] + new_ai_block + html[end:]
            print("✅ Injected via fallback method")

path.write_text(html)
print("File saved.")

# Verify by counting
import re
ai_start = html.find('async function generateAI')
ai_end = html.find('\n}', ai_start) + 2
ai_block = html[ai_start:ai_end]
saving_count = ai_block.count('const saving=')
distdiff_count = ai_block.count('const distDiff=')
print(f"\nVerification inside generateAI:")
print(f"  'const saving=' count: {saving_count} (should be 1)")
print(f"  'const distDiff=' count: {distdiff_count} (should be 1)")
