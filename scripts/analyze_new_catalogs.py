import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdfs = [
    'Tai Lieu/High Precision Conveyor Chains and Sprockets.pdf',
    'Tai Lieu/tsubaki large size conveyor chains catalogue.pdf',
    'Tai Lieu/TSUBAKI general-catalog.pdf'
]

for p in pdfs:
    print('='*70)
    print('FILE:', p)
    if not os.path.exists(p):
        print('NOT FOUND!')
        continue
    doc = fitz.open(p)
    print('Total Pages:', len(doc))
    
    # Extract Title and Table of Contents / Outline if present
    toc = doc.get_toc()
    if toc:
        print('Outline / Table of Contents (first 15 entries):')
        for item in toc[:15]:
            print(f'  Level {item[0]}: {item[1]} (Page {item[2]})')
    else:
        # Search first 10 pages for headings
        print('First 5 pages titles/headers:')
        for i in range(min(5, len(doc))):
            blocks = doc[i].get_text('blocks')
            headers = [b[4].strip() for b in blocks if len(b[4].strip()) < 80 and any(w in b[4].lower() for w in ['contents', 'chain', 'sprocket', 'index', 'catalogue', 'tsubaki', 'conveyor'])]
            if headers:
                print(f'  Page {i+1}: {headers[:3]}')

    # Search for sprocket and toothing details
    sprocket_pages = []
    for idx, page in enumerate(doc):
        t = page.get_text().lower()
        if 'sprocket' in t and any(w in t for w in ['dimension', 'toothing', 'tooth', 'hub', 'bore', 'pitch circle', 'contour']):
            sprocket_pages.append(idx + 1)
    print(f'Sprocket technical pages count: {len(sprocket_pages)}')
    print(f'Key sprocket pages: {sprocket_pages[:12]}')
