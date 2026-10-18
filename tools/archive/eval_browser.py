import subprocess
import time
import json
import asyncio
import websockets
import requests
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

script_match = re.search(r'<script>([\s\S]*?)</script>', text)
script_code = script_match.group(1) if script_match else ""

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9338
proc = subprocess.Popen([
    chrome_path,
    f"--remote-debugging-port={port}",
    "--headless",
    "--disable-gpu",
    "about:blank"
])

time.sleep(1.5)

async def check():
    try:
        r = requests.get(f"http://localhost:{port}/json")
        tabs = r.json()
        ws_url = tabs[0]["webSocketDebuggerUrl"]
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            res1 = await ws.recv()
            
            cmd = {
                "id": 2,
                "method": "Runtime.compileScript",
                "params": {
                    "expression": script_code,
                    "sourceURL": "index.html",
                    "persistScript": False
                }
            }
            await ws.send(json.dumps(cmd))
            
            # Loop to find response to id 2
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                if data.get("id") == 2:
                    print("COMPILE RESULT:")
                    if "exceptionDetails" in data.get("result", {}):
                        exc = data["result"]["exceptionDetails"]
                        line_no = exc.get("lineNumber", 0)
                        col_no = exc.get("columnNumber", 0)
                        print(f"SYNTAX ERROR at line {line_no+1}, col {col_no}:")
                        print(exc.get("text"))
                        print(exc.get("exception", {}).get("description"))
                        lines = script_code.split('\n')
                        start_l = max(0, line_no - 4)
                        end_l = min(len(lines), line_no + 5)
                        for i in range(start_l, end_l):
                            prefix = ">> " if i == line_no else "   "
                            print(f"{prefix}{i+1}: {lines[i]}")
                    else:
                        print("No syntax error in script! ScriptId:", data.get("result", {}).get("scriptId"))
                    break
    finally:
        proc.terminate()

asyncio.run(check())
