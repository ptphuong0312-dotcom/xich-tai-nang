import math

def simulate_mesh(standard="KWN_001", z=8, p=12.7, d1=8.51):
    alpha_deg = 360.0 / z
    alpha_rad = 2 * math.pi / z
    d0 = p / math.sin(math.pi / z)
    R0 = d0 / 2.0
    df = d0 - d1
    Rf = df / 2.0
    da = d0 + 0.55 * d1
    Ra = da / 2.0

    # Let's check tooth flank points of gap 0:
    half_X = math.radians(60.0)
    z1 = 8
    r1 = 0.505 * d1 + 0.069 * (d1 ** (1/3))
    r2 = 0.008 * d1 * (z1**2 + 180)

    C1_y = Rf + r1
    P_bed_x = r1 * math.sin(half_X)
    P_bed_y = C1_y - r1 * math.cos(half_X)

    ux = math.sin(half_X)
    uy = -math.cos(half_X)
    C2_x = P_bed_x + r2 * ux
    C2_y = P_bed_y + r2 * uy

    d_c2 = math.hypot(C2_x, C2_y)
    a = (Ra**2 - r2**2 + d_c2**2) / (2 * d_c2)
    h = math.sqrt(max(0, Ra**2 - a**2))
    int1_x = a * C2_x / d_c2 + h * (-C2_y) / d_c2
    int1_y = a * C2_y / d_c2 + h * (C2_x) / d_c2

    # Half gap points:
    half_pts = []
    for i in range(11):
        th = half_X * (i / 10.0)
        half_pts.append((r1 * math.sin(th), C1_y - r1 * math.cos(th)))
    th_s = math.atan2(P_bed_y - C2_y, P_bed_x - C2_x)
    th_e = math.atan2(int1_y - C2_y, int1_x - C2_x)
    for i in range(1, 11):
        th = th_s + (th_e - th_s) * (i / 10.0)
        half_pts.append((C2_x + r2 * math.cos(th), C2_y + r2 * math.sin(th)))

    single_gap = [(-x, y) for x, y in reversed(half_pts[1:])] + half_pts

    # Full sprocket contour:
    sprocket_teeth = []
    for k in range(z):
        gap_ang = k * alpha_rad
        cos_g = math.cos(gap_ang)
        sin_g = math.sin(gap_ang)
        for pt in single_gap:
            sprocket_teeth.append((
                pt[0] * cos_g + pt[1] * sin_g,
                -( -pt[0] * sin_g + pt[1] * cos_g ) # in SVG coordinates: y is flipped
            ))

    # Now let's check for 10 animation angles from 0 to alpha_rad:
    for step in range(10):
        theta = step * (alpha_rad / 10.0)
        rotDeg = -theta # sprocket rotates by -theta

        cos_r = math.cos(rotDeg)
        sin_r = math.sin(rotDeg)

        # Rotated sprocket teeth:
        rot_teeth = [(x * cos_r - y * sin_r, x * sin_r + y * cos_r) for x, y in sprocket_teeth]

        # Joints from kinematic strand:
        K_base = math.floor(theta / alpha_rad)
        d_theta = theta - K_base * alpha_rad

        seated_slots = [m for m in range(-2, z + 3) if -1e-4 <= d_theta + m * alpha_rad <= math.pi + 1e-4]
        min_m = min(seated_slots)
        phi_0 = d_theta + min_m * alpha_rad
        j0_x = -R0 * math.sin(phi_0)
        j0_y = -R0 * math.cos(phi_0)

        dy_top = -R0 - j0_y
        dx_top = math.sqrt(max(0, p * p - dy_top * dy_top))
        j_prev_x = j0_x + dx_top

        joints = []
        for k_idx in range(4, 0, -1):
            joints.append((j_prev_x + (k_idx - 1) * p, -R0))
        for m in seated_slots:
            phi = d_theta + m * alpha_rad
            joints.append((-R0 * math.sin(phi), -R0 * math.cos(phi)))

        # Check minimum distance from every tooth point to every joint center
        # If distance < d1/2, then tooth penetrates roller!
        min_clearance = 999.0
        colliding_pair = None
        for j_idx, (jx, jy) in enumerate(joints):
            for tx, ty in rot_teeth:
                d = math.hypot(tx - jx, ty - jy)
                c = d - d1 / 2.0
                if c < min_clearance:
                    min_clearance = c
                    colliding_pair = (j_idx, (jx, jy), (tx, ty))

        print(f"Step {step} (theta={math.degrees(theta):.1f}°): min clearance = {min_clearance:.3f} mm")
        if min_clearance < -1e-3:
            j_id, j_pos, t_pos = colliding_pair
            print(f"  --> COLLISION! Joint {j_id} at {j_pos}, tooth at {t_pos}")

simulate_mesh()
