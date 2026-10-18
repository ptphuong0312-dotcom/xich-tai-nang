import subprocess
import os
import json
import time
import shutil
import ezdxf

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
ARTIFACT_DIR = r'C:\Users\SirPhuong\.gemini\antigravity\brain\90e08704-e58c-4fcf-bc9d-3ff943cadba1'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def setup_harness():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    harness_js = """
<script>
window.__dxf_outputs = {};
window.__errors = [];

window.onerror = function(msg, url, lineNo, columnNo, error) {
    window.__errors.push({msg: msg, line: lineNo, col: columnNo, err: String(error)});
    return false;
};

// Hook URL.createObjectURL to capture DXF strings
const originalCreateObjectURL = URL.createObjectURL;
let currentMode = '';
URL.createObjectURL = function(blob) {
    const reader = new FileReader();
    reader.onload = function() {
        window.__dxf_outputs[currentMode] = reader.result;
    };
    reader.readAsText(blob);
    return originalCreateObjectURL(blob);
};

window.__runAllTests = async function() {
    const modes = ['sprocket', 'assembly', 'gap', 'section', 'combined'];
    for (const m of modes) {
        try {
            console.log('Testing mode:', m);
            await new Promise(resolve => {
                const orig = URL.createObjectURL;
                URL.createObjectURL = function(blob) {
                    const reader = new FileReader();
                    reader.onload = function() {
                        window.__dxf_outputs[m] = reader.result;
                        URL.createObjectURL = orig;
                        resolve();
                    };
                    reader.readAsText(blob);
                    return orig(blob);
                };
                exportDXF(m);
            });
        } catch (e) {
            console.error('Error in mode ' + m + ':', e);
            window.__errors.push({mode: m, error: e.message, stack: e.stack});
        }
    }
    
    // Save results to hidden elements
    const resDiv = document.createElement('div');
    resDiv.id = 'test_results';
    resDiv.textContent = JSON.stringify({
        errors: window.__errors,
        outputs: Object.keys(window.__dxf_outputs).reduce((acc, k) => {
            acc[k] = window.__dxf_outputs[k].length;
            return acc;
        }, {})
    });
    document.body.appendChild(resDiv);

    for (const [k, v] of Object.entries(window.__dxf_outputs)) {
        const sc = document.createElement('script');
        sc.type = 'text/plain';
        sc.id = 'dxf_' + k;
        sc.textContent = v;
        document.body.appendChild(sc);
    }
    
    document.title = 'TESTS_FINISHED';
};

window.addEventListener('DOMContentLoaded', () => {
    setTimeout(window.__runAllTests, 1500);
});
</script>
"""
    modified_html = html.replace('</body>', harness_js + '\n</body>')
    harness_path = os.path.join(WORKSPACE, 'test_harness.html')
    with open(harness_path, 'w', encoding='utf-8') as f:
        f.write(modified_html)
    return harness_path

def run_tests():
    harness_path = setup_harness()
    out_png = os.path.join(WORKSPACE, 'shot_app_after_fixes.png')
    temp_profile = os.path.join(os.environ['TEMP'], 'chrome_test_profile_' + str(int(time.time())))
    
    # Run Chrome headless and dump DOM
    cmd = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--virtual-time-budget=8000',
        f'--user-data-dir={temp_profile}',
        '--window-size=1920,1080',
        f'--screenshot={out_png}',
        '--dump-dom',
        f'file:///{harness_path.replace("\\\\", "/")}'
    ]
    
    print("Launching Chrome headless to run live JavaScript test harness...")
    # Wait a bit by letting page execute
    time.sleep(1)
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    
    dom_output = proc.stdout
    print(f"Captured screenshot to: {out_png}")
    
    # Extract test_results from DOM
    if 'id="test_results">' in dom_output:
        start_idx = dom_output.find('id="test_results">') + len('id="test_results">')
        end_idx = dom_output.find('</div>', start_idx)
        json_str = dom_output[start_idx:end_idx]
        try:
            results = json.loads(json_str)
            print("LIVE BROWSER TEST RESULTS:")
            print(json.dumps(results, indent=2))
            
            # Check for errors
            if results.get('errors'):
                print("FAILED! Browser reported errors:")
                for err in results['errors']:
                    print("  ", err)
            else:
                print("SUCCESS: 0 JavaScript errors during export of all 5 DXF modes!")
                
            # Extract each DXF file and validate with ezdxf
            dxf_modes = ['sprocket', 'assembly', 'gap', 'section', 'combined']
            for m in dxf_modes:
                marker = f'id="dxf_{m}">'
                if marker in dom_output:
                    m_start = dom_output.find(marker) + len(marker)
                    m_end = dom_output.find('</script>', m_start)
                    dxf_content = dom_output[m_start:m_end]
                    # Unescape html entities
                    dxf_content = dxf_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
                    dxf_filename = os.path.join(WORKSPACE, f'live_export_{m}.dxf')
                    with open(dxf_filename, 'w', encoding='utf-8') as df:
                        df.write(dxf_content)
                    
                    # Validate with ezdxf
                    try:
                        doc = ezdxf.readfile(dxf_filename)
                        msp = doc.modelspace()
                        entities = list(msp)
                        layers = list(doc.layers)
                        print(f"[{m.upper()}] Parsed OK! File size: {len(dxf_content)} bytes, {len(entities)} entities, {len(layers)} layers.")
                    except Exception as e:
                        print(f"[{m.upper()}] EZDXF Parse ERROR: {e}")
                else:
                    print(f"[{m.upper()}] Marker {marker} not found in DOM!")

        except Exception as ex:
            print("Error parsing results JSON:", ex)
    else:
        print("Note: test_results div not found. Let's check screenshot or retry.")

    # Clean up harness file
    if os.path.exists(harness_path):
        os.remove(harness_path)
    if os.path.exists(temp_profile):
        shutil.rmtree(temp_profile, ignore_errors=True)

if __name__ == '__main__':
    run_tests()
