import subprocess
import os
import time

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
ARTIFACT_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
USER_DATA = r'C:\Users\SirPhuong\AppData\Local\Temp\chrome_shots_' + str(int(time.time()))

def capture_visuals():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Section View
    html_sec = html.replace('recalculateLoad();', 'recalculateLoad(); setTimeout(() => setMode("section"), 100);')
    test_sec = os.path.join(WORKSPACE, 'test_sec.html')
    with open(test_sec, 'w', encoding='utf-8') as f:
        f.write(html_sec)

    out_sec = os.path.join(ARTIFACT_DIR, 'shot_section_full.png')
    subprocess.run([
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}_1',
        '--virtual-time-budget=2000',
        '--window-size=1600,1000',
        f'--screenshot={out_sec}',
        f'file:///{test_sec.replace("\\\\", "/")}'
    ], capture_output=True)
    if os.path.exists(test_sec):
        os.remove(test_sec)
    print("Section screenshot captured:", os.path.exists(out_sec))

    # 2. KWN 016 Gap View
    html_gap = html.replace('recalculateLoad();', 'recalculateLoad(); setTimeout(() => { applyPreset("KWN016"); setMode("gap"); }, 100);')
    test_gap = os.path.join(WORKSPACE, 'test_gap.html')
    with open(test_gap, 'w', encoding='utf-8') as f:
        f.write(html_gap)

    out_gap = os.path.join(ARTIFACT_DIR, 'shot_gap_kwn016.png')
    subprocess.run([
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}_2',
        '--virtual-time-budget=2000',
        '--window-size=1600,1000',
        f'--screenshot={out_gap}',
        f'file:///{test_gap.replace("\\\\", "/")}'
    ], capture_output=True)
    if os.path.exists(test_gap):
        os.remove(test_gap)
    print("KWN 016 Gap screenshot captured:", os.path.exists(out_gap))

if __name__ == '__main__':
    capture_visuals()
