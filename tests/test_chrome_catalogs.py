import subprocess
import os
import sys
import time
import json

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
BRAIN_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'

sys.stdout.reconfigure(encoding='utf-8')

def test_chrome_catalogs():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    harness_js = """
<script>
window.__test_results = {};
window.__js_errors = [];

window.onerror = function(msg, url, lineNo, columnNo, error) {
    window.__js_errors.push({msg: msg, line: lineNo, err: String(error)});
    return false;
};

window.runCatalogTests = async function() {
    try {
        // 1. Verify all series in dropdown
        const selSeries = document.getElementById('selChainSeries');
        const series = Array.from(selSeries.options).map(o => o.value);
        window.__test_results.series = series;

        // 2. Select DIN8175
        selSeries.value = 'DIN8175';
        AppState.currentSeries = 'DIN8175';
        populateModelDropdown();
        
        const selModel = document.getElementById('selChainModel');
        const din8175_models = Array.from(selModel.options).map(o => o.value);
        window.__test_results.din8175_models = din8175_models;

        // Select F 800
        selModel.value = 'F 800';
        AppState.currentModelName = 'F 800';
        populatePitchDropdown();
        renderCAD();
        
        window.__test_results.f800_state = {
            FB: AppState.FB,
            p: AppState.p,
            d1: AppState.d1,
            b1: AppState.b1,
            s: AppState.s
        };

        // 3. Select FVC
        selSeries.value = 'FVC';
        AppState.currentSeries = 'FVC';
        populateModelDropdown();
        const fvc_models = Array.from(selModel.options).map(o => o.value);
        window.__test_results.fvc_models = fvc_models;

        // Select FVC 900
        selModel.value = 'FVC 900';
        AppState.currentModelName = 'FVC 900';
        populatePitchDropdown();
        renderCAD();

        window.__test_results.fvc900_state = {
            FB: AppState.FB,
            p: AppState.p,
            d1: AppState.d1,
            d8: AppState.d8,
            b1: AppState.b1
        };

        // 4. Select MC
        selSeries.value = 'MC';
        AppState.currentSeries = 'MC';
        populateModelDropdown();
        const mc_models = Array.from(selModel.options).map(o => o.value);
        window.__test_results.mc_models = mc_models;

        // Back to DIN8175 F 800 for screenshot
        selSeries.value = 'DIN8175';
        AppState.currentSeries = 'DIN8175';
        populateModelDropdown();
        selModel.value = 'F 800';
        AppState.currentModelName = 'F 800';
        populatePitchDropdown();
        renderCAD();

    } catch (e) {
        window.__js_errors.push({error: e.message, stack: e.stack});
    }

    const resDiv = document.createElement('div');
    resDiv.id = 'catalog_test_results';
    resDiv.textContent = JSON.stringify({
        errors: window.__js_errors,
        results: window.__test_results
    });
    document.body.appendChild(resDiv);
    document.title = 'TESTS_DONE';
};

window.addEventListener('DOMContentLoaded', () => {
    setTimeout(window.runCatalogTests, 400);
});
</script>
"""

    harness_html = html.replace('</body>', harness_js + '\n</body>')
    harness_path = os.path.join(WORKSPACE, 'test_catalog_live.html')
    with open(harness_path, 'w', encoding='utf-8') as f:
        f.write(harness_html)

    temp_profile = os.path.join(os.environ['TEMP'], f'chrome_profile_{int(time.time())}')
    screenshot_path = os.path.join(BRAIN_DIR, 'shot_din8175_f800_live.png')

    cmd = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={temp_profile}',
        '--virtual-time-budget=3000',
        '--window-size=1920,1080',
        f'--screenshot={screenshot_path}',
        '--dump-dom',
        f'file:///{harness_path.replace("\\\\", "/")}'
    ]

    print("Running Chrome headless test...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    dom = proc.stdout

    if os.path.exists(harness_path):
        os.remove(harness_path)

    import re
    match = re.search(r'<div id="catalog_test_results">(.*?)</div>', dom)
    if not match:
        print("ERROR: Did not find catalog_test_results in DOM!")
        print("DOM tail:", dom[-500:])
        return False

    data = json.loads(match.group(1))
    print("\n--- Browser Test Output ---")
    print("JS Errors:", data['errors'])
    results = data['results']
    print("Available Series in Browser:", results.get('series'))
    print("DIN 8175 Models in Browser:", results.get('din8175_models'))
    print("FVC Models in Browser:", results.get('fvc_models'))
    print("MC Models in Browser:", results.get('mc_models'))
    print("F 800 State:", results.get('f800_state'))
    print("FVC 900 State:", results.get('fvc900_state'))
    print("Screenshot saved to:", screenshot_path)

    assert len(data['errors']) == 0, f"JS Errors detected: {data['errors']}"
    assert 'DIN8175' in results.get('series'), "DIN8175 must be in series!"
    assert 'FVC' in results.get('series'), "FVC must be in series!"
    assert 'MC' in results.get('series'), "MC must be in series!"
    assert 'F 800' in results.get('din8175_models'), "F 800 must be in DIN 8175 models!"
    assert 'FVC 900' in results.get('fvc_models'), "FVC 900 must be in FVC models!"
    print("\n>>> ALL IN-BROWSER CATALOG VERIFICATIONS PASSED WITH ZERO ERRORS! <<<")
    return True

if __name__ == '__main__':
    test_chrome_catalogs()
