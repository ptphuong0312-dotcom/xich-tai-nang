import subprocess
import time
import json
import urllib.request

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9222
cmd = [
    chrome_path,
    f"--remote-debugging-port={port}",
    "--headless",
    "--disable-gpu",
    "file:///d:/Google%20Antigravity/Xich%20tai%20nang/index.html"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    with urllib.request.urlopen(f"http://localhost:{port}/json") as resp:
        tabs = json.loads(resp.read().decode())
    print("Tabs found:", len(tabs))
    ws_url = tabs[0].get("webSocketDebuggerUrl")
    print("WebSocket URL:", ws_url)
finally:
    proc.terminate()
