#!/usr/bin/env python3
import pathlib

path = pathlib.Path('policy-lab.html')
if not path.exists():
    print("ERROR: policy-lab.html not found")
    exit(1)

lines = path.read_text().split('\n')
new_lines = []
seen_saving = False
skip_next = False

for line in lines:
    if skip_next:
        skip_next = False
        continue
        
    # Look for the exact line that is duplicated
    if 'const saving=((prod.expectedCost-conv.expectedCost)/conv.expectedCost*100);' in line:
        if seen_saving:
            # This is the SECOND time we've seen it. Skip it and the line right below it.
            skip_next = True
            continue
        else:
            # This is the FIRST time. Keep it.
            seen_saving = True
            
    new_lines.append(line)
    
path.write_text('\n'.join(new_lines))
print("✅ Fixed! Removed the duplicate 'const saving' declaration.")
