import os
import shutil

def update_file(filepath, replacements):
    if not os.path.exists(filepath):
        print("File not found: " + filepath)
        return

    shutil.copyfile(filepath, filepath + ".bak")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changes_made = 0
    for old_text, new_text in replacements:
        if old_text in content:
            content = content.replace(old_text, new_text)
            changes_made += 1
        else:
            print("Could not find text in " + filepath)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Updated " + filepath + " with " + str(changes_made) + " 
changes.")

print("Starting website updates...")

# 1. Update index.html
banner_html = """<body>
    <!-- SENATE SUBMISSION BANNER -->
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 
100%); color: white; text-align: center; padding: 10px; font-size: 0.9rem; 
position: relative; z-index: 1000;">
        🏛️ <strong>Official Submission:</strong> Accepted and published by 
the Senate Select Committee on Productivity in Australia (Submission 
#240). 
        <a 
href="https://www.aph.gov.au/DocumentStore.ashx?id=25e9d73e-76be-4f7f-87af-5fb5b3e71058&subId=805961" 
target="_blank" style="color: #fbbf24; text-decoration: underline; 
margin-left: 8px;">Read the submission here</a>
    </div>"""

index_replacements = [
    ('"sameAs": [', '"sameAs": [\n        
"https://www.aph.gov.au/DocumentStore.ashx?id=25e9d73e-76be-4f7f-87af-5fb5b3e71058&subId=805961",'),
    ('Optimal portfolio: <strong>30%</strong> Productivity Bonds <span 
style="display:inline-block; background:rgba(255,255,255,0.05); padding:0 
0.5rem; border-radius:4px; margin-left:0.25rem;">(minimizes the combined 
cost-volatility-distress welfare function; Welfare = lower is 
better)</span>', 'Prudent portfolio: <strong>30%</strong> Productivity 
Bonds <span style="display:inline-block; 
background:rgba(255,255,255,0.05); padding:0 0.5rem; border-radius:4px; 
margin-left:0.25rem;">(30% minimizes distress probability; 50% minimizes 
cost on paper but increases risk)</span>'),
    ('<body>', banner_html)
]
update_file('index.html', index_replacements)

# 2. Update README.md
readme_disclaimer = """## 📌 Important Note on Portfolio Optimisation

The simulation reveals a **trade-off** between cost reduction and fiscal 
distress:
- **30% Productivity Bonds** = minimises distress probability (34%)
- **50% Productivity Bonds** = lower expected cost on paper, but distress 
jumps to 48%

"Optimal" depends on what you're optimising for. The book recommends 30% 
as a prudent starting point.

---

"""
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    if "Important Note on Portfolio Optimisation" not in readme_content:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_disclaimer + readme_content)
        print("Updated README.md")

# 3. Update appendix.html
appendix_replacements = [
    ('<p><strong>Example:</strong> The simulation results show that the 
optimal share is 30%.</p>', '<p><strong>Example:</strong> The simulation 
shows a trade-off. A 30% share minimizes fiscal distress (34%), while a 
50% share lowers expected cost on paper but raises distress probability to 
48%. 30% is recommended as the prudent balance.</p>')
]
update_file('appendix.html', appendix_replacements)

print("All updates complete!")
