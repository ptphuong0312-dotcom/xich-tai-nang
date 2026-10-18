import math

p = 12.7
z = 8
d1 = 8.51
R0 = p / (2 * math.sin(math.pi / z))
Rf = (p / math.sin(math.pi / z) - d1) / 2
Ra = (p / math.sin(math.pi / z) + 0.55 * d1) / 2

half_X = math.radians(60.0)
r1 = 0.505 * d1 + 0.069 * (d1 ** (1/3))
r2 = 0.008 * d1 * (8**2 + 180)

C1_y = Rf + r1
P_bed_x = r1 * math.sin(half_X)
P_bed_y = C1_y - r1 * math.cos(half_X)

ux = math.sin(half_X)
uy = -math.cos(half_X)
C2_x = P_bed_x + r2 * ux
C2_y = P_bed_y + r2 * uy

# int1 on Ra:
d_c2 = math.hypot(C2_x, C2_y)
a = (Ra**2 - r2**2 + d_c2**2) / (2 * d_c2)
h = math.sqrt(Ra**2 - a**2)
int1_x = a * C2_x / d_c2 + h * (-C2_y) / d_c2
int1_y = a * C2_y / d_c2 + h * (C2_x) / d_c2

# Tooth flank points in sprocket coordinate frame:
flank_pts = []
for i in range(21):
    ang = math.atan2(P_bed_y - C2_y, P_bed_x - C2_x) + i/20.0 * (math.atan2(int1_y - C2_y, int1_x - C2_x) - math.atan2(P_bed_y - C2_y, P_bed_x - C2_x))
    flank_pts.append((C2_x + r2 * math.cos(ang), C2_y + r2 * math.sin(ang)))

print("Min distance from flank to roller at (0, R0):")
min_d = min(math.hypot(pt[0], pt[1] - R0) for pt in flank_pts)
print(f"min_dist = {min_d:.3f} mm, roller_r = {d1/2:.3f} mm, margin = {min_d - d1/2:.3f} mm")
