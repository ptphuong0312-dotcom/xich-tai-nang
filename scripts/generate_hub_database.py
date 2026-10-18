import pymupdf
import json
import collections
import re

doc = pymupdf.open(r'Tai Lieu\High Precision Conveyor Chains and Sprockets.pdf')

hub_db = {}
# hub_db format:
# {
#   "FV": {
#       "FV63": {
#           "p100": { "8": { Dn: 190, Ln1: 120, Ln2: 100, Z1: 20, Z2: 14, Pb: 30 }, ... }
#       }
#   },
#   "M": { ... }
# }

for pno in [15, 16, 17, 18]:
    page = doc[pno]
    family = "FV" if pno in [15, 16] else "M"
    words = page.get_text("words")
    
    rows_by_y = collections.defaultdict(list)
    for w in words:
        y = round(w[1], 1)
        matched_y = None
        for ey in rows_by_y.keys():
            if abs(ey - y) <= 2.5:
                matched_y = ey
                break
        if matched_y is None:
            matched_y = y
        rows_by_y[matched_y].append(w)
        
    for y, rwords in sorted(rows_by_y.items()):
        if y < 100 or y > 780:
            continue
        rwords = sorted(rwords, key=lambda w: w[0])
        tokens = [w[4].replace(',', '.') for w in rwords]
        
        # Check if line starts with FV or M
        first = tokens[0].upper()
        if not (first.startswith('FV') or first.startswith('M')):
            continue
            
        # Extract fields
        # Typical line: ['FV63', '100', '8', '261.31', '279.31', '243.31', '18', '190', '120', '100', '20', '14', '30']
        # Or with " for ditto
        try:
            iso_code = first
            pitch = int(float(tokens[1]))
            z = int(float(tokens[2]))
            d0 = float(tokens[3])
            da = float(tokens[4])
            df = float(tokens[5])
            bush_d = float(tokens[6])
            
            # Check remaining tokens
            rem = tokens[7:]
            # If Dn is missing or symbol:
            dn_val = rem[0]
            if dn_val in ['“', '"', '', '-', '']:
                dn = 0
            else:
                dn = float(dn_val)
                
            ln1 = float(rem[1]) if len(rem) > 1 and rem[1].replace('.','').isdigit() else 0
            ln2 = float(rem[2]) if len(rem) > 2 and rem[2].replace('.','').isdigit() else 0
            z1 = float(rem[3]) if len(rem) > 3 and rem[3].replace('.','').isdigit() else 0
            z2 = float(rem[4]) if len(rem) > 4 and rem[4].replace('.','').isdigit() else 0
            pb = float(rem[5]) if len(rem) > 5 and rem[5].replace('.','').isdigit() else 0
            
            if family not in hub_db:
                hub_db[family] = {}
            if iso_code not in hub_db[family]:
                hub_db[family][iso_code] = {}
            p_key = f"p{pitch}"
            if p_key not in hub_db[family][iso_code]:
                hub_db[family][iso_code][p_key] = {}
                
            hub_db[family][iso_code][p_key][str(z)] = {
                "d0": d0,
                "da": da,
                "df": df,
                "bush_d": bush_d,
                "Dn": dn,
                "Ln1": ln1,
                "Ln2": ln2,
                "Z1": z1,
                "Z2": z2,
                "Pb": pb
            }
        except Exception as ex:
            # print("Skip line:", tokens, ex)
            pass

print("Extracted hub database summary:")
for fam, codes in hub_db.items():
    print(f"Family {fam}: {len(codes)} models -> {list(codes.keys())}")
    for c, pitches in list(codes.items())[:2]:
        print(f"  {c}: pitches {list(pitches.keys())}")

with open('data/scanchain_sprocket_hubs.json', 'w', encoding='utf-8') as f:
    json.dump(hub_db, f, indent=2)

print("Saved data/scanchain_sprocket_hubs.json")
