"""
Applies all 5 critical user feedback fixes to index.html:
1. Tooth tip crest: true circular arc (high density 0.5 deg step, steps = max(36, ceil(arc_deg * 2)))
2. Fix exportDXF('gap') ReferenceError: textH is not defined
3. Complete cross-section with Hub Types A, B, C and exact 45-deg ANSI 31 polygon hatching
4. Clear radial clearance c = 0.15*m annotation in renderGapView for KWN 016
"""

import re
import json

def apply_fixes():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # -------------------------------------------------------------
    # FIX 1: Tooth tip crest circular arc in computeFullContour
    # -------------------------------------------------------------
    old_crest_code = '''        const ang_start = gap_ang + tip_ang;
        const ang_end = gap_ang + alpha_rad - tip_ang;
        if (ang_end > ang_start + 1e-4) {
          const steps = 6;
          for (let i = 1; i < steps; i++) {
            const cur = ang_start + (ang_end - ang_start) * (i / steps);
            full_pts.push({ x: Ra * Math.sin(cur), y: Ra * Math.cos(cur) });
          }
        }'''

    new_crest_code = '''        const ang_start = gap_ang + tip_ang;
        const ang_end = gap_ang + alpha_rad - tip_ang;
        if (ang_end > ang_start + 1e-4) {
          // BẢO ĐẢM ĐỈNH RĂNG LÀ CUNG TRÒN BÁN KÍNH Ra CHUẨN XÁC TUYỆT ĐỐI (ĐỘ VÕNG CHORD < 0.005mm):
          const crest_span_deg = (ang_end - ang_start) * (180.0 / Math.PI);
          const steps = Math.max(36, Math.ceil(crest_span_deg * 2.0));
          for (let i = 1; i < steps; i++) {
            const cur = ang_start + (ang_end - ang_start) * (i / steps);
            full_pts.push({ x: Ra * Math.sin(cur), y: Ra * Math.cos(cur) });
          }
        }'''

    assert old_crest_code in html, "Could not find old_crest_code"
    html = html.replace(old_crest_code, new_crest_code)
    print("Fix 1: Tooth tip circular arc applied to computeFullContour!")

    # -------------------------------------------------------------
    # FIX 2: In writeGap inside exportDXF, increase steps for smooth tip arc
    # -------------------------------------------------------------
    old_gap_steps = '''        const span = Math.min(Math.PI * 0.48, alpha_rad * 1.55);
        const steps = 14;'''
    new_gap_steps = '''        const span = Math.min(Math.PI * 0.48, alpha_rad * 1.55);
        const steps = 36; // Cung tròn đỉnh và đáy hốc răng mịn mượt tuyệt đối'''
    assert old_gap_steps in html, "Could not find old_gap_steps"
    html = html.replace(old_gap_steps, new_gap_steps)

    # -------------------------------------------------------------
    # FIX 3: Top scope of exportDXF - define textH & S_gap to fix ReferenceError
    # -------------------------------------------------------------
    old_export_dxf_head = '''      const geom = CurrentGeom;
      const { p, z, d1, b1, R0, Rf, Ra, Rs, r4, u, r1, h3, r2, beta_deg, gamma_deg, alpha_deg, alpha_rad, d0, df, da, ds, B1, standard } = geom;'''

    new_export_dxf_head = '''      const geom = CurrentGeom;
      const { p, z, d1, b1, R0, Rf, Ra, Rs, r4, u, r1, h3, r2, beta_deg, gamma_deg, alpha_deg, alpha_rad, d0, df, da, ds, B1, standard } = geom;

      // Biến tỷ lệ kích thước chữ & mũi tên toàn cục trong exportDXF (khắc phục triệt để lỗi ReferenceError khi xuất hốc răng):
      const S_gap = Ra - Rf;
      const textH = Math.min(8.0, Math.max(3.2, p * 0.025, S_gap * 0.12));
      const arrowSz = textH * 1.1;'''

    assert old_export_dxf_head in html, "Could not find old_export_dxf_head"
    html = html.replace(old_export_dxf_head, new_export_dxf_head)
    print("Fix 2: Scope textH defined at exportDXF top level!")

    # -------------------------------------------------------------
    # FIX 4: Complete Section View & Exact 45-degree Polygon Hatching
    # -------------------------------------------------------------
    # In writeSection, replace entire function with full-height section & robust hatcher
    old_write_section_pattern = re.compile(
        r'      // HÀM 4: GHI MẶT CẮT THÂN RĂNG \(SECTION VIEW\)\s+const writeSection = \(ox = 0, oy = 0\) => \{.*?\n      \};',
        re.DOTALL
    )

    new_write_section_code = '''      // HÀM 4: GHI MẶT CẮT HOÀN THIỆN ĐẦY ĐỦ THÂN RĂNG, MAY-Ơ (TYPE A/B/C) & GẠCH MẶT CẮT ANSI 31
      const writeSection = (ox = 0, oy = 0) => {
        const isKWN001 = (standard === 'KWN_001');
        const w2 = B1 / 2.0;
        const r_sec_s = isKWN001 ? (Rf - (d0 - ds) * 0.5) : Rs;
        const w_rim2 = isKWN001 ? (w2 + 4.0) : (w2 + (r4 || 5.0) + 18.0);
        const w_tip2 = isKWN001 ? (w2 * 0.82) : (w2 * 0.72);
        const rtip = isKWN001 ? Math.min(2.5, B1 * 0.08) : Math.min(6.0, B1 * 0.10);
        const w_flat2 = w_tip2 - rtip;

        // Thông số may-ơ chuẩn Catalog KettenWulf Trang 54 & 56:
        const dw = AppState.dw || 80.0;
        const r_bore = dw / 2.0;
        const NL = AppState.hub_NL || 180.0;
        const hubType = AppState.hubType || 'Type_C';
        const dH = Math.max(dw + 35.0, Math.min(ds - 20.0, dw * 1.65));
        const RH = dH / 2.0;

        // Xác định vị trí hai mép ngoài may-ơ theo Type A, B, C:
        let xh_L, xh_R;
        if (hubType === 'Type_A') {
          // Type A: Đĩa phẳng (Plate wheel) - không may-ơ nhô ra, bề dày B1 xuyên suốt
          xh_L = -w2;
          xh_R = +w2;
        } else if (hubType === 'Type_B') {
          // Type B: May-ơ nhô 1 phía
          xh_L = -w_rim2;
          xh_R = -w_rim2 + NL;
        } else {
          // Type C: May-ơ đối xứng 2 phía (Symmetrical hub - Mặc định)
          xh_L = -NL / 2.0;
          xh_R = +NL / 2.0;
        }

        // XÂY DỰNG ĐA GIÁC KHÉP KÍN TOÀN DIỆN MẶT CẮT (SOLID SECTION POLYGON):
        const poly = [];
        if (hubType === 'Type_A') {
          poly.push({ x: ox - w2, y: oy + r_bore });
          poly.push({ x: ox - w2, y: oy + Rf });
          poly.push({ x: ox - w_tip2, y: oy + (Ra - rtip) });
          poly.push({ x: ox - w_flat2, y: oy + Ra });
          poly.push({ x: ox + w_flat2, y: oy + Ra });
          poly.push({ x: ox + w_tip2, y: oy + (Ra - rtip) });
          poly.push({ x: ox + w2, y: oy + Rf });
          poly.push({ x: ox + w2, y: oy + r_bore });
        } else {
          // Type B & Type C (Có may-ơ và vành đĩa lõm ds)
          poly.push({ x: ox + xh_L, y: oy + r_bore });
          poly.push({ x: ox + xh_L, y: oy + RH });
          poly.push({ x: ox - w_rim2, y: oy + RH });
          poly.push({ x: ox - w_rim2, y: oy + r_sec_s });
          poly.push({ x: ox - w2, y: oy + (r_sec_s + (r4 || 5.0)) });
          poly.push({ x: ox - w2, y: oy + Rf });
          poly.push({ x: ox - w_tip2, y: oy + (Ra - rtip) });
          poly.push({ x: ox - w_flat2, y: oy + Ra });
          poly.push({ x: ox + w_flat2, y: oy + Ra });
          poly.push({ x: ox + w_tip2, y: oy + (Ra - rtip) });
          poly.push({ x: ox + w2, y: oy + Rf });
          poly.push({ x: ox + w2, y: oy + (r_sec_s + (r4 || 5.0)) });
          poly.push({ x: ox + w_rim2, y: oy + r_sec_s });
          poly.push({ x: ox + w_rim2, y: oy + RH });
          poly.push({ x: ox + xh_R, y: oy + RH });
          poly.push({ x: ox + xh_R, y: oy + r_bore });
        }

        // 1. Ghi đường bao mặt cắt hoàn chỉnh (SECTION_CONTOUR)
        addPolyline(poly, 'SECTION_CONTOUR', true);

        // 2. THUẬT TOÁN GẠCH MẶT CẮT ANSI 31 (45 ĐỘ) CHUẨN XÁC TUYỆT ĐỐI CHO ĐA GIÁC BẤT KỲ:
        // Đảm bảo phủ kín 100% diện tích kim loại, đối xứng 2 bên, không hở, không lem ra ngoài
        const hatchStep = Math.max(6.0, Math.min(14.0, (Ra - r_bore) * 0.025));
        const u_vals = poly.map(pt => pt.x - pt.y);
        const u_min = Math.min(...u_vals);
        const u_max = Math.max(...u_vals);
        let c_hatch = u_min + hatchStep * 0.5;
        const N_poly = poly.length;

        while (c_hatch <= u_max) {
          const inters = [];
          for (let i = 0; i < N_poly; i++) {
            const p1 = poly[i];
            const p2 = poly[(i + 1) % N_poly];
            const u1 = p1.x - p1.y;
            const u2 = p2.x - p2.y;
            if (Math.abs(u1 - u2) < 1e-7) continue;
            if ((u1 <= c_hatch && c_hatch <= u2) || (u2 <= c_hatch && c_hatch <= u1)) {
              const t = (c_hatch - u1) / (u2 - u1);
              const ix = p1.x + t * (p2.x - p1.x);
              const iy = p1.y + t * (p2.y - p1.y);
              inters.push({ x: ix, y: iy });
            }
          }
          inters.sort((a, b) => a.x - b.x);
          const uniq = [];
          for (const pt of inters) {
            if (uniq.length === 0 || Math.abs(pt.x - uniq[uniq.length - 1].x) > 1e-3) {
              uniq.push(pt);
            }
          }
          for (let k = 0; k < uniq.length - 1; k += 2) {
            addLine(uniq[k].x, uniq[k].y, uniq[k + 1].x, uniq[k + 1].y, 'SECTION_HATCH');
          }
          c_hatch += hatchStep;
        }

        // 3. TRỤC TÂM CHỮ THẬP & ĐƯỜNG TRỤC LỖ
        // Trục đứng đối xứng bánh xích
        addLine(ox, oy + r_bore - 15, ox, oy + Ra + 25, 'CENTER_LINES');
        // Trục ngang tâm lỗ trục (y = oy)
        const L_axis_x = Math.max(NL, w_rim2 * 2) * 0.8;
        addLine(ox - L_axis_x, oy, ox + L_axis_x, oy, 'CENTER_LINES');

        // 4. KÍCH THƯỚC BỀ RỘNG VÀ CHIỀU DÀI MAY-Ơ:
        // Kích thước B1
        const dimH = Math.max(3.0, p * 0.028);
        const aSz = dimH * 1.1;
        addLine(ox - w2, oy + Ra + 12, ox + w2, oy + Ra + 12, 'SECTION_DIMS');
        addLine(ox - w2, oy + Ra, ox - w2, oy + Ra + 15, 'SECTION_DIMS');
        addLine(ox + w2, oy + Ra, ox + w2, oy + Ra + 15, 'SECTION_DIMS');
        addArrowSolid(ox - w2, oy + Ra + 12, ox - w2 + aSz, oy + Ra + 12, aSz * 0.8, 'SECTION_DIMS');
        addArrowSolid(ox + w2, oy + Ra + 12, ox + w2 - aSz, oy + Ra + 12, aSz * 0.8, 'SECTION_DIMS');
        addText(ox - dimH * 2.2, oy + Ra + 15, dimH, 'B1 = ' + B1.toFixed(1) + ' mm', 'SECTION_DIMS');

        // Kích thước Chiều dài may-ơ NL (nếu có may-ơ Type B / C)
        if (hubType !== 'Type_A') {
          const y_nl = oy + r_bore - 18;
          addLine(ox + xh_L, y_nl, ox + xh_R, y_nl, 'SECTION_DIMS');
          addLine(ox + xh_L, oy + r_bore, ox + xh_L, y_nl - 5, 'SECTION_DIMS');
          addLine(ox + xh_R, oy + r_bore, ox + xh_R, y_nl - 5, 'SECTION_DIMS');
          addArrowSolid(ox + xh_L, y_nl, ox + xh_L + aSz, y_nl, aSz * 0.8, 'SECTION_DIMS');
          addArrowSolid(ox + xh_R, y_nl, ox + xh_R - aSz, y_nl, aSz * 0.8, 'SECTION_DIMS');
          const hubLbl = (hubType === 'Type_B') ? ('NL (Type B) = ' + NL.toFixed(0) + ' mm') : ('NL (Type C) = ' + NL.toFixed(0) + ' mm');
          addText(ox - dimH * 3.5, y_nl - dimH * 1.2, dimH, hubLbl, 'SECTION_DIMS');
        }

        // 5. CÁC ĐƯỜNG DÓNG ĐƯỜNG KÍNH ĐỨNG BÊN PHẢI (da, d0, df, ds, dH, dw):
        const x_ref = ox + Math.max(xh_R, w_rim2) + 18.0;
        const addDiaRef = (diaY, diaVal, diaName, layerColor) => {
          addLine(ox, oy + diaY, x_ref + 25.0, oy + diaY, 'SECTION_REFS');
          addText(x_ref + 28.0, oy + diaY - dimH * 0.35, dimH, '%%c ' + diaName + ' = ' + diaVal.toFixed(2) + ' mm', 'SECTION_DIMS');
        };

        addDiaRef(Ra, da, 'da', 'SECTION_DIMS');
        addDiaRef(R0, d0, 'd0', 'SECTION_DIMS');
        addDiaRef(Rf, df, 'df', 'SECTION_DIMS');
        if (Rs > 0 && hubType !== 'Type_A') addDiaRef(r_sec_s, ds, 'ds', 'SECTION_DIMS');
        if (hubType !== 'Type_A') addDiaRef(RH, dH, 'dH (May-o)', 'SECTION_DIMS');
        addDiaRef(r_bore, dw, 'dw (Lo truc)', 'SECTION_DIMS');
      };'''

    assert old_write_section_pattern.search(html), "Could not find old_write_section_pattern"
    html = old_write_section_pattern.sub(new_write_section_code, html)
    print("Fix 3: Complete writeSection & 45-degree ANSI 31 polygon hatching implemented!")

    # -------------------------------------------------------------
    # FIX 5: In renderGapView, add explicit radial clearance dimension for KWN 016
    # -------------------------------------------------------------
    old_gap_sim_marker = '''        const contactLbl = (standard === 'KWN_001' || AppState.chainType === 'with_roller') ? `Ø d1 = ${d1.toFixed(2)} mm (Con lăn)` : `Ø d3 = ${d1.toFixed(2)} mm (Ống lót)`;
        g.innerHTML += cadLeaderDim(0, roller_y - roller_r, 45, S_gap * 0.16, textSz * 5.2, contactLbl, colRollerDimText, arrowSz, textSz);
      }'''

    new_gap_sim_marker = '''        const contactLbl = (standard === 'KWN_001' || AppState.chainType === 'with_roller') ? `Ø d1 = ${d1.toFixed(2)} mm (Con lăn)` : (standard === 'KWN_016' ? `Ø d1 = ${d1.toFixed(2)} mm (Chốt lồng đèn)` : `Ø d3 = ${d1.toFixed(2)} mm (Ống lót)`);
        g.innerHTML += cadLeaderDim(0, roller_y - roller_r, 45, S_gap * 0.16, textSz * 5.2, contactLbl, colRollerDimText, arrowSz, textSz);

        // ĐỐI VỚI TIÊU CHUẨN KWN 016: DÓNG RÕ KHE HỞ ĐÁY RÃNH CHỐT c = 0.15·m (TRÁNH HIỂU NHẦM LƠ LỬNG)
        if (standard === 'KWN_016') {
          const c_clearance = 0.15 * (p / Math.PI);
          const y_pin_bot = -(R0 - r1);
          const y_gap_bot = -Rf;
          const x_c = textSz * 3.5;
          g.innerHTML += `
            <!-- Đường dóng khe hở chân răng kỹ thuật KWN 016 Trang 49 -->
            <line x1="0" y1="${y_pin_bot.toFixed(2)}" x2="${(x_c + textSz * 1.5).toFixed(2)}" y2="${y_pin_bot.toFixed(2)}" stroke="#10b981" stroke-width="0.5" vector-effect="non-scaling-stroke" stroke-dasharray="3,2"/>
            <line x1="0" y1="${y_gap_bot.toFixed(2)}" x2="${(x_c + textSz * 1.5).toFixed(2)}" y2="${y_gap_bot.toFixed(2)}" stroke="#10b981" stroke-width="0.5" vector-effect="non-scaling-stroke" stroke-dasharray="3,2"/>
            <line x1="${x_c.toFixed(2)}" y1="${y_pin_bot.toFixed(2)}" x2="${x_c.toFixed(2)}" y2="${y_gap_bot.toFixed(2)}" stroke="#10b981" stroke-width="0.7" vector-effect="non-scaling-stroke"/>
          `;
          g.innerHTML += cadArrow(x_c, y_pin_bot, x_c, y_gap_bot, arrowSz * 0.75, '#10b981');
          g.innerHTML += cadArrow(x_c, y_gap_bot, x_c, y_pin_bot, arrowSz * 0.75, '#10b981');
          g.innerHTML += `<text x="${(x_c + textSz * 0.4).toFixed(2)}" y="${((y_pin_bot + y_gap_bot) / 2 + textSz * 0.35).toFixed(2)}" fill="#10b981" font-size="${textSz * 0.85}" font-weight="700">c = 0.15·m = ${c_clearance.toFixed(2)} mm (Khe hở chân răng - Trang 49)</text>`;
        }
      }'''

    assert old_gap_sim_marker in html, "Could not find old_gap_sim_marker"
    html = html.replace(old_gap_sim_marker, new_gap_sim_marker)
    print("Fix 4: Added KWN 016 bottom clearance dimension line in renderGapView!")

    # -------------------------------------------------------------
    # FIX 6: In SVG renderSectionView, also render complete hub & dimensions down to bore
    # -------------------------------------------------------------
    old_render_section_start = '''    function renderSectionView(g, showDims) {
      const { B1, Ra, R0, Rf, Rs, r4, b1, da, d0, df, ds, standard, p } = CurrentGeom;

      const isKWN001 = (standard === 'KWN_001');
      const w2 = B1 / 2.0; // Nửa bề rộng răng tại vòng chia d0
      const r_sec_s = isKWN001 ? (Rf - (d0 - ds) * 0.5) : Rs;
      const w_rim2 = isKWN001 ? (w2 + 4.0) : (w2 + (r4 || 5.0) + 18.0);

      // Vát mép đỉnh răng theo chuẩn kỹ thuật (Trang 46 đối với KWN 001, Trang 48 đối với KWN 017)
      const w_tip2 = isKWN001 ? (w2 * 0.82) : (w2 * 0.72);
      const rtip = isKWN001 ? Math.min(2.5, B1 * 0.08) : Math.min(6.0, B1 * 0.10);
      const w_flat2 = w_tip2 - rtip;

      const y_break = -(r_sec_s - (isKWN001 ? 25.0 : 70.0));'''

    new_render_section_start = '''    function renderSectionView(g, showDims) {
      const { B1, Ra, R0, Rf, Rs, r4, b1, da, d0, df, ds, standard, p } = CurrentGeom;

      const isKWN001 = (standard === 'KWN_001');
      const w2 = B1 / 2.0;
      const r_sec_s = isKWN001 ? (Rf - (d0 - ds) * 0.5) : Rs;
      const w_rim2 = isKWN001 ? (w2 + 4.0) : (w2 + (r4 || 5.0) + 18.0);

      const w_tip2 = isKWN001 ? (w2 * 0.82) : (w2 * 0.72);
      const rtip = isKWN001 ? Math.min(2.5, B1 * 0.08) : Math.min(6.0, B1 * 0.10);
      const w_flat2 = w_tip2 - rtip;

      const dw = AppState.dw || 80.0;
      const r_bore = dw / 2.0;
      const NL = AppState.hub_NL || 180.0;
      const hubType = AppState.hubType || 'Type_C';
      const dH = Math.max(dw + 35.0, Math.min(ds - 20.0, dw * 1.65));
      const RH = dH / 2.0;

      let xh_L, xh_R;
      if (hubType === 'Type_A') {
        xh_L = -w2;
        xh_R = +w2;
      } else if (hubType === 'Type_B') {
        xh_L = -w_rim2;
        xh_R = -w_rim2 + NL;
      } else {
        xh_L = -NL / 2.0;
        xh_R = +NL / 2.0;
      }

      const y_break = -r_bore;'''

    assert old_render_section_start in html, "Could not find old_render_section_start"
    html = html.replace(old_render_section_start, new_render_section_start)

    # In renderSectionView, update dRim path to include hub
    old_drim_chunk = '''        // Xích tải nặng KWN 017 & KWN 015: Vành bậc lõm ds với góc lượn r4
        const act_r4 = r4 || 5.0;
        dRim = `
          M ${(-w2).toFixed(2)} ${(-Rf).toFixed(2)}
          L ${w2.toFixed(2)} ${(-Rf).toFixed(2)}
          L ${w2.toFixed(2)} ${(-(r_sec_s + act_r4)).toFixed(2)}
          A ${act_r4.toFixed(2)} ${act_r4.toFixed(2)} 0 0 0 ${(w2 + act_r4).toFixed(2)} ${(-r_sec_s).toFixed(2)}
          L ${w_rim2.toFixed(2)} ${(-r_sec_s).toFixed(2)}
          L ${w_rim2.toFixed(2)} ${y_break.toFixed(2)}
          Q ${(w_rim2 * 0.5).toFixed(2)} ${(y_break + 6).toFixed(2)} 0.00 ${y_break.toFixed(2)}
          Q ${(-w_rim2 * 0.5).toFixed(2)} ${(y_break - 6).toFixed(2)} ${(-w_rim2).toFixed(2)} ${y_break.toFixed(2)}
          L ${(-w_rim2).toFixed(2)} ${(-r_sec_s).toFixed(2)}
          L ${(-(w2 + act_r4)).toFixed(2)} ${(-r_sec_s).toFixed(2)}
          A ${act_r4.toFixed(2)} ${act_r4.toFixed(2)} 0 0 0 ${(-w2).toFixed(2)} ${(-(r_sec_s + act_r4)).toFixed(2)}
          Z
        `;'''

    new_drim_chunk = '''        // Vành đĩa và May-ơ hoàn thiện (Type A / B / C):
        if (hubType === 'Type_A') {
          dRim = `
            M ${(-w2).toFixed(2)} ${(-Rf).toFixed(2)}
            L ${w2.toFixed(2)} ${(-Rf).toFixed(2)}
            L ${w2.toFixed(2)} ${(-r_bore).toFixed(2)}
            L ${(-w2).toFixed(2)} ${(-r_bore).toFixed(2)}
            Z
          `;
        } else {
          const act_r4 = r4 || 5.0;
          dRim = `
            M ${(-w2).toFixed(2)} ${(-Rf).toFixed(2)}
            L ${w2.toFixed(2)} ${(-Rf).toFixed(2)}
            L ${w2.toFixed(2)} ${(-(r_sec_s + act_r4)).toFixed(2)}
            A ${act_r4.toFixed(2)} ${act_r4.toFixed(2)} 0 0 0 ${(w2 + act_r4).toFixed(2)} ${(-r_sec_s).toFixed(2)}
            L ${w_rim2.toFixed(2)} ${(-r_sec_s).toFixed(2)}
            L ${w_rim2.toFixed(2)} ${(-RH).toFixed(2)}
            L ${xh_R.toFixed(2)} ${(-RH).toFixed(2)}
            L ${xh_R.toFixed(2)} ${(-r_bore).toFixed(2)}
            L ${xh_L.toFixed(2)} ${(-r_bore).toFixed(2)}
            L ${xh_L.toFixed(2)} ${(-RH).toFixed(2)}
            L ${(-w_rim2).toFixed(2)} ${(-RH).toFixed(2)}
            L ${(-w_rim2).toFixed(2)} ${(-r_sec_s).toFixed(2)}
            L ${(-(w2 + act_r4)).toFixed(2)} ${(-r_sec_s).toFixed(2)}
            A ${act_r4.toFixed(2)} ${act_r4.toFixed(2)} 0 0 0 ${(-w2).toFixed(2)} ${(-(r_sec_s + act_r4)).toFixed(2)}
            Z
          `;
        }'''

    assert old_drim_chunk in html, "Could not find old_drim_chunk"
    html = html.replace(old_drim_chunk, new_drim_chunk)
    print("Fix 5: Updated SVG section view with full hub and shaft bore!")

    # Write back to index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("ALL 5 FIXES SUCCESSFULLY APPLIED TO index.html!")

if __name__ == '__main__':
    apply_fixes()
