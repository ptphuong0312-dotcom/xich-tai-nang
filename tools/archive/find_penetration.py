import tempfile
import subprocess
import time
import requests
import json
import asyncio
import websockets
import os
import sys
import math

sys.stdout.reconfigure(encoding='utf-8')

temp_dir = tempfile.mkdtemp()
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9353
html_path = os.path.abspath('index.html').replace('\\', '/')

proc = subprocess.Popen([
    chrome_path,
    f"--remote-debugging-port={port}",
    "--headless=new",
    f"--user-data-dir={temp_dir}",
    "--disable-gpu",
    f"file:///{html_path}"
])
time.sleep(2.0)

async def test():
    try:
        r = requests.get(f"http://localhost:{port}/json").json()
        ws_url = [t for t in r if t['type']=='page'][0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url) as ws:
            code = """
            (() => {
                document.getElementById('selStandard').value = 'KWN_001';
                onStandardChange();
                document.getElementById('selChainSeries').value = 'DIN8187';
                onChainSeriesChange();
                const selMod = document.getElementById('selChainModel');
                for (let i = 0; i < selMod.options.length; i++) {
                    if (selMod.options[i].value.includes('08B-1')) {
                        selMod.selectedIndex = i;
                        break;
                    }
                }
                onChainModelChange();
                setMode('full');

                const contour = computeFullContour(CurrentGeom);
                const svgContour = contour.map(p => ({ x: p.x, y: -p.y }));

                // Roller 3 is at (12.70, -16.59), radius = 8.51 / 2 = 4.255
                // Check all contour points distance to (12.70, -16.59):
                const r3 = { x: 12.70, y: -16.59, r: 8.51 / 2 };
                const collisions = [];
                for (let i = 0; i < svgContour.length; i++) {
                    const pt = svgContour[i];
                    const d = Math.hypot(pt.x - r3.x, pt.y - r3.y);
                    if (d < r3.r) {
                        collisions.push({ i, pt, dist: d, penetration: r3.r - d });
                    }
                }

                // Also check roller 4 at (0.0, -16.59)
                const r4 = { x: 0.0, y: -16.59, r: 8.51 / 2 };
                const collisions4 = [];
                for (let i = 0; i < svgContour.length; i++) {
                    const pt = svgContour[i];
                    const d = Math.hypot(pt.x - r4.x, pt.y - r4.y);
                    if (d < r4.r - 0.05) { // allow 0.05mm contact
                        collisions4.push({ i, pt, dist: d, penetration: r4.r - d });
                    }
                }

                return {
                    roller3_collisions: collisions,
                    roller4_collisions: collisions4,
                    r3,
                    r4
                };
            })()
            """
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': code, 'returnByValue': True}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == 1:
                    res = msg['result']['result']['value']
                    print("Roller 3 (incoming at 12.70, -16.59) collisions:")
                    for c in res['roller3_collisions']:
                        print(f"  pt=({c['pt']['x']:.2f}, {c['pt']['y']:.2f}), dist={c['dist']:.2f}, penetration={c['penetration']:.2f} mm")
                    print("\nRoller 4 (seated at 0.0, -16.59) collisions:")
                    for c in res['roller4_collisions']:
                        print(f"  pt=({c['pt']['x']:.2f}, {c['pt']['y']:.2f}), dist={c['dist']:.2f}, penetration={c['penetration']:.2f} mm")
                    break
    finally:
        proc.terminate()

asyncio.run(test())
