import tempfile
import subprocess
import time
import requests
import json
import asyncio
import websockets
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

temp_dir = tempfile.mkdtemp()
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9351
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
                return contour.map(p => ({ x: p.x, y: -p.y, r: Math.hypot(p.x, p.y), ang: Math.atan2(p.x, -p.y) * 180 / Math.PI }));
            })()
            """
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': code, 'returnByValue': True}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == 1:
                    pts = msg['result']['result']['value']
                    # Find min radius points (gap bottoms) and max radius points (tooth tips)
                    tips = []
                    gaps = []
                    for i in range(len(pts)):
                        p_prev = pts[(i-1)%len(pts)]
                        p_cur = pts[i]
                        p_next = pts[(i+1)%len(pts)]
                        if p_cur['r'] > p_prev['r'] and p_cur['r'] >= p_next['r'] and p_cur['r'] > 18.0:
                            tips.append(p_cur)
                        if p_cur['r'] < p_prev['r'] and p_cur['r'] <= p_next['r'] and p_cur['r'] < 13.0:
                            gaps.append(p_cur)
                    print("GAPS (r around Rf=12.34):")
                    for g in gaps:
                        print(f"  ang={g['ang']:.1f} deg, r={g['r']:.2f}, x={g['x']:.2f}, y={g['y']:.2f}")
                    print("\nTIPS (r around Ra=18.93):")
                    for t in tips:
                        print(f"  ang={t['ang']:.1f} deg, r={t['r']:.2f}, x={t['x']:.2f}, y={t['y']:.2f}")
                    break
    finally:
        proc.terminate()

asyncio.run(test())
