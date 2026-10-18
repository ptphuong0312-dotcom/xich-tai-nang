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

z1 = 8
X_deg = 120.0
half_X = math.radians(X_deg / 2.0)

r1 = 0.505 * d1 + 0.069 * (d1 ** (1/3))
r2 = 0.008 * d1 * (z1**2 + 180)

# C1 is the center of the bottom bed arc r1.
# At theta = 0, y = Rf. C1 = (0, Rf + r1)
# So for theta from 0 to half_X:
# x = r1 * sin(theta)
# y = C1.y - r1 * cos(theta) = Rf + r1 * (1 - cos(theta))
C1_x = 0.0
C1_y = Rf + r1

P_bed_x = r1 * math.sin(half_X)
P_bed_y = C1_y - r1 * math.cos(half_X)

# u_dir is unit vector from C1 to P_bed:
# (P_bed_x - C1_x, P_bed_y - C1_y) = (r1 * sin(half_X), -r1 * cos(half_X))
ux = math.sin(half_X)
uy = -math.cos(half_X)

# Since r2 is convex, its center C2 is in the direction of +u_dir from P_bed:
C2_x = P_bed_x + r2 * ux
C2_y = P_bed_y + r2 * uy

print(f"P_bed: ({P_bed_x:.2f}, {P_bed_y:.2f})")
print(f"C2: ({C2_x:.2f}, {C2_y:.2f})")

# Intersection of circle (C2, r2) with circle (0, Ra):
# Equation: x^2 + y^2 = Ra^2 and (x - C2_x)^2 + (y - C2_y)^2 = r2^2
d_c2 = math.hypot(C2_x, C2_y)
# Check if circles intersect:
print(f"Distance to C2: {d_c2:.2f}, Ra={Ra:.2f}, r2={r2:.2f}")
# Distance between (0,0) and C2:
# For intersection: |Ra - r2| <= d_c2 <= Ra + r2
print(f"|Ra - r2| = {abs(Ra - r2):.2f} <= {d_c2:.2f} <= {Ra + r2:.2f}")

a = (Ra**2 - r2**2 + d_c2**2) / (2 * d_c2)
h = math.sqrt(Ra**2 - a**2)
x2 = a * C2_x / d_c2
y2 = a * C2_y / d_c2

int1_x = x2 + h * (-C2_y) / d_c2
int1_y = y2 + h * (C2_x) / d_c2

int2_x = x2 - h * (-C2_y) / d_c2
int2_y = y2 - h * (C2_x) / d_c2

print(f"int1: ({int1_x:.2f}, {int1_y:.2f}), polar_ang: {math.degrees(math.atan2(int1_x, int1_y)):.2f} deg")
print(f"int2: ({int2_x:.2f}, {int2_y:.2f}), polar_ang: {math.degrees(math.atan2(int2_x, int2_y)):.2f} deg")
print(f"half_alpha = {math.degrees(half_alpha):.2f} deg")
