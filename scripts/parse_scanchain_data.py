import pymupdf
import json
import re

doc = pymupdf.open(r'Tai Lieu\High Precision Conveyor Chains and Sprockets.pdf')

# 1. Parse SMS 1698 (Page 11)
page11 = doc[10]
text11 = page11.get_text()

# We can also parse with blocks or words to ensure table columns align
blocks = page11.get_text("words")
# Sort by y0, then x0
# Let's inspect the text structure
with open('debug_page11_words.txt', 'w', encoding='utf-8') as f:
    for b in sorted(blocks, key=lambda w: (round(w[1], 1), w[0])):
        f.write(f'{b[0]:.1f}, {b[1]:.1f}: {b[4]}\n')

print('Saved debug_page11_words.txt')
