import subprocess
import os

presets = ['MC112', 'ANSI80', 'KWN016']
chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

for preset in presets:
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace('initChainCatalogUI();', f'initChainCatalogUI(); applyPreset("{preset}");')
    test_file = f'test_{preset}.html'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    out_png = f'd:\\Google Antigravity\\Xich tai nang\\shot_{preset}.png'
    subprocess.run([
        chrome_exe,
        '--headless',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir=C:\\Users\\SirPhuong\\AppData\\Local\\Temp\\chrome_{preset}',
        '--window-size=1920,1200',
        f'--screenshot={out_png}',
        f'file:///d:/Google Antigravity/Xich tai nang/{test_file}'
    ], capture_output=True)
    print(f'Captured {out_png}, exists: {os.path.exists(out_png)}')

    # Clean up test html
    if os.path.exists(test_file):
        os.remove(test_file)
