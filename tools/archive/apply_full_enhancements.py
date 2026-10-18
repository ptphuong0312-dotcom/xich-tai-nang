import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. Update UI Header: Dropdown for DXF export options + styles
# -----------------------------------------------------------------------------
old_btn_pattern = r'<button class="btn btn-primary" onclick="exportDXF\(\)">[\s\S]*?Xuất Bản Vẽ DXF \(AutoCAD\)[\s\S]*?</button>'

new_btn_html = """<div class="dxf-dropdown-wrap" style="position:relative; display:inline-block;">
        <button class="btn btn-primary" onclick="toggleDxfMenu(event)" id="btnDxfDropdown" style="display:flex; align-items:center; gap:6px;">
          <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
          Xuất Bản Vẽ DXF (AutoCAD)
          <span style="font-size:10px; margin-left:2px;">▼</span>
        </button>
        <div id="dxfMenu" class="dxf-menu-dropdown" style="display:none; position:absolute; right:0; top:calc(100% + 6px); background:#1e293b; border:1px solid #475569; border-radius:8px; box-shadow:0 12px 28px rgba(0,0,0,0.4); z-index:9999; min-width:330px; padding:6px 0;">
          <div style="padding:6px 14px 4px; font-size:11px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:0.5px;">Tùy chọn xuất bản vẽ DXF:</div>
          <button class="dxf-menu-item" onclick="exportDXF('assembly')">
            <span class="dxf-item-title">1. Đĩa xích + Dải xích ăn khớp</span>
            <span class="dxf-item-desc">Mô hình 2D đĩa xích kết hợp má xích & con lăn</span>
          </button>
          <button class="dxf-menu-item" onclick="exportDXF('gap')">
            <span class="dxf-item-title">2. Chi tiết hốc răng (Phân màu lớp CAD)</span>
            <span class="dxf-item-desc">Macro hốc răng với các layer màu riêng biệt (u, r1, h3, r2)</span>
          </button>
          <button class="dxf-menu-item" onclick="exportDXF('section')">
            <span class="dxf-item-title">3. Mặt cắt ngang thân răng</span>
            <span class="dxf-item-desc">Mặt cắt kỹ thuật có gạch mặt cắt (Hatch) và kích thước</span>
          </button>
          <div style="height:1px; background:#334155; margin:4px 0;"></div>
          <button class="dxf-menu-item highlight" onclick="exportDXF('combined')">
            <span class="dxf-item-title" style="color:#38bdf8; font-weight:700;">⭐ 4. Xuất TỔNG HỢP 3 hình chiếu + Khung tên</span>
            <span class="dxf-item-desc">Bản vẽ tổng hợp chuẩn Model Space kèm khung tên kỹ thuật</span>
          </button>
        </div>
      </div>"""

html = re.sub(old_btn_pattern, new_btn_html, html, count=1)
print("Updated DXF dropdown in header.")

# Add CSS for dxf-menu-item if not present
if '.dxf-menu-item' not in html:
    css_to_add = """
    .dxf-menu-item {
      display: flex;
      flex-direction: column;
      width: 100%;
      text-align: left;
      padding: 8px 14px;
      background: transparent;
      border: none;
      cursor: pointer;
      transition: background 0.15s ease;
      color: #f1f5f9;
    }
    .dxf-menu-item:hover {
      background: #334155;
    }
    .dxf-menu-item.highlight:hover {
      background: #0f2b48;
    }
    .dxf-item-title {
      font-size: 13px;
      font-weight: 600;
    }
    .dxf-item-desc {
      font-size: 11px;
      color: #94a3b8;
      margin-top: 2px;
    }
    """
    html = html.replace('</style>', css_to_add + '\n</style>')
    print("Added CSS for DXF menu.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved Step 1.")
