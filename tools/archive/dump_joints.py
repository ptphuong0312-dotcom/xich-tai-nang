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
port = 9350
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
            # Switch to 08B-1
            switch_code = """
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

                // Return the HTML of sprocketRotated and kinematicChainStrand
                return {
                    geom: {
                        R0: CurrentGeom.R0,
                        Rf: CurrentGeom.Rf,
                        Ra: CurrentGeom.Ra,
                        d0: CurrentGeom.d0,
                        df: CurrentGeom.df,
                        da: CurrentGeom.da,
                        d1: CurrentGeom.d1,
                        p: CurrentGeom.p,
                        z: CurrentGeom.z
                    },
                    sprocketPath: document.querySelector('#sprocketRotated path')?.getAttribute('d')?.slice(0, 500),
                    joints: Array.from(document.querySelectorAll('#rollersLayer circle')).map(c => ({
                        cx: c.getAttribute('cx'),
                        cy: c.getAttribute('cy'),
                        r: c.getAttribute('r')
                    }))
                };
            })()
            """
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': switch_code, 'returnByValue': True}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == 1:
                    val = msg['result']['result']['value']
                    print("GEOM:", json.dumps(val['geom'], indent=2))
                    print("\nJOINTS:")
                    for idx, j in enumerate(val['joints']):
                        print(f"Joint {idx}: cx={j['cx']}, cy={j['cy']}, r={j['r']}")
                    break
    finally:
        proc.terminate()

asyncio.run(test())
