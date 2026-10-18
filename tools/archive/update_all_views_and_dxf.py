import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. Update renderFullView styling for light canvas & smooth graphics
# -----------------------------------------------------------------------------
old_fullview_pattern = r'function renderFullView\(g, showCircles, showDims, showSim\) \{[\s\S]*?if \(showSim && showChainStrand\) \{\s*g\.innerHTML \+= renderDynamicChainStrand\(CurrentGeom\);\s*\}\s*\}'

new_fullview_func = """function renderFullView(g, showCircles, showDims, showSim) {
      const { R0, Rf, Ra, Rs, z, alpha_rad, d0, df, da, ds, alpha_deg, d1, p } = CurrentGeom;
      const L = Ra * 1.25;

      const textSz = Math.max(3.0, Ra * 0.038);
      const arrowSz = textSz * 0.95;

      // Nhóm đĩa xích quay ngược chiều kim đồng hồ đồng bộ chuẩn xác với dải xích
      const rotDeg = -AppState.animAngle * (180.0 / Math.PI);
      let sprocketGroupHtml = `<g id="sprocketRotated" transform="rotate(${rotDeg})">`;

      // Trục tâm chữ thập nét mảnh gạch-chấm quay đồng bộ cùng đĩa xích
      sprocketGroupHtml += `
        <line x1="${-L}" y1="0" x2="${L}" y2="0" stroke="#0284c7" stroke-width="0.5" vector-effect="non-scaling-stroke" stroke-dasharray="${Ra*0.04}, ${Ra*0.015}, ${Ra*0.008}, ${Ra*0.015}"/>
        <line x1="0" y1="${-L}" x2="0" y2="${L}" stroke="#0284c7" stroke-width="0.5" vector-effect="non-scaling-stroke" stroke-dasharray="${Ra*0.04}, ${Ra*0.015}, ${Ra*0.008}, ${Ra*0.015}"/>
      `;

      // Các đường tròn cơ sở
      if (showCircles) {
        sprocketGroupHtml += `
          <!-- Vòng chân răng df: nét đứt đỏ tươi rõ ràng -->
          <circle cx="0" cy="0" r="${Rf}" fill="none" stroke="#dc2626" stroke-width="0.5" vector-effect="non-scaling-stroke" stroke-dasharray="${Ra*0.03}, ${Ra*0.02}"/>
          <!-- Vòng chia d0: nét gạch-chấm tâm màu xanh dương -->
          <circle cx="0" cy="0" r="${R0}" fill="none" stroke="#0284c7" stroke-width="0.6" vector-effect="non-scaling-stroke" stroke-dasharray="${Ra*0.06}, ${Ra*0.02}, ${Ra*0.01}, ${Ra*0.02}"/>
          <!-- Vòng đỉnh răng da: nét hai chấm gạch màu tím -->
          <circle cx="0" cy="0" r="${Ra}" fill="none" stroke="#7c3aed" stroke-width="0.5" vector-effect="non-scaling-stroke" stroke-dasharray="${Ra*0.04}, ${Ra*0.015}, ${Ra*0.01}, ${Ra*0.015}"/>
          <!-- Bậc lõm vành ds: nét gạch chấm màu cam -->
          ${Rs > 0 ? `<circle cx="0" cy="0" r="${Rs}" fill="none" stroke="#d97706" stroke-width="0.5" vector-effect="non-scaling-stroke" stroke-dasharray="${Ra*0.03}, ${Ra*0.015}"/>` : ''}
        `;
      }

      // Đường bao răng đĩa xích nét mảnh CAD (Nền kim loại sáng sắc nét #e2e8f0, viền đậm kỹ thuật #0f172a)
      const contour = computeFullContour(CurrentGeom);
      let pathD = `M ${contour[0].x.toFixed(2)} ${(-contour[0].y).toFixed(2)} `;
      for (let i = 1; i < contour.length; i++) {
        pathD += `L ${contour[i].x.toFixed(2)} ${(-contour[i].y).toFixed(2)} `;
      }
      pathD += 'Z';
      sprocketGroupHtml += `
        <path d="${pathD}" fill="#e2e8f0" stroke="#0f172a" stroke-width="0.8" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>
      `;

      // Lỗ trục & Rãnh then nét mảnh CAD (Nền trắng #ffffff)
      const r_bore = AppState.dw / 2.0;
      if (r_bore > 0) {
        sprocketGroupHtml += `<circle cx="0" cy="0" r="${r_bore}" fill="#ffffff" stroke="#0f172a" stroke-width="0.8" vector-effect="non-scaling-stroke"/>`;
        if (AppState.key_b > 0) {
          const kw2 = AppState.key_b / 2.0;
          const y_key = -(r_bore + AppState.key_t2);
          sprocketGroupHtml += `
            <rect x="${-kw2}" y="${y_key}" width="${AppState.key_b}" height="${AppState.key_t2 + 8}" fill="#ffffff" stroke="#0f172a" stroke-width="0.8" vector-effect="non-scaling-stroke"/>
          `;
        }
      }

      // Con lăn tĩnh gắn trên hốc răng khi không bật dải xích
      const showChainStrand = document.getElementById('layerChainStrand')?.checked ?? true;
      if (showSim && !showChainStrand) {
        const roller_r = AppState.d1 / 2.0;
        for (let k = 0; k < z; k++) {
          const ang = k * alpha_rad;
          const rx = R0 * Math.sin(ang);
          const ry = -R0 * Math.cos(ang);
          sprocketGroupHtml += `
            <circle cx="${rx}" cy="${ry}" r="${roller_r}" fill="#ffffff" stroke="#0f172a" stroke-width="0.6" vector-effect="non-scaling-stroke"/>
            <circle cx="${rx}" cy="${ry}" r="${textSz * 0.25}" fill="#0284c7"/>
          `;
        }
      }

      sprocketGroupHtml += `</g>`;
      g.innerHTML += sprocketGroupHtml;

      // 2. MÔ PHỎNG DẢI XÍCH ĐỘNG HỌC ĂN KHỚP (KINEMATIC RIGID CHAIN STRAND)
      if (showSim && showChainStrand) {
        g.innerHTML += renderDynamicChainStrand(CurrentGeom);
      }
    }"""

html = re.sub(old_fullview_pattern, new_fullview_func, html, count=1)
print("Updated renderFullView for light CAD canvas.")

# -----------------------------------------------------------------------------
# 2. Update renderDynamicChainStrand (Colors on light canvas & smooth tangent)
# -----------------------------------------------------------------------------
old_strand_pattern = r'function renderDynamicChainStrand\(geom\) \{[\s\S]*?return strandHtml;\s*\}'

new_strand_func = """function renderDynamicChainStrand(geom) {
      const { R0, z, p, d1, alpha_rad } = geom;
      const theta = AppState.animAngle;
      const ser = AppState.currentSeries;
      const g1 = AppState.g1 || AppState.g || 90;
      const g2 = AppState.g2 || AppState.g || 60;

      // ĐỒNG PHA 100% VỚI ĐĨA XÍCH:
      const K_base = Math.floor(theta / alpha_rad);
      const d_theta = theta - K_base * alpha_rad;

      const seated_slots = [];
      for (let m = -2; m <= z + 2; m++) {
        const phi = d_theta + m * alpha_rad;
        if (phi >= -1e-4 && phi <= Math.PI + 1e-4) {
          seated_slots.push(m);
        }
      }
      if (seated_slots.length === 0) seated_slots.push(0);

      const min_m = Math.min(...seated_slots);
      const max_m = Math.max(...seated_slots);

      const phi_0 = d_theta + min_m * alpha_rad;
      const j0_x = -R0 * Math.sin(phi_0);
      const j0_y = -R0 * Math.cos(phi_0);

      // Điểm tiếp tuyến đỉnh nhánh tới (y = -R0):
      const dy_top = -R0 - j0_y;
      const dx_top = Math.sqrt(Math.max(0, p * p - dy_top * dy_top));
      const j_prev_x = j0_x + dx_top;
      const j_prev_y = -R0;

      const joints = [];
      const n_extra_top = 4;
      const n_extra_bot = 4;

      // 1. Nhánh xích tới trên cùng (y = -R0)
      for (let k = n_extra_top; k >= 1; k--) {
        joints.push({
          x: j_prev_x + (k - 1) * p,
          y: -R0,
          id: K_base + min_m - k
        });
      }

      // 2. Các khớp xích đang ngồi trong hốc răng trên đĩa xích (Seated joints)
      for (const m of seated_slots) {
        const phi = d_theta + m * alpha_rad;
        joints.push({
          x: -R0 * Math.sin(phi),
          y: -R0 * Math.cos(phi),
          id: K_base + m
        });
      }

      // 3. Nhánh xích rời đáy đĩa (y = +R0)
      const phi_L = d_theta + max_m * alpha_rad;
      const jL_x = -R0 * Math.sin(phi_L);
      const jL_y = -R0 * Math.cos(phi_L);

      const dy_bot = R0 - jL_y;
      const dx_bot = Math.sqrt(Math.max(0, p * p - dy_bot * dy_bot));
      const j_next_x = jL_x + dx_bot;
      const j_next_y = R0;

      for (let k = 1; k <= n_extra_bot; k++) {
        joints.push({
          x: j_next_x + (k - 1) * p,
          y: R0,
          id: K_base + max_m + k
        });
      }

      // Danh sách các mắt xích (links)
      const links = [];
      for (let i = 0; i < joints.length - 1; i++) {
        const jA = joints[i];
        const jB = joints[i + 1];
        const isOuter = (Math.abs(jA.id) % 2 === 0);
        const pathD = generateLinkPlateSvgPath(jA.x, jA.y, jB.x, jB.y, ser, g1, g2, p);
        links.push({ jA, jB, isOuter, pathD });
      }

      let strandHtml = '<g id="kinematicChainStrand">';
      const r_contact = d1 / 2.0;
      const r_pin = (AppState.d1_pin || 36.0) / 2.0;
      const opVal = AppState.plateOpacity;
      const strokeOp = Math.min(1.0, opVal + 0.25);

      // LỚP 1: CÁC MÁ TRONG (INNER LINK PLATES)
      strandHtml += '<g id="innerPlatesLayer">';
      for (const lnk of links) {
        if (!lnk.isOuter) {
          strandHtml += `
            <path d="${lnk.pathD}" fill="#64748b" fill-opacity="${opVal * 0.9}" stroke="#334155" stroke-opacity="${strokeOp}" stroke-width="0.8" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>
          `;
        }
      }
      strandHtml += '</g>';

      // LỚP 2: ỐNG LÓT / CON LĂN (ROLLERS / BUSHINGS) - Tiếp xúc chính xác tại các khớp (Nền trắng #ffffff viền đậm #0f172a)
      strandHtml += '<g id="rollersLayer">';
      for (let i = 0; i < joints.length; i++) {
        const j = joints[i];
        strandHtml += `
          <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${r_contact.toFixed(2)}" fill="#ffffff" stroke="#0f172a" stroke-width="0.7" vector-effect="non-scaling-stroke"/>
        `;
      }
      strandHtml += '</g>';

      // LỚP 3: CÁC MÁ NGOÀI (OUTER LINK PLATES)
      strandHtml += '<g id="outerPlatesLayer">';
      for (const lnk of links) {
        if (lnk.isOuter) {
          strandHtml += `
            <path d="${lnk.pathD}" fill="#475569" fill-opacity="${opVal}" stroke="#0f172a" stroke-opacity="${strokeOp}" stroke-width="0.8" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>
          `;
        }
      }
      strandHtml += '</g>';

      // LỚP 4: ĐẦU TÁN CHỐT XÍCH (PIN RIVETS)
      strandHtml += '<g id="pinsLayer">';
      for (let i = 0; i < joints.length; i++) {
        const j = joints[i];
        const isOuterPin = (Math.abs(j.id) % 2 === 0);
        strandHtml += `
          <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${r_pin.toFixed(2)}" fill="${isOuterPin ? '#0284c7' : '#0369a1'}" stroke="#0f172a" stroke-width="0.5" vector-effect="non-scaling-stroke"/>
          <circle cx="${j.x.toFixed(2)}" cy="${j.y.toFixed(2)}" r="${(r_pin * 0.40).toFixed(2)}" fill="#020617" stroke="none"/>
        `;
      }
      strandHtml += '</g>';

      strandHtml += '</g>';
      return strandHtml;
    }"""

html = re.sub(old_strand_pattern, new_strand_func, html, count=1)
print("Updated renderDynamicChainStrand for light CAD canvas.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved Step 2.")
