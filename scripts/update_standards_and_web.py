"""
Antigravity CAD Studio - Teamwork Implementation Script
Roles:
- Chuyên gia 1 (Dữ liệu & Tiêu chuẩn Xích KettenWulf)
- Chuyên gia 2 (Lập trình CAD & Web Engine)
- Chuyên gia 3 (Kiểm định & QA/QC)

Integrates:
1. Toothing standards: KWN 017, KWN 015, KWN 001, KWN 016
2. Chain series: MT, FV, M, FVT, MC (Hollow pin), DIN 8187, ANSI, LANTERN (Total 87 models)
3. Sprocket Hub Types: Type A (Plate wheel), Type B (One-sided), Type C (Symmetrical)
4. SVG rendering with hollow pin hole d8 & DXF export for all 5 modes
"""

import json
import re

def update_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    with open('data/chain_catalogs.json', 'r', encoding='utf-8') as f:
        chain_catalogs = json.load(f)

    # 1. Update selStandard in HTML
    old_sel_std = '''          <select id="selStandard" onchange="onStandardChange()" style="font-weight: 600; color: #38bdf8;">
            <option value="KWN_017" selected>KWN 017 – Xích tải cào tiêu chuẩn (ISO 1977 / DIN 8167 / DIN 8165)</option>
            <option value="KWN_015">KWN 015 – Hốc răng sâu chống dồn kẹt (Khai triển góc sườn γ)</option>
            <option value="KWN_001">KWN 001 – Đĩa xích con lăn truyền động tiêu chuẩn (DIN 8187 / ISO 606)</option>
          </select>'''

    new_sel_std = '''          <select id="selStandard" onchange="onStandardChange()" style="font-weight: 600; color: #38bdf8;">
            <option value="KWN_017" selected>KWN 017 – Xích tải cào tiêu chuẩn (ISO 1977 / DIN 8167 / DIN 8165)</option>
            <option value="KWN_015">KWN 015 – Hốc răng sâu chống dồn kẹt (Khai triển góc sườn γ)</option>
            <option value="KWN_001">KWN 001 – Đĩa xích con lăn truyền động tiêu chuẩn (DIN 8187 & ANSI B29.1)</option>
            <option value="KWN_016">KWN 016 – Đĩa chốt lồng đèn (Lantern Pinion - Modun m = p/π)</option>
          </select>'''

    assert old_sel_std in html, "Could not find old_sel_std"
    html = html.replace(old_sel_std, new_sel_std)

    # 2. Update Quick Presets
    old_presets = '''            <button type="button" class="quick-badge-btn" onclick="applyPreset('MT630')">MT 630 (p=400)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('MT900')">MT 900 (p=400)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('FV90')">FV 90 (p=100)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('FV140')">FV 140 (p=160)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('16B-1')">16B-1 (Con lăn)</button>'''

    new_presets = '''            <button type="button" class="quick-badge-btn" onclick="applyPreset('MT630')">MT 630 (p=400)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('FV90')">FV 90 (p=100)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('MC112')">MC 112 (Chốt rỗng)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('16B-1')">16B-1 (DIN 8187)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('ANSI80')">80-1 (ANSI)</button>
            <button type="button" class="quick-badge-btn" onclick="applyPreset('KWN016')">KWN 016 (Lồng đèn)</button>'''

    assert old_presets in html, "Could not find old_presets"
    html = html.replace(old_presets, new_presets)

    # 3. Add Hub Type selector in Tab 3 (Trục & May-ơ)
    old_tab_shaft_start = '''        <div id="controlTabShaft" style="display: none;">
          <div class="form-group">
            <div class="form-label"><span>Vật liệu trục</span></div>'''

    new_tab_shaft_start = '''        <div id="controlTabShaft" style="display: none;">
          <div class="form-group" style="margin-bottom: 7px;">
            <div class="form-label">
              <span>Kết cấu May-ơ (Sprocket Hub Type - Catalog Trang 56)</span>
            </div>
            <select id="selHubType" onchange="onHubTypeChange()" style="font-weight: 600; color: #10b981;">
              <option value="Type_C" selected>Type C – May-ơ đối xứng 2 phía (Symmetrical hub)</option>
              <option value="Type_B">Type B – May-ơ 1 phía (One-sided hub)</option>
              <option value="Type_A">Type A – Đĩa xích phẳng (Plate wheel / Không may-ơ)</option>
            </select>
          </div>
          <div class="form-group">
            <div class="form-label"><span>Vật liệu trục</span></div>'''

    assert old_tab_shaft_start in html, "Could not find old_tab_shaft_start"
    html = html.replace(old_tab_shaft_start, new_tab_shaft_start)

    # 4. Replace KETTENWULF_CATALOG definition
    cat_json_str = json.dumps(chain_catalogs, indent=2, ensure_ascii=False)
    new_catalog_code = f'''    const CHAIN_CATALOGS = {cat_json_str};

    const KETTENWULF_CATALOG = {{
      KWN_017: {{
        MT: CHAIN_CATALOGS.MT,
        FV: CHAIN_CATALOGS.FV,
        M: CHAIN_CATALOGS.M,
        FVT: CHAIN_CATALOGS.FVT,
        MC: CHAIN_CATALOGS.MC
      }},
      KWN_015: {{
        MT: CHAIN_CATALOGS.MT,
        FV: CHAIN_CATALOGS.FV,
        M: CHAIN_CATALOGS.M,
        FVT: CHAIN_CATALOGS.FVT,
        MC: CHAIN_CATALOGS.MC
      }},
      KWN_001: {{
        DIN8187: CHAIN_CATALOGS.DIN8187,
        ANSI: CHAIN_CATALOGS.ANSI
      }},
      KWN_016: {{
        LANTERN: CHAIN_CATALOGS.LANTERN,
        MT: CHAIN_CATALOGS.MT,
        M: CHAIN_CATALOGS.M
      }}
    }};'''

    cat_pattern = re.compile(r'    const KETTENWULF_CATALOG = \{.*?\n\};\n', re.DOTALL)
    assert cat_pattern.search(html), "Could not find KETTENWULF_CATALOG regex"
    html = cat_pattern.sub(new_catalog_code + '\n', html)

    # 5. Update AppState
    old_app_state_chunk = '''      key_t2: 11.0,
      hub_NL: 180.0,'''

    new_app_state_chunk = '''      key_t2: 11.0,
      hub_NL: 180.0,
      hubType: 'Type_C', // 'Type_C' (đối xứng) | 'Type_B' (1 phía) | 'Type_A' (đĩa phẳng)
      d8: 0.0,          // Lỗ rỗng trong chốt xích (cho dòng MC)
      m: 0.0,           // Modun răng KWN 016
      S1: 0.0,          // Khe hở đáy rãnh KWN 016'''

    assert old_app_state_chunk in html, "Could not find old_app_state_chunk"
    html = html.replace(old_app_state_chunk, new_app_state_chunk)

    # 6. Update populateSeriesDropdown
    old_series_labels = '''      const seriesLabels = {
        'MT': 'Dòng MT – ISO 1977 / DIN 8167 Má sâu cào vật liệu (Deep-link)',
        'FV': 'Dòng FV – DIN 8165 Má phẳng tiêu chuẩn (Standard flat-link)',
        'M': 'Dòng M – ISO 1977 / DIN 8167 Má phẳng (Standard flat-link)',
        'FVT': 'Dòng FVT – DIN 8165 Má sâu (Deep-link plate)',
        'DIN8187': 'Dòng DIN 8187 – Xích con lăn truyền động tiêu chuẩn ISO 606'
      };'''

    new_series_labels = '''      const seriesLabels = {
        'MT': 'Dòng MT – ISO 1977 / DIN 8167 Má sâu cào vật liệu (Deep-link)',
        'FV': 'Dòng FV – DIN 8165 Má phẳng tiêu chuẩn (Standard flat-link)',
        'M': 'Dòng M – ISO 1977 / DIN 8167 Má phẳng (Standard flat-link)',
        'FVT': 'Dòng FVT – DIN 8165 Má sâu (Deep-link plate)',
        'MC': 'Dòng MC / FVC – ISO 1977 & DIN 8168/8165 Xích chốt rỗng (Hollow pin)',
        'DIN8187': 'Dòng DIN 8187 – Xích con lăn truyền động tiêu chuẩn Châu Âu ISO 606',
        'ANSI': 'Dòng ANSI – ASME B29.1 / DIN 8188 Xích con lăn hệ Mỹ',
        'LANTERN': 'Dòng chốt lồng đèn tiêu chuẩn KettenWulf KWN 016 (Modun m=p/π)'
      };'''

    assert old_series_labels in html, "Could not find old_series_labels"
    html = html.replace(old_series_labels, new_series_labels)

    # 7. Update applyModelParams
    old_apply_model = '''      // Xác định đường kính tiếp xúc ăn khớp với hốc răng d1:
      if (AppState.currentSeries === 'DIN8187') {
        AppState.d1 = model.d1; // Con lăn DIN 8187
        AppState.pin_d1 = model.d1 * 0.6;
        AppState.roller_d5 = model.d1;
        AppState.chainType = 'with_roller';
      } else {
        // Xích tải cào / ống lót ISO 1977 & DIN 8165/8167:
        // Mặc định là xích ống lót type A (không con lăn), hốc răng ăn khớp với ống lót d3
        AppState.d1 = model.d3;
        AppState.pin_d1 = model.d1;
        AppState.roller_d5 = model.d5 || 0;
        AppState.chainType = 'without_roller';
      }'''

    new_apply_model = '''      // Xác định đường kính tiếp xúc ăn khớp với hốc răng d1 theo tiêu chuẩn:
      if (AppState.currentSeries === 'DIN8187' || AppState.currentSeries === 'ANSI') {
        AppState.d1 = model.d1; // Con lăn chuẩn DIN 8187 / ANSI
        AppState.pin_d1 = model.d1 * 0.6;
        AppState.roller_d5 = model.d1;
        AppState.chainType = 'with_roller';
        AppState.d8 = 0.0;
      } else if (AppState.currentSeries === 'MC') {
        // Xích chốt rỗng DIN 8168 / DIN 8165
        AppState.d1 = model.d3;
        AppState.pin_d1 = model.d1;
        AppState.roller_d5 = model.d5 || 0;
        AppState.chainType = 'without_roller';
        AppState.d8 = model.d8 || 0.0;
      } else if (AppState.standard === 'KWN_016') {
        // Chốt lồng đèn KWN 016
        AppState.d1 = model.d1;
        AppState.pin_d1 = model.d1;
        AppState.roller_d5 = model.d1;
        AppState.chainType = 'without_roller';
        AppState.d8 = 0.0;
        AppState.m = AppState.p / Math.PI;
        AppState.S1 = 0.04 * AppState.m;
      } else {
        // Xích tải cào / ống lót ISO 1977 & DIN 8165/8167:
        AppState.d1 = model.d3;
        AppState.pin_d1 = model.d1;
        AppState.roller_d5 = model.d5 || 0;
        AppState.chainType = 'without_roller';
        AppState.d8 = 0.0;
      }'''

    assert old_apply_model in html, "Could not find old_apply_model"
    html = html.replace(old_apply_model, new_apply_model)

    # 8. Update onStandardChange
    old_on_std_change = '''      if (AppState.standard === 'KWN_017') {
        if (badge) badge.innerText = 'KWN 017';
        if (tab1Badge) tab1Badge.innerText = 'KWN 017';
        if (tab1Desc) tab1Desc.innerText = 'Xích tải cào (ISO 1977 & DIN 8167/8165). Tự động tra góc mở rãnh β theo số răng z.';
        if (catBadge) catBadge.innerText = 'ISO 1977 / DIN 8167';
        if (AppState.currentSeries === 'DIN8187') AppState.currentSeries = 'MT';
      } else if (AppState.standard === 'KWN_015') {
        if (badge) badge.innerText = 'KWN 015';
        if (tab1Badge) tab1Badge.innerText = 'KWN 015';
        if (tab1Desc) tab1Desc.innerText = 'Hốc răng sâu chống dồn kẹt / tải nặng. Cho phép tùy chỉnh góc sườn γ.';
        if (catBadge) catBadge.innerText = 'Hốc Sâu KWN 015';
        if (AppState.currentSeries === 'DIN8187') AppState.currentSeries = 'MT';
      } else { // KWN_001
        if (badge) badge.innerText = 'KWN 001 / DIN 8187';
        if (tab1Badge) tab1Badge.innerText = 'KWN 001 / DIN 8187';
        if (tab1Desc) tab1Desc.innerText = 'Xích con lăn truyền động tiêu chuẩn châu Âu ISO 606 / DIN 8187.';
        if (catBadge) catBadge.innerText = 'DIN 8187 / ISO 606';
        AppState.currentSeries = 'DIN8187';
      }'''

    new_on_std_change = '''      if (AppState.standard === 'KWN_017') {
        if (badge) badge.innerText = 'KWN 017';
        if (tab1Badge) tab1Badge.innerText = 'KWN 017';
        if (tab1Desc) tab1Desc.innerText = 'Xích tải cào (ISO 1977 & DIN 8167/8165). Tự động tra góc mở rãnh β theo số răng z.';
        if (catBadge) catBadge.innerText = 'ISO 1977 / DIN 8167';
        if (!['MT', 'FV', 'M', 'FVT', 'MC'].includes(AppState.currentSeries)) AppState.currentSeries = 'MT';
      } else if (AppState.standard === 'KWN_015') {
        if (badge) badge.innerText = 'KWN 015';
        if (tab1Badge) tab1Badge.innerText = 'KWN 015';
        if (tab1Desc) tab1Desc.innerText = 'Hốc răng sâu chống dồn kẹt / tải nặng. Cho phép tùy chỉnh góc sườn γ.';
        if (catBadge) catBadge.innerText = 'Hốc Sâu KWN 015';
        if (!['MT', 'FV', 'M', 'FVT', 'MC'].includes(AppState.currentSeries)) AppState.currentSeries = 'MT';
      } else if (AppState.standard === 'KWN_001') {
        if (badge) badge.innerText = 'KWN 001 (ISO 606)';
        if (tab1Badge) tab1Badge.innerText = 'KWN 001 / Con lăn';
        if (tab1Desc) tab1Desc.innerText = 'Xích con lăn truyền động tiêu chuẩn DIN 8187 (Châu Âu) & ASME B29.1 (Mỹ ANSI).';
        if (catBadge) catBadge.innerText = 'DIN 8187 / ANSI B29.1';
        if (!['DIN8187', 'ANSI'].includes(AppState.currentSeries)) AppState.currentSeries = 'DIN8187';
      } else if (AppState.standard === 'KWN_016') {
        if (badge) badge.innerText = 'KWN 016 (Lồng đèn)';
        if (tab1Badge) tab1Badge.innerText = 'KWN 016 / Lồng đèn';
        if (tab1Desc) tab1Desc.innerText = 'Đĩa chốt lồng đèn (Lantern Pinion). Modun m = p/π, khe hở chân răng S1 = 0.04m, bề rộng răng B1 = 3.3m.';
        if (catBadge) catBadge.innerText = 'KWN 016 / Triebstock';
        if (!['LANTERN', 'MT', 'M'].includes(AppState.currentSeries)) AppState.currentSeries = 'LANTERN';
      }'''

    assert old_on_std_change in html, "Could not find old_on_std_change"
    html = html.replace(old_on_std_change, new_on_std_change)

    # 9. Update updateChainSpecCard
    old_spec_card_chunk = '''      const contactLabel = AppState.currentSeries === 'DIN8187' ? `Con lăn d1: ${model.d1}mm` : `Ống lót d3: ${model.d3}mm`;
      const pinLabel = `Chốt d1: ${model.d1}mm`;
      const rollerLarge = model.d5 ? `<div class="spec-item"><div class="s-lbl">Con lăn d5</div><div class="s-val">${model.d5} mm</div></div>` : '';'''

    new_spec_card_chunk = '''      let contactLabel = `Ống lót d3: ${model.d3 || model.d1}mm`;
      if (AppState.currentSeries === 'DIN8187' || AppState.currentSeries === 'ANSI') {
        contactLabel = `Con lăn d1: ${model.d1}mm`;
      } else if (AppState.standard === 'KWN_016') {
        contactLabel = `Chốt d1: ${model.d1}mm`;
      }
      const pinLabel = (model.d8 > 0) ? `Chốt d1/d8: Ø${model.d1} / Ø${model.d8}mm` : `Chốt d1: ${model.d1}mm`;
      const rollerLarge = model.d5 ? `<div class="spec-item"><div class="s-lbl">Con lăn d5</div><div class="s-val">${model.d5} mm</div></div>` : '';
      const hollowPinBadge = (model.d8 > 0) ? `<div class="spec-item"><div class="s-lbl">Lỗ chốt rỗng d8</div><div class="s-val" style="color:#10b981;font-weight:700;">Ø ${model.d8} mm</div></div>` : '';
      const modunBadge = (AppState.standard === 'KWN_016') ? `<div class="spec-item"><div class="s-lbl">Modun m = p/π</div><div class="s-val" style="color:#38bdf8;font-weight:700;">${(pitch / Math.PI).toFixed(2)} mm</div></div>` : '';'''

    assert old_spec_card_chunk in html, "Could not find old_spec_card_chunk"
    html = html.replace(old_spec_card_chunk, new_spec_card_chunk)

    # Also insert hollowPinBadge & modunBadge in spec-grid
    old_spec_grid_end = '''          ${rollerLarge}
          <div class="spec-item"><div class="s-lbl">Trục gợi ý dw</div><div class="s-val">${model.dw_rec || '--'} mm</div></div>'''

    new_spec_grid_end = '''          ${rollerLarge}
          ${hollowPinBadge}
          ${modunBadge}
          <div class="spec-item"><div class="s-lbl">Trục gợi ý dw</div><div class="s-val">${model.dw_rec || '--'} mm</div></div>'''

    assert old_spec_grid_end in html, "Could not find old_spec_grid_end"
    html = html.replace(old_spec_grid_end, new_spec_grid_end)

    # 10. Update applyPreset
    old_apply_presets_func = '''      if (presetName === 'MT630') {
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'MT';
        AppState.currentModelName = 'MT 630';
        AppState.p = 400;
        AppState.z = 8;
      } else if (presetName === 'MT900') {
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'MT';
        AppState.currentModelName = 'MT 900';
        AppState.p = 400;
        AppState.z = 8;
      } else if (presetName === 'FV90') {
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'FV';
        AppState.currentModelName = 'FV 90';
        AppState.p = 100;
        AppState.z = 12;
      } else if (presetName === 'FV140') {
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'FV';
        AppState.currentModelName = 'FV 140';
        AppState.p = 160;
        AppState.z = 10;
      } else if (presetName === '16B-1') {
        AppState.standard = 'KWN_001';
        AppState.currentSeries = 'DIN8187';
        AppState.currentModelName = '16B-1 (1")';
        AppState.p = 25.4;
        AppState.z = 19;
      }'''

    new_apply_presets_func = '''      if (presetName === 'MT630') {
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'MT';
        AppState.currentModelName = 'MT 630';
        AppState.p = 400;
        AppState.z = 8;
      } else if (presetName === 'FV90') {
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'FV';
        AppState.currentModelName = 'FV 90';
        AppState.p = 100;
        AppState.z = 12;
      } else if (presetName === 'MC112') {
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'MC';
        AppState.currentModelName = 'MC 112';
        AppState.p = 160;
        AppState.z = 10;
      } else if (presetName === '16B-1') {
        AppState.standard = 'KWN_001';
        AppState.currentSeries = 'DIN8187';
        AppState.currentModelName = '16B-1';
        AppState.p = 25.4;
        AppState.z = 19;
      } else if (presetName === 'ANSI80') {
        AppState.standard = 'KWN_001';
        AppState.currentSeries = 'ANSI';
        AppState.currentModelName = '80-1';
        AppState.p = 25.4;
        AppState.z = 19;
      } else if (presetName === 'KWN016') {
        AppState.standard = 'KWN_016';
        AppState.currentSeries = 'LANTERN';
        AppState.currentModelName = 'KWN016-p100 (m=31.83)';
        AppState.p = 100;
        AppState.z = 12;
      }'''

    assert old_apply_presets_func in html, "Could not find old_apply_presets_func"
    html = html.replace(old_apply_presets_func, new_apply_presets_func)

    # 11. Add onHubTypeChange function
    hub_func = '''    function onHubTypeChange() {
      const sel = document.getElementById('selHubType');
      if (sel) {
        AppState.hubType = sel.value;
        if (AppState.hubType === 'Type_A') {
          AppState.hub_NL = CurrentGeom ? CurrentGeom.B1 : (AppState.b1 * 0.9);
          const inp = document.getElementById('input_hub_NL');
          if (inp) inp.value = AppState.hub_NL.toFixed(1);
        }
      }
      recalculateGeom();
      renderCAD();
    }
'''
    html = html.replace('    function onParamChange() {', hub_func + '\n    function onParamChange() {')

    # 12. Update recalculateGeom for KWN 016
    old_recalc_geom_chunk = '''      const alpha_deg = 360.0 / z;
      const alpha_rad = (alpha_deg * Math.PI) / 180.0;
      const d0 = p / Math.sin(Math.PI / z);
      const df = d0 - d1;

      let da;
      if (standard === 'KWN_001') {
        // Chuẩn KettenWulf KWN 001 (Catalog Trang 46) cho xích con lăn DIN 8187:
        if (z <= 8) da = d0 + 0.50 * d1;
        else if (z <= 12) da = d0 + 0.55 * d1;
        else if (z <= 25) da = d0 + 0.65 * d1;
        else da = d0 + 0.75 * d1;
      } else {
        // Chuẩn xích tải KettenWulf KWN 017 (Trang 48) & KWN 015 (Trang 47):
        if (chainType === 'with_roller') da = d0 + 0.4 * d1;
        else if (chainType === 'with_protection_roller') da = d0 + 0.6 * d1;
        else da = d0 + 0.8 * d1;
      }

      let ds;
      if (standard === 'KWN_001') {
        ds = d0 - p; // Chuẩn KettenWulf Trang 46: ds = d0 - p
      } else {
        ds = (p / Math.tan(alpha_rad / 2.0)) - g - (2.0 * r4);
      }

      let beta_deg, gamma_deg, u, r1, h3, r2, B1, X_deg, z1_factor;

      if (standard === 'KWN_017') {
        // Chuẩn KettenWulf KWN 017 Trang 48:
        if (z <= 11) beta_deg = 74.0;
        else if (z <= 29) beta_deg = 56.0;
        else beta_deg = 38.0;
        gamma_deg = (beta_deg / 2.0) - (180.0 / z);
        u = 0.02 * p;
        r1 = 0.51 * d1;
        h3 = 0.3 * d1;
        r2 = 0.8 * p;
        B1 = 0.9 * b1;
      } else if (standard === 'KWN_015') {
        // Chuẩn KettenWulf KWN 015 Trang 47 (Góc sườn gamma tùy chỉnh theo ứng dụng):
        gamma_deg = gammaCustom;
        beta_deg = (alpha_deg / 2.0 + gamma_deg) * 2.0;
        u = 0.02 * p;
        r1 = 0.51 * d1;
        h3 = 0.3 * d1;
        r2 = 0.8 * p;
        B1 = 0.9 * b1;
      } else { 
        // Chuẩn KettenWulf KWN 001 Trang 46:
        if (z <= 6) { z1_factor = 6; X_deg = 115.0; }
        else if (z <= 12) { z1_factor = 8; X_deg = 120.0; }
        else { z1_factor = 12; X_deg = 125.0; }

        beta_deg = X_deg;
        gamma_deg = (X_deg / 2.0) - (180.0 / z);
        u = 0.0; // Đáy rãnh tròn ôm con lăn
        r1 = 0.505 * d1 + 0.069 * Math.cbrt(d1); // Trang 46
        h3 = 0.0; // KWN 001 không có đoạn thẳng h3
        r2 = 0.008 * d1 * (z1_factor * z1_factor + 180.0); // Trang 46
        B1 = 0.9 * b1; // Trang 46
      }'''

    new_recalc_geom_chunk = '''      const alpha_deg = 360.0 / z;
      const alpha_rad = (alpha_deg * Math.PI) / 180.0;

      let d0, df, da, ds, beta_deg, gamma_deg, u, r1, h3, r2, B1, X_deg, z1_factor, m_mod, S1;

      if (standard === 'KWN_016') {
        // CHUẨN KETTENWULF KWN 016 (TRANG 49 - ĐĨA CHỐT LỒNG ĐÈN):
        m_mod = p / Math.PI;
        d0 = (z * p) / Math.PI; // d0 = z * m
        r1 = 0.5 * d1;
        df = d0 - 2.0 * (0.15 * m_mod + r1);
        const hk = 0.15 * m_mod + r1; // Chiều cao đầu răng addendum
        da = d0 + 2.0 * hk;
        B1 = 3.3 * m_mod;
        S1 = 0.04 * m_mod;
        u = S1;
        h3 = 0.0;
        r2 = 0.8 * p;
        beta_deg = alpha_deg;
        gamma_deg = 0.0;
        ds = df - Math.min(25.0, 0.15 * p);
      } else if (standard === 'KWN_001') {
        // Chuẩn KettenWulf KWN 001 (Catalog Trang 46) cho xích con lăn DIN 8187 & ANSI:
        d0 = p / Math.sin(Math.PI / z);
        df = d0 - d1;
        if (z <= 8) da = d0 + 0.50 * d1;
        else if (z <= 12) da = d0 + 0.55 * d1;
        else if (z <= 25) da = d0 + 0.65 * d1;
        else da = d0 + 0.75 * d1;

        ds = d0 - p;

        if (z <= 6) { z1_factor = 6; X_deg = 115.0; }
        else if (z <= 12) { z1_factor = 8; X_deg = 120.0; }
        else { z1_factor = 12; X_deg = 125.0; }

        beta_deg = X_deg;
        gamma_deg = (X_deg / 2.0) - (180.0 / z);
        u = 0.0;
        r1 = 0.505 * d1 + 0.069 * Math.cbrt(d1);
        h3 = 0.0;
        r2 = 0.008 * d1 * (z1_factor * z1_factor + 180.0);
        B1 = 0.9 * b1;
      } else {
        // Chuẩn xích tải KettenWulf KWN 017 (Trang 48) & KWN 015 (Trang 47):
        d0 = p / Math.sin(Math.PI / z);
        df = d0 - d1;
        if (chainType === 'with_roller') da = d0 + 0.4 * d1;
        else if (chainType === 'with_protection_roller') da = d0 + 0.6 * d1;
        else da = d0 + 0.8 * d1;

        ds = (p / Math.tan(alpha_rad / 2.0)) - g - (2.0 * r4);

        if (standard === 'KWN_017') {
          if (z <= 11) beta_deg = 74.0;
          else if (z <= 29) beta_deg = 56.0;
          else beta_deg = 38.0;
          gamma_deg = (beta_deg / 2.0) - (180.0 / z);
        } else {
          gamma_deg = gammaCustom;
          beta_deg = (alpha_deg / 2.0 + gamma_deg) * 2.0;
        }
        u = 0.02 * p;
        r1 = 0.51 * d1;
        h3 = 0.3 * d1;
        r2 = 0.8 * p;
        B1 = 0.9 * b1;
      }'''

    assert old_recalc_geom_chunk in html, "Could not find old_recalc_geom_chunk"
    html = html.replace(old_recalc_geom_chunk, new_recalc_geom_chunk)

    # 13. Update renderDynamicChainStrand for hollow pin hole d8
    old_pin_layer = '''      // LỚP 4: ĐẦU TÁN CHỐT XÍCH (PIN RIVETS)
      strandHtml += '<g id="pinsLayer">';
      for (let i = 0; i < joints.length; i++) {
        const j = joints[i];
        const isOuterPin = (Math.abs(j.id) % 2 === 0);
        strandHtml += `
          <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${r_pin.toFixed(2)}" fill="${isOuterPin ? '#0284c7' : '#0369a1'}" stroke="#0f172a" stroke-width="0.5" vector-effect="non-scaling-stroke"/>
          <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${(r_pin * 0.40).toFixed(2)}" fill="#020617" stroke="none"/>
        `;
      }
      strandHtml += '</g>';'''

    new_pin_layer = '''      // LỚP 4: ĐẦU TÁN CHỐT XÍCH & LỖ CHỐT RỖNG HOLLOW PIN (PIN RIVETS / HOLLOW PIN)
      strandHtml += '<g id="pinsLayer">';
      const isHollow = (AppState.currentSeries === 'MC' && AppState.d8 > 0);
      const r_d8 = isHollow ? (AppState.d8 / 2.0) : 0;
      for (let i = 0; i < joints.length; i++) {
        const j = joints[i];
        const isOuterPin = (Math.abs(j.id) % 2 === 0);
        if (isHollow) {
          // Xích chốt rỗng MC: Vẽ thân chốt và lỗ thông qua tâm d8
          strandHtml += `
            <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${r_pin.toFixed(2)}" fill="#0284c7" stroke="#0f172a" stroke-width="0.6" vector-effect="non-scaling-stroke"/>
            <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${r_d8.toFixed(2)}" fill="${isLight ? '#f1f5f9' : '#090d16'}" stroke="${isLight ? '#0284c7' : '#38bdf8'}" stroke-width="0.8" vector-effect="non-scaling-stroke"/>
          `;
        } else {
          strandHtml += `
            <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${r_pin.toFixed(2)}" fill="${isOuterPin ? '#0284c7' : '#0369a1'}" stroke="#0f172a" stroke-width="0.5" vector-effect="non-scaling-stroke"/>
            <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${(r_pin * 0.40).toFixed(2)}" fill="#020617" stroke="none"/>
          `;
        }
      }
      strandHtml += '</g>';'''

    assert old_pin_layer in html, "Could not find old_pin_layer"
    html = html.replace(old_pin_layer, new_pin_layer)

    # 14. Update generateLinkPlateSvgPath for ANSI
    old_is_roller_line = "      const is_roller = (chainSeries === 'DIN8187' || chainSeries === 'KWN_001');"
    new_is_roller_line = "      const is_roller = (chainSeries === 'DIN8187' || chainSeries === 'ANSI' || chainSeries === 'KWN_001');"
    assert old_is_roller_line in html, "Could not find old_is_roller_line"
    html = html.replace(old_is_roller_line, new_is_roller_line)

    # 15. Update renderSectionView to display Hub Type info
    old_sec_title = "      // 1. Trục tâm đứng đối xứng (Centerline)"
    new_sec_title = """      // Hiển thị huy hiệu loại kết cấu may-ơ
      const hubTypeLabel = (AppState.hubType === 'Type_A') ? 'Type A: Đĩa phẳng (Plate wheel)' :
                           (AppState.hubType === 'Type_B') ? 'Type B: May-ơ 1 phía (One-sided)' :
                           'Type C: May-ơ 2 phía đối xứng (Symmetrical)';
      g.innerHTML += `
        <text x="0" y="${-Ra - textSz * 5.2}" fill="#10b981" font-size="${textSz * 0.9}" font-weight="700" text-anchor="middle">
          KẾT CẤU MAY-Ơ: ${hubTypeLabel} (NL = ${AppState.hub_NL.toFixed(1)} mm)
        </text>
      `;

      // 1. Trục tâm đứng đối xứng (Centerline)"""
    assert old_sec_title in html, "Could not find old_sec_title"
    html = html.replace(old_sec_title, new_sec_title)

    # 16. Update DXF export writeAssembly for hollow pin d8 and ANSI
    old_dxf_chain_loop = '''        // Ghi con lăn và chốt xích
        for (const j of joints) {
          addCircle(ox + j.x, oy - j.y, r_contact, 'CHAIN_ROLLERS');
          addCircle(ox + j.x, oy - j.y, r_pin, 'CHAIN_PINS');
        }'''

    new_dxf_chain_loop = '''        // Ghi con lăn và chốt xích (bao gồm chốt rỗng d8 cho xích MC)
        const isHollow = (ser === 'MC' && AppState.d8 > 0);
        for (const j of joints) {
          addCircle(ox + j.x, oy - j.y, r_contact, 'CHAIN_ROLLERS');
          addCircle(ox + j.x, oy - j.y, r_pin, 'CHAIN_PINS');
          if (isHollow) {
            addCircle(ox + j.x, oy - j.y, AppState.d8 / 2.0, 'CHAIN_PINS');
          }
        }'''

    assert old_dxf_chain_loop in html, "Could not find old_dxf_chain_loop"
    html = html.replace(old_dxf_chain_loop, new_dxf_chain_loop)

    old_dxf_is_roller = "            const is_roller = (ser === 'DIN8187' || ser === 'KWN_001');"
    new_dxf_is_roller = "            const is_roller = (ser === 'DIN8187' || ser === 'ANSI' || ser === 'KWN_001');"
    assert old_dxf_is_roller in html, "Could not find old_dxf_is_roller"
    html = html.replace(old_dxf_is_roller, new_dxf_is_roller)

    # Save upgraded index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: index.html upgraded with all standards and models!")

if __name__ == '__main__':
    update_index_html()
