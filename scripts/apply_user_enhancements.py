import re

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'

def apply_fixes():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Dark theme default
    html = html.replace(
        "bgTheme: 'light', // 'light' (xám hơi sáng kỹ thuật - mặc định) | 'dark' (nền tối gốc)",
        "bgTheme: 'dark', // 'dark' (nền tối CAD Studio - mặc định) | 'light' (xám hơi sáng)"
    )
    html = html.replace(
        '<button class="btn-theme-opt active" id="btnThemeLight" onclick="setCanvasBg(\'light\')">\n              <span>☀️</span> Nền xám sáng\n            </button>\n            <button class="btn-theme-opt" id="btnThemeDark" onclick="setCanvasBg(\'dark\')">',
        '<button class="btn-theme-opt" id="btnThemeLight" onclick="setCanvasBg(\'light\')">\n              <span>☀️</span> Nền xám sáng\n            </button>\n            <button class="btn-theme-opt active" id="btnThemeDark" onclick="setCanvasBg(\'dark\')">'
    )
    html = html.replace(
        '<div class="canvas-container theme-light" id="canvasBox">',
        '<div class="canvas-container theme-dark" id="canvasBox">'
    )
    print("1. Set default theme to dark")

    # 2. Fix autoLookupDIN6885 to stop overwriting hub_NL
    old_din = """      const Md_str = document.getElementById('res_load_Md')?.innerText || '20000';
      const Md = parseFloat(Md_str) || 20000;
      const l_req = (2.0 * Md * 1000.0) / (dw * row.t2 * 90.0);
      const NL_rec = Math.max(Math.ceil((1.2 * l_req + row.b) / 5) * 5, Math.ceil((1.2 * dw) / 5) * 5);
      AppState.hub_NL = NL_rec;
      document.getElementById('input_hub_NL').value = NL_rec;"""
    if old_din in html:
        html = html.replace(old_din, "      // Không tự ý đè hub_NL - để autoApplyStandardHubDimensions hoặc người dùng tự thiết kế")
        print("2. Fixed autoLookupDIN6885: removed destructive NL overwrite")
    else:
        print("WARN: old_din not found!")

    # 3. Add autoApplyStandardHubDimensions and user edit detection
    auto_hub_fn = """
    // HÀM TỰ ĐỘNG THIẾT KẾ MAY-Ơ THEO CHUẨN CÔNG NGHIỆP SCANCHAIN & KETTENWULF
    function autoApplyStandardHubDimensions(force = false) {
      if (AppState.isUserCustomHub && !force) return;

      const hub = lookupScanChainHub();
      if (hub && hub.Dn > 0) {
        // Áp dụng chuẩn ScanChain (DIN 8165 FV & DIN 8167 M)
        AppState.hub_Dn = hub.Dn;
        AppState.hub_NL = hub.Ln1;
        AppState.b1 = parseFloat((hub.Z1 / 0.9).toFixed(1));
        const inpNL = document.getElementById('input_hub_NL');
        const inpB1 = document.getElementById('input_b1');
        if (inpNL) inpNL.value = hub.Ln1;
        if (inpB1) inpB1.value = AppState.b1;
      } else {
        // Áp dụng tỉ lệ cơ khí chuẩn KettenWulf (Catalog Trang 56)
        const dw = AppState.dw || 80.0;
        const ds_val = CurrentGeom && CurrentGeom.ds ? CurrentGeom.ds : (AppState.p * 2.0);
        const Dn_std = Math.min(ds_val - 15.0, Math.max(dw + 30.0, Math.round(dw * 1.55)));
        const NL_std = Math.max(Math.round(AppState.b1 * 1.5), Math.round(dw * 1.35));
        AppState.hub_Dn = Dn_std;
        AppState.hub_NL = NL_std;
        const inpNL = document.getElementById('input_hub_NL');
        if (inpNL) inpNL.value = NL_std;
      }
      updateScanChainHubUI();
    }

    function onUserHubNLEdit() {
      const inp = document.getElementById('input_hub_NL');
      if (inp) {
        AppState.hub_NL = parseFloat(inp.value) || 100.0;
        AppState.isUserCustomHub = true;
        const badge = document.getElementById('sc_hub_badge');
        if (badge) {
          badge.innerText = '⚙ Tuỳ chỉnh riêng';
          badge.style.background = 'rgba(56, 189, 248, 0.2)';
          badge.style.color = '#38bdf8';
        }
        onParamChange();
        recalculateShaft();
      }
    }

    function resetStandardHub() {
      AppState.isUserCustomHub = false;
      autoApplyStandardHubDimensions(true);
      onParamChange();
      recalculateShaft();
    }
"""
    # Insert right before recalculateShaft
    html = html.replace("function recalculateShaft() {", auto_hub_fn + "\n    function recalculateShaft() {")
    print("3. Added autoApplyStandardHubDimensions & onUserHubNLEdit")

    # 4. Hook autoApplyStandardHubDimensions into onChainModelChange & applyPreset
    html = html.replace("applyModelParams(model);\n    }", "applyModelParams(model);\n      autoApplyStandardHubDimensions();\n    }")
    print("4. Hooked autoApplyStandardHubDimensions into model change")

    # 5. Add user edit event and Reset button in HTML
    html = html.replace(
        '<input type="number" id="input_hub_NL" value="180" oninput="onParamChange()" onchange="onParamChange()">',
        '<input type="number" id="input_hub_NL" value="180" oninput="onUserHubNLEdit()" onchange="onUserHubNLEdit()">'
    )
    # Add Reset button to scanchain_hub_card
    html = html.replace(
        '<button type="button" class="btn btn-secondary" onclick="applyScanChainHubParams()" style="margin-top: 7px; width: 100%; font-size: 11px; padding: 5px; border-color: #10b981; color: #10b981; font-weight: 600;">\n              ✔ Áp Dụng Thông Số May-ơ Chuẩn ScanChain\n            </button>',
        '<div style="display: flex; gap: 6px; margin-top: 7px;">\n              <button type="button" class="btn btn-primary" onclick="resetStandardHub()" style="flex: 1; font-size: 10.5px; padding: 4px; background: #10b981; border-color: #10b981;">✔ Thiết Kế Theo Chuẩn</button>\n              <span style="font-size: 9.5px; color: var(--text-muted); align-self: center;">(hoặc gõ số sửa riêng)</span>\n            </div>'
    )
    print("5. Added reset button and onUserHubNLEdit hook in HTML")

    # 6. Fix renderSectionView viewBox to properly fit any hub length
    old_sec_box = """      const right_extent = x_base + colStep * (isKWN001 ? 3.0 : 4.0) + textSz * 18.0;
      const vX = -w_rim2 - textSz * 6.0;
      const vW = right_extent - vX;
      const top_y = -Ra - textSz * 5.0;
      const bot_y = y_break + textSz * 4.0;
      const rawH = bot_y - top_y;
      const vH = Math.max(rawH, vW * 0.60);
      const vY = top_y - (vH - rawH) * 0.5;"""

    new_sec_box = """      const right_extent = x_base + colStep * (isKWN001 ? 3.0 : 4.0) + textSz * 18.0;
      const min_X = Math.min(xh_L, -w_rim2) - textSz * 5.0;
      const max_X = Math.max(xh_R + textSz * 3.0, right_extent);
      const vX = min_X;
      const vW = max_X - min_X;
      const top_y = -Ra - textSz * 5.5;
      const bot_y = y_break + textSz * 4.0;
      const rawH = bot_y - top_y;
      const vH = Math.max(rawH, vW * 0.55);
      const vY = top_y - (vH - rawH) * 0.5;"""
    if old_sec_box in html:
        html = html.replace(old_sec_box, new_sec_box)
        print("6. Fixed renderSectionView viewBox to perfectly bound any hub length")
    else:
        print("WARN: old_sec_box not found!")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("ALL FIXES APPLIED SUCCESSFULLY!")

if __name__ == '__main__':
    apply_fixes()
