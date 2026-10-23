import glob

files = glob.glob('*.html')
count = 0

for f in files:
    if f == 'contributions.html':
        continue
        
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    original = content

    # 1. Force add to Nav (right before </nav>)
    if '</nav>' in content and 'href="contributions.html"' not in content:
        content = content.replace('</nav>', '    <a href="contributions.html" style="color: #fbbf24; margin-left: 15px;">Contributions</a>\n</nav>')

    # 2. Force add to Footer (right before </footer>)
    if '</footer>' in content and 'href="contributions.html"' not in content:
        content = content.replace('</footer>', '<div style="text-align:center; padding: 10px; font-size: 0.9rem;"><a href="contributions.html" style="color: #60a5fa; text-decoration: underline;">Contributions</a></div>\n</footer>')

    if content != original:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1
        print('Updated ' + f)

print('Done! Force-updated ' + str(count) + ' files.')
