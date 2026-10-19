import subprocess
import os
import sys

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
BRAIN_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'

sys.stdout.reconfigure(encoding='utf-8')

def verify_plan3_wizard():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    # Test 1: Verify conveyor_diff mode with Application Wizard and Scorecard
    harness_diff = """
<script>
window.__wizard_test_results = {};
window.addEventListener('DOMContentLoaded', () => {
    // 1. Activate conveyor_diff mode via Wizard
    setAppMode('conveyor_diff');

    // 2. Choose MT 112 to verify standard catalog pitch pairs
    const selModel = document.getElementById('selChainModel');
    if (selModel) {
        selModel.value = 'MT 112';
        onChainModelChange();
    }

    // 3. Collect state
    const selPair = document.getElementById('selDualPitchPair');
    const pairOptions = selPair ? Array.from(selPair.options).map(o => o.text) : [];
    const scorecard = document.getElementById('diffPitchScorecard');

    window.__wizard_test_results = {
        appMode: AppState.appMode,
        isDifferentPitch: AppState.isDifferentPitch,
        model: AppState.currentModelName,
        diff_p1: AppState.diff_p1,
        diff_p2: AppState.diff_p2,
        z: AppState.z,
        pairOptions: pairOptions,
        scorecardVisible: scorecard ? scorecard.style.display !== 'none' : false,
        scorecardText: scorecard ? scorecard.innerText : ''
    };
});
</script>
"""
    test1_html = html.replace('</body>', harness_diff + '\n</body>')
    test1_path = os.path.join(WORKSPACE, 'temp_test_wizard_diff.html')
    with open(test1_path, 'w', encoding='utf-8') as f:
        f.write(test1_html)

    shot1_path = os.path.join(BRAIN_DIR, 'shot_plan3_conveyor_diff_scorecard.png')
    cmd1 = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--window-size=1650,1300',
        '--virtual-time-budget=2000',
        f'--screenshot={shot1_path}',
        f'file:///{test1_path.replace(chr(92), "/")}'
    ]
    subprocess.run(cmd1, capture_output=True, check=True)
    print(f"Plan 3 conveyor_diff screenshot saved to: {shot1_path}")

    # Test 2: Verify roller_drive mode via Wizard
    harness_roller = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    setAppMode('roller_drive');
});
</script>
"""
    test2_html = html.replace('</body>', harness_roller + '\n</body>')
    test2_path = os.path.join(WORKSPACE, 'temp_test_wizard_roller.html')
    with open(test2_path, 'w', encoding='utf-8') as f:
        f.write(test2_html)

    shot2_path = os.path.join(BRAIN_DIR, 'shot_plan3_roller_drive_wizard.png')
    cmd2 = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--window-size=1650,1300',
        '--virtual-time-budget=2000',
        f'--screenshot={shot2_path}',
        f'file:///{test2_path.replace(chr(92), "/")}'
    ]
    subprocess.run(cmd2, capture_output=True, check=True)
    print(f"Plan 3 roller_drive screenshot saved to: {shot2_path}")

    # Cleanup temp files
    try:
        os.remove(test1_path)
        os.remove(test2_path)
    except:
        pass

    print("ALL PLAN 3 VISUAL VERIFICATIONS COMPLETED!")

if __name__ == '__main__':
    verify_plan3_wizard()
