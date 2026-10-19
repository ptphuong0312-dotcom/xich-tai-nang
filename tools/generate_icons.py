import subprocess
import os
import struct
import pymupdf

def create_ico(png_paths, ico_path):
    """Packs standard PNGs into a multi-resolution .ico file."""
    images = []
    for p in png_paths:
        with open(p, 'rb') as f:
            data = f.read()
        doc = pymupdf.open(p)
        page = doc[0]
        # read dimensions
        w = int(page.rect.width)
        h = int(page.rect.height)
        images.append({'width': w, 'height': h, 'data': data})
    
    count = len(images)
    header = struct.pack('<HHH', 0, 1, count)
    
    offset = 6 + count * 16
    dir_entries = []
    image_data_block = bytearray()
    
    for img in images:
        w_byte = img['width'] if img['width'] < 256 else 0
        h_byte = img['height'] if img['height'] < 256 else 0
        size = len(img['data'])
        entry = struct.pack('<BBBBHHII', w_byte, h_byte, 0, 0, 1, 32, size, offset)
        dir_entries.append(entry)
        image_data_block.extend(img['data'])
        offset += size
        
    with open(ico_path, 'wb') as f:
        f.write(header)
        for entry in dir_entries:
            f.write(entry)
        f.write(image_data_block)
    print(f"Generated {ico_path} with {count} resolutions ({[i['width'] for i in images]}).")

def generate_icons():
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if not os.path.exists(chrome):
        chrome = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    
    with open('apple-touch-icon.svg', 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # SVG 1: Regular icon with rounded dark background
    svg_any = svg_content.replace('width="180" height="180"', 'width="100%" height="100%" style="display:block;"')
    
    # SVG 2: Maskable icon (square background, no rounded corners)
    svg_maskable = svg_any.replace('rx="22"', 'rx="0"').replace('rx="21"', 'rx="0"')

    html_template = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; width: 100vw; height: 100vh; overflow: hidden; background: transparent; }
  svg { width: 100vw; height: 100vh; display: block; }
</style>
</head>
<body>
__SVG_CONTENT__
</body>
</html>"""

    html_any_path = os.path.abspath('temp_icon_any.html')
    with open(html_any_path, 'w', encoding='utf-8') as f:
        f.write(html_template.replace('__SVG_CONTENT__', svg_any))

    html_maskable_path = os.path.abspath('temp_icon_maskable.html')
    with open(html_maskable_path, 'w', encoding='utf-8') as f:
        f.write(html_template.replace('__SVG_CONTENT__', svg_maskable))

    # 1. Render master high-res 512x512 images via Chrome
    master_renders = [
        (html_any_path, 'icon-512.png', 512, 512),
        (html_maskable_path, 'icon-maskable-512.png', 512, 512),
    ]

    for html_file, out_name, w, h in master_renders:
        out_abs = os.path.abspath(out_name)
        in_url = 'file:///' + html_file.replace('\\', '/')
        cmd = [
            chrome,
            '--headless=new',
            '--disable-gpu',
            f'--window-size={w},{h}',
            '--default-background-color=00000000',
            f'--screenshot={out_abs}',
            in_url
        ]
        subprocess.run(cmd, check=True)
        print(f"Rendered master {out_name} ({w}x{h}) via Chrome")

    # Clean up temp html
    if os.path.exists(html_any_path): os.remove(html_any_path)
    if os.path.exists(html_maskable_path): os.remove(html_maskable_path)

    # 2. Resample from master 512 into all required sizes using PyMuPDF high quality scaling
    doc_any = pymupdf.open('icon-512.png')
    page_any = doc_any[0]
    base_w = page_any.rect.width

    any_targets = [
        ('icon-192.png', 192),
        ('apple-touch-icon.png', 180),
        ('apple-touch-icon-180x180.png', 180),
        ('apple-touch-icon-152x152.png', 152),
        ('apple-touch-icon-120x120.png', 120),
        ('favicon-32x32.png', 32),
        ('favicon-16x16.png', 16),
    ]

    for out_name, target_size in any_targets:
        scale = target_size / base_w
        pix = page_any.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
        pix.save(out_name)
        print(f"Resized {out_name}: {pix.width}x{pix.height} ({os.path.getsize(out_name)} bytes)")

    # 3. Resample maskable 192
    doc_mask = pymupdf.open('icon-maskable-512.png')
    page_mask = doc_mask[0]
    scale_mask = 192.0 / page_mask.rect.width
    pix_mask = page_mask.get_pixmap(matrix=pymupdf.Matrix(scale_mask, scale_mask))
    pix_mask.save('icon-maskable-192.png')
    print(f"Resized icon-maskable-192.png: {pix_mask.width}x{pix_mask.height}")

    # 4. Generate favicon.ico
    create_ico(['favicon-16x16.png', 'favicon-32x32.png'], 'favicon.ico')
    print("All mobile icons and favicons generated successfully!")

if __name__ == '__main__':
    generate_icons()
