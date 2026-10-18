import os
import re

INDEX_PATH = r'd:\Google Antigravity\Xich tai nang\index.html'

def apply_overhaul():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. NEW renderSectionView IMPLEMENTATION
    new_renderSectionView = '''    function renderSectionView(g, showDims) {
      const { B1, Ra, R0, Rf, Rs, r4, b1, da, d0, df, ds, standard, p } = CurrentGeom;

      const isKWN001 = (standard === 'KWN_001');
      const w2 = B1 / 2.0;

      const w_tip2 = isKWN001 ? (w2 * 0.82) : (w2 * 0.72);
      const rtip = isKWN001 ? Math.min(2.5, B1 * 0.08) : Math.min(6.0, B1 * 0.10);
      const w_flat2 = w_tip2 - rtip;

      const dw = AppState.dw || 80.0;
      const r_bore = dw / 2.0;
      const NL = AppState.hub_NL || 180.0;
      const hubType = AppState.hubType || 'Type_C';

      // May-o ngoai Dn:
      let rawDn = AppState.hub_Dn || Math.max(dw + 35.0, Math.min(ds - 20.0, dw * 1.65));
      const max_RH = Math.max(r_bore + 12.0, Rf - 5.0);
      const min_RH = r_bore + 8.0;
      const RH = Math.max(min_RH, Math.min(max_RH, rawDn / 2.0));
      const Dn = RH * 2.0;

      let xh_L, xh_R;
      if (hubType === 'Type_A') {
        xh_L = -w2;
        xh_R = +w2;
      } else if (hubType === 'Type_B') {
        xh_L = -w2;
        xh_R = -w2 + NL;
      } else {
        xh_L = -NL / 2.0;
        xh_R = +NL / 2.0;
      }

      const bk = AppState.key_b || 10.0;
      const t2 = AppState.key_t2 || 3.3;

      const S_sec = Math.max(B1 * 2.8, (Ra - r_bore) * 1.25);
      const textSz = Math.max(2.6, Math.min(S_sec * 0.035, B1 * 0.28));
      const arrowSz = textSz * 0.95;

      const isLight = (AppState.bgTheme === 'light');
      const colMetalFill = isLight ? '#f8fafc' : '#0f172a';
      const colToothFill = isLight ? '#e2e8f0' : '#1e293b';
      const colStroke = isLight ? '#0f172a' : '#38bdf8';
      const colHatch = isLight ? '#64748b' : '#38bdf8';
      const colCenter = isLight ? '#0284c7' : '#38bdf8';
      const colGhost = isLight ? '#94a3b8' : '#475569';

      const hubTypeLabel = (hubType === 'Type_A') ? 'Type A: Đĩa phẳng (Plate wheel)' :
                           (hubType === 'Type_B') ? 'Type B: May-ơ 1 phía (One-sided hub)' :
                           'Type C: May-ơ 2 phía đối xứng (Symmetrical hub)';

      g.innerHTML += `
        <text x="0" y="${-Ra - textSz * 6.5}" fill="${isLight ? '#0f172a' : '#f8fafc'}" font-size="${textSz * 1.25}" font-weight="800" text-anchor="middle" letter-spacing="1">
          BẢN VẼ MẶT CẮT DỌC TRỤC A-A (AXIAL SECTION VIEW A-A)
        </text>
        <text x="0" y="${-Ra - textSz * 4.8}" fill="#10b981" font-size="${textSz * 0.95}" font-weight="700" text-anchor="middle">
          KẾT CẤU: ${hubTypeLabel} | NL = ${NL.toFixed(1)} mm | ØDn = ${Dn.toFixed(1)} mm | Ødw = ${dw.toFixed(1)} mm
        </text>
      `;

      // 1. Trục tâm quay nằm ngang (Y = 0) và đứng (X = 0)
      const x_axis_min = Math.min(xh_L, -w2) - textSz * 9.0;
      const x_axis_max = Math.max(xh_R, +w2) + textSz * 9.0;
      g.innerHTML += `
        <line x1="${x_axis_min}" y1="0" x2="${x_axis_max}" y2="0" stroke="${colCenter}" stroke-width="0.6" vector-effect="non-scaling-stroke" stroke-dasharray="16, 3, 2, 3"/>
        <line x1="0" y1="${-Ra - textSz * 3.5}" x2="0" y2="${Ra + textSz * 3.5}" stroke="${colCenter}" stroke-width="0.6" vector-effect="non-scaling-stroke" stroke-dasharray="16, 3, 2, 3"/>
      `;

      // 2. Thân kim loại Nửa trên (Top) và Nửa dưới (Bottom)
      let dTopBody = '';
      let dBotBody = '';
      if (hubType === 'Type_A') {
        dTopBody = `
          M ${-w2} ${-r_bore}
          L ${-w2} ${-Rf}
          L ${w2} ${-Rf}
          L ${w2} ${-r_bore}
          L ${bk/2} ${-r_bore}
          L ${bk/2} ${-(r_bore + t2)}
          L ${-bk/2} ${-(r_bore + t2)}
          L ${-bk/2} ${-r_bore}
          Z
        `;
        dBotBody = `
          M ${-w2} ${r_bore}
          L ${-w2} ${Rf}
          L ${w2} ${Rf}
          L ${w2} ${r_bore}
          Z
        `;
      } else if (hubType === 'Type_B') {
        dTopBody = `
          M ${xh_L} ${-r_bore}
          L ${xh_L} ${-Rf}
          L ${w2} ${-Rf}
          L ${w2} ${-RH}
          L ${xh_R} ${-RH}
          L ${xh_R} ${-r_bore}
          L ${bk/2} ${-r_bore}
          L ${bk/2} ${-(r_bore + t2)}
          L ${-bk/2} ${-(r_bore + t2)}
          L ${-bk/2} ${-r_bore}
          Z
        `;
        dBotBody = `
          M ${xh_L} ${r_bore}
          L ${xh_L} ${Rf}
          L ${w2} ${Rf}
          L ${w2} ${RH}
          L ${xh_R} ${RH}
          L ${xh_R} ${r_bore}
          Z
        `;
      } else {
        dTopBody = `
          M ${xh_L} ${-r_bore}
          L ${xh_L} ${-RH}
          L ${-w2} ${-RH}
          L ${-w2} ${-Rf}
          L ${w2} ${-Rf}
          L ${w2} ${-RH}
          L ${xh_R} ${-RH}
          L ${xh_R} ${-r_bore}
          L ${bk/2} ${-r_bore}
          L ${bk/2} ${-(r_bore + t2)}
          L ${-bk/2} ${-(r_bore + t2)}
          L ${-bk/2} ${-r_bore}
          Z
        `;
        dBotBody = `
          M ${xh_L} ${r_bore}
          L ${xh_L} ${RH}
          L ${-w2} ${RH}
          L ${-w2} ${Rf}
          L ${w2} ${Rf}
          L ${w2} ${RH}
          L ${xh_R} ${RH}
          L ${xh_R} ${r_bore}
          Z
        `;
      }

      // 3. Răng đỉnh trên và đỉnh dưới
      const dToothTop = `
        M ${-w_flat2.toFixed(2)} ${(-Ra).toFixed(2)}
        L ${w_flat2.toFixed(2)} ${(-Ra).toFixed(2)}
        A ${rtip.toFixed(2)} ${rtip.toFixed(2)} 0 0 1 ${w_tip2.toFixed(2)} ${(-(Ra - rtip)).toFixed(2)}
        L ${w2.toFixed(2)} ${(-R0).toFixed(2)}
        L ${w2.toFixed(2)} ${(-Rf).toFixed(2)}
        L ${(-w2).toFixed(2)} ${(-Rf).toFixed(2)}
        L ${(-w2).toFixed(2)} ${(-R0).toFixed(2)}
        L ${(-w_tip2).toFixed(2)} ${(-(Ra - rtip)).toFixed(2)}
        A ${rtip.toFixed(2)} ${rtip.toFixed(2)} 0 0 1 ${(-w_flat2).toFixed(2)} ${(-Ra).toFixed(2)}
        Z
      `;

      const dToothBot = `
        M ${-w_flat2.toFixed(2)} ${Ra.toFixed(2)}
        L ${w_flat2.toFixed(2)} ${Ra.toFixed(2)}
        A ${rtip.toFixed(2)} ${rtip.toFixed(2)} 0 0 0 ${w_tip2.toFixed(2)} ${(Ra - rtip).toFixed(2)}
        L ${w2.toFixed(2)} ${R0.toFixed(2)}
        L ${w2.toFixed(2)} ${Rf.toFixed(2)}
        L ${(-w2).toFixed(2)} ${Rf.toFixed(2)}
        L ${(-w2).toFixed(2)} ${R0.toFixed(2)}
        L ${(-w_tip2).toFixed(2)} ${(Ra - rtip).toFixed(2)}
        A ${rtip.toFixed(2)} ${rtip.toFixed(2)} 0 0 0 ${(-w_flat2).toFixed(2)} ${Ra.toFixed(2)}
        Z
      `;

      const hatchPitch = Math.max(3.5, textSz * 0.75);
      g.innerHTML += `
        <defs>
          <pattern id="cadHatchLight" patternUnits="userSpaceOnUse" width="${hatchPitch.toFixed(1)}" height="${hatchPitch.toFixed(1)}" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="${hatchPitch.toFixed(1)}" stroke="${colHatch}" stroke-width="0.5"/>
          </pattern>
        </defs>

        <!-- Thân kim loại NỬA TRÊN -->
        <path d="${dTopBody}" fill="${colMetalFill}" stroke="${colStroke}" stroke-width="0.9" vector-effect="non-scaling-stroke"/>
        <path d="${dTopBody}" fill="url(#cadHatchLight)" stroke="${colStroke}" stroke-width="0.9" vector-effect="non-scaling-stroke"/>

        <!-- Thân kim loại NỬA DƯỚI -->
        <path d="${dBotBody}" fill="${colMetalFill}" stroke="${colStroke}" stroke-width="0.9" vector-effect="non-scaling-stroke"/>
        <path d="${dBotBody}" fill="url(#cadHatchLight)" stroke="${colStroke}" stroke-width="0.9" vector-effect="non-scaling-stroke"/>

        <!-- Răng đỉnh TRÊN & DƯỚI (Không gạch mặt cắt theo ISO 128 / TCVN 8-24) -->
        <path d="${dToothTop}" fill="${colToothFill}" stroke="${colStroke}" stroke-width="0.9" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>
        <path d="${dToothBot}" fill="${colToothFill}" stroke="${colStroke}" stroke-width="0.9" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>

        <!-- Ranh giới chân răng df nét đứt mảnh -->
        <line x1="${-w2 - textSz*0.8}" y1="${-Rf}" x2="${w2 + textSz*0.8}" y2="${-Rf}" stroke="${isLight ? '#dc2626' : '#ef4444'}" stroke-width="0.6" vector-effect="non-scaling-stroke" stroke-dasharray="5, 2.5"/>
        <line x1="${-w2 - textSz*0.8}" y1="${Rf}" x2="${w2 + textSz*0.8}" y2="${Rf}" stroke="${isLight ? '#dc2626' : '#ef4444'}" stroke-width="0.6" vector-effect="non-scaling-stroke" stroke-dasharray="5, 2.5"/>

        <!-- Vòng chia d0 nét gạch chấm mảnh -->
        <line x1="${-w2 - textSz*1.2}" y1="${-R0}" x2="${w2 + textSz*1.2}" y2="${-R0}" stroke="${isLight ? '#0284c7' : '#38bdf8'}" stroke-width="0.6" vector-effect="non-scaling-stroke" stroke-dasharray="8, 2.5, 2, 2.5"/>
        <line x1="${-w2 - textSz*1.2}" y1="${R0}" x2="${w2 + textSz*1.2}" y2="${R0}" stroke="${isLight ? '#0284c7' : '#38bdf8'}" stroke-width="0.6" vector-effect="non-scaling-stroke" stroke-dasharray="8, 2.5, 2, 2.5"/>

        <!-- Đường danh nghĩa lỗ trục qua rãnh then (Ghost line) -->
        <line x1="${-bk/2}" y1="${-r_bore}" x2="${bk/2}" y2="${-r_bore}" stroke="${colGhost}" stroke-width="0.5" vector-effect="non-scaling-stroke" stroke-dasharray="3, 2"/>
      `;

      // 4. HỆ THỐNG ĐƯỜNG GIÓNG VÀ KÍCH THƯỚC CHUẨN ISO 129
      const x_base_R = Math.max(xh_R, w2) + textSz * 2.5;
      const colStep = textSz * 4.2;
      const x_df = x_base_R + colStep * 1;
      const x_d0 = x_base_R + colStep * 2;
      const x_da = x_base_R + colStep * 3;

      const x_base_L = Math.min(xh_L, -w2) - textSz * 2.5;
      const x_dw = x_base_L - colStep * 1;
      const x_Dn = x_base_L - colStep * 2;

      if (showDims) {
        let dimsHtml = '';

        // Kích thước B1 ở đỉnh
        dimsHtml += `
          <line x1="${-w2}" y1="${-Ra - textSz * 2.2}" x2="${w2}" y2="${-Ra - textSz * 2.2}" stroke="#0284c7" stroke-width="0.5"/>
          <line x1="${-w2}" y1="${-Ra}" x2="${-w2}" y2="${-Ra - textSz * 2.8}" stroke="#0284c7" stroke-width="0.4"/>
          <line x1="${w2}" y1="${-Ra}" x2="${w2}" y2="${-Ra - textSz * 2.8}" stroke="#0284c7" stroke-width="0.4"/>
          <text x="0" y="${-Ra - textSz * 2.6}" fill="#0284c7" font-size="${textSz}" font-weight="700" text-anchor="middle">B1 = ${B1.toFixed(1)} mm</text>
        `;

        // Kích thước NL ở đáy may-ơ
        if (hubType !== 'Type_A') {
          dimsHtml += `
            <line x1="${xh_L}" y1="${RH + textSz * 3.0}" x2="${xh_R}" y2="${RH + textSz * 3.0}" stroke="#10b981" stroke-width="0.5"/>
            <line x1="${xh_L}" y1="${RH}" x2="${xh_L}" y2="${RH + textSz * 3.6}" stroke="#10b981" stroke-width="0.4"/>
            <line x1="${xh_R}" y1="${RH}" x2="${xh_R}" y2="${RH + textSz * 3.6}" stroke="#10b981" stroke-width="0.4"/>
            <text x="${(xh_L + xh_R)/2.0}" y="${RH + textSz * 4.4}" fill="#10b981" font-size="${textSz}" font-weight="700" text-anchor="middle">NL = ${NL.toFixed(1)} mm</text>
          `;

          // Nếu Type B: dóng thêm độ nhô may-ơ Ln2
          if (hubType === 'Type_B') {
            const ln2 = NL - B1;
            dimsHtml += `
              <line x1="${w2}" y1="${RH + textSz * 1.5}" x2="${xh_R}" y2="${RH + textSz * 1.5}" stroke="#10b981" stroke-width="0.5"/>
              <line x1="${w2}" y1="${RH}" x2="${w2}" y2="${RH + textSz * 2.0}" stroke="#10b981" stroke-width="0.4"/>
              <text x="${(w2 + xh_R)/2.0}" y="${RH + textSz * 2.6}" fill="#10b981" font-size="${textSz * 0.9}" font-weight="700" text-anchor="middle">Ln2 = ${ln2.toFixed(1)} mm</text>
            `;
          }
        }

        // Cột df bên phải (dóng đối xứng từ -Rf đến +Rf)
        dimsHtml += `
          <line x1="${w2}" y1="${-Rf}" x2="${x_df + textSz}" y2="${-Rf}" stroke="#ef4444" stroke-width="0.5" stroke-dasharray="4,2"/>
          <line x1="${w2}" y1="${Rf}" x2="${x_df + textSz}" y2="${Rf}" stroke="#ef4444" stroke-width="0.5" stroke-dasharray="4,2"/>
          <line x1="${x_df}" y1="${-Rf}" x2="${x_df}" y2="${Rf}" stroke="#ef4444" stroke-width="0.7"/>
          <text x="${x_df + textSz * 0.5}" y="${-Rf * 0.4}" fill="#ef4444" font-size="${textSz * 0.95}" font-weight="700">Ø df = ${df.toFixed(2)} (h11)</text>
        `;

        // Cột d0 bên phải
        dimsHtml += `
          <line x1="${w2}" y1="${-R0}" x2="${x_d0 + textSz}" y2="${-R0}" stroke="#38bdf8" stroke-width="0.5" stroke-dasharray="4,2"/>
          <line x1="${w2}" y1="${R0}" x2="${x_d0 + textSz}" y2="${R0}" stroke="#38bdf8" stroke-width="0.5" stroke-dasharray="4,2"/>
          <line x1="${x_d0}" y1="${-R0}" x2="${x_d0}" y2="${R0}" stroke="#38bdf8" stroke-width="0.7"/>
          <text x="${x_d0 + textSz * 0.5}" y="0" fill="#38bdf8" font-size="${textSz * 0.95}" font-weight="700">Ø d0 = ${d0.toFixed(2)}</text>
        `;

        // Cột da bên phải
        dimsHtml += `
          <line x1="${w_tip2}" y1="${-Ra}" x2="${x_da + textSz}" y2="${-Ra}" stroke="#c084fc" stroke-width="0.5" stroke-dasharray="4,2"/>
          <line x1="${w_tip2}" y1="${Ra}" x2="${x_da + textSz}" y2="${Ra}" stroke="#c084fc" stroke-width="0.5" stroke-dasharray="4,2"/>
          <line x1="${x_da}" y1="${-Ra}" x2="${x_da}" y2="${Ra}" stroke="#c084fc" stroke-width="0.7"/>
          <text x="${x_da + textSz * 0.5}" y="${Rf * 0.4}" fill="#c084fc" font-size="${textSz * 0.95}" font-weight="700">Ø da = ${da.toFixed(2)}</text>
        `;

        // Cột dw bên trái (dóng đối xứng từ -r_bore đến +r_bore)
        dimsHtml += `
          <line x1="${xh_L}" y1="${-r_bore}" x2="${x_dw - textSz}" y2="${-r_bore}" stroke="#fbbf24" stroke-width="0.5" stroke-dasharray="4,2"/>
          <line x1="${xh_L}" y1="${r_bore}" x2="${x_dw - textSz}" y2="${r_bore}" stroke="#fbbf24" stroke-width="0.5" stroke-dasharray="4,2"/>
          <line x1="${x_dw}" y1="${-r_bore}" x2="${x_dw}" y2="${r_bore}" stroke="#fbbf24" stroke-width="0.7"/>
          <text x="${x_dw - textSz * 0.5}" y="${-r_bore * 0.4}" fill="#fbbf24" font-size="${textSz * 0.95}" font-weight="700" text-anchor="end">Ø dw = ${dw.toFixed(1)} (H7)</text>
        `;

        // Cột Dn bên trái (dóng đối xứng từ -RH đến +RH)
        if (hubType !== 'Type_A') {
          dimsHtml += `
            <line x1="${xh_L}" y1="${-RH}" x2="${x_Dn - textSz}" y2="${-RH}" stroke="#34d399" stroke-width="0.5" stroke-dasharray="4,2"/>
            <line x1="${xh_L}" y1="${RH}" x2="${x_Dn - textSz}" y2="${RH}" stroke="#34d399" stroke-width="0.5" stroke-dasharray="4,2"/>
            <line x1="${x_Dn}" y1="${-RH}" x2="${x_Dn}" y2="${RH}" stroke="#34d399" stroke-width="0.7"/>
            <text x="${x_Dn - textSz * 0.5}" y="${RH * 0.4}" fill="#34d399" font-size="${textSz * 0.95}" font-weight="700" text-anchor="end">Ø Dn = ${Dn.toFixed(1)}</text>
          `;
        }

        // Leader chỉ vào rãnh then
        dimsHtml += `
          <line x1="0" y1="${-(r_bore + t2)}" x2="${-textSz * 3.5}" y2="${-(r_bore + t2 + textSz * 3.0)}" stroke="#fbbf24" stroke-width="0.5"/>
          <line x1="${-textSz * 3.5}" y1="${-(r_bore + t2 + textSz * 3.0)}" x2="${-textSz * 8.0}" y2="${-(r_bore + t2 + textSz * 3.0)}" stroke="#fbbf24" stroke-width="0.5"/>
          <text x="${-textSz * 8.2}" y="${-(r_bore + t2 + textSz * 3.3)}" fill="#fbbf24" font-size="${textSz * 0.85}" font-weight="700" text-anchor="end">Rãnh then ${bk.toFixed(0)}x${t2.toFixed(1)} (DIN 6885)</text>
        `;

        g.innerHTML += dimsHtml;
      }

      // Khung hình quan sát cân đối bao trọn mặt cắt và chuỗi kích thước 2 bên
      const padY = Math.max(textSz * 12.0, Ra * 0.22);
      const padX = Math.max(textSz * 14.0, Ra * 0.25);
      const raw_min_X = x_Dn - padX;
      const raw_max_X = x_da + padX;
      const min_Y = -Ra - padY;
      const max_Y = Ra + padY;
      const vH = max_Y - min_Y;
      const min_vW = (raw_max_X - raw_min_X);
      const vW = Math.max(min_vW, vH * 1.35);
      const mid_X = (raw_min_X + raw_max_X) / 2.0;
      const vX = mid_X - vW / 2.0;

      document.getElementById('cadSvg').setAttribute('viewBox', `${vX.toFixed(2)} ${min_Y.toFixed(2)} ${vW.toFixed(2)} ${vH.toFixed(2)}`);
      document.getElementById('hudStatus').innerText = `Mặt cắt dọc trục A-A chuẩn ${standard} | B1: ${B1.toFixed(1)} mm | da: Ø${da.toFixed(1)} | df: Ø${df.toFixed(1)} | NL: ${NL.toFixed(1)} mm`;
    }'''

    # Replace renderSectionView
    pattern_render = re.compile(r'    function renderSectionView\(g, showDims\) \{.*?document\.getElementById\(\'hudStatus\'\)\.innerText = `.*?\n    \}', re.DOTALL)
    if not pattern_render.search(content):
        print("ERROR: Could not find renderSectionView pattern")
        return False
    content = pattern_render.sub(new_renderSectionView, content)
    print("renderSectionView replaced successfully!")

    # 2. NEW writeSection IMPLEMENTATION (DXF)
    new_writeSection = '''      const writeSection = (ox = 0, oy = 0) => {
        const isKWN001 = (standard === 'KWN_001');
        const w2 = B1 / 2.0;
        const w_tip2 = isKWN001 ? (w2 * 0.82) : (w2 * 0.72);
        const rtip = isKWN001 ? Math.min(2.5, B1 * 0.08) : Math.min(6.0, B1 * 0.10);
        const w_flat2 = w_tip2 - rtip;

        const dw = AppState.dw || 80.0;
        const r_bore = dw / 2.0;
        const NL = AppState.hub_NL || 180.0;
        const hubType = AppState.hubType || 'Type_C';

        let rawDn = AppState.hub_Dn || Math.max(dw + 35.0, Math.min(ds - 20.0, dw * 1.65));
        const max_RH = Math.max(r_bore + 12.0, Rf - 5.0);
        const min_RH = r_bore + 8.0;
        const RH = Math.max(min_RH, Math.min(max_RH, rawDn / 2.0));
        const Dn = RH * 2.0;

        let xh_L, xh_R;
        if (hubType === 'Type_A') {
          xh_L = -w2;
          xh_R = +w2;
        } else if (hubType === 'Type_B') {
          xh_L = -w2;
          xh_R = -w2 + NL;
        } else {
          xh_L = -NL / 2.0;
          xh_R = +NL / 2.0;
        }

        const bk = AppState.key_b || 10.0;
        const t2 = AppState.key_t2 || 3.3;

        // Đa giác NỬA TRÊN (y > oy)
        const polyTop = [];
        if (hubType === 'Type_A') {
          polyTop.push({ x: ox - w2, y: oy + r_bore });
          polyTop.push({ x: ox - w2, y: oy + Rf });
          polyTop.push({ x: ox - w_tip2, y: oy + (Ra - rtip) });
          polyTop.push({ x: ox - w_flat2, y: oy + Ra });
          polyTop.push({ x: ox + w_flat2, y: oy + Ra });
          polyTop.push({ x: ox + w_tip2, y: oy + (Ra - rtip) });
          polyTop.push({ x: ox + w2, y: oy + Rf });
          polyTop.push({ x: ox + w2, y: oy + r_bore });
          polyTop.push({ x: ox + bk / 2, y: oy + r_bore });
          polyTop.push({ x: ox + bk / 2, y: oy + r_bore + t2 });
          polyTop.push({ x: ox - bk / 2, y: oy + r_bore + t2 });
          polyTop.push({ x: ox - bk / 2, y: oy + r_bore });
        } else if (hubType === 'Type_B') {
          polyTop.push({ x: ox + xh_L, y: oy + r_bore });
          polyTop.push({ x: ox + xh_L, y: oy + Rf });
          polyTop.push({ x: ox - w_tip2, y: oy + (Ra - rtip) });
          polyTop.push({ x: ox - w_flat2, y: oy + Ra });
          polyTop.push({ x: ox + w_flat2, y: oy + Ra });
          polyTop.push({ x: ox + w_tip2, y: oy + (Ra - rtip) });
          polyTop.push({ x: ox + w2, y: oy + Rf });
          polyTop.push({ x: ox + w2, y: oy + RH });
          polyTop.push({ x: ox + xh_R, y: oy + RH });
          polyTop.push({ x: ox + xh_R, y: oy + r_bore });
          polyTop.push({ x: ox + bk / 2, y: oy + r_bore });
          polyTop.push({ x: ox + bk / 2, y: oy + r_bore + t2 });
          polyTop.push({ x: ox - bk / 2, y: oy + r_bore + t2 });
          polyTop.push({ x: ox - bk / 2, y: oy + r_bore });
        } else {
          polyTop.push({ x: ox + xh_L, y: oy + r_bore });
          polyTop.push({ x: ox + xh_L, y: oy + RH });
          polyTop.push({ x: ox - w2, y: oy + RH });
          polyTop.push({ x: ox - w2, y: oy + Rf });
          polyTop.push({ x: ox - w_tip2, y: oy + (Ra - rtip) });
          polyTop.push({ x: ox - w_flat2, y: oy + Ra });
          polyTop.push({ x: ox + w_flat2, y: oy + Ra });
          polyTop.push({ x: ox + w_tip2, y: oy + (Ra - rtip) });
          polyTop.push({ x: ox + w2, y: oy + Rf });
          polyTop.push({ x: ox + w2, y: oy + RH });
          polyTop.push({ x: ox + xh_R, y: oy + RH });
          polyTop.push({ x: ox + xh_R, y: oy + r_bore });
          polyTop.push({ x: ox + bk / 2, y: oy + r_bore });
          polyTop.push({ x: ox + bk / 2, y: oy + r_bore + t2 });
          polyTop.push({ x: ox - bk / 2, y: oy + r_bore + t2 });
          polyTop.push({ x: ox - bk / 2, y: oy + r_bore });
        }

        // Đa giác NỬA DƯỚI (y < oy, đối xứng hoàn toàn)
        const polyBot = [];
        if (hubType === 'Type_A') {
          polyBot.push({ x: ox - w2, y: oy - r_bore });
          polyBot.push({ x: ox - w2, y: oy - Rf });
          polyBot.push({ x: ox - w_tip2, y: oy - (Ra - rtip) });
          polyBot.push({ x: ox - w_flat2, y: oy - Ra });
          polyBot.push({ x: ox + w_flat2, y: oy - Ra });
          polyBot.push({ x: ox + w_tip2, y: oy - (Ra - rtip) });
          polyBot.push({ x: ox + w2, y: oy - Rf });
          polyBot.push({ x: ox + w2, y: oy - r_bore });
        } else if (hubType === 'Type_B') {
          polyBot.push({ x: ox + xh_L, y: oy - r_bore });
          polyBot.push({ x: ox + xh_L, y: oy - Rf });
          polyBot.push({ x: ox - w_tip2, y: oy - (Ra - rtip) });
          polyBot.push({ x: ox - w_flat2, y: oy - Ra });
          polyBot.push({ x: ox + w_flat2, y: oy - Ra });
          polyBot.push({ x: ox + w_tip2, y: oy - (Ra - rtip) });
          polyBot.push({ x: ox + w2, y: oy - Rf });
          polyBot.push({ x: ox + w2, y: oy - RH });
          polyBot.push({ x: ox + xh_R, y: oy - RH });
          polyBot.push({ x: ox + xh_R, y: oy - r_bore });
        } else {
          polyBot.push({ x: ox + xh_L, y: oy - r_bore });
          polyBot.push({ x: ox + xh_L, y: oy - RH });
          polyBot.push({ x: ox - w2, y: oy - RH });
          polyBot.push({ x: ox - w2, y: oy - Rf });
          polyBot.push({ x: ox - w_tip2, y: oy - (Ra - rtip) });
          polyBot.push({ x: ox - w_flat2, y: oy - Ra });
          polyBot.push({ x: ox + w_flat2, y: oy - Ra });
          polyBot.push({ x: ox + w_tip2, y: oy - (Ra - rtip) });
          polyBot.push({ x: ox + w2, y: oy - Rf });
          polyBot.push({ x: ox + w2, y: oy - RH });
          polyBot.push({ x: ox + xh_R, y: oy - RH });
          polyBot.push({ x: ox + xh_R, y: oy - r_bore });
        }

        // 1. Xuất đường bao 2 nửa (SECTION_CONTOUR)
        addPolyline(polyTop, 'SECTION_CONTOUR', true);
        addPolyline(polyBot, 'SECTION_CONTOUR', true);

        // 2. Gạch mặt cắt ANSI 31 cho cả 2 nửa
        const hatchStep = Math.max(6.0, Math.min(14.0, (Ra - r_bore) * 0.025));
        const hatchPolygon = (poly) => {
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
        };

        hatchPolygon(polyTop);
        hatchPolygon(polyBot);

        // 3. Trục tâm ngang (Shaft Axis) & Trục tâm đứng (Sprocket Axis)
        const L_axis_x = Math.max(NL, B1 * 2) * 0.85;
        addLine(ox - L_axis_x, oy, ox + L_axis_x, oy, 'CENTER_LINES');
        addLine(ox, oy - Ra - 25, ox, oy + Ra + 25, 'CENTER_LINES');

        // 4. Kích thước ngang (B1 đỉnh, NL đáy)
        const dimH = Math.max(3.2, p * 0.028);
        const aSz = dimH * 1.1;

        // B1
        const y_b1 = oy + Ra + 12;
        addLine(ox - w2, y_b1, ox + w2, y_b1, 'SECTION_DIMS');
        addLine(ox - w2, oy + Ra, ox - w2, y_b1 + 3, 'SECTION_DIMS');
        addLine(ox + w2, oy + Ra, ox + w2, y_b1 + 3, 'SECTION_DIMS');
        addArrowSolid(ox - w2, y_b1, ox - w2 + aSz, y_b1, aSz * 0.8, 'SECTION_DIMS');
        addArrowSolid(ox + w2, y_b1, ox + w2 - aSz, y_b1, aSz * 0.8, 'SECTION_DIMS');
        addText(ox - dimH * 2.2, y_b1 + 3, dimH, 'B1 = ' + B1.toFixed(1) + ' mm', 'SECTION_DIMS');

        // NL
        if (hubType !== 'Type_A') {
          const y_nl = oy - RH - 15;
          addLine(ox + xh_L, y_nl, ox + xh_R, y_nl, 'SECTION_DIMS');
          addLine(ox + xh_L, oy - RH, ox + xh_L, y_nl - 3, 'SECTION_DIMS');
          addLine(ox + xh_R, oy - RH, ox + xh_R, y_nl - 3, 'SECTION_DIMS');
          addArrowSolid(ox + xh_L, y_nl, ox + xh_L + aSz, y_nl, aSz * 0.8, 'SECTION_DIMS');
          addArrowSolid(ox + xh_R, y_nl, ox + xh_R - aSz, y_nl, aSz * 0.8, 'SECTION_DIMS');
          const hubLbl = (hubType === 'Type_B') ? ('NL (Type B) = ' + NL.toFixed(0) + ' mm') : ('NL (Type C) = ' + NL.toFixed(0) + ' mm');
          addText(ox - dimH * 3.5, y_nl - dimH * 1.2, dimH, hubLbl, 'SECTION_DIMS');
        }

        // 5. Chuỗi kích thước đường kính đứng bên phải (df, d0, da)
        const x_base_dxf = ox + Math.max(xh_R, w2) + 15.0;
        const colStep_dxf = dimH * 4.5;
        const x_df_dxf = x_base_dxf + colStep_dxf * 1;
        const x_d0_dxf = x_base_dxf + colStep_dxf * 2;
        const x_da_dxf = x_base_dxf + colStep_dxf * 3;

        const addDualDim = (xCol, yVal, labelText, yTextOffset) => {
          addLine(ox + w2, oy + yVal, xCol + 5, oy + yVal, 'SECTION_DIMS');
          addLine(ox + w2, oy - yVal, xCol + 5, oy - yVal, 'SECTION_DIMS');
          addLine(xCol, oy - yVal, xCol, oy + yVal, 'SECTION_DIMS');
          addArrowSolid(xCol, oy + yVal, xCol, oy + yVal - aSz, aSz * 0.8, 'SECTION_DIMS');
          addArrowSolid(xCol, oy - yVal, xCol, oy - yVal + aSz, aSz * 0.8, 'SECTION_DIMS');
          addText(xCol + dimH * 0.4, oy + yTextOffset, dimH, labelText, 'SECTION_DIMS');
        };

        addDualDim(x_df_dxf, Rf, '%%c df = ' + df.toFixed(2) + ' (h11)', Rf * 0.4);
        addDualDim(x_d0_dxf, R0, '%%c d0 = ' + d0.toFixed(2), 0);
        addDualDim(x_da_dxf, Ra, '%%c da = ' + da.toFixed(2), -Rf * 0.4);

        // 6. Kích thước đường kính đứng bên trái (dw, Dn)
        const x_base_L_dxf = ox + Math.min(xh_L, -w2) - 15.0;
        const x_dw_dxf = x_base_L_dxf - colStep_dxf * 1;
        const x_Dn_dxf = x_base_L_dxf - colStep_dxf * 2;

        addDualDim(x_dw_dxf, r_bore, '%%c dw = ' + dw.toFixed(1) + ' (H7)', r_bore * 0.4);
        if (hubType !== 'Type_A') {
          addDualDim(x_Dn_dxf, RH, '%%c Dn = ' + Dn.toFixed(1), -RH * 0.4);
        }

        // Leader then DIN 6885
        addCadLeaderDim(ox, oy + r_bore + t2, 135, dimH * 3.5, dimH * 6.5, 'Then ' + bk.toFixed(0) + 'x' + t2.toFixed(1) + ' (DIN 6885)', 'SECTION_DIMS', dimH, aSz);
      };'''

    pattern_write = re.compile(r'      const writeSection = \(ox = 0, oy = 0\) => \{.*?addDiaRef\(r_bore, dw, \'dw \(Lo truc\)\', \'SECTION_DIMS\'\);\n      \};', re.DOTALL)
    if not pattern_write.search(content):
        print("ERROR: Could not find writeSection pattern")
        return False
    content = pattern_write.sub(new_writeSection, content)
    print("writeSection replaced successfully!")

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("All changes written to index.html successfully!")
    return True

if __name__ == '__main__':
    apply_overhaul()
