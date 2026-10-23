import glob

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # If the footer link exists, change the color from gold to light blue
    if 'Submission #240' in content and 'color:#fbbf24;' in content:
        content = content.replace('color:#fbbf24;', 'color:#60a5fa;')
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print('Fixed color in ' + f)
        count += 1

print('Done! Updated ' + str(count) + ' files.')
