import subprocess
import os
import time

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
ARTIFACT_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'
WORKSPACE = r'd:\Google Antigravity\Xich tai nang'

with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Test 1: FV 90 Section Mode
html_fv = html.replace('recalculateLoad();\n    });', 'recalculateLoad(); applyPreset("FV90"); setMode("section"); switchControlTab("shaft");\n    });')
test_fv_path = os.path.join(WORKSPACE, 'test_live_fv.html')
with open(test_fv_path, 'w', encoding='utf-8') as f:
    f.write(html_fv)

out_fv = os.path.join(ARTIFACT_DIR, 'shot_live_section_fv90.png')
user_data_1 = r'C:\Users\SirPhuong\AppData\Local\Temp\chrome_live_' + str(int(time.time())) + '_1'
subprocess.run([
    CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
    f'--user-data-dir={user_data_1}',
    '--virtual-time-budget=2000',
    '--window-size=1600,1000',
    f'--screenshot={out_fv}',
    f'file:///{test_fv_path.replace("\\\\", "/")}'
], capture_output=True)

if os.path.exists(test_fv_path):
    os.remove(test_fv_path)

print("Shot FV90 Section:", os.path.exists(out_fv))

# Test 2: KWN 016 MT 20 Section Mode (User image 2 case)
html_mt = html.replace(
    'recalculateLoad();\n    });',
    'recalculateLoad(); document.getElementById("selectChainStandard").value = "KWN_016"; onStandardChange(); document.getElementById("selectChainSeries").value = "MT"; onSeriesChange(); document.getElementById("selectChainModel").value = "MT 20"; onChainModelChange(); setMode("section"); switchControlTab("shaft");\n    });'
)
test_mt_path = os.path.join(WORKSPACE, 'test_live_mt.html')
with open(test_mt_path, 'w', encoding='utf-8') as f:
    f.write(html_mt)

out_mt = os.path.join(ARTIFACT_DIR, 'shot_live_section_mt20.png')
user_data_2 = r'C:\Users\SirPhuong\AppData\Local\Temp\chrome_live_' + str(int(time.time())) + '_2'
subprocess.run([
    CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
    f'--user-data-dir={user_data_2}',
    '--virtual-time-budget=2000',
    '--window-size=1600,1000',
    f'--screenshot={out_mt}',
    f'file:///{test_mt_path.replace("\\\\", "/")}'
], capture_output=True)

if os.path.exists(test_mt_path):
    os.remove(test_mt_path)

print("Shot MT20 Section:", os.path.exists(out_mt))
