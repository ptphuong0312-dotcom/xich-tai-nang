import re
import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')

# 1. Parse user file: c:\Users\SirPhuong\Desktop\New Text Document.txt
user_file_path = r'c:\Users\SirPhuong\Desktop\New Text Document.txt'
with open(user_file_path, 'r', encoding='utf-8') as f:
    user_lines = f.readlines()

user_tables = {'FV 40': [], 'FV 63': []}
current_chain = None

for line in user_lines:
    line_s = line.strip()
    if 'Dòng xích FV 40' in line_s:
        current_chain = 'FV 40'
    elif 'Dòng xích FV 63' in line_s:
        current_chain = 'FV 63'
    elif line_s.startswith('|') and current_chain:
        parts = [p.strip() for p in line_s.split('|')[1:-1]]
        if len(parts) >= 13 and not parts[0].startswith('Bước') and not parts[0].startswith(':---'):
            # Data row
            p_val = parts[0].replace('*', '').strip()
            z_val = parts[1].strip()
            d0_val = parts[2].strip()
            da_d3 = parts[3].strip()
            da_d4 = parts[4].strip()
            da_d5 = parts[5].strip()
            da_d6 = parts[6].strip()
            dN_val = parts[7].strip()
            NL_val = parts[8].strip()
            B1_val = parts[9].strip()
            B1_flange = parts[10].strip()
            dB_val = parts[11].strip()
            wt_val = parts[12].strip()
            user_tables[current_chain].append({
                'p': p_val, 'Z': z_val, 'd0': d0_val,
                'da_d3': da_d3, 'da_d4': da_d4, 'da_d5': da_d5, 'da_d6': da_d6,
                'dN': dN_val, 'NL': NL_val, 'B1': B1_val, 'B1_flange': B1_flange,
                'dB': dB_val, 'wt': wt_val
            })

print(f"Parsed from User File:")
print(f"  FV 40 rows: {len(user_tables['FV 40'])}")
print(f"  FV 63 rows: {len(user_tables['FV 63'])}")

# 2. Parse Catalog Page 58
doc = fitz.open(r'Tai Lieu/kettenwulf-conveyor-chains-and-sprockets.pdf')
page = doc[57] # Page 58

# Let's extract the structured blocks from Page 58
# In Page 58, blocks are:
# Block 44: FV 40 (y0 ~ 446)
# Block 45: 40 -> rows 46-50 (Z=6,8,10,12,15)
# Block 51: 63 -> rows 52-56 (Z=6,8,10,12,15)
# Block 57: 100 -> rows 58-62 (Z=6,8,10,12,15)
# Block 2: FV 63 (y0 ~ 668)
# Block 3: 63 -> rows 4-8 (Z=6,8,10,12,15)
# Block 9: 100 -> rows 10-14 (Z=6,8,10,12,15)
# Block 15: 125 -> rows 16-20 (Z=6,8,10,12,15)
# Block 21: 160 -> rows 22-26 (Z=6,8,10,12,15)

catalog_tables = {'FV 40': [], 'FV 63': []}

def parse_block_rows(p_val, block_ids):
    rows = []
    for bid in block_ids:
        b = [blk for blk in page.get_text('blocks') if blk[5] == bid][0]
        lines = [l.strip() for l in b[4].split('\n') if l.strip()]
        # lines format: [Z, d0, da_d3, da_d4, da_d5, da_d6, dN, NL, B1, B1_flange, dB, wt]
        if len(lines) == 12:
            rows.append({
                'p': str(p_val),
                'Z': lines[0],
                'd0': lines[1].replace(',', '.'),
                'da_d3': lines[2],
                'da_d4': lines[3],
                'da_d5': lines[4],
                'da_d6': lines[5],
                'dN': lines[6],
                'NL': lines[7],
                'B1': lines[8],
                'B1_flange': lines[9],
                'dB': lines[10],
                'wt': lines[11]
            })
    return rows

catalog_tables['FV 40'].extend(parse_block_rows(40, [46, 47, 48, 49, 50]))
catalog_tables['FV 40'].extend(parse_block_rows(63, [52, 53, 54, 55, 56]))
catalog_tables['FV 40'].extend(parse_block_rows(100, [58, 59, 60, 61, 62]))

catalog_tables['FV 63'].extend(parse_block_rows(63, [4, 5, 6, 7, 8]))
catalog_tables['FV 63'].extend(parse_block_rows(100, [10, 11, 12, 13, 14]))
catalog_tables['FV 63'].extend(parse_block_rows(125, [16, 17, 18, 19, 20]))
catalog_tables['FV 63'].extend(parse_block_rows(160, [22, 23, 24, 25, 26]))

print(f"\nParsed from Catalog Page 58:")
print(f"  FV 40 rows: {len(catalog_tables['FV 40'])}")
print(f"  FV 63 rows: {len(catalog_tables['FV 63'])}")

# 3. COMPARE CELL BY CELL
print("\n" + "="*80)
print("CHI TIẾT SO SÁNH TỪNG HÀNG SỐ LIỆU GIỮA FILE CỦA BẠN VÀ TRANG 58 CATALOG:")
print("="*80)

fields = ['p', 'Z', 'd0', 'da_d3', 'da_d4', 'da_d5', 'da_d6', 'dN', 'NL', 'B1', 'B1_flange', 'dB', 'wt']

for chain in ['FV 40', 'FV 63']:
    print(f"\n>>> DÒNG XÍCH: {chain}")
    u_rows = user_tables[chain]
    c_rows = catalog_tables[chain]
    
    # Check rows in user file vs catalog
    for i, u_row in enumerate(u_rows):
        if i < len(c_rows):
            c_row = c_rows[i]
            diffs = []
            for fld in fields:
                u_v = u_row[fld]
                c_v = c_row[fld]
                # Compare as float if possible
                try:
                    if float(u_v) != float(c_v):
                        diffs.append(f"{fld}: User='{u_v}' vs Cat='{c_v}'")
                except:
                    if u_v != c_v:
                        diffs.append(f"{fld}: User='{u_v}' vs Cat='{c_v}'")
            if diffs:
                print(f"  [KHÁC BIỆT] p={u_row['p']}, Z={u_row['Z']}: {', '.join(diffs)}")
            else:
                print(f"  [TRÙNG KHỚP 100%] p={u_row['p']}, Z={u_row['Z']}, d0={u_row['d0']}")
        else:
            print(f"  [THỪA] Hàng p={u_row['p']}, Z={u_row['Z']} không có trong catalog!")
            
    if len(c_rows) > len(u_rows):
        print(f"\n  [THIẾU TRONG TÀI LIỆU CỦA BẠN]: Thiếu {len(c_rows) - len(u_rows)} hàng của {chain}!")
        for j in range(len(u_rows), len(c_rows)):
            missing_row = c_rows[j]
            print(f"    - p={missing_row['p']}, Z={missing_row['Z']}: d0={missing_row['d0']}, da_d3={missing_row['da_d3']}, da_d4={missing_row['da_d4']}, da_d5={missing_row['da_d5']}, da_d6={missing_row['da_d6']}, dN={missing_row['dN']}, NL={missing_row['NL']}, B1={missing_row['B1']}, B1_flange={missing_row['B1_flange']}, dB={missing_row['dB']}, wt={missing_row['wt']} kg")
