import math

z = 8
alpha_rad = 2 * math.pi / z

print(f"alpha_deg = {math.degrees(alpha_rad)}")

# In computeFullContour:
# For k = 0, 1, 2:
for k in range(z):
    gap_ang = k * alpha_rad
    cos_g = math.cos(gap_ang)
    sin_g = math.sin(gap_ang)
    # pt = (0, Rf)
    pt_x, pt_y = 0, 100 # Rf = 100
    x_gap = pt_x * cos_g + pt_y * sin_g
    y_gap = -pt_x * sin_g + pt_y * cos_g
    # in SVG: (x_gap, -y_gap)
    svg_x = x_gap
    svg_y = -y_gap
    ang_svg = math.atan2(svg_x, -svg_y) # angle from 12 o'clock (0 rad)
    print(f"Gap k={k}: svg=({svg_x:.1f}, {svg_y:.1f}), angle={math.degrees(ang_svg):.1f} deg")

print("\nChain strand joints:")
for m in range(5):
    phi = m * alpha_rad
    x_j = -100 * math.sin(phi)
    y_j = -100 * math.cos(phi)
    ang_svg = math.atan2(x_j, -y_j)
    print(f"Joint m={m}: svg=({x_j:.1f}, {y_j:.1f}), angle={math.degrees(ang_svg):.1f} deg")
