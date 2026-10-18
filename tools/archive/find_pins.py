with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'd1_pin' in l or 'pin_d1' in l:
        clean = l.strip().encode('ascii', errors='replace').decode('ascii')
        print(f'{i+1}: {clean}')
