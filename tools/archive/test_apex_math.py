import math

z = 8
p = 40.0
d1 = 15.0
d0 = p / math.sin(math.pi / z)
R0 = d0 / 2.0
df = d0 - d1
Rf = df / 2.0
da = (d0 + 0.8 * d1) / 2.0 * 2.0
Ra = da / 2.0

alpha_deg = 360.0 / z
alpha_rad = math.radians(alpha_deg)
half_alpha = alpha_rad / 2.0

beta_deg = 74.0
beta_rad = math.radians(beta_deg)
half_beta = beta_rad / 2.0

gamma_deg = beta_deg / 2.0 - alpha_deg / 2.0
gamma_rad = math.radians(gamma_deg)

u = 0.02 * p
r1 = 0.51 * d1
h3 = 0.3 * d1

C1_x = u / 2.0
C1_y = Rf + r1
theta_end = math.pi / 2.0 - half_beta
P1_x = C1_x + r1 * math.sin(theta_end)
P1_y = C1_y - r1 * math.cos(theta_end)

P2_x = P1_x + h3 * math.sin(half_beta)
P2_y = P1_y + h3 * math.cos(half_beta)

print(f"P1: ({P1_x:.2f}, {P1_y:.2f})")
print(f"P2: ({P2_x:.2f}, {P2_y:.2f})")

# Intersection in SVG coordinates:
# Line 1 (centerline): (t * sin(half_alpha), -t * cos(half_alpha))
# Line 2 (flank): (P2_x + s * sin(half_beta), -P2_y - s * cos(half_beta))
# s = (P2_y * sin(half_alpha) - P2_x * cos(half_alpha)) / sin(gamma_rad)
s = (P2_y * math.sin(half_alpha) - P2_x * math.cos(half_alpha)) / math.sin(gamma_rad)
t = (P2_x + s * math.sin(half_beta)) / math.sin(half_alpha)

I_x = t * math.sin(half_alpha)
I_y = -t * math.cos(half_alpha)
print(f"Intersection Apex: ({I_x:.2f}, {I_y:.2f}), distance t = {t:.2f} mm")
print(f"Ra = {Ra:.2f} mm")

# Verify:
P_check_x = P2_x + s * math.sin(half_beta)
P_check_y = -P2_y - s * math.cos(half_beta)
print(f"P_check: ({P_check_x:.2f}, {P_check_y:.2f}) -> matches Apex!")
