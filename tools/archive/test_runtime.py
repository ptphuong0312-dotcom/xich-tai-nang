import subprocess
import time
import json
import asyncio
import websockets
import requests
import os
import base64
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')

temp_dir = tempfile.mkdtemp()
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9348

html_path = os.path.abspath('index.html').replace('\\', '/')
file_url = f"file:///{html_path}"

proc = subprocess.Popen([
    chrome_path,
    f"--remote-debugging-port={port}",
    "--headless=new",
    f"--user-data-dir={temp_dir}",
    "--disable-gpu",
    "--window-size=1600,1000",
    file_url
])

time.sleep(2.0)

async def run_tests():
    try:
        r = requests.get(f"http://localhost:{port}/json", timeout=5)
        tabs = r.json()
        page_tab = next(t for t in tabs if t.get("type") == "page")
        ws_url = page_tab["webSocketDebuggerUrl"]
        
        async with websockets.connect(ws_url, ping_interval=None) as ws:
            async def send_cmd(method, params=None):
                cmd_id = int(time.time() * 1000) % 1000000
                msg = {"id": cmd_id, "method": method}
                if params:
                    msg["params"] = params
                await ws.send(json.dumps(msg))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get("id") == cmd_id:
                        return resp.get("result", {})

            await send_cmd("Runtime.enable")
            await send_cmd("Page.enable")
            await asyncio.sleep(1.0)

            # 1. Switch to DIN 8187 08B-1
            switch_08b1 = """
            (() => {
                const selStd = document.getElementById('selStandard');
                selStd.value = 'KWN_001';
                onStandardChange();

                const selSer = document.getElementById('selChainSeries');
                selSer.value = 'DIN8187';
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
            })()
            """
            await send_cmd("Runtime.evaluate", {"expression": switch_08b1})

            # Full view screenshot of 08B-1
            shot = await send_cmd("Page.captureScreenshot", {"format": "png"})
            with open("screenshot_08b1_full.png", "wb") as f:
                f.write(base64.b64decode(shot["data"]))
            print("Captured screenshot_08b1_full.png")

            # Gap view screenshot of 08B-1
            await send_cmd("Runtime.evaluate", {"expression": "setMode('gap');"})
            shot = await send_cmd("Page.captureScreenshot", {"format": "png"})
            with open("screenshot_08b1_gap.png", "wb") as f:
                f.write(base64.b64decode(shot["data"]))
            print("Captured screenshot_08b1_gap.png")

            # Section view screenshot of 08B-1
            await send_cmd("Runtime.evaluate", {"expression": "setMode('section');"})
            shot = await send_cmd("Page.captureScreenshot", {"format": "png"})
            with open("screenshot_08b1_section.png", "wb") as f:
                f.write(base64.b64decode(shot["data"]))
            print("Captured screenshot_08b1_section.png")

            # 2. Switch to KWN 017 MT 630 section
            switch_mt630 = """
            (() => {
                const selStd = document.getElementById('selStandard');
                selStd.value = 'KWN_017';
                onStandardChange();

                const selSer = document.getElementById('selChainSeries');
                selSer.value = 'MT';
                onChainSeriesChange();

                const selMod = document.getElementById('selChainModel');
                for (let i = 0; i < selMod.options.length; i++) {
                    if (selMod.options[i].value.includes('MT 630')) {
                        selMod.selectedIndex = i;
                        break;
                    }
                }
                onChainModelChange();

                setMode('section');
            })()
            """
            await send_cmd("Runtime.evaluate", {"expression": switch_mt630})
            shot = await send_cmd("Page.captureScreenshot", {"format": "png"})
            with open("screenshot_kwn017_section.png", "wb") as f:
                f.write(base64.b64decode(shot["data"]))
            print("Captured screenshot_kwn017_section.png")

            # 3. Test DXF generation for all 4 modes
            dxf_eval = """
            (() => {
                const results = {};
                ['assembly', 'gap', 'section', 'combined'].forEach(mode => {
                    try {
                        exportDXF(mode);
                        results[mode] = "SUCCESS";
                    } catch(e) {
                        results[mode] = "FAILED: " + e.message;
                    }
                });
                return results;
            })()
            """
            res = await send_cmd("Runtime.evaluate", {"expression": dxf_eval, "returnByValue": True})
            print("3. DXF Export Test:", json.dumps(res.get("result", {}).get("value", {}), indent=2))

    finally:
        proc.terminate()

asyncio.run(run_tests())
