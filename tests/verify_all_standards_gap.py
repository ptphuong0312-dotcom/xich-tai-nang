import subprocess
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

test_script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const results = {};
        const standards = ['KWN_017', 'KWN_015', 'KWN_001', 'KWN_016'];
        
        for (const std of standards) {
            document.getElementById('selStandard').value = std;
            onStandardChange();
            setMode('gap');
            
            const g = document.getElementById('mainViewport');
            results[std] = {
                svg_len: g.innerHTML.length,
                has_beta_or_X: g.innerHTML.includes('β') || g.innerHTML.includes('X ='),
                has_r1: g.innerHTML.includes('r1 ='),
                has_r2: g.innerHTML.includes('r2 ='),
                hud: document.getElementById('hudStatus')?.innerText
            };
        }
        
        const div = document.createElement('div');
        div.id = 'ALL_STD_OUTPUT';
        div.textContent = JSON.stringify(results);
        document.body.appendChild(div);
    }, 500);
});
</script>
"""

harness = html.replace('</body>', test_script + '\n</body>')
harness_path = os.path.join(WORKSPACE, 'temp_test_all_std.html')
with open(harness_path, 'w', encoding='utf-8') as f:
    f.write(harness)

cmd = [
    CHROME_EXE,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--virtual-time-budget=3000',
    '--dump-dom',
    f'file:///{harness_path.replace("\\\\", "/")}'
]

proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
dom = proc.stdout

if os.path.exists(harness_path):
    os.remove(harness_path)

match = re.search(r'<div id="ALL_STD_OUTPUT">(.*?)</div>', dom, re.DOTALL)
if match:
    import json
    import html as html_module
    data = json.loads(html_module.unescape(match.group(1)))
    all_ok = True
    for std, res in data.items():
        print(f"[{std}]: svg_len={res['svg_len']}, has_beta/X={res['has_beta_or_X']}, has_r1={res['has_r1']}, has_r2={res['has_r2']}")
        print(f"       hud: {res['hud']}")
        if not (res['has_beta_or_X'] and res['has_r1'] and res['has_r2']):
            print(f"FAILED: Missing dimensions in {std}")
            all_ok = False
    if not all_ok:
        sys.exit(1)
    print("ALL STANDARDS GAP VIEW DIMENSIONS VERIFIED!")
    sys.exit(0)
else:
    print("ERROR: No output found in DOM!")
    sys.exit(1)
