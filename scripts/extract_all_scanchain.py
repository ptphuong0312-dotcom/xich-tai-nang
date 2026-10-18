import pymupdf
import json
import collections

doc = pymupdf.open(r'Tai Lieu\High Precision Conveyor Chains and Sprockets.pdf')

# 1. Parse SMS 1698 (Page 11)
page11 = doc[10]
words11 = page11.get_text("words")

# Group words by line (y coordinate ~ 110.9, 121.8, ...)
rows_by_y = collections.defaultdict(list)
for w in words11:
    y = round(w[1], 1)
    # Find matching y bucket within 3 pts
    matched_y = None
    for existing_y in rows_by_y.keys():
        if abs(existing_y - y) <= 3.0:
            matched_y = existing_y
            break
    if matched_y is None:
        matched_y = y
    rows_by_y[matched_y].append(w)

sms_data = []
# Filter for table data rows (y > 105 and y < 750)
for y, row_words in sorted(rows_by_y.items()):
    if y < 105 or y > 750:
        continue
    # Sort words by x
    row_words = sorted(row_words, key=lambda w: w[0])
    text_line = ' '.join(w[4] for w in row_words)
    tokens = [w[4].replace(',', '.') for w in row_words]
    # Check if this row looks like data (ends with a number kN)
    if len(tokens) >= 12:
        try:
            # Last token is breaking load
            fb = float(tokens[-1])
            # Pitch is second or third token
            sms_data.append({
                'raw': text_line,
                'tokens': tokens
            })
        except:
            pass

print(f'Extracted {len(sms_data)} raw rows for SMS 1698')

# 2. Parse Sprocket Hubs from Pages 16, 17, 18, 19
sprocket_rows = []
for pno in [15, 16, 17, 18]:
    page = doc[pno]
    std_name = 'DIN 8165 FV' if pno in [15, 16] else 'DIN 8167 M'
    words = page.get_text("words")
    p_rows = collections.defaultdict(list)
    for w in words:
        y = round(w[1], 1)
        matched_y = None
        for ey in p_rows.keys():
            if abs(ey - y) <= 2.5:
                matched_y = ey
                break
        if matched_y is None:
            matched_y = y
        p_rows[matched_y].append(w)
    
    for y, rwords in sorted(p_rows.items()):
        if y < 100 or y > 780:
            continue
        rwords = sorted(rwords, key=lambda w: w[0])
        line = ' '.join(w[4] for w in rwords)
        tokens = [w[4].replace(',', '.') for w in rwords]
        # Columns: ISO Nr, P, z, Dd, Da1, Da2, Bush dia, Dn, Ln1, Ln2, Z1, Z2, Pb
        if len(tokens) >= 10:
            sprocket_rows.append({
                'page': pno + 1,
                'std': std_name,
                'tokens': tokens,
                'line': line
            })

print(f'Extracted {len(sprocket_rows)} sprocket rows from Pages 16-19')

with open('debug_extracted_data.json', 'w', encoding='utf-8') as f:
    json.dump({'sms_rows': sms_data, 'sprocket_rows': sprocket_rows}, f, indent=2)

print('Saved debug_extracted_data.json')
