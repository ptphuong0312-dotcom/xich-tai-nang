import subprocess
import os
import time

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
ARTIFACT_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
USER_DATA = r'C:\Users\SirPhuong\AppData\Local\Temp\chrome_clean_shots_' + str(int(time.time()))

def capture_clean_shots():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Shot A: SMS 18 (Main view showing sprocket + chain assembly)
    html_sms = html.replace('initChainCatalogUI();', 'initChainCatalogUI(); applyPreset("SMS18");')
    test_sms = os.path.join(WORKSPACE, 'test_sms_clean.html')
    with open(test_sms, 'w', encoding='utf-8') as f:
        f.write(html_sms)

    out_sms = os.path.join(ARTIFACT_DIR, 'shot_sms18_main.png')
    subprocess.run([
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}_sms',
        '--virtual-time-budget=2000',
        '--window-size=1600,1000',
        f'--screenshot={out_sms}',
        f'file:///{test_sms.replace("\\\\", "/")}'
    ], capture_output=True)
    if os.path.exists(test_sms):
        os.remove(test_sms)
    print("Clean SMS 18 screenshot captured:", os.path.exists(out_sms))

    # 2. Shot B: Tab 3 with ScanChain Hub card for FV 90
    html_tab3 = html.replace('initChainCatalogUI();', 'initChainCatalogUI(); applyPreset("FV90"); switchControlTab("shaft");')
    test_tab3 = os.path.join(WORKSPACE, 'test_tab3_clean.html')
    with open(test_tab3, 'w', encoding='utf-8') as f:
        f.write(html_tab3)

    out_tab3 = os.path.join(ARTIFACT_DIR, 'shot_scanchain_hub_tab3.png')
    subprocess.run([
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}_tab3',
        '--virtual-time-budget=2000',
        '--window-size=1600,1000',
        f'--screenshot={out_tab3}',
        f'file:///{test_tab3.replace("\\\\", "/")}'
    ], capture_output=True)
    if os.path.exists(test_tab3):
        os.remove(test_tab3)
    print("Clean ScanChain Hub Tab 3 screenshot captured:", os.path.exists(out_tab3))

    # 3. Shot C: Section View showing Hub with ScanChain diameter
    html_sec = html.replace('initChainCatalogUI();', 'initChainCatalogUI(); applyPreset("FV90"); applyScanChainHubParams(); setMode("section");')
    test_sec = os.path.join(WORKSPACE, 'test_sec_clean.html')
    with open(test_sec, 'w', encoding='utf-8') as f:
        f.write(html_sec)

    out_sec = os.path.join(ARTIFACT_DIR, 'shot_scanchain_hub_section.png')
    subprocess.run([
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}_sec',
        '--virtual-time-budget=2000',
        '--window-size=1600,1000',
        f'--screenshot={out_sec}',
        f'file:///{test_sec.replace("\\\\", "/")}'
    ], capture_output=True)
    if os.path.exists(test_sec):
        os.remove(test_sec)
    print("Clean Section screenshot captured:", os.path.exists(out_sec))

if __name__ == '__main__':
    capture_clean_shots()
