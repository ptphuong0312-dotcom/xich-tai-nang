import subprocess
import os

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
ARTIFACT_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
USER_DATA = r'C:\Users\SirPhuong\AppData\Local\Temp\chrome_tip_zoom'

with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

zoom_script = """
recalculateLoad();
setTimeout(() => {
    AppState.zoom = 5.0;
    AppState.panX = 250;
    AppState.panY = 2700;
    updateTransform();
}, 200);
"""
html_zoom = html.replace('recalculateLoad();', zoom_script)
test_zoom = os.path.join(WORKSPACE, 'test_zoom.html')
with open(test_zoom, 'w', encoding='utf-8') as f:
    f.write(html_zoom)

out_tip = os.path.join(ARTIFACT_DIR, 'shot_tip_zoom.png')
file_url = 'file:///' + test_zoom.replace('\\', '/')
subprocess.run([
    CHROME_EXE,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    f'--user-data-dir={USER_DATA}',
    '--virtual-time-budget=2000',
    '--window-size=1600,1000',
    f'--screenshot={out_tip}',
    file_url
], capture_output=True)

if os.path.exists(test_zoom):
    os.remove(test_zoom)
print('Tip zoom captured:', os.path.exists(out_tip))
