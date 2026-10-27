#!/usr/bin/env python3
import pathlib, re, sys

VERSION = "1.2"

print(f"Applying cache-busting version: ?v={VERSION}\n")

def bust_url(match):
    full_match = match.group(0)
    url = match.group(1)
    
    # Ignore external URLs (CDNs, fonts, etc.)
    if url.startswith('http://') or url.startswith('https://') or url.startswith('//') or url.startswith('data:'):
        return full_match
        
    # Strip any existing ?v= string
    base_url = url.split('?')[0]
    
    # Extract the prefix (e.g., href=" or src=")
    prefix = full_match.split('="')[0] + '="'
    
    return f'{prefix}{base_url}?v={VERSION}"'

updated_files = 0
for path in pathlib.Path('.').glob('*.html'):
    if 'backup' in path.name or 'beta' in path.name or '404' in path.name:
        continue
        
    html = path.read_text()
    original_html = html
    
    # Bust local CSS and JS
    html = re.sub(r'href="([^"]*\.css)"', bust_url, html)
    html = re.sub(r'src="([^"]*\.js)"', bust_url, html)
    
    # Inject no-cache meta tags into <head> if they don't exist
    meta_tags = """<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">"""
    
    if 'http-equiv="Cache-Control"' not in html:
        html = html.replace('<head>', '<head>\n  ' + meta_tags, 1)
        
    if html != original_html:
        path.write_text(html)
        print(f"  OK  {path.name}")
        updated_files += 1

print(f"\nDone. {updated_files} HTML files updated.")
