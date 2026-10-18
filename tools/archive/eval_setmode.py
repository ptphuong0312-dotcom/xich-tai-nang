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
port = 9349
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
            cmd = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "setMode('section')",
                    "returnByValue": True
                }
            }
            await ws.send(json.dumps(cmd))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == 1:
                    print("setMode('section') response:", json.dumps(msg, indent=2))
                    break
    finally:
        proc.terminate()

asyncio.run(test())
