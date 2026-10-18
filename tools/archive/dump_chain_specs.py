import sys, pymupdf
sys.stdout.reconfigure(encoding='utf-8')

doc = pymupdf.open(r'D:\Google Antigravity\Xich tai nang\Tai Lieu\kettenwulf-conveyor-chains-and-sprockets.pdf')

for pno in [31, 32, 33, 34]: # pages 32, 33, 34, 35 (0-indexed)
    page = doc[pno]
    print(f'==============================')
    print(f'=== PAGE {pno+1} ===')
    print(f'==============================')
    print(page.get_text('text'))
