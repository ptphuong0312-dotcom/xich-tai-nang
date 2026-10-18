import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<div[^>]*id=[\'"]canvasBox[\'"][^>]*>([\s\S]*?)</div>', text)
if m:
    print('canvasBox inner:')
    print(m.group(0)[:800])

m2 = re.search(r'function updateTransform\(\)\s*\{([\s\S]*?)\}', text)
if m2:
    print('updateTransform:')
    print(m2.group(0))

m3 = re.search(r'function renderCAD\(\)\s*\{([\s\S]*?)\n    \}', text)
if m3:
    print('renderCAD:')
    print(m3.group(0)[:1200])
