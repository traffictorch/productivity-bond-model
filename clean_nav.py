import glob

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()

    # Clean up the weird line break from the previous script
    broken_nav = '<li><a href="contributions.html">Contributions</a>\n            <a href="about.html">Traffic Torch</a></li>'
    fixed_nav = '<li><a href="contributions.html">Contributions</a></li><li><a href="about.html">Traffic Torch</a></li>'
    
    broken_nav_2 = '<a href="contributions.html">Contributions</a>\n            <a href="about.html">About</a>'
    fixed_nav_2 = '<a href="contributions.html">Contributions</a></li><li><a href="about.html">About</a>'

    if broken_nav in content:
        content = content.replace(broken_nav, fixed_nav)
    if broken_nav_2 in content:
        content = content.replace(broken_nav_2, fixed_nav_2)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        count += 1

print('Cleaned up nav in ' + str(count) + ' files.')
