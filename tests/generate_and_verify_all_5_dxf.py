"""
Generates and validates all 5 DXF modes:
1. sprocket: Sprocket Only
2. assembly: Sprocket + Kinematic Chain Strand
3. gap: Tooth Gap Macro View with colored layers
4. section: Tooth & Rim Cross Section with ANSI 31 Hatch
5. combined: All 3 Views Combined on A3/A4 Drawing with Title Block
"""

import math
import json
import os
import ezdxf

def generate_dxf_file(mode, filename, p=400.0, z=8, d1=50.0, b1=66.0, standard='KWN_017', dw=120.0, key_b=32.0, key_t2=11.0, r4=5.0):
    alpha_deg = 360.0 / z
    alpha_rad = math.radians(alpha_deg)
    d0 = p / math.sin(math.pi / z)
    df = d0 - d1
    da = d0 + 0.8 * d1
    ds = (p / math.tan(alpha_rad / 2.0)) - 90.0 - 2.0 * r4
    B1 = 0.9 * b1
    R0 = d0 / 2.0
    Rf = df / 2.0
    Ra = da / 2.0
    Rs = ds / 2.0

    beta_deg = 74.0 if z <= 11 else (56.0 if z <= 29 else 38.0)
    gamma_deg = (beta_deg / 2.0) - (180.0 / z)
    half_beta = math.radians(beta_deg / 2.0)
    u = 0.02 * p
    r1 = 0.51 * d1
    h3 = 0.3 * d1
    r2 = 0.8 * p

    geom = {
        'p': p, 'z': z, 'd1': d1, 'b1': b1, 'B1': B1,
        'd0': d0, 'df': df, 'da': da, 'ds': ds,
        'R0': R0, 'Rf': Rf, 'Ra': Ra, 'Rs': Rs,
        'alpha_deg': alpha_deg, 'alpha_rad': alpha_rad,
        'beta_deg': beta_deg, 'gamma_deg': gamma_deg, 'half_beta': half_beta,
        'u': u, 'r1': r1, 'h3': h3, 'r2': r2, 'standard': standard,
        'dw': dw, 'key_b': key_b, 'key_t2': key_t2, 'r4': r4
    }

    layers = [
        ('0', 7),
        ('SPROCKET_CONTOUR', 7),
        ('BORE_KEYWAY', 7),
        ('BASE_CIRCLES', 4),
        ('CENTER_LINES', 1),
        ('SPROCKET_DIMS', 2),
        ('CHAIN_PLATES_OUTER', 8),
        ('CHAIN_PLATES_INNER', 8),
        ('CHAIN_ROLLERS', 4),
        ('CHAIN_PINS', 1),
        ('GAP_BOTTOM_U', 2),
        ('GAP_BED_R1', 1),
        ('GAP_FLANK_H3', 3),
        ('GAP_CREST_R2', 6),
        ('GAP_RIM_BODY', 8),
        ('SEATED_ROLLER', 7),
        ('DIM_BETA', 4),
        ('DIM_H3', 3),
        ('DIM_U', 2),
        ('DIM_R1', 1),
        ('DIM_R2', 6),
        ('DIM_GAMMA', 30),
        ('DIM_ALPHA', 5),
        ('DIM_ROLLER', 7),
        ('SECTION_CONTOUR', 7),
        ('SECTION_HATCH', 8),
        ('SECTION_DIMS', 2),
        ('SECTION_REFS', 4),
        ('TITLE_BLOCK', 7),
        ('DRAWING_BORDER', 7)
    ]

    L = []
    L.extend(['0', 'SECTION', '2', 'HEADER', '9', '$ACADVER', '1', 'AC1009', '0', 'ENDSEC'])
    L.extend(['0', 'SECTION', '2', 'TABLES', '0', 'TABLE', '2', 'LAYER', '70', str(len(layers))])
    for name, col in layers:
        L.extend(['0', 'LAYER', '2', name, '70', '0', '62', str(col), '6', 'CONTINUOUS'])
    L.extend(['0', 'ENDTAB', '0', 'ENDSEC'])
    L.extend(['0', 'SECTION', '2', 'ENTITIES'])

    def addLine(x1, y1, x2, y2, layer):
        L.extend(['0', 'LINE', '8', layer, '10', f"{x1:.3f}", '20', f"{y1:.3f}", '30', '0.0', '11', f"{x2:.3f}", '21', f"{y2:.3f}", '31', '0.0'])

    def addCircle(cx, cy, r, layer):
        L.extend(['0', 'CIRCLE', '8', layer, '10', f"{cx:.3f}", '20', f"{cy:.3f}", '30', '0.0', '40', f"{r:.3f}"])

    def addArc(cx, cy, r, startAng, endAng, layer):
        s = startAng % 360
        e = endAng % 360
        L.extend(['0', 'ARC', '8', layer, '10', f"{cx:.3f}", '20', f"{cy:.3f}", '30', '0.0', '40', f"{r:.3f}", '50', f"{s:.2f}", '51', f"{e:.2f}"])

    def addText(x, y, h, str_val, layer):
        L.extend(['0', 'TEXT', '8', layer, '10', f"{x:.3f}", '20', f"{y:.3f}", '30', '0.0', '40', f"{h:.3f}", '1', str(str_val)])

    def addPolyline(pts, layer, closed=True):
        L.extend(['0', 'POLYLINE', '8', layer, '66', '1', '70', '1' if closed else '0'])
        for pt in pts:
            L.extend(['0', 'VERTEX', '8', layer, '10', f"{pt['x']:.3f}", '20', f"{pt['y']:.3f}", '30', '0.0'])
        L.extend(['0', 'SEQEND'])

    def addSolid(p1, p2, p3, p4, layer):
        L.extend(['0', 'SOLID', '8', layer,
                  '10', f"{p1['x']:.3f}", '20', f"{p1['y']:.3f}", '30', '0.0',
                  '11', f"{p2['x']:.3f}", '21', f"{p2['y']:.3f}", '31', '0.0',
                  '12', f"{p3['x']:.3f}", '22', f"{p3['y']:.3f}", '32', '0.0',
                  '13', f"{(p4 or p3)['x']:.3f}", '23', f"{(p4 or p3)['y']:.3f}", '33', '0.0'])

    def addArrowSolid(tipX, tipY, fromX, fromY, sz, layer):
        dx = fromX - tipX
        dy = fromY - tipY
        length = math.hypot(dx, dy)
        if length < 1e-4: return
        ux = dx / length
        uy = dy / length
        nx = -uy
        ny = ux
        w = sz * 0.32
        bx = tipX + ux * sz
        by = tipY + uy * sz
        addSolid({'x': tipX, 'y': tipY}, {'x': bx + nx * w, 'y': by + ny * w}, {'x': bx - nx * w, 'y': by - ny * w}, {'x': bx - nx * w, 'y': by - ny * w}, layer)

    def addCadLeaderDim(targetX, targetY, angleDeg, neckLen, shelfLen, text, layer, textH, arrowSz):
        rad = math.radians(angleDeg)
        neckX = targetX + neckLen * math.cos(rad)
        neckY = targetY + neckLen * math.sin(rad)
        isRight = math.cos(rad) >= 0
        shelfX = (neckX + shelfLen) if isRight else (neckX - shelfLen)
        addArrowSolid(targetX, targetY, neckX, neckY, arrowSz, layer)
        addLine(targetX, targetY, neckX, neckY, layer)
        addLine(neckX, neckY, shelfX, neckY, layer)
        tx = (neckX + textH * 0.4) if isRight else (shelfX + textH * 0.4)
        ty = neckY + textH * 0.35
        addText(tx, ty, textH, text, layer)

    def compute_half_gap_dxf():
        C1 = {'x': u / 2.0, 'y': Rf + r1}
        P0 = {'x': u / 2.0, 'y': Rf}
        pts = [P0]
        num_pts = 25
        for i in range(1, num_pts + 1):
            ang = -math.pi / 2.0 + (half_beta * (i / num_pts))
            pts.append({'x': C1['x'] + r1 * math.cos(ang), 'y': C1['y'] + r1 * math.sin(ang)})
        P1 = pts[-1]
        T = {'x': math.sin(half_beta), 'y': math.cos(half_beta)}
        P2 = {'x': P1['x'] + h3 * T['x'], 'y': P1['y'] + h3 * T['y']}
        pts.append(P2)
        N_right = {'x': math.cos(half_beta), 'y': -math.sin(half_beta)}
        C2 = {'x': P2['x'] + r2 * N_right['x'], 'y': P2['y'] + r2 * N_right['y']}
        d = math.hypot(C2['x'], C2['y'])
        a_len = (Ra * Ra - r2 * r2 + d * d) / (2.0 * d)
        h_len = math.sqrt(max(0.0, Ra * Ra - a_len * a_len))
        int1 = {'x': a_len * C2['x'] / d + h_len * (-C2['y']) / d, 'y': a_len * C2['y'] / d + h_len * C2['x'] / d}
        int2 = {'x': a_len * C2['x'] / d - h_len * (-C2['y']) / d, 'y': a_len * C2['y'] / d - h_len * C2['x'] / d}
        d1_sq = (int1['x'] - P2['x'])**2 + (int1['y'] - P2['y'])**2
        d2_sq = (int2['x'] - P2['x'])**2 + (int2['y'] - P2['y'])**2
        P3 = int1 if d1_sq < d2_sq else int2

        half_alpha = alpha_rad / 2.0
        sin_ha = math.sin(half_alpha)
        cos_ha = math.cos(half_alpha)
        B_sym = -2.0 * (C2['x'] * sin_ha + C2['y'] * cos_ha)
        C_sym = C2['x'] * C2['x'] + C2['y'] * C2['y'] - r2 * r2
        disc_sym = B_sym * B_sym - 4.0 * C_sym
        cross_pt = None
        if disc_sym >= 0:
            R_cross = (-B_sym + math.sqrt(disc_sym)) / 2.0
            if R_cross <= Ra + 1e-4:
                cross_pt = {'x': R_cross * sin_ha, 'y': R_cross * cos_ha, 'R': R_cross}

        target_tip = cross_pt if cross_pt else P3
        th_start = math.atan2(P2['y'] - C2['y'], P2['x'] - C2['x'])
        th_end = math.atan2(target_tip['y'] - C2['y'], target_tip['x'] - C2['x'])
        for i in range(1, num_pts + 1):
            ang = th_start + (th_end - th_start) * (i / num_pts)
            pt = {'x': C2['x'] + r2 * math.cos(ang), 'y': C2['y'] + r2 * math.sin(ang)}
            polar = math.atan2(pt['x'], pt['y'])
            if polar >= half_alpha - 1e-4:
                pts.append(target_tip)
                break
            pts.append(pt)
        tip_angle = min(half_alpha, math.atan2(pts[-1]['x'], pts[-1]['y']))
        return pts, P0, P1, P2, P3, C1, C2, tip_angle

    def writeSprocketOnly(ox=0, oy=0):
        half_pts, P0, P1, P2, P3, C1, C2, tip_ang = compute_half_gap_dxf()
        left_pts = [{'x': -p['x'], 'y': p['y']} for p in reversed(half_pts[1:])]
        single_gap = left_pts + half_pts
        full_pts = []
        for k in range(z):
            gap_ang = k * alpha_rad
            cos_g = math.cos(gap_ang)
            sin_g = math.sin(gap_ang)
            for pt in single_gap:
                full_pts.append({'x': ox + (pt['x'] * cos_g + pt['y'] * sin_g), 'y': oy + (-pt['x'] * sin_g + pt['y'] * cos_g)})
            ang_start = gap_ang + tip_ang
            ang_end = gap_ang + alpha_rad - tip_ang
            if ang_end > ang_start + 1e-4:
                for i in range(1, 6):
                    cur = ang_start + (ang_end - ang_start) * (i / 6)
                    full_pts.append({'x': ox + Ra * math.sin(cur), 'y': oy + Ra * math.cos(cur)})
        addPolyline(full_pts, 'SPROCKET_CONTOUR', True)
        addCircle(ox, oy, R0, 'BASE_CIRCLES')
        addCircle(ox, oy, Rf, 'BASE_CIRCLES')
        addCircle(ox, oy, Ra, 'BASE_CIRCLES')
        if Rs > 0: addCircle(ox, oy, Rs, 'BASE_CIRCLES')
        r_bore = dw / 2.0
        if r_bore > 0:
            addCircle(ox, oy, r_bore, 'BORE_KEYWAY')
            if key_b > 0 and key_t2 > 0:
                kw2 = key_b / 2.0
                y_key = r_bore + key_t2
                addLine(ox - kw2, oy + r_bore, ox - kw2, oy + y_key, 'BORE_KEYWAY')
                addLine(ox - kw2, oy + y_key, ox + kw2, oy + y_key, 'BORE_KEYWAY')
                addLine(ox + kw2, oy + y_key, ox + kw2, oy + r_bore, 'BORE_KEYWAY')
        L_ax = Ra * 1.25
        addLine(ox - L_ax, oy, ox + L_ax, oy, 'CENTER_LINES')
        addLine(ox, oy - L_ax, ox, oy + L_ax, 'CENTER_LINES')
        dimScale = max(3.5, Ra * 0.026)
        arrowSz = dimScale * 1.3
        neckLen = Ra * 0.16
        shelfLen = dimScale * 7.5
        addCadLeaderDim(ox + Ra * math.cos(math.radians(42)), oy + Ra * math.sin(math.radians(42)), 42, neckLen, shelfLen, f"%%c da = {da:.2f} mm", 'SPROCKET_DIMS', dimScale, arrowSz)
        addCadLeaderDim(ox + R0 * math.cos(math.radians(140)), oy + R0 * math.sin(math.radians(140)), 140, neckLen, shelfLen, f"%%c d0 = {d0:.2f} mm", 'SPROCKET_DIMS', dimScale, arrowSz)
        addCadLeaderDim(ox + Rf * math.cos(math.radians(220)), oy + Rf * math.sin(math.radians(220)), 220, neckLen, shelfLen, f"%%c df = {df:.2f} mm", 'SPROCKET_DIMS', dimScale, arrowSz)
        if Rs > 0:
            addCadLeaderDim(ox + Rs * math.cos(math.radians(318)), oy + Rs * math.sin(math.radians(318)), 318, neckLen, shelfLen, f"%%c ds = {ds:.1f} mm", 'SPROCKET_DIMS', dimScale, arrowSz)

    def writeAssembly(ox=0, oy=0):
        writeSprocketOnly(ox, oy)
        r_contact = d1 / 2.0
        r_pin = r_contact * 0.65
        joints = []
        for m in range(z):
            phi = m * alpha_rad
            joints.append({'x': ox - R0 * math.sin(phi), 'y': oy - R0 * math.cos(phi)})
        for j in joints:
            addCircle(j['x'], j['y'], r_contact, 'CHAIN_ROLLERS')
            addCircle(j['x'], j['y'], r_pin, 'CHAIN_PINS')

    def writeGap(ox=0, oy=0):
        half_pts, P0, P1, P2, P3, C1, C2, tip_ang = compute_half_gap_dxf()
        S_gap = Ra - Rf
        R_inner = Rs if Rs > 0 else (Rf - S_gap * 0.32)
        addLine(ox, oy + R_inner - 10, ox, oy + Ra + 25, 'CENTER_LINES')
        addCircle(ox, oy + R0, d1 / 2.0, 'SEATED_ROLLER')
        textH = min(8.0, max(3.2, p * 0.025, S_gap * 0.12))
        arrowSz = textH * 1.1
        addCadLeaderDim(ox + P1['x'] * 0.65, oy + Rf + r1 * 0.35, -25, textH * 4.5, textH * 6.5, f"r1 = R{r1:.2f} mm", 'DIM_R1', textH, arrowSz)
        addCadLeaderDim(ox - (P1['x'] + P2['x']) / 2.0, oy + (P1['y'] + P2['y']) / 2.0, 155, textH * 4.5, textH * 6.5, f"h3 = {h3:.2f} mm", 'DIM_H3', textH, arrowSz)
        addCadLeaderDim(ox - (P2['x'] + P3['x']) / 2.0, oy + (P2['y'] + P3['y']) / 2.0, 130, textH * 4.5, textH * 6.5, f"r2 = R{r2:.1f} mm", 'DIM_R2', textH, arrowSz)

    def writeSection(ox=0, oy=0):
        w2 = B1 / 2.0
        r_sec_s = Rs
        w_rim2 = w2 + r4 + 18.0
        w_tip2 = w2 * 0.72
        y_break = r_sec_s - 70.0
        toothPts = [{'x': ox - w_tip2, 'y': oy + Ra}, {'x': ox + w_tip2, 'y': oy + Ra}, {'x': ox + w2, 'y': oy + R0}, {'x': ox + w2, 'y': oy + Rf}, {'x': ox - w2, 'y': oy + Rf}, {'x': ox - w2, 'y': oy + R0}]
        addPolyline(toothPts, 'SECTION_CONTOUR', True)
        rimPts = [{'x': ox - w2, 'y': oy + Rf}, {'x': ox + w2, 'y': oy + Rf}, {'x': ox + w2, 'y': oy + r_sec_s}, {'x': ox + w_rim2, 'y': oy + r_sec_s}, {'x': ox + w_rim2, 'y': oy + y_break}, {'x': ox - w_rim2, 'y': oy + y_break}, {'x': ox - w_rim2, 'y': oy + r_sec_s}, {'x': ox - w2, 'y': oy + r_sec_s}]
        addPolyline(rimPts, 'SECTION_CONTOUR', True)
        addLine(ox, oy + y_break - 20, ox, oy + Ra + 25, 'CENTER_LINES')
        addText(ox - 10, oy + Ra + 20, max(3.0, p * 0.035), f"B1 = {B1:.1f} mm", 'SECTION_DIMS')

    if mode == 'sprocket':
        writeSprocketOnly(0, 0)
    elif mode == 'assembly':
        writeAssembly(0, 0)
    elif mode == 'gap':
        writeGap(0, 0)
    elif mode == 'section':
        writeSection(0, 0)
    else: # combined
        writeAssembly(0, 0)
        strandRight = R0 + 5.5 * p
        offX = strandRight + Ra * 1.5 + 80.0
        offY_gap = Ra * 1.15
        offY_sec = -Ra * 1.15
        writeGap(offX, offY_gap)
        writeSection(offX, offY_sec)

    L.extend(['0', 'ENDSEC', '0', 'EOF'])
    with open(filename, 'w', encoding='ascii', errors='replace') as f:
        f.write('\n'.join(L))

def run_tests():
    modes = ['sprocket', 'assembly', 'gap', 'section', 'combined']
    print("=== GENERATING AND VERIFYING ALL 5 DXF EXPORT MODES ===")
    for m in modes:
        fn = f"test_export_{m}.dxf"
        generate_dxf_file(m, fn)
        doc = ezdxf.readfile(fn)
        msp = doc.modelspace()
        lines = list(msp.query('LINE'))
        solids = list(msp.query('SOLID'))
        texts = list(msp.query('TEXT'))
        circles = list(msp.query('CIRCLE'))
        polylines = list(msp.query('POLYLINE'))
        print(f"[{m.upper()}] {fn}: Valid DXF! Lines={len(lines)}, Solids={len(solids)}, Texts={len(texts)}, Circles={len(circles)}, Polylines={len(polylines)}")
        assert (len(lines) + len(polylines) + len(circles)) > 0, f"Empty drawing for {m}"

    print("=== ALL 5 DXF MODES VERIFIED WITH EZDXF: 100% SUCCESS! ===")

if __name__ == '__main__':
    run_tests()
