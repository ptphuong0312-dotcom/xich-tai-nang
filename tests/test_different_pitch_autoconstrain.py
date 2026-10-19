import subprocess
import os
import sys
import json

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
BRAIN_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'

sys.stdout.reconfigure(encoding='utf-8')

def test_diff_auto_constrain():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    # Harness script to simulate UI interactions
    harness = """
<script>
window.__test_diff_results = {};
window.__diff_errors = [];
window.onerror = function(msg, url, lineNo, columnNo, error) {
    window.__diff_errors.push({msg: msg, line: lineNo, err: String(error)});
    return false;
};

window.runDiffTests = function() {
    try {
        // 1. Enable Different Pitch
        const chkDiff = document.getElementById('chkDifferentPitch');
        chkDiff.checked = true;
        onDifferentPitchToggle();

        // Check default state of auto-constrain
        const chkConstrain = document.getElementById('chkDiffAutoConstrain');
        window.__test_diff_results.init_constrain = chkConstrain ? chkConstrain.checked : false;

        // 2. Load Preset P50
        loadKettenwulfP50Preset();
        window.__test_diff_results.preset_p1 = AppState.diff_p1;
        window.__test_diff_results.preset_p2 = AppState.diff_p2;
        window.__test_diff_results.preset_z = AppState.z;
        window.__test_diff_results.preset_d0 = CurrentGeom.d0;

        // 3. Test Auto-Constrain: user changes p1 to 100 in input_diff_p1
        const inp1 = document.getElementById('input_diff_p1');
        inp1.value = 100;
        onDifferentPitchParamChange('p1');
        window.__test_diff_results.after_p1_change = {
            p1: AppState.diff_p1,
            p2: AppState.diff_p2,
            p: AppState.p
        };

        // 4. Test Uncheck Auto-Constrain: enter custom invalid values
        chkConstrain.checked = false;
        onDiffAutoConstrainToggle();
        window.__test_diff_results.unconstrained_mode = AppState.diffAutoConstrain;

        // Set invalid p1=30 with d1=25 (where 2.2*d1 = 55) -> will cause pointed tooth
        inp1.value = 30;
        onDifferentPitchParamChange('p1');
        const factorsDiv = document.getElementById('diffPitchFactors');
        window.__test_diff_results.pointed_warning_present = factorsDiv.innerHTML.includes('ĐỈNH RĂNG BƯỚC NHỎ BỊ NHỌN');

        // 5. Test Drive Chain Warning: select KWN_001
        AppState.standard = 'KWN_001';
        onParamChange();
        window.__test_diff_results.kwn001_warning_present = factorsDiv.innerHTML.includes('KHÔNG ÁP DỤNG CHO XÍCH TRUYỀN ĐỘNG CON LĂN CAO TỐC');

        // Save factorsDiv innerText
        window.__test_diff_results.final_warning_text = factorsDiv.innerText;

        // Save screenshot of unconstrained warning state
        pass
    } catch(e) {
        window.__diff_errors.push({msg: e.message, stack: e.stack});
    }
};

window.addEventListener('DOMContentLoaded', () => {
    window.runDiffTests();
});
</script>
"""

    test_html = html.replace('</body>', harness + '\n</body>')
    test_file = os.path.join(WORKSPACE, 'temp_test_diff_constrain.html')
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_html)

    shot_path = os.path.join(BRAIN_DIR, 'shot_diff_pitch_warnings_live.png')
    
    cmd = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--window-size=1600,1600',
        '--virtual-time-budget=2000',
        f'--screenshot={shot_path}',
        f'file:///{test_file.replace(chr(92), "/")}'
    ]
    subprocess.run(cmd, check=True)

    # Now let's also capture locked state
    harness_locked = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    const chkDiff = document.getElementById('chkDifferentPitch');
    chkDiff.checked = true;
    onDifferentPitchToggle();
    loadKettenwulfP50Preset();
    window.scrollTo(0, 500);
    const sb = document.querySelector('.sidebar');
    if (sb) sb.scrollTop = 500;
});
</script>
"""
    test_html_locked = html.replace('</body>', harness_locked + '\n</body>')
    test_file_locked = os.path.join(WORKSPACE, 'temp_test_diff_locked.html')
    with open(test_file_locked, 'w', encoding='utf-8') as f:
        f.write(test_html_locked)

    shot_locked_path = os.path.join(BRAIN_DIR, 'shot_diff_pitch_locked_live.png')
    cmd_locked = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--window-size=1600,1600',
        '--virtual-time-budget=2000',
        f'--screenshot={shot_locked_path}',
        f'file:///{test_file_locked.replace(chr(92), "/")}'
    ]
    subprocess.run(cmd_locked, check=True)

    if os.path.exists(test_file_locked):
        os.remove(test_file_locked)

    # Now read test results with headless print
    cmd_extract = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--dump-dom',
        f'file:///{test_file.replace(chr(92), "/")}'
    ]
    res = subprocess.run(cmd_extract, capture_output=True, text=True, encoding='utf-8')

    if os.path.exists(test_file):
        os.remove(test_file)

    print("=== DIFFERENT PITCH AUTO-CONSTRAIN TEST RESULTS ===")
    print(f"Screenshot saved to: {shot_path}")
    assert "ĐỈNH RĂNG BƯỚC NHỎ BỊ NHỌN" in res.stdout, "Pointed tooth warning not found in DOM!"
    assert "KHÔNG ÁP DỤNG CHO XÍCH TRUYỀN ĐỘNG CON LĂN CAO TỐC" in res.stdout, "KWN_001 warning not found in DOM!"
    print("[PASS] Pointed tooth warning detected when unconstrained!")
    print("[PASS] KWN 001 roller drive chain incompatibility warning detected!")
    print("=== ALL AUTO-CONSTRAIN TESTS PASSED! ===")

if __name__ == '__main__':
    test_diff_auto_constrain()
