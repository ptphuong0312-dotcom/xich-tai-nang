import json
import re

WORKSPACE = r'd:\Google Antigravity\Xich tai nang'

def run_integration():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Load data
    with open('data/sms_1698_standard.json', 'r', encoding='utf-8') as f:
        sms_data = json.load(f)

    with open('data/scanchain_sprocket_hubs.json', 'r', encoding='utf-8') as f:
        hub_data = json.load(f)

    # 1. Update CHAIN_CATALOGS: insert SMS1698 before the closing bracket of CHAIN_CATALOGS
    sms_json_str = ',\n  "SMS1698": ' + json.dumps(sms_data, indent=2)
    # Target right before LANTERN ends
    target_catalog_end = '\n};\n\n    const KETTENWULF_CATALOG = {'
    if target_catalog_end in html:
        html = html.replace(target_catalog_end, sms_json_str + target_catalog_end)
        print("1. Added SMS1698 to CHAIN_CATALOGS")
    else:
        print("ERROR: target_catalog_end not found!")
        return

    # 2. Add SCANCHAIN_HUBS constant after KETTENWULF_CATALOG
    hub_js_str = '\n    // BẢNG TRA KÍCH THƯỚC MAY-Ơ TIÊU CHUẨN CÔNG NGHIỆP SCANCHAIN (PAGES 16-19)\n    const SCANCHAIN_HUBS = ' + json.dumps(hub_data) + ';\n'
    target_kw_cat_end = '      KWN_016: {\n        LANTERN: CHAIN_CATALOGS.LANTERN,\n        MT: CHAIN_CATALOGS.MT,\n        M: CHAIN_CATALOGS.M\n      }\n    };'
    if target_kw_cat_end in html:
        # Also add SMS1698 to KWN_017 and KWN_015
        replacement_kw_cat = target_kw_cat_end.replace(
            'MC: CHAIN_CATALOGS.MC\n      },',
            'MC: CHAIN_CATALOGS.MC,\n        SMS1698: CHAIN_CATALOGS.SMS1698\n      },'
        )
        html = html.replace(target_kw_cat_end, replacement_kw_cat + '\n' + hub_js_str)
        print("2. Added SCANCHAIN_HUBS and updated KETTENWULF_CATALOG")
    else:
        print("ERROR: target_kw_cat_end not found!")
        return

    # 3. Update seriesLabels to include SMS1698
    target_labels = "'MC': 'Dòng MC / FVC – ISO 1977 & DIN 8168/8165 Xích chốt rỗng (Hollow pin)',"
    replacement_labels = target_labels + "\n        'SMS1698': 'Dòng SMS – Tiêu chuẩn Bắc Âu SMS 1698 (ScanChain / Thụy Điển)',"
    if target_labels in html:
        html = html.replace(target_labels, replacement_labels)
        print("3. Added SMS1698 label")
    else:
        print("ERROR: target_labels not found!")
        return

    # 4. Update onStandardChange to include SMS1698
    target_std_check = "!['MT', 'FV', 'M', 'FVT', 'MC'].includes(AppState.currentSeries)"
    replacement_std_check = "!['MT', 'FV', 'M', 'FVT', 'MC', 'SMS1698'].includes(AppState.currentSeries)"
    html = html.replace(target_std_check, replacement_std_check)
    print("4. Updated onStandardChange series check")

    # 5. Add Quick Preset button in HTML
    target_badges = """<button type="button" class="quick-badge-btn" onclick="applyPreset('KWN016')">KWN 016 (Lồng đèn)</button>"""
    replacement_badges = target_badges + """\n            <button type="button" class="quick-badge-btn" onclick="applyPreset('SMS18')" style="border-color: #10b981; color: #10b981;">SMS 18 (Bắc Âu)</button>"""
    if target_badges in html:
        html = html.replace(target_badges, replacement_badges)
        print("5. Added SMS 18 quick preset button in HTML")
    else:
        print("ERROR: target_badges not found!")
        return

    # 6. Add preset 'SMS18' in applyPreset()
    target_preset = """      } else if (presetName === 'KWN016') {
        AppState.standard = 'KWN_016';
        AppState.currentSeries = 'LANTERN';
        AppState.currentModelName = 'KWN016-p100 (m=31.83)';
        AppState.p = 100;
        AppState.z = 12;
      }"""
    replacement_preset = target_preset + """ else if (presetName === 'SMS18') {
        AppState.standard = 'KWN_017';
        AppState.currentSeries = 'SMS1698';
        AppState.currentModelName = 'SMS 18';
        AppState.p = 150;
        AppState.z = 10;
      }"""
    if target_preset in html:
        html = html.replace(target_preset, replacement_preset)
        print("6. Added SMS18 preset in JS")
    else:
        print("ERROR: target_preset not found!")
        return

    # 7. Add ScanChain Hub card in Tab 3 (Trục & May-ơ)
    target_tab3_card = """          <!-- BẢNG KIỂM NGHIỆM ĐỘ BỀN THEN & CHIỀU DÀI MAY-Ơ THEO KETTENWULF TRANG 54 -->"""
    scanchain_hub_html = """          <!-- BẢNG TRA MAY-Ơ CÔNG NGHIỆP SCANCHAIN (PAGES 16-19) -->
          <div id="scanchain_hub_card" style="background: rgba(16, 185, 129, 0.08); padding: 10px; border-radius: 8px; border: 1px solid #10b981; margin-top: 8px; display: none;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
              <span style="font-size: 11px; font-weight: 700; color: #10b981;">★ CHUẨN MAY-Ơ SCANCHAIN (Trang 16–19):</span>
              <span id="sc_hub_badge" style="font-size: 9.5px; padding: 2px 6px; background: rgba(16, 185, 129, 0.2); border-radius: 4px; color: #10b981; font-weight: 600;">DIN 8165/8167</span>
            </div>
            <div style="font-size: 10.5px; color: var(--text-main); line-height: 1.55;">
              <div>• ĐK May-ơ ngoài (Dn): <b id="sc_hub_dn" style="color: #38bdf8;">--</b> mm</div>
              <div>• Chiều dài May-ơ (Ln1 / Ln2): <b id="sc_hub_ln" style="color: #38bdf8;">-- / --</b> mm</div>
              <div>• Bề dày vành Z1: <b id="sc_hub_z1" style="color: #38bdf8;">--</b> mm | Bề rộng đỉnh Z2: <b id="sc_hub_z2" style="color: #38bdf8;">--</b> mm</div>
              <div>• Lỗ mồi gia công trước (Pb): <b id="sc_hub_pb" style="color: #38bdf8;">--</b> mm</div>
            </div>
            <button type="button" class="btn btn-secondary" onclick="applyScanChainHubParams()" style="margin-top: 7px; width: 100%; font-size: 11px; padding: 5px; border-color: #10b981; color: #10b981; font-weight: 600;">
              ✔ Áp Dụng Thông Số May-ơ Chuẩn ScanChain
            </button>
          </div>

          <!-- BẢNG KIỂM NGHIỆM ĐỘ BỀN THEN & CHIỀU DÀI MAY-Ơ THEO KETTENWULF TRANG 54 -->"""
    if target_tab3_card in html:
        html = html.replace(target_tab3_card, scanchain_hub_html)
        print("7. Added ScanChain Hub card in Tab 3 HTML")
    else:
        print("ERROR: target_tab3_card not found!")
        return

    # 8. Add AppState.hub_Dn and ScanChain lookup logic in JS
    hub_lookup_js = """
    // HÀM TRA CỨU MAY-Ơ CÔNG NGHIỆP SCANCHAIN
    function lookupScanChainHub() {
      const ser = AppState.currentSeries;
      const model = AppState.currentModelName || '';
      const p = Math.round(AppState.p);
      const z = String(Math.round(AppState.z));

      let fam = null;
      let code = null;

      if (ser === 'FV' || ser === 'FVT') {
        fam = 'FV';
        code = model.replace(/[^A-Za-z0-9]/g, '');
      } else if (ser === 'M' || ser === 'MT') {
        fam = 'M';
        code = model.replace('MT', 'M').replace(/[^A-Za-z0-9]/g, '');
      }

      if (!fam || !SCANCHAIN_HUBS[fam] || !SCANCHAIN_HUBS[fam][code]) return null;
      const pKey = 'p' + p;
      if (!SCANCHAIN_HUBS[fam][code][pKey]) return null;
      const match = SCANCHAIN_HUBS[fam][code][pKey][z];
      return match ? { ...match, fam, code } : null;
    }

    function updateScanChainHubUI() {
      const card = document.getElementById('scanchain_hub_card');
      if (!card) return;
      const hub = lookupScanChainHub();
      if (!hub || hub.Dn <= 0) {
        card.style.display = 'none';
        return;
      }
      card.style.display = 'block';
      document.getElementById('sc_hub_dn').innerText = hub.Dn;
      document.getElementById('sc_hub_ln').innerText = `${hub.Ln1} / ${hub.Ln2}`;
      document.getElementById('sc_hub_z1').innerText = hub.Z1;
      document.getElementById('sc_hub_z2').innerText = hub.Z2;
      document.getElementById('sc_hub_pb').innerText = hub.Pb;
      document.getElementById('sc_hub_badge').innerText = `${hub.code} (z=${AppState.z}, p=${AppState.p})`;
    }

    function applyScanChainHubParams() {
      const hub = lookupScanChainHub();
      if (!hub) return;
      if (hub.Ln1 > 0) {
        AppState.hub_NL = hub.Ln1;
        const inp = document.getElementById('input_hub_NL');
        if (inp) inp.value = hub.Ln1;
      }
      if (hub.Dn > 0) {
        AppState.hub_Dn = hub.Dn;
      }
      if (hub.Z1 > 0) {
        AppState.b1 = roundTo1(hub.Z1 / 0.9);
      }
      onParamChange();
      recalculateShaft();
      alert(`Đã áp dụng thông số May-ơ chuẩn ScanChain:\\n- Đường kính may-ơ Dn = ${hub.Dn} mm\\n- Chiều dài may-ơ NL = ${hub.Ln1} mm\\n- Vành đĩa Z1 = ${hub.Z1} mm`);
    }
"""
    # Insert right before recalculateShaft
    target_shaft_fn = "function recalculateShaft() {"
    if target_shaft_fn in html:
        html = html.replace(target_shaft_fn, hub_lookup_js + "\n    " + target_shaft_fn)
        print("8. Added ScanChain Hub lookup JS functions")
    else:
        print("ERROR: target_shaft_fn not found!")
        return

    # 9. Update recalculateShaft to call updateScanChainHubUI()
    target_recalc_call = "function recalculateShaft() {"
    replacement_recalc_call = "function recalculateShaft() {\n      updateScanChainHubUI();"
    html = html.replace(target_recalc_call, replacement_recalc_call, 1)
    print("9. Hooked updateScanChainHubUI into recalculateShaft")

    # 10. Update onParamChange to also call updateScanChainHubUI()
    target_param_change = "function onParamChange() {"
    replacement_param_change = "function onParamChange() {\n      updateScanChainHubUI();"
    html = html.replace(target_param_change, replacement_param_change, 1)
    print("10. Hooked updateScanChainHubUI into onParamChange")

    # 11. Update renderSectionView and writeSection to use AppState.hub_Dn
    target_dh_svg = "const dH = Math.max(dw + 35.0, Math.min(ds - 20.0, dw * 1.65));"
    replacement_dh_svg = "const dH = AppState.hub_Dn || Math.max(dw + 35.0, Math.min(ds - 20.0, dw * 1.65));"
    html = html.replace(target_dh_svg, replacement_dh_svg)
    print("11. Updated dH in SVG Section view and DXF to use AppState.hub_Dn")

    # 12. Also dimension Dn on the Section SVG if dH exists
    target_sec_dims = "<!-- Kích thước đường kính đỉnh da -->"
    dn_svg_dim = """<!-- Kích thước đường kính may-ơ Dn -->
        <g stroke="#10b981" stroke-width="0.5" vector-effect="non-scaling-stroke">
          <line x1="${xh_R}" y1="${-RH}" x2="${xh_R + 30}" y2="${-RH}" stroke-dasharray="3,2"/>
          <line x1="${xh_R + 25}" y1="0" x2="${xh_R + 25}" y2="${-RH}"/>
        </g>
        <text x="${xh_R + 32}" y="${-RH / 2}" fill="#10b981" font-size="${textSz * 0.9}" font-weight="700" alignment-baseline="middle">
          Ø Dn = ${dH.toFixed(1)} mm
        </text>

        <!-- Kích thước đường kính đỉnh da -->"""
    if target_sec_dims in html:
        html = html.replace(target_sec_dims, dn_svg_dim)
        print("12. Added Ø Dn dimension on Section View SVG")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("=== INTEGRATION COMPLETED SUCCESSFULLY! ===")

if __name__ == '__main__':
    run_integration()
