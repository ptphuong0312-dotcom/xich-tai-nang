import pymupdf
import json
import collections

doc = pymupdf.open(r'Tai Lieu\High Precision Conveyor Chains and Sprockets.pdf')

# 1. Parse SMS 1698 (Page 11)
page11 = doc[10]
words11 = page11.get_text("words")

rows_by_y = collections.defaultdict(list)
for w in words11:
    y = round(w[1], 1)
    matched_y = None
    for ey in rows_by_y.keys():
        if abs(ey - y) <= 2.5:
            matched_y = ey
            break
    if matched_y is None:
        matched_y = y
    rows_by_y[matched_y].append(w)

sms_entries = collections.defaultdict(lambda: {
    'name': '',
    'FB': 0,
    'p_list': [],
    'b1': 0,
    'd1': 0,
    'd3': 0,
    'd5': 0,
    'l': 0,
    's': 0,
    's1': 0,
    'g': 0,
    'g1': 0,
    'g2': 0
})

for y, rwords in sorted(rows_by_y.items()):
    if y < 105 or y > 750:
        continue
    rwords = sorted(rwords, key=lambda w: w[0])
    tokens = [w[4].replace(',', '.') for w in rwords]
    
    # Identify chain name and heavy modifier
    # Tokens can be: ['8.5', '63', '25', ...] or ['8.5', 'heavy', '63', '25', ...]
    if len(tokens) >= 12:
        try:
            if tokens[1].lower() == 'heavy':
                c_name = f"SMS {tokens[0]} Heavy"
                num_tokens = tokens[2:]
            else:
                c_name = f"SMS {tokens[0]}"
                num_tokens = tokens[1:]
                
            pitch = int(float(num_tokens[0]))
            b1 = float(num_tokens[1])
            d1 = float(num_tokens[2])
            d3 = float(num_tokens[3])
            d5 = float(num_tokens[4])
            l = float(num_tokens[5])
            s = float(num_tokens[6])
            s1 = float(num_tokens[7])
            g = float(num_tokens[8])
            g1 = float(num_tokens[9]) if len(num_tokens) > 9 else g
            g2 = float(num_tokens[10]) if len(num_tokens) > 10 else g
            fb = float(num_tokens[-1])
            
            entry = sms_entries[c_name]
            entry['name'] = c_name
            entry['FB'] = fb
            entry['Fper'] = round(fb / 6.0, 1) # Standard safety factor 6
            if pitch not in entry['p_list']:
                entry['p_list'].append(pitch)
            entry['b1'] = b1
            entry['d1'] = d1
            entry['d3'] = d3
            entry['d4'] = d3 # Bushing
            entry['d5'] = d5 # Roller
            entry['l'] = l
            entry['s'] = s
            entry['s1'] = s1
            entry['g'] = g
            entry['g1'] = g1
            entry['g2'] = g2
            entry['dw_rec'] = int(d1 * 2.5)
        except Exception as ex:
            # print("Skip line:", tokens, ex)
            pass

# Convert to list
sms_list = list(sms_entries.values())
for s in sms_list:
    s['p_list'].sort()
    print(f"{s['name']}: FB={s['FB']}kN, p={s['p_list']}, b1={s['b1']}, d3={s['d3']}, d5={s['d5']}")

with open('data/sms_1698_standard.json', 'w', encoding='utf-8') as f:
    json.dump(sms_list, f, indent=2)

print(f"Saved {len(sms_list)} SMS 1698 chain series to data/sms_1698_standard.json")
