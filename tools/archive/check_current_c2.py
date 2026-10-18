import math

p = 12.7
z = 8
d1 = 8.51

d0 = p / math.sin(math.pi / z)
R0 = d0 / 2.0
df = d0 - d1
Rf = df / 2.0
da = d0 + 0.55 * d1
Ra = da / 2.0

alpha_rad = 2 * math.pi / z
half_alpha = alpha_rad / 2.0

# Tooth 0 is between gap 0 (ang = 0) and gap 1 (ang = alpha_rad)
# Centerline of Tooth 0 is at ang = alpha_rad / 2 = 22.5 deg.
# The tooth flank of Tooth 0 on the RIGHT side of gap 0:
# Gap 0 is centered at angle 0.
# The right flank of gap 0 is the left flank of Tooth 0!
# Wait! In computeFullContour:
# For k = 0: gap_ang = 0.
# single_gap has right_pts (which go from x=0, y=Rf towards positive x, positive y in gap frame)
# In SVG: x_svg = x, y_svg = -y.
# Let's check the exact points of Tooth 0 in SVG:

half_X = math.radians(60.0)
z1 = 8
r1 = 0.505 * d1 + 0.069 * (d1 ** (1/3))
r2 = 0.008 * d1 * (z1**2 + 180)

C1_y = Rf + r1
P_bed_x = r1 * math.sin(half_X)
P_bed_y = C1_y - r1 * math.cos(half_X)

# In our current code (index.html):
# What does index.html have for C2?
# Let's check C2 in index.html!
ux = math.sin(half_X)
uy = -math.cos(half_X)
# In index.html line 3976:
C2_code_x = P_bed_x - r2 * ux
C2_code_y = P_bed_y - r2 * uy

print(f"C2_code in index.html: ({C2_code_x:.2f}, {C2_code_y:.2f})")

# Let's check points of this curve in SVG:
pts_svg = []
for i in range(21):
    th = math.radians(60.0) + i/20.0 * math.radians(40.0)
    # in index.html lines 4003-4007:
    # pt = { x: C2.x + r2 * cos(ang), y: C2.y + r2 * sin(ang) }
    # in SVG: (pt.x, -pt.y)
    pass
