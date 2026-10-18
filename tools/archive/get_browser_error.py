import subprocess
import time
import json
import asyncio
import websockets
import requests

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9334
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
            await ws.send(json.dumps({"id": 2, "method": "Log.enable"}))
            await ws.send(json.dumps({"id": 3, "method": "Page.enable"}))
            
            # Navigate to file
            await ws.send(json.dumps({
                "id": 4,
                "method": "Page.navigate",
                "params": {"url": "file:///d:/Google%20Antigravity/Xich%20tai%20nang/index.html"}
            }))
            
            start = time.time()
            while time.time() - start < 4:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    if "Runtime.exceptionThrown" in data.get("method", ""):
                        details = data["params"]["exceptionDetails"]
                        print("EXCEPTION OCCURRED:")
                        print("Message:", details.get("text"))
                        print("Exception:", details.get("exception", {}).get("description"))
                        print("Line number:", details.get("lineNumber"))
                        print("Column number:", details.get("columnNumber"))
                        if "stackTrace" in details:
                            for frame in details["stackTrace"].get("callFrames", []):
                                print(f"  at {frame.get('functionName')} ({frame.get('url')}:{frame.get('lineNumber')}:{frame.get('columnNumber')})")
                    elif "consoleAPICalled" in data.get("method", ""):
                        print("CONSOLE:", data["params"]["type"], [arg.get("value") for arg in data["params"]["args"]])
                except asyncio.TimeoutError:
                    pass
    finally:
        proc.terminate()

asyncio.run(check())
