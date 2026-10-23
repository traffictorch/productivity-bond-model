import glob

html_snippet = """
<div style="margin-top:1.5rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,0.1); font-size:0.85rem; color:var(--text-muted);">
    <p>🏛️ Official Submission #240 to the <a href="https://www.aph.gov.au/DocumentStore.ashx?id=25e9d73e-76be-4f7f-87af-5fb5b3e71058&subId=805961" target="_blank" style="color:#fbbf24; text-decoration:underline;">Senate Select Committee on Productivity in Australia</a>.</p>
</div>
"""

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '</footer>' in content and 'Submission #240' not in content:
        content = content.replace('</footer>', html_snippet + '\n</footer>')
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print('Updated ' + f)
        count += 1

print('Done! Updated ' + str(count) + ' files.')
