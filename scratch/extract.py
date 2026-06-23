import re

with open('dashboard/index.html', encoding='utf-8') as f:
    html = f.read()

# Find the "Audience web" navigation item
nav_match = re.search(r'<div[^>]*data-nav="web"[^>]*>.*?</div>', html)
if nav_match:
    print("NAV TAB FOUND:", nav_match.group(0))

# Find the body section for web
start = html.find('id="webBody"')
if start != -1:
    end = html.find('id="retBody"', start)
    if end == -1: end = len(html)
    content = html[start-50:end]
    with open('web_body.html', 'w', encoding='utf-8') as out:
        out.write(content)
    print("Wrote web_body.html")
else:
    print("webBody not found")
