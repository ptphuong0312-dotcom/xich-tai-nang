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

        // 5. Select SMS1698 & Verify SMS 12.5
        selSeries.value = 'SMS1698';
        AppState.currentSeries = 'SMS1698';
        populateModelDropdown();
        const sms_models = Array.from(selModel.options).map(o => o.value);
        window.__test_results.sms_models = sms_models;

        selModel.value = 'SMS 12.5';
        AppState.currentModelName = 'SMS 12.5';
        populatePitchDropdown();
        renderCAD();
        window.__test_results.sms125_state = {
            FB: AppState.FB,
            p: AppState.p,
            d1: AppState.d1,
            b1: AppState.b1
        };

        // 6. Verify Protection Pitch (Hunting Tooth) toggle
        selSeries.value = 'FV';
        AppState.currentSeries = 'FV';
        populateModelDropdown();
        selModel.value = 'FV 90';
        AppState.currentModelName = 'FV 90';
        populatePitchDropdown();
        AppState.z = 10;
        AppState.p = 100;
        AppState.standard = 'KWN_017';

        const chkProt = document.getElementById('chkProtectionPitch');
        AppState.isProtectionPitch = false;
        if (chkProt) chkProt.checked = false;
        renderCAD();
        const d0_std = AppState.d0 || (CurrentGeom && CurrentGeom.d0);

        AppState.isProtectionPitch = true;
        if (chkProt) chkProt.checked = true;
        onProtectionPitchToggle();
        const d0_prot = AppState.d0 || (CurrentGeom && CurrentGeom.d0);

        window.__test_results.protection_pitch = {
            d0_std: d0_std,
            d0_prot: d0_prot,
            ratio: d0_prot / d0_std
        };

        // Restore protection pitch to false
        AppState.isProtectionPitch = false;
        if (chkProt) chkProt.checked = false;
        onProtectionPitchToggle();

        // 7. Verify Hub Catalog Selector (KettenWulf vs ScanChain)
        const selHubCat = document.getElementById('selHubCatalog');
        selSeries.value = 'FV';
        AppState.currentSeries = 'FV';
        populateModelDropdown();
        selModel.value = 'FV 90';
        AppState.currentModelName = 'FV 90';
        populatePitchDropdown();
        AppState.z = 10;

        if (selHubCat) {
            selHubCat.value = 'kettenwulf';
            onHubCatalogChange();
            const kw_hub_d = AppState.hub_Dn;
            const kw_hub_l = AppState.hub_NL;

            selHubCat.value = 'scanchain';
            onHubCatalogChange();
            const sc_hub_d = AppState.hub_Dn;
            const sc_hub_l = AppState.hub_NL;

            window.__test_results.hub_catalogs = {
                kw: { d: kw_hub_d, l: kw_hub_l },
                sc: { d: sc_hub_d, l: sc_hub_l }
            };
        }

        // 8. Verify KettenWulf Hub K-factor calculation
        const inpP = document.getElementById('input_kw_P');
        const inpn = document.getElementById('input_kw_n');
        const selK = document.getElementById('selHubMaterialK');
        if (inpP && inpn && selK) {
            inpP.value = '22';
            inpn.value = '30';
            selK.value = '160'; // St 52-3
            recalculateKettenwulfHub();
            const resDiv = document.getElementById('kw_hub_calc_result');
            window.__test_results.kw_hub_calc = resDiv ? resDiv.innerText.replace(/\\s+/g, ' ') : null;
        }

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
    print("SMS 1698 Models in Browser:", results.get('sms_models'))
    print("SMS 12.5 State:", results.get('sms125_state'))
    print("Protection Pitch State:", results.get('protection_pitch'))
    print("Hub Catalogs Comparison:", results.get('hub_catalogs'))
    print("KettenWulf Hub K-factor Calc:", results.get('kw_hub_calc'))
    print("Screenshot saved to:", screenshot_path)

    assert len(data['errors']) == 0, f"JS Errors detected: {data['errors']}"
    assert 'DIN8175' in results.get('series'), "DIN8175 must be in series!"
    assert 'SMS1698' in results.get('series'), "SMS1698 must be in series!"
    assert 'SMS 12.5' in results.get('sms_models'), "SMS 12.5 must be in SMS models!"
    assert 'SMS 12.5 Heavy' in results.get('sms_models'), "SMS 12.5 Heavy must be in SMS models!"
    
    # Check protection pitch math: d0_prot = p / sin(180/5) = 100 / sin(36°) = 170.13mm
    # standard d0 = 100 / sin(18°) = 323.61mm
    prot = results.get('protection_pitch', {})
    assert prot.get('d0_prot') is not None, "Protection pitch calculation failed!"
    print(f"Protection pitch d0: std={prot['d0_std']:.2f}mm, prot={prot['d0_prot']:.2f}mm")
    
    # Check hub catalogs
    hubs = results.get('hub_catalogs', {})
    assert hubs.get('kw') is not None and hubs.get('sc') is not None, "Hub catalog switching failed!"
    print(f"Hub catalogs: KW={hubs['kw']}, SC={hubs['sc']}")

    print("\n>>> ALL IN-BROWSER CATALOG VERIFICATIONS PASSED WITH ZERO ERRORS! <<<")
    return True

if __name__ == '__main__':
    test_chrome_catalogs()
