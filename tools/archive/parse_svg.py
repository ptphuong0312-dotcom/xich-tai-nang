from bs4 import BeautifulSoup
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('rendered_svg.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("Groups:")
for g in soup.find_all('g'):
    gid = g.get('id', 'no-id')
    children = [c.name for c in g.find_all(recursive=False)]
    print(f"  <g id='{gid}'> contains {len(children)} elements: {set(children)}")

# Find all paths
paths = soup.find_all('path')
print(f"\nTotal paths: {len(paths)}")
for p in paths:
    parent_id = p.parent.get('id', 'no-id')
    fill = p.get('fill', 'none')
    stroke = p.get('stroke', 'none')
    print(f"  path under {parent_id}: fill={fill}, stroke={stroke}, d_len={len(p.get('d', ''))}")
