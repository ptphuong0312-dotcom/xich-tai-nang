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
port = 9352
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

                return document.getElementById('cadSvg').innerHTML;
            })()
            """
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': code, 'returnByValue': True}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == 1:
                    svg_html = msg['result']['result']['value']
                    with open('rendered_svg.html', 'w', encoding='utf-8') as f:
                        f.write(svg_html)
                    print("Saved rendered_svg.html, length:", len(svg_html))
                    break
    finally:
        proc.terminate()

asyncio.run(test())
