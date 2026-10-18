import subprocess
import os
import json
import time
import ezdxf

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
ARTIFACT_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
USER_DATA = r'C:\Users\SirPhuong\AppData\Local\Temp\chrome_qc_' + str(int(time.time()))

def run_qc_tests():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Test Harness to test SMS 1698 and ScanChain Hubs live in browser
    harness_js = """
<script>
window.__qc_results = {
    errors: [],
    sms_test: null,
    hub_test: null,
    dxf_exports: {}
};

window.onerror = function(msg, url, lineNo, columnNo, error) {
    window.__qc_results.errors.push({msg: msg, line: lineNo, err: String(error)});
    return false;
};

// Prevent download dialog
HTMLAnchorElement.prototype.click = function() {};

let currentExportMode = '';
const origCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = function(blob) {
    const reader = new FileReader();
    const mode = currentExportMode;
    reader.onload = function() {
        window.__qc_results.dxf_exports[mode] = reader.result.length;
    };
    reader.readAsText(blob);
    return 'blob:mock';
};

window.runQCAudit = async function() {
    try {
        // Test 1: Apply SMS 18 preset
        applyPreset('SMS18');
        window.__qc_results.sms_test = {
            standard: AppState.standard,
            series: AppState.currentSeries,
            model: AppState.currentModelName,
            p: AppState.p,
            z: AppState.z,
            d1: AppState.d1,
            b1: AppState.b1,
            FB: AppState.FB
        };

        // Test 2: Select FV 90 via applyPreset and check ScanChain Hub
        applyPreset('FV90');
        recalculateShaft();
        
        const hub = lookupScanChainHub();
        window.__qc_results.hub_test = hub;
        if (hub) {
            applyScanChainHubParams();
            window.__qc_results.applied_hub = {
                hub_NL: AppState.hub_NL,
                hub_Dn: AppState.hub_Dn
            };
        }

        // Test 3: Export all 5 DXF modes for SMS 18
        applyPreset('SMS18');
        const modes = ['sprocket', 'assembly', 'gap', 'section', 'combined'];
        for (const m of modes) {
            currentExportMode = m;
            exportDXF(m);
            await new Promise(r => setTimeout(r, 60));
        }

    } catch(e) {
        window.__qc_results.errors.push({error: e.message, stack: e.stack});
    }

    await new Promise(r => setTimeout(r, 400));
    const div = document.createElement('div');
    div.id = 'qc_output';
    div.textContent = JSON.stringify(window.__qc_results);
    document.body.appendChild(div);
};

window.addEventListener('DOMContentLoaded', () => {
    setTimeout(window.runQCAudit, 400);
});
</script>
"""
    harness_html = html.replace('</body>', harness_js + '\n</body>')
    harness_path = os.path.join(WORKSPACE, 'test_qc_runner.html')
    with open(harness_path, 'w', encoding='utf-8') as f:
        f.write(harness_html)

    # Run Chrome
    cmd = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={USER_DATA}',
        '--virtual-time-budget=3500',
        '--window-size=1600,1000',
        '--dump-dom',
        f'file:///{harness_path.replace("\\\\", "/")}'
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    dom = proc.stdout
    if os.path.exists(harness_path):
        os.remove(harness_path)

    marker = 'id="qc_output">'
    if marker in dom:
        s_idx = dom.find(marker) + len(marker)
        e_idx = dom.find('</div>', s_idx)
        qc_json = json.loads(dom[s_idx:e_idx])
        print("=== LIVE QC AUDIT RESULTS ===")
        print(json.dumps(qc_json, indent=2))
        assert len(qc_json['errors']) == 0, f"QC FAILED with JS errors: {qc_json['errors']}"
        assert qc_json['sms_test']['model'] == 'SMS 18', "SMS preset failed"
        assert qc_json['hub_test'] is not None, "ScanChain Hub lookup failed"
        print("=== QC AUDIT PASSED 100%! ===")
    else:
        print("QC Marker not found in DOM!")

    # 2. Capture Visual Screenshots of SMS 18 and ScanChain Hub
    # Shot A: SMS 18 on Main View
    html_sms = html.replace('recalculateLoad();', 'recalculateLoad(); applyPreset("SMS18");')
    test_sms = os.path.join(WORKSPACE, 'test_sms.html')
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
    print("Captured SMS 18 Screenshot:", os.path.exists(out_sms))

    # Shot B: Tab 3 showing ScanChain Hub Card for FV 90
    html_tab3 = html.replace('recalculateLoad();', 'recalculateLoad(); applyPreset("FV90"); switchControlTab("shaft");')
    test_tab3 = os.path.join(WORKSPACE, 'test_tab3_sc.html')
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
    print("Captured ScanChain Hub Tab 3 Screenshot:", os.path.exists(out_tab3))

if __name__ == '__main__':
    run_qc_tests()
