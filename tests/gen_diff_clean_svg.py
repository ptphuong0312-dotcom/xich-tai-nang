import math

z = 6
p1 = 80.0
p2 = 120.0
d1 = 25.0
b1 = 25.0
g = 35.0
r4 = 3.0

n_factor = 1.0 / math.sin(math.pi / z)
f_factor = 2.0 * (1.0 - math.cos(math.pi / z))
d0 = n_factor * math.sqrt((p1 + p2)**2 - f_factor * p1 * p2)
df = d0 - d1
da = d0 + 0.8 * d1
R0 = d0 / 2.0
Rf = df / 2.0
Ra = da / 2.0

theta1 = 2.0 * math.asin(p1 / d0)
theta2 = 2.0 * math.asin(p2 / d0)
tc = theta1 + theta2

# Recess diameter ds
H2 = math.sqrt(R0**2 - (p2 / 2.0)**2)
ds = 2.0 * (H2 - g / 2.0) - 2.0 * r4
Rs = ds / 2.0

# Tooth profile over p1 (KWN 017 standard)
# For the tooth of angular width theta1, the effective tooth pitch is p1.
# Equivalent z_eff for beta: z_eff = 360 / theta1_deg
z_eff = 360.0 / math.degrees(theta1)
beta_deg = 74.0 if z_eff <= 11 else (56.0 if z_eff <= 29 else 38.0)
half_beta = math.radians(beta_deg / 2.0)
u = 0.02 * p1
r1 = 0.51 * d1
h3 = 0.3 * d1
r2 = 0.8 * p1

# Half-gap / flank points for KWN 017
# Bed arc r1 from u/2
num_bed = 10
theta_bed = math.pi / 2.0 - half_beta
C1 = {'x': u / 2.0, 'y': Rf + r1}

pts_flank = [{'x': 0.0, 'y': Rf}, {'x': u / 2.0, 'y': Rf}]
for i in range(1, num_bed + 1):
    th = theta_bed * (i / num_bed)
    pts_flank.append({'x': C1['x'] + r1 * math.sin(th), 'y': C1['y'] - r1 * math.cos(th)})

P1 = pts_flank[-1]
T = {'x': math.sin(half_beta), 'y': math.cos(half_beta)}
P2 = {'x': P1['x'] + h3 * T['x'], 'y': P1['y'] + h3 * T['y']}
pts_flank.append(P2)

N_right = {'x': math.cos(half_beta), 'y': -math.sin(half_beta)}
C2 = {'x': P2['x'] + r2 * N_right['x'], 'y': P2['y'] + r2 * N_right['y']}

# Intersection of circle (C2, r2) with tip circle Ra
d = math.hypot(C2['x'], C2['y'])
a_len = (Ra * Ra - r2 * r2 + d * d) / (2.0 * d)
h_len = math.sqrt(max(0, Ra * Ra - a_len * a_len))
int1 = {'x': a_len * C2['x'] / d + h_len * (-C2['y']) / d, 'y': a_len * C2['y'] / d + h_len * C2['x'] / d}
int2 = {'x': a_len * C2['x'] / d - h_len * (-C2['y']) / d, 'y': a_len * C2['y'] / d - h_len * C2['x'] / d}
P3 = int1 if math.hypot(int1['x'] - P2['x'], int1['y'] - P2['y']) < math.hypot(int2['x'] - P2['x'], int2['y'] - P2['y']) else int2

# Tooth apex check with tooth symmetry axis (ha1 = theta1 / 2)
ha1 = theta1 / 2.0
sin_ha = math.sin(ha1)
cos_ha = math.cos(ha1)
B_sym = -2.0 * (C2['x'] * sin_ha + C2['y'] * cos_ha)
C_sym = C2['x']**2 + C2['y']**2 - r2**2
disc_sym = B_sym**2 - 4.0 * C_sym
cross_pt = None
if disc_sym >= 0:
    R_cross = (-B_sym + math.sqrt(disc_sym)) / 2.0
    if R_cross <= Ra + 1e-4:
        cross_pt = {'x': R_cross * sin_ha, 'y': R_cross * cos_ha}

target_tip = cross_pt or P3
th_start = math.atan2(P2['y'] - C2['y'], P2['x'] - C2['x'])
th_end = math.atan2(target_tip['y'] - C2['y'], target_tip['x'] - C2['x'])

num_r2 = 12
for i in range(1, num_r2 + 1):
    ang = th_start + (th_end - th_start) * (i / num_r2)
    pt = {'x': C2['x'] + r2 * math.cos(ang), 'y': C2['y'] + r2 * math.sin(ang)}
    polar = math.atan2(pt['x'], pt['y'])
    if polar >= ha1 - 1e-4:
        pts_flank.append(target_tip)
        break
    pts_flank.append(pt)

flank_polar = [{'r': math.hypot(p['x'], p['y']), 'xi': math.atan2(p['x'], p['y'])} for p in pts_flank]

# Polar helper
def polar_pt(r, psi):
    return (r * math.sin(psi), -r * math.cos(psi))

# Build complete 2D contour:
# For each cycle k:
# Tooth is at angle psi_tooth = k * tc + theta1 / 2
# Roller A is at psi_A = k * tc
# Roller B is at psi_B = k * tc + theta1
# Over p1: from psi_A to psi_B is the tooth
# Over p2: from psi_B to (k+1)*tc is the bridge at Rf!
contour_pts = []

for k in range(z):
    psi_A = k * tc
    psi_tooth = psi_A + ha1
    psi_B = psi_A + theta1
    psi_next_A = (k + 1) * tc

    # 1. Right half of gap A & left flank of tooth
    for p in flank_polar:
        contour_pts.append(polar_pt(p['r'], psi_A + p['xi']))

    # 2. Crest arc at Ra if not closed at apex
    last_xi = flank_polar[-1]['xi']
    if last_xi < ha1 - 1e-4:
        ang_start = psi_A + last_xi
        ang_end = psi_B - last_xi
        n_crest = max(4, int((ang_end - ang_start) * 180 / math.pi))
        for i in range(1, n_crest):
            psi = ang_start + (ang_end - ang_start) * (i / n_crest)
            contour_pts.append(polar_pt(Ra, psi))

    # 3. Right flank of tooth into gap B
    for p in reversed(flank_polar):
        contour_pts.append(polar_pt(p['r'], psi_B - p['xi']))

    # 4. Bridge over p2 (from gap B to next gap A at radius Rf)
    # The gap B bed ends around psi_B + u/(2*Rf)
    n_bridge = 12
    for i in range(1, n_bridge):
        psi = psi_B + (psi_next_A - psi_B) * (i / n_bridge)
        contour_pts.append(polar_pt(Rf, psi))

# Write SVG
svg_w = 600
svg_h = 600
scale = 0.9 * (svg_w / (da * 1.3))
cx = svg_w / 2.0
cy = svg_h / 2.0

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" style="background:#0f172a;">']

# Draw reference circles
svg.append(f'<circle cx="{cx}" cy="{cy}" r="{R0 * scale}" fill="none" stroke="#0284c7" stroke-dasharray="8,4" stroke-width="1"/>')
svg.append(f'<circle cx="{cx}" cy="{cy}" r="{Rf * scale}" fill="none" stroke="#dc2626" stroke-dasharray="6,3" stroke-width="0.8"/>')
svg.append(f'<circle cx="{cx}" cy="{cy}" r="{Ra * scale}" fill="none" stroke="#7c3aed" stroke-dasharray="6,3" stroke-width="0.8"/>')
svg.append(f'<circle cx="{cx}" cy="{cy}" r="{Rs * scale}" fill="none" stroke="#ea580c" stroke-dasharray="4,2" stroke-width="0.8"/>')

# Draw contour
path_d = f"M {cx + contour_pts[0][0]*scale:.2f} {cy + contour_pts[0][1]*scale:.2f} "
for pt in contour_pts[1:]:
    path_d += f"L {cx + pt[0]*scale:.2f} {cy + pt[1]*scale:.2f} "
path_d += "Z"
svg.append(f'<path d="{path_d}" fill="none" stroke="#38bdf8" stroke-width="2"/>')

# Draw rollers
for k in range(z):
    for psi in [k * tc, k * tc + theta1]:
        rx, ry = polar_pt(R0, psi)
        svg.append(f'<circle cx="{cx + rx*scale}" cy="{cy + ry*scale}" r="{(d1/2)*scale}" fill="rgba(56, 189, 248, 0.2)" stroke="#38bdf8" stroke-width="1.2"/>')

svg.append('</svg>')

with open('assets/screenshots/test_diff_clean.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg))

print("Saved test_diff_clean.svg successfully!")
