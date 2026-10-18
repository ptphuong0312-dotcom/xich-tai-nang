import subprocess
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Switch to Tab 3 on load
html = html.replace('initChainCatalogUI();', 'initChainCatalogUI(); switchControlTab("shaft");')
test_file = 'test_tab3.html'
with open(test_file, 'w', encoding='utf-8') as f:
    f.write(html)

chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
out_png = r'd:\Google Antigravity\Xich tai nang\shot_tab3.png'
subprocess.run([
    chrome_exe,
    '--headless',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=C:\\Users\\SirPhuong\\AppData\\Local\\Temp\\chrome_tab3',
    '--window-size=1920,1200',
    f'--screenshot={out_png}',
    f'file:///d:/Google Antigravity/Xich tai nang/{test_file}'
], capture_output=True)

if os.path.exists(test_file):
    os.remove(test_file)
print(f'Captured {out_png}, exists: {os.path.exists(out_png)}')
