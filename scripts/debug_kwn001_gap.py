import subprocess
import os

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

test_code = """
initChainCatalogUI();
AppState.standard = 'KWN_001';
AppState.currentSeries = 'ANSI';
AppState.currentModelName = '50-1';
AppState.p = 15.875;
AppState.z = 8;
syncUIFromState();
onParamChange();
setTimeout(() => setMode('gap'), 100);
"""
html_test = html.replace('initChainCatalogUI();', test_code)
test_file = os.path.join(WORKSPACE, 'test_gap_debug.html')
with open(test_file, 'w', encoding='utf-8') as f:
    f.write(html_test)

cmd = [
    CHROME_EXE,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--virtual-time-budget=2000',
    '--dump-dom',
    'file:///' + test_file.replace('\\', '/')
]
proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
dom = proc.stdout
if os.path.exists(test_file):
    os.remove(test_file)

with open('debug_dom_gap.txt', 'w', encoding='utf-8') as f:
    f.write(dom)

print('Saved debug_dom_gap.txt, length:', len(dom))

# Find circle cx="0"
c_idx = dom.find('<circle cx="0"')
if c_idx != -1:
    print('Circle:', dom[c_idx:c_idx+200])
else:
    print('Circle not found!')

# Find dR1
r1_idx = dom.find('Cung đáy tiếp xúc r1')
if r1_idx != -1:
    print('R1 section:', dom[r1_idx:r1_idx+400])
else:
    print('R1 not found!')

# Find dSector
sec_idx = dom.find('Khối thân vành răng')
if sec_idx != -1:
    print('Sector section:', dom[sec_idx:sec_idx+300])
