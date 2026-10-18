import re

dxf_func = r"""    function exportDXF(mode = 'combined') {
      const menu = document.getElementById('dxfMenu');
      if (menu) menu.style.display = 'none';

      const geom = CurrentGeom;
      const { p, z, d1, b1, R0, Rf, Ra, Rs, r4, u, r1, h3, r2, beta_deg, gamma_deg, alpha_deg, alpha_rad, d0, df, da, ds, B1, standard } = geom;

      // Danh sách các layer AutoCAD và mã màu AutoCAD Color Index (ACI):
      // 1: Red, 2: Yellow, 3: Green, 4: Cyan, 5: Blue, 6: Magenta, 7: White/Black, 8: Grey, 30: Orange
      const layers = [
        ['0', 7],
        ['SPROCKET_CONTOUR', 7],
        ['BORE_KEYWAY', 7],
        ['BASE_CIRCLES', 4],
        ['CENTER_LINES', 1],
        ['CHAIN_PLATES_OUTER', 8],
        ['CHAIN_PLATES_INNER', 8],
        ['CHAIN_ROLLERS', 4],
        ['CHAIN_PINS', 1],
        ['GAP_BOTTOM_U', 2],
        ['GAP_BED_R1', 1],
        ['GAP_FLANK_H3', 3],
        ['GAP_CREST_R2', 6],
        ['GAP_RIM_BODY', 8],
        ['SEATED_ROLLER', 7],
        ['DIM_BETA', 4],
        ['DIM_H3', 3],
        ['DIM_U', 2],
        ['DIM_R1', 1],
        ['DIM_R2', 6],
        ['DIM_GAMMA', 30],
        ['DIM_ALPHA', 5],
        ['DIM_ROLLER', 7],
        ['SECTION_CONTOUR', 7],
        ['SECTION_HATCH', 8],
        ['SECTION_DIMS', 2],
        ['SECTION_REFS', 4],
        ['TITLE_BLOCK', 7],
        ['DRAWING_BORDER', 7]
      ];

      const L = [];
      L.push('0', 'SECTION', '2', 'HEADER', '9', '$ACADVER', '1', 'AC1009', '0', 'ENDSEC');
      L.push('0', 'SECTION', '2', 'TABLES', '0', 'TABLE', '2', 'LAYER', '70', String(layers.length));
      for (const [name, col] of layers) {
        L.push('0', 'LAYER', '2', name, '70', '0', '62', String(col), '6', 'CONTINUOUS');
      }
      L.push('0', 'ENDTAB', '0', 'ENDSEC');
      L.push('0', 'SECTION', '2', 'ENTITIES');

      // Các hàm phụ trợ ghi thực thể DXF:
      const addLine = (x1, y1, x2, y2, layer) => {
        L.push('0', 'LINE', '8', layer,
               '10', x1.toFixed(3), '20', y1.toFixed(3), '30', '0.0',
               '11', x2.toFixed(3), '21', y2.toFixed(3), '31', '0.0');
      };
      const addCircle = (cx, cy, r, layer) => {
        L.push('0', 'CIRCLE', '8', layer,
               '10', cx.toFixed(3), '20', cy.toFixed(3), '30', '0.0',
               '40', r.toFixed(3));
      };
      const addArc = (cx, cy, r, startAngDeg, endAngDeg, layer) => {
        let s = startAngDeg % 360; if (s < 0) s += 360;
        let e = endAngDeg % 360; if (e < 0) e += 360;
        L.push('0', 'ARC', '8', layer,
               '10', cx.toFixed(3), '20', cy.toFixed(3), '30', '0.0',
               '40', r.toFixed(3),
               '50', s.toFixed(2), '51', e.toFixed(2));
      };
      const addText = (x, y, h, str, layer) => {
        L.push('0', 'TEXT', '8', layer,
               '10', x.toFixed(3), '20', y.toFixed(3), '30', '0.0',
               '40', h.toFixed(3),
               '1', String(str));
      };
      const addPolyline = (pts, layer, closed = true) => {
        L.push('0', 'POLYLINE', '8', layer, '66', '1', '70', closed ? '1' : '0');
        for (const pt of pts) {
          L.push('0', 'VERTEX', '8', layer,
                 '10', pt.x.toFixed(3), '20', pt.y.toFixed(3), '30', '0.0');
        }
        L.push('0', 'SEQEND');
      };

      // HÀM 1: GHI ĐĨA XÍCH TOÀN BỘ (SPROCKET ASSEMBLY)
      const writeAssembly = (ox = 0, oy = 0) => {
        // Đường bao răng
        const contour = computeFullContour(geom);
        addPolyline(contour.map(pt => ({ x: pt.x + ox, y: pt.y + oy })), 'SPROCKET_CONTOUR', true);

        // Vòng tròn cơ sở
        addCircle(ox, oy, R0, 'BASE_CIRCLES');
        addCircle(ox, oy, Rf, 'BASE_CIRCLES');
        addCircle(ox, oy, Ra, 'BASE_CIRCLES');
        if (Rs > 0) addCircle(ox, oy, Rs, 'BASE_CIRCLES');

        // Lỗ trục & Rãnh then
        const r_bore = (AppState.dw || 40) / 2.0;
        if (r_bore > 0) {
          addCircle(ox, oy, r_bore, 'BORE_KEYWAY');
          if (AppState.key_b > 0 && AppState.key_t2 > 0) {
            const kw2 = AppState.key_b / 2.0;
            const y_key = r_bore + AppState.key_t2;
            addLine(ox - kw2, oy + r_bore, ox - kw2, oy + y_key, 'BORE_KEYWAY');
            addLine(ox - kw2, oy + y_key, ox + kw2, oy + y_key, 'BORE_KEYWAY');
            addLine(ox + kw2, oy + y_key, ox + kw2, oy + r_bore, 'BORE_KEYWAY');
          }
        }

        // Trục tâm
        const L_ax = Ra * 1.25;
        addLine(ox - L_ax, oy, ox + L_ax, oy, 'CENTER_LINES');
        addLine(ox, oy - L_ax, ox, oy + L_ax, 'CENTER_LINES');

        // Dải xích ăn khớp (Khớp con lăn & má xích)
        const ser = AppState.currentSeries;
        const g1 = AppState.g1 || AppState.g || 90;
        const g2 = AppState.g2 || AppState.g || 60;
        const r_contact = d1 / 2.0;
        const r_pin = (AppState.d1_pin || 36.0) / 2.0;

        const seated_slots = [];
        for (let m = -2; m <= z + 2; m++) {
          const phi = m * alpha_rad;
          if (phi >= -1e-4 && phi <= Math.PI + 1e-4) seated_slots.push(m);
        }
        if (seated_slots.length === 0) seated_slots.push(0);

        const min_m = Math.min(...seated_slots);
        const max_m = Math.max(...seated_slots);

        const j0_x = -R0 * Math.sin(min_m * alpha_rad);
        const j0_y = -R0 * Math.cos(min_m * alpha_rad);
        const dy_top = -R0 - j0_y;
        const dx_top = Math.sqrt(Math.max(0, p * p - dy_top * dy_top));
        const j_prev_x = j0_x + dx_top;

        const joints = [];
        for (let k = 4; k >= 1; k--) joints.push({ x: j_prev_x + (k - 1) * p, y: -R0, id: min_m - k });
        for (const m of seated_slots) joints.push({ x: -R0 * Math.sin(m * alpha_rad), y: -R0 * Math.cos(m * alpha_rad), id: m });

        const jL_x = -R0 * Math.sin(max_m * alpha_rad);
        const jL_y = -R0 * Math.cos(max_m * alpha_rad);
        const dy_bot = R0 - jL_y;
        const dx_bot = Math.sqrt(Math.max(0, p * p - dy_bot * dy_bot));
        const j_next_x = jL_x + dx_bot;
        for (let k = 1; k <= 4; k++) joints.push({ x: j_next_x + (k - 1) * p, y: R0, id: max_m + k });

        // Ghi con lăn và chốt xích
        for (const j of joints) {
          addCircle(ox + j.x, oy - j.y, r_contact, 'CHAIN_ROLLERS');
          addCircle(ox + j.x, oy - j.y, r_pin, 'CHAIN_PINS');
        }

        // Ghi biên dạng các má xích
        for (let i = 0; i < joints.length - 1; i++) {
          const jA = joints[i];
          const jB = joints[i + 1];
          const isOuter = (Math.abs(jA.id) % 2 === 0);
          const layerPlate = isOuter ? 'CHAIN_PLATES_OUTER' : 'CHAIN_PLATES_INNER';

          const dx_l = jB.x - jA.x;
          const dy_l = (-jB.y) - (-jA.y);
          const L_l = Math.hypot(dx_l, dy_l);
          if (L_l > 1e-4) {
            const ux_l = dx_l / L_l;
            const uy_l = dy_l / L_l;
            const nx_l = -uy_l;
            const ny_l = ux_l;

            const is_roller = (ser === 'DIN8187' || ser === 'KWN_001');
            const is_deep = (ser === 'MT' || ser === 'FVT' || (g1 > g2 && g1 > 0));

            const platePts = [];
            const steps_arc = 12;

            if (is_roller) {
              const h = (g2 > 0) ? g2 : (g1 > 0 ? g1 : 11.8);
              const r_end = h / 2.0;
              const w_radius = Math.max(p * 0.85, h * 1.3);

              for (let s = 0; s <= steps_arc; s++) {
                const ang = -Math.PI * 0.5 - Math.PI * (s / steps_arc);
                platePts.push({
                  x: ox + jA.x + r_end * (nx_l * Math.sin(ang) - ux_l * Math.cos(ang)),
                  y: oy - jA.y + r_end * (ny_l * Math.sin(ang) - uy_l * Math.cos(ang))
                });
              }
              for (let s = 1; s < steps_arc; s++) {
                const frac = s / steps_arc;
                const dX = (frac - 0.5) * p;
                const sag = w_radius - Math.sqrt(Math.max(0, w_radius * w_radius - dX * dX));
                const midX = jA.x + ux_l * (frac * p) + nx_l * (r_end - sag);
                const midY = (-jA.y) + uy_l * (frac * p) + ny_l * (r_end - sag);
                platePts.push({ x: ox + midX, y: oy + midY });
              }
              for (let s = 0; s <= steps_arc; s++) {
                const ang = Math.PI * 0.5 - Math.PI * (s / steps_arc);
                platePts.push({
                  x: ox + jB.x + r_end * (nx_l * Math.sin(ang) - ux_l * Math.cos(ang)),
                  y: oy - jB.y + r_end * (ny_l * Math.sin(ang) - uy_l * Math.cos(ang))
                });
              }
              for (let s = 1; s < steps_arc; s++) {
                const frac = 1.0 - s / steps_arc;
                const dX = (frac - 0.5) * p;
                const sag = w_radius - Math.sqrt(Math.max(0, w_radius * w_radius - dX * dX));
                const midX = jA.x + ux_l * (frac * p) - nx_l * (r_end - sag);
                const midY = (-jA.y) + uy_l * (frac * p) - ny_l * (r_end - sag);
                platePts.push({ x: ox + midX, y: oy + midY });
              }
            } else if (is_deep) {
              const r_end = g2 / 2.0;
              const h_top = g1 - r_end;
              const h_bot = r_end;
              const setback = r_end * 0.65;

              for (let s = 0; s <= steps_arc; s++) {
                const ang = -Math.PI * 0.5 - Math.PI * 0.5 * (s / steps_arc);
                platePts.push({
                  x: ox + jA.x + r_end * (nx_l * Math.sin(ang) - ux_l * Math.cos(ang)),
                  y: oy - jA.y + r_end * (ny_l * Math.sin(ang) - uy_l * Math.cos(ang))
                });
              }
              platePts.push({
                x: ox + jA.x - ux_l * setback + nx_l * h_top,
                y: oy - jA.y - uy_l * setback + ny_l * h_top
              });
              platePts.push({
                x: ox + jB.x + ux_l * setback + nx_l * h_top,
                y: oy - jB.y + uy_l * setback + ny_l * h_top
              });
              for (let s = 0; s <= steps_arc; s++) {
                const ang = Math.PI * 0.5 - Math.PI * 0.5 * (s / steps_arc);
                platePts.push({
                  x: ox + jB.x + r_end * (nx_l * Math.sin(ang) - ux_l * Math.cos(ang)),
                  y: oy - jB.y + r_end * (ny_l * Math.sin(ang) - uy_l * Math.cos(ang))
                });
              }
            } else {
              const h = (g2 > 0) ? g2 : (g1 > 0 ? g1 : 60.0);
              const r_end = h / 2.0;
              for (let s = 0; s <= steps_arc; s++) {
                const ang = Math.PI * 0.5 + Math.PI * (s / steps_arc);
                platePts.push({
                  x: ox + jA.x + r_end * (nx_l * Math.sin(ang) - ux_l * Math.cos(ang)),
                  y: oy - jA.y + r_end * (ny_l * Math.sin(ang) - uy_l * Math.cos(ang))
                });
              }
              for (let s = 0; s <= steps_arc; s++) {
                const ang = -Math.PI * 0.5 + Math.PI * (s / steps_arc);
                platePts.push({
                  x: ox + jB.x + r_end * (nx_l * Math.sin(ang) - ux_l * Math.cos(ang)),
                  y: oy - jB.y + r_end * (ny_l * Math.sin(ang) - uy_l * Math.cos(ang))
                });
              }
            }
            addPolyline(platePts, layerPlate, true);
          }
        }
      };

      // HÀM 2: GHI CHI TIẾT HỐC RĂNG MACRO (GAP VIEW VỚI CÁC LAYER MÀU RIÊNG BIỆT)
      const writeGap = (ox = 0, oy = 0) => {
        const half = computeHalfGapPoints(geom, 25);
        const { P0, P1, P2, P3, C1 } = half;
        const pts_half = half.pts;
        const isKWN001 = (standard === 'KWN_001');

        // A. Đáy phẳng u (Layer GAP_BOTTOM_U - Màu 2 Vàng)
        if (u > 0.05) {
          addLine(ox - u / 2.0, oy + Rf, ox + u / 2.0, oy + Rf, 'GAP_BOTTOM_U');
          addLine(ox - u / 2.0, oy + Rf, ox - u / 2.0, oy + Rf - p * 0.06, 'DIM_U');
          addLine(ox + u / 2.0, oy + Rf, ox + u / 2.0, oy + Rf - p * 0.06, 'DIM_U');
          addLine(ox - u / 2.0, oy + Rf - p * 0.04, ox + u / 2.0, oy + Rf - p * 0.04, 'DIM_U');
          addText(ox - p * 0.02, oy + Rf - p * 0.08, p * 0.035, 'u = ' + u.toFixed(2) + ' mm', 'DIM_U');
        }

        // B. Cung đáy r1 (Layer GAP_BED_R1 - Màu 1 Đỏ)
        const nBed = half.num_bed_pts || (isKWN001 ? 21 : 26);
        const r1Pts_R = [];
        const r1Pts_L = [];
        for (let i = (isKWN001 ? 0 : 1); i < nBed; i++) {
          r1Pts_R.push({ x: ox + pts_half[i].x, y: oy + pts_half[i].y });
          r1Pts_L.push({ x: ox - pts_half[i].x, y: oy + pts_half[i].y });
        }
        addPolyline(r1Pts_R, 'GAP_BED_R1', false);
        addPolyline(r1Pts_L, 'GAP_BED_R1', false);
        addText(ox + P1.x + p * 0.04, oy + P1.y, p * 0.035, 'r1 = R' + r1.toFixed(2) + ' mm', 'DIM_R1');

        // C. Đoạn thẳng sườn h3 (Layer GAP_FLANK_H3 - Màu 3 Xanh lá)
        if (h3 > 0.01 && !isKWN001) {
          addLine(ox + P1.x, oy + P1.y, ox + P2.x, oy + P2.y, 'GAP_FLANK_H3');
          addLine(ox - P1.x, oy + P1.y, ox - P2.x, oy + P2.y, 'GAP_FLANK_H3');
          addLine(ox - P1.x - p * 0.03, oy + P1.y, ox - P2.x - p * 0.03, oy + P2.y, 'DIM_H3');
          addText(ox - P2.x - p * 0.12, oy + (P1.y + P2.y) / 2.0, p * 0.035, 'h3 = ' + h3.toFixed(2) + ' mm', 'DIM_H3');
        }

        // D. Cung đỉnh r2 (Layer GAP_CREST_R2 - Màu 6 Tím Magenta)
        const r2Pts_R = [];
        const r2Pts_L = [];
        const startR2 = isKWN001 ? nBed : (half.idx_P2 || 27);
        for (let i = startR2; i < pts_half.length; i++) {
          r2Pts_R.push({ x: ox + pts_half[i].x, y: oy + pts_half[i].y });
          r2Pts_L.push({ x: ox - pts_half[i].x, y: oy + pts_half[i].y });
        }
        addPolyline(r2Pts_R, 'GAP_CREST_R2', false);
        addPolyline(r2Pts_L, 'GAP_CREST_R2', false);
        addText(ox - P3.x - p * 0.06, oy + P3.y + p * 0.02, p * 0.035, 'r2 = R' + r2.toFixed(1) + ' mm', 'DIM_R2');

        // E. Con lăn tiếp xúc trong rãnh
        addCircle(ox, oy + R0, d1 / 2.0, 'SEATED_ROLLER');
        addText(ox - p * 0.08, oy + R0 + d1 * 0.6, p * 0.035, 'd1 = Ø' + d1.toFixed(2) + ' mm', 'DIM_ROLLER');

        // F. Kích thước góc mở beta và góc sườn gamma
        addLine(ox, oy, ox, oy + Ra * 1.15, 'CENTER_LINES');
        addText(ox - p * 0.04, oy + Ra * 1.05, p * 0.045, (isKWN001 ? ('X = ' + beta_deg.toFixed(1) + '°') : ('β = ' + beta_deg.toFixed(1) + '°')), 'DIM_BETA');
        if (!isKWN001) {
          const half_alpha = alpha_rad / 2.0;
          addLine(ox, oy, ox + Ra * Math.sin(half_alpha), oy + Ra * Math.cos(half_alpha), 'CENTER_LINES');
          addText(ox + Ra * Math.sin(half_alpha) + p * 0.02, oy + Ra * Math.cos(half_alpha) * 0.8, p * 0.038, 'γ = ' + gamma_deg.toFixed(2) + '°', 'DIM_GAMMA');
        }
      };

      // HÀM 3: GHI MẶT CẮT THÂN RĂNG (SECTION VIEW)
      const writeSection = (ox = 0, oy = 0) => {
        const isKWN001 = (standard === 'KWN_001');
        const w2 = B1 / 2.0;
        const r_sec_s = isKWN001 ? (Rf - (d0 - ds) * 0.5) : Rs;
        const w_rim2 = isKWN001 ? (w2 + 4.0) : (w2 + (r4 || 5.0) + 18.0);
        const w_tip2 = isKWN001 ? (w2 * 0.82) : (w2 * 0.72);
        const y_break = r_sec_s - (isKWN001 ? 25.0 : 70.0);

        // Biên dạng răng trên
        const toothPts = [
          { x: ox - w_tip2, y: oy + Ra },
          { x: ox + w_tip2, y: oy + Ra },
          { x: ox + w2, y: oy + R0 },
          { x: ox + w2, y: oy + Rf },
          { x: ox - w2, y: oy + Rf },
          { x: ox - w2, y: oy + R0 }
        ];
        addPolyline(toothPts, 'SECTION_CONTOUR', true);

        // Biên dạng vành đĩa
        const rimPts = [
          { x: ox - w2, y: oy + Rf },
          { x: ox + w2, y: oy + Rf },
          { x: ox + w2, y: oy + r_sec_s },
          { x: ox + w_rim2, y: oy + r_sec_s },
          { x: ox + w_rim2, y: oy + y_break },
          { x: ox - w_rim2, y: oy + y_break },
          { x: ox - w_rim2, y: oy + r_sec_s },
          { x: ox - w2, y: oy + r_sec_s }
        ];
        addPolyline(rimPts, 'SECTION_CONTOUR', true);

        // Gạch mặt cắt ANSI 31 (Hatch 45 độ)
        const hStep = Math.max(4.0, p * 0.02);
        for (let y = y_break; y <= Rf; y += hStep) {
          const w_cur = (y <= r_sec_s) ? w_rim2 : w2;
          addLine(ox - w_cur, oy + y, ox + Math.min(w_cur, -w_cur + (Rf - y)), oy + Math.min(Rf, y + w_cur * 2), 'SECTION_HATCH');
        }

        // Trục tâm và kích thước mặt cắt
        addLine(ox, oy + y_break - 20, ox, oy + Ra + 25, 'CENTER_LINES');
        addLine(ox - w2, oy + Ra + 15, ox + w2, oy + Ra + 15, 'SECTION_DIMS');
        addText(ox - 10, oy + Ra + 20, Math.max(3.0, p * 0.035), 'B1 = ' + B1.toFixed(1) + ' mm', 'SECTION_DIMS');
        addLine(ox + w_rim2 + 10, oy + Rf, ox + w_rim2 + 40, oy + Rf, 'SECTION_REFS');
        addText(ox + w_rim2 + 45, oy + Rf - 2, Math.max(3.0, p * 0.032), 'Ø df = ' + df.toFixed(2) + ' mm', 'SECTION_DIMS');
        addLine(ox + w_rim2 + 10, oy + Ra, ox + w_rim2 + 40, oy + Ra, 'SECTION_REFS');
        addText(ox + w_rim2 + 45, oy + Ra - 2, Math.max(3.0, p * 0.032), 'Ø da = ' + da.toFixed(2) + ' mm', 'SECTION_DIMS');
      };

      // THỰC THI THEO TÙY CHỌN MODE
      if (mode === 'assembly') {
        writeAssembly(0, 0);
      } else if (mode === 'gap') {
        writeGap(0, 0);
      } else if (mode === 'section') {
        writeSection(0, 0);
      } else {
        // COMBINED: TỔNG HỢP CẢ 3 HÌNH CHIẾU + KHUNG TÊN KỸ THUẬT A3/A4
        const offX = Ra * 2.7;
        const offY_gap = Ra * 0.75;
        const offY_sec = -Ra * 0.75;

        // Hình 1: Toàn bộ đĩa xích + xích ăn khớp
        writeAssembly(0, 0);
        addText(-Ra * 0.8, -Ra * 1.35, Math.max(4.0, p * 0.05), 'HINH 1: BAN VE LAP TOAN BO DIA XICH & XICH AN KHOP', 'TITLE_BLOCK');

        // Hình 2: Chi tiết hốc răng phóng to
        writeGap(offX, offY_gap);
        addText(offX - Ra * 0.4, offY_gap - Ra * 0.6, Math.max(4.0, p * 0.05), 'HINH 2: CHI TIET BIEN DANG HOC RANG (MACRO VIEW)', 'TITLE_BLOCK');

        // Hình 3: Mặt cắt ngang thân răng
        writeSection(offX, offY_sec);
        addText(offX - Ra * 0.3, offY_sec - Ra * 0.6, Math.max(4.0, p * 0.05), 'HINH 3: MAT CAT NGANG THAN RANG', 'TITLE_BLOCK');

        // Khung bản vẽ và Khung tên kỹ thuật tiêu chuẩn
        const minX = -Ra * 1.6;
        const maxX = offX + Ra * 1.8;
        const minY = -Ra * 1.6;
        const maxY = Ra * 1.6;
        const borderPts = [
          { x: minX, y: minY },
          { x: maxX, y: minY },
          { x: maxX, y: maxY },
          { x: minX, y: maxY }
        ];
        addPolyline(borderPts, 'DRAWING_BORDER', true);

        // Khung tên góc dưới bên phải
        const tbW = Ra * 1.4;
        const tbH = Ra * 0.45;
        const tbX = maxX - tbW;
        const tbY = minY;
        const tbPts = [
          { x: tbX, y: tbY },
          { x: maxX, y: tbY },
          { x: maxX, y: tbY + tbH },
          { x: tbX, y: tbY + tbH }
        ];
        addPolyline(tbPts, 'TITLE_BLOCK', true);
        addLine(tbX, tbY + tbH * 0.65, maxX, tbY + tbH * 0.65, 'TITLE_BLOCK');
        addLine(tbX, tbY + tbH * 0.35, maxX, tbY + tbH * 0.35, 'TITLE_BLOCK');

        addText(tbX + 10, tbY + tbH * 0.72, Math.max(3.0, p * 0.038), 'KETTENWULF SPROCKET CAD STUDIO', 'TITLE_BLOCK');
        addText(tbX + 10, tbY + tbH * 0.42, Math.max(2.5, p * 0.030), 'TIEU CHUAN: ' + standard + ' | p = ' + p + ' mm | z = ' + z + ' RANG', 'TITLE_BLOCK');
        addText(tbX + 10, tbY + tbH * 0.12, Math.max(2.5, p * 0.026), 'd0 = ' + d0.toFixed(2) + ' mm | da = ' + da.toFixed(2) + ' mm | NGAY: ' + new Date().toLocaleDateString('vi-VN'), 'TITLE_BLOCK');
      }

      L.push('0', 'ENDSEC', '0', 'EOF');
      const dxf = L.join('\r\n');

      const blob = new Blob([dxf], { type: 'application/dxf' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `sprocket_${mode}_${AppState.standard}_p${AppState.p}_z${AppState.z}.dxf`;
      a.click();
      URL.revokeObjectURL(url);
    }"""

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('function exportDXF(mode = \'combined\') {')
assert start_idx != -1, 'exportDXF start not found'
end_marker = 'function setupCanvasPanZoom() {'
end_idx = text.find(end_marker, start_idx)
assert end_idx != -1, 'setupCanvasPanZoom not found'

updated = text[:start_idx] + dxf_func.strip() + '\n\n    /* =========================================================================\n       HỆ THỐNG ZOOM CHUẨN CAD VÀO VỊ TRÍ CON TRỎ CHUỘT (ZOOM TO CURSOR)\n       ========================================================================= */\n    ' + text[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated)
print('Updated index.html successfully with safe strings.')
