"""
Standard Backup Tool for KettenWulf Sprocket Studio
Creates a dual-format backup inside the `backup/` directory:
1. `index_backup_YYYYMMDD[_HHMM].html`: Direct standalone HTML file for instant viewing.
2. `backup_xich_tai_nang_YYYYMMDD[_HHMM].zip`: Full project ZIP archive containing:
   - index.html
   - icons (favicon.svg, apple-touch-icon.*, sprocket_logo.svg)
   - data/ (all JSON databases)
   - docs/ (all documentation and analyses)
   - assets/ (catalog crops, screenshots, logo)
   - tests/ (all test scripts, outputs, harnesses)
   - scripts/ (all python build & helper scripts)
   - tools/ & .agents/
   - configs (.gitignore, vercel.json, README.md)
   Excludes: backup/, .git/, __pycache__/, Tai Lieu/ (>50MB PDFs), *.pyc
"""

import os
import sys
import shutil
import zipfile
from datetime import datetime

def create_backup():
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    backup_dir = os.path.join(workspace, 'backup')
    os.makedirs(backup_dir, exist_ok=True)

    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    time_str = now.strftime('%H%M')

    # Determine base filename: use YYYYMMDD, add _HHMM if file already exists today
    html_backup_name = f"index_backup_{date_str}.html"
    html_backup_path = os.path.join(backup_dir, html_backup_name)
    if os.path.exists(html_backup_path):
        html_backup_name = f"index_backup_{date_str}_{time_str}.html"
        html_backup_path = os.path.join(backup_dir, html_backup_name)

    zip_backup_name = f"backup_xich_tai_nang_{date_str}.zip"
    zip_backup_path = os.path.join(backup_dir, zip_backup_name)
    if os.path.exists(zip_backup_path):
        zip_backup_name = f"backup_xich_tai_nang_{date_str}_{time_str}.zip"
        zip_backup_path = os.path.join(backup_dir, zip_backup_name)

    # 1. Standalone HTML backup
    source_index = os.path.join(workspace, 'index.html')
    if not os.path.exists(source_index):
        print(f"ERROR: Cannot find {source_index}")
        sys.exit(1)

    shutil.copy2(source_index, html_backup_path)
    html_size = os.path.getsize(html_backup_path)
    print(f"[OK] Standalone HTML Backup created: {html_backup_name} ({html_size:,} bytes)")

    # 2. Comprehensive ZIP backup
    exclude_dirs = {'.git', '__pycache__', 'backup', 'Tai Lieu'}
    exclude_exts = {'.pyc'}

    count = 0
    with zipfile.ZipFile(zip_backup_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for root, dirs, files in os.walk(workspace):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in exclude_exts:
                    continue
                file_path = os.path.join(root, f)
                rel_path = os.path.relpath(file_path, workspace)
                parts = rel_path.replace('\\', '/').split('/')
                if parts[0] in exclude_dirs:
                    continue
                zf.write(file_path, rel_path)
                count += 1

    zip_size = os.path.getsize(zip_backup_path)
    print(f"[OK] Full Project ZIP Archive created: {zip_backup_name} ({count} files, {zip_size:,} bytes)")
    print(f"\nAll backups successfully saved to: {backup_dir}")

if __name__ == '__main__':
    create_backup()
