with open('rendered_svg.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find all path elements
paths = re.findall(r'<path[^>]*>', text)
print(f"Total paths: {len(paths)}")
for p in paths:
    print(p[:120])
