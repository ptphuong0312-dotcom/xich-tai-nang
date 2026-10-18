import subprocess
import os
import sys
import time

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
BRAIN_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'

sys.stdout.reconfigure(encoding='utf-8')

def run_test(scenario_name, setup_js, screenshot_filename):
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    harness_js = f"""
<script>
window.runTestScenario = async function() {{
    try {{
        {setup_js}
    }} catch (e) {{
        console.error(e);
    }}
    document.title = 'TESTS_DONE';
}};

window.addEventListener('DOMContentLoaded', () => {{
    setTimeout(window.runTestScenario, 1200);
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
        '--virtual-time-budget=4000',
        '--window-size=1600,1000',
        f'--screenshot={screenshot_path}',
        f'file:///{harness_path.replace("\\\\", "/")}'
    ]

    print(f"Running Chrome test for {scenario_name}...")
    subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

    if os.path.exists(harness_path):
        os.remove(harness_path)

    print(f"Screenshot saved to: {screenshot_path}, exists: {os.path.exists(screenshot_path)}")
    return screenshot_path

if __name__ == '__main__':
    # Test 1: Gap view macro
    run_test(
        "gap_d3_check",
        """
        AppState.standard = 'KWN_017';
        AppState.chainType = 'without_roller';
        AppState.p = 400;
        AppState.d1 = 50;
        AppState.z = 8;
        onParamChange();
        setMode('gap');
        """,
        "shot_gap_d3_elevated.png"
    )

    # Test 2: Different pitch full view
    run_test(
        "diff_pitch_check",
        """
        setMode('full');
        loadKettenwulfP50Preset();
        fitView();
        AppState.zoom = 2.0;
        AppState.panX = 200;
        AppState.panY = 50;
        updateTransform();
        """,
        "shot_diff_pitch_zoomed.png"
    )
