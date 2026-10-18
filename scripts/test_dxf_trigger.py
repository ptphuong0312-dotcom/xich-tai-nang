import subprocess
import os
import time

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
WORKSPACE = r'd:\Google Antigravity\Xich tai nang'

with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# Add a trigger to download DXF section
trigger = '''
<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        applyPreset('FV90');
        exportDXF('section');
    }, 500);
});
</script>
'''
test_dxf_html = html.replace('</body>', trigger + '</body>')
test_path = os.path.join(WORKSPACE, 'test_export_dxf.html')
with open(test_path, 'w', encoding='utf-8') as f:
    f.write(test_dxf_html)

user_data = r'C:\Users\SirPhuong\AppData\Local\Temp\chrome_dxf_' + str(int(time.time()))
subprocess.run([
    CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
    f'--user-data-dir={user_data}',
    '--virtual-time-budget=2000',
    f'file:///{test_path.replace("\\\\", "/")}'
], capture_output=True)

if os.path.exists(test_path):
    os.remove(test_path)

print("DXF export triggered successfully!")
