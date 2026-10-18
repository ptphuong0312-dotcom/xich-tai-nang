import xml.etree.ElementTree as ET
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('rendered_svg.html', 'r', encoding='utf-8') as f:
    text = f.read()

# wrap in root
tree = ET.fromstring(f"<svg>{text}</svg>")

for elem in tree.iter():
    eid = elem.get('id', '')
    if eid in ['sprocketRotated', 'kinematicChainStrand', 'innerPlatesLayer', 'outerPlatesLayer', 'rollersLayer', 'pinsLayer']:
        print(f"Element <{elem.tag} id='{eid}'>: children = {len(elem)}")
        for ch in elem:
            print(f"   <{ch.tag}> fill={ch.get('fill')} stroke={ch.get('stroke')}")
