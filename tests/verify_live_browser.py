import subprocess
import os
import json
import time
import ezdxf

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'
CHROME_EXE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def test_live_browser():
    with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    harness_js = """
<script>
window.__dxf_results = {};
window.__js_errors = [];

window.onerror = function(msg, url, lineNo, columnNo, error) {
    window.__js_errors.push({msg: msg, line: lineNo, err: String(error)});
    return false;
};

// Prevent download popup in headless Chrome
HTMLAnchorElement.prototype.click = function() {
    console.log('Mock click download:', this.download);
};

let currentTestMode = '';
const origCreateObjectURL = URL.createObjectURL;
URL.createObjectURL = function(blob) {
    // Read blob text synchronously or via promise
    const reader = new FileReader();
    const mode = currentTestMode;
    reader.onload = function() {
        window.__dxf_results[mode] = {
            length: reader.result.length,
            content: reader.result
        };
    };
    reader.readAsText(blob);
    return 'blob:mock';
};

window.runDXFTests = async function() {
    const modes = ['sprocket', 'assembly', 'gap', 'section', 'combined'];
    for (const m of modes) {
        currentTestMode = m;
        try {
            exportDXF(m);
        } catch(e) {
            window.__js_errors.push({mode: m, error: e.message, stack: e.stack});
        }
        await new Promise(r => setTimeout(r, 100));
    }
    await new Promise(r => setTimeout(r, 500));
    
    const statusDiv = document.createElement('div');
    statusDiv.id = 'dxf_test_status';
    statusDiv.textContent = JSON.stringify({
        errors: window.__js_errors,
        results: Object.keys(window.__dxf_results).reduce((acc, k) => {
            acc[k] = window.__dxf_results[k].length;
            return acc;
        }, {})
    });
    document.body.appendChild(statusDiv);

    // Write contents
    for (const [k, v] of Object.entries(window.__dxf_results)) {
        const sc = document.createElement('script');
        sc.type = 'text/plain';
        sc.id = 'dxf_data_' + k;
        sc.textContent = v.content;
        document.body.appendChild(sc);
    }
    document.title = 'TESTS_DONE';
};

window.addEventListener('DOMContentLoaded', () => {
    setTimeout(window.runDXFTests, 500);
});
</script>
"""
    harness_html = html.replace('</body>', harness_js + '\n</body>')
    harness_path = os.path.join(WORKSPACE, 'test_dxf_live.html')
    with open(harness_path, 'w', encoding='utf-8') as f:
        f.write(harness_html)

    temp_profile = os.path.join(os.environ['TEMP'], f'chrome_profile_{int(time.time())}')
    screenshot_path = os.path.join(WORKSPACE, 'shot_live_test.png')
    
    cmd = [
        CHROME_EXE,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--user-data-dir={temp_profile}',
        '--virtual-time-budget=4000',
        '--window-size=1920,1080',
        f'--screenshot={screenshot_path}',
        '--dump-dom',
        f'file:///{harness_path.replace("\\\\", "/")}'
    ]
    
    print("Executing Chrome headless...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    dom = proc.stdout
    
    if os.path.exists(harness_path):
        os.remove(harness_path)
        
    print(f"Captured DOM size: {len(dom)} characters.")
    
    marker = 'id="dxf_test_status">'
    if marker in dom:
        s_idx = dom.find(marker) + len(marker)
        e_idx = dom.find('</div>', s_idx)
        status = json.loads(dom[s_idx:e_idx])
        print("TEST STATUS FROM BROWSER:")
        print(json.dumps(status, indent=2))
        
        # Now extract each DXF file and test with ezdxf
        modes = ['sprocket', 'assembly', 'gap', 'section', 'combined']
        for m in modes:
            d_marker = f'id="dxf_data_{m}">'
            if d_marker in dom:
                d_start = dom.find(d_marker) + len(d_marker)
                d_end = dom.find('</script>', d_start)
                dxf_str = dom[d_start:d_end]
                # Fix unescaping if needed
                dxf_str = dxf_str.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
                out_dxf = os.path.join(WORKSPACE, f'verified_{m}.dxf')
                with open(out_dxf, 'w', encoding='utf-8') as f:
                    f.write(dxf_str)
                
                try:
                    doc = ezdxf.readfile(out_dxf)
                    msp = doc.modelspace()
                    entities = list(msp)
                    layers = [l.dxf.name for l in doc.layers]
                    print(f"[{m.upper()}] SUCCESS: {len(entities)} entities, {len(layers)} layers: {layers}")
                except Exception as ex:
                    print(f"[{m.upper()}] EZDXF Error: {ex}")
            else:
                print(f"[{m.upper()}] Data marker not found in DOM!")
    else:
        print("Status marker not found! DOM dump head:")
        print(dom[:500])

if __name__ == '__main__':
    test_live_browser()
