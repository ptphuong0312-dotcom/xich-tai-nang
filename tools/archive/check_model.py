import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'\{[^{}]*?"name":\s*"08B-1[^{}]*?\}', text)
if m:
    print('08B-1:', m.group(0))
else:
    print('Not found')
