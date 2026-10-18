import subprocess
import os
import sys
import time
import json

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
BRAIN_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'

sys.stdout.reconfigure(encoding='utf-8')

def run_test(scenario_name, setup_js, screenshot_filename):
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    harness_js = f"""
<script>
window.__test_results = {{}};
window.__js_errors = [];

window.onerror = function(msg, url, lineNo, columnNo, error) {{
    window.__js_errors.push({{msg: msg, line: lineNo, err: String(error)}});
    return false;
}};

window.runTestScenario = async function() {{
    try {{
        {setup_js}
    }} catch (e) {{
        window.__js_errors.push({{error: e.message, stack: e.stack}});
    }}

    const resDiv = document.createElement('div');
    resDiv.id = 'scenario_test_results';
    resDiv.textContent = JSON.stringify({{
        errors: window.__js_errors,
        results: window.__test_results
    }});
    document.body.appendChild(resDiv);
    document.title = 'TESTS_DONE';
}};

window.addEventListener('DOMContentLoaded', () => {{
    setTimeout(window.runTestScenario, 300);
}});
</script>
"""

    harness_html = html.replace('</body>', harness_js + '\n</body>')
    harness_path = os.path.join(WORKSPACE, f'temp_{scenario_name}.html')
    with open(harness_path, 'w', encoding='utf-8') as f:
        f.write(harness_html)

    temp_profile = os.path.join(os.environ['TEMP'], f'chrome_profile_{scenario_name}_{int(time.time())}')
    screenshot_path = os.path.join(BRAIN_DIR, screenshot_filename)

    cmd = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={temp_profile}',
        '--virtual-time-budget=2500',
        '--window-size=1920,1080',
        f'--screenshot={screenshot_path}',
        '--dump-dom',
        f'file:///{harness_path.replace("\\\\", "/")}'
    ]

    print(f"Running Chrome test for {scenario_name}...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    dom = proc.stdout

    if os.path.exists(harness_path):
        os.remove(harness_path)

    import re
    match = re.search(r'<div id="scenario_test_results">(.*?)</div>', dom)
    if not match:
        print(f"ERROR: Did not find scenario_test_results for {scenario_name}!")
        return False

    data = json.loads(match.group(1))
    print(f"Errors for {scenario_name}:", data['errors'])
    print(f"Results for {scenario_name}:", data['results'])
    print(f"Screenshot saved to: {screenshot_path}")
    assert len(data['errors']) == 0, f"Errors: {data['errors']}"
    return True

if __name__ == '__main__':
    # 1. KWN 001 ANSI 80-1 Gap View
    setup_ansi = """
        AppState.standard = 'KWN_001';
        AppState.currentSeries = 'ANSI';
        AppState.currentModelName = '80-1';
        AppState.p = 25.4;
        AppState.z = 19;
        const selStd = document.getElementById('selStandard');
        if (selStd) selStd.value = 'KWN_001';
        onStandardChange();
        const selSer = document.getElementById('selChainSeries');
        if (selSer) selSer.value = 'ANSI';
        onChainSeriesChange();
        const selM = document.getElementById('selChainModel');
        if (selM) selM.value = '80-1';
        onChainModelChange();
        setMode('gap');
        window.__test_results = {
            opacity: AppState.plateOpacity,
            X_deg: CurrentGeom.X_deg,
            r1: CurrentGeom.r1,
            r2: CurrentGeom.r2,
            d1: CurrentGeom.d1
        };
    """
    run_test('kwn001_ansi80_gap', setup_ansi, 'shot_verify_kwn001_ansi80_gap.png')

    # 2. KWN 001 DIN 8187 16B-1 Gap View
    setup_din = """
        AppState.standard = 'KWN_001';
        AppState.currentSeries = 'DIN8187';
        AppState.currentModelName = '16B-1';
        AppState.p = 25.4;
        AppState.z = 19;
        const selStd = document.getElementById('selStandard');
        if (selStd) selStd.value = 'KWN_001';
        onStandardChange();
        const selSer = document.getElementById('selChainSeries');
        if (selSer) selSer.value = 'DIN8187';
        onChainSeriesChange();
        const selM = document.getElementById('selChainModel');
        if (selM) selM.value = '16B-1';
        onChainModelChange();
        setMode('gap');
        window.__test_results = {
            opacity: AppState.plateOpacity,
            X_deg: CurrentGeom.X_deg,
            r1: CurrentGeom.r1,
            r2: CurrentGeom.r2,
            d1: CurrentGeom.d1
        };
    """
    run_test('kwn001_16b1_gap', setup_din, 'shot_verify_kwn001_16b1_gap.png')

    # 3. Different Pitch (KettenWulf P50) MT 160 with p1=90, p2=120
    setup_diff = """
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'MT';
        AppState.currentModelName = 'MT 160';
        AppState.z = 8;
        const selStd = document.getElementById('selStandard');
        if (selStd) selStd.value = 'KWN_017';
        onStandardChange();
        const selSer = document.getElementById('selChainSeries');
        if (selSer) selSer.value = 'MT';
        onChainSeriesChange();
        const selM = document.getElementById('selChainModel');
        if (selM) selM.value = 'MT 160';
        onChainModelChange();

        // Turn on Different Pitch with p1=90, p2=120
        const chk = document.getElementById('chkDifferentPitch');
        if (chk) chk.checked = true;
        onDifferentPitchToggle();
        const inp1 = document.getElementById('input_diff_p1');
        const inp2 = document.getElementById('input_diff_p2');
        if (inp1) inp1.value = 90;
        if (inp2) inp2.value = 120;
        onDifferentPitchParamChange();

        setMode('full');
        window.__test_results = {
            opacity: AppState.plateOpacity,
            isDifferentPitch: AppState.isDifferentPitch,
            p1: CurrentGeom.p1,
            p2: CurrentGeom.p2,
            d0: CurrentGeom.d0,
            theta1_deg: CurrentGeom.theta1 * 180 / Math.PI,
            theta2_deg: CurrentGeom.theta2 * 180 / Math.PI
        };
    """
    run_test('different_pitch_live', setup_diff, 'shot_verify_diff_pitch_live.png')

    # 4. Different Pitch Dynamic Rotating Mesh (animAngle = 0.35 rad)
    setup_diff_rotating = setup_diff + """
        AppState.animAngle = 0.35;
        renderCAD();
    """
    run_test('different_pitch_rotating', setup_diff_rotating, 'shot_verify_diff_pitch_rotating.png')
    print("\nALL VERIFICATION SCREENSHOTS COMPLETED SUCCESSFULLY!")
