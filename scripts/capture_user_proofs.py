import subprocess
import os
import time

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
ARTIFACT_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
USER_DATA = r'C:\Users\SirPhuong\AppData\Local\Temp\chrome_user_shots_' + str(int(time.time()))

def capture_updated_shots():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    # Shot 1: Default view right on load (Dark mode check)
    out_dark = os.path.join(ARTIFACT_DIR, 'shot_dark_default.png')
    subprocess.run([
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}_1',
        '--virtual-time-budget=2000',
        '--window-size=1600,1000',
        f'--screenshot={out_dark}',
        'file:///d:/Google Antigravity/Xich tai nang/index.html'
    ], capture_output=True)
    print("Shot 1 (Dark Default) captured:", os.path.exists(out_dark))

    # Shot 2: Section view for MT 630 (Check reasonable hub length ~ 180 mm instead of 1055 mm)
    html_mt_sec = html.replace('recalculateLoad();\n    });', 'recalculateLoad(); setMode("section"); switchControlTab("shaft");\n    });')
    test_mt = os.path.join(WORKSPACE, 'test_mt_sec.html')
    with open(test_mt, 'w', encoding='utf-8') as f:
        f.write(html_mt_sec)

    out_mt = os.path.join(ARTIFACT_DIR, 'shot_section_auto_hub.png')
    subprocess.run([
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}_2',
        '--virtual-time-budget=2000',
        '--window-size=1600,1000',
        f'--screenshot={out_mt}',
        f'file:///{test_mt.replace("\\\\", "/")}'
    ], capture_output=True)
    if os.path.exists(test_mt):
        os.remove(test_mt)
    print("Shot 2 (MT 630 Auto Hub Section) captured:", os.path.exists(out_mt))

    # Shot 3: Section view for FV 90 (ScanChain Hub auto applied)
    html_fv_sec = html.replace('recalculateLoad();\n    });', 'recalculateLoad(); applyPreset("FV90"); setMode("section"); switchControlTab("shaft");\n    });')
    test_fv = os.path.join(WORKSPACE, 'test_fv_sec.html')
    with open(test_fv, 'w', encoding='utf-8') as f:
        f.write(html_fv_sec)

    out_fv = os.path.join(ARTIFACT_DIR, 'shot_section_fv90_auto.png')
    subprocess.run([
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}_3',
        '--virtual-time-budget=2000',
        '--window-size=1600,1000',
        f'--screenshot={out_fv}',
        f'file:///{test_fv.replace("\\\\", "/")}'
    ], capture_output=True)
    if os.path.exists(test_fv):
        os.remove(test_fv)
    print("Shot 3 (FV 90 Auto Hub Section) captured:", os.path.exists(out_fv))

if __name__ == '__main__':
    capture_updated_shots()
