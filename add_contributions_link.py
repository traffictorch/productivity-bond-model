import glob

files = glob.glob('*.html')
count = 0

for f in files:
    if f == 'contributions.html':
        continue # Skip the file we just made
        
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    original_content = content

    # 1. Add to Navigation (Looks for About link and adds Contributions next to it)
    if 'href="about.html"' in content and 'href="contributions.html"' not in content:
        # Try to match the exact style of the About link
        content = content.replace('<a href="about.html">About</a>', '<a href="about.html">About</a>\n            <a href="contributions.html">Contributions</a>')
        content = content.replace('<a href="about.html"', '<a href="contributions.html">Contributions</a>\n            <a href="about.html"')

    # 2. Add to Footer
    if '</footer>' in content and 'href="contributions.html"' not in content:
        footer_link = '<a href="contributions.html" style="margin-left:15px; color:#60a5fa; text-decoration:underline;">Contributions</a>'
        content = content.replace('</footer>', '<div style="text-align:center; padding-bottom: 15px; font-size:0.85rem;">' + footer_link + '</div>\n</footer>')

    if content != original_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print('Added Contributions link to: ' + f)
        count += 1

print('Done! Updated ' + str(count) + ' files.')
