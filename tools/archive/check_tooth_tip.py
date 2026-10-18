import math

p = 12.7
z = 8
d1 = 8.51

alpha_deg = 360.0 / z
alpha_rad = 2 * math.pi / z

# DIN 8187 formulas from Kettenwulf page 46:
d0 = p / math.sin(math.pi / z)
R0 = d0 / 2.0

# da = d0 + 1.25 * p - d1   or   d0 + (1 - 1.6/z)*p
# For z=8: (1 - 1.6/8) = 0.8
da_kw = d0 + 1.25 * p - d1
da_alt = d0 + 0.8 * p

# df = d0 - d1
df = d0 - d1
Rf = df / 2.0
Ra = da_kw / 2.0

# X angle: 120 - 90/z = 120 - 90/8 = 108.75 deg? Or X = 120?
# In our code:
# let X_deg = 120 - 90/z ?
print(f"p={p}, z={z}, d1={d1}")
print(f"d0={d0:.2f}, R0={R0:.2f}")
print(f"df={df:.2f}, Rf={Rf:.2f}")
print(f"da={da_kw:.2f}, Ra={Ra:.2f}")

# Joint 0: (0, -R0)
# Joint 1: (-R0 * sin(alpha), -R0 * cos(alpha))
# The tooth centerline between Joint 0 and Joint 1 is at angle: -alpha/2 (-22.5 deg)!
# Tooth tip is at Ra along angle -22.5 deg!
# Tooth tip point in SVG coordinates:
tip_x = Ra * math.sin(-alpha_rad / 2.0)
tip_y = -Ra * math.cos(-alpha_rad / 2.0)
print(f"Tooth tip between 0 and 1: ({tip_x:.2f}, {tip_y:.2f})")

# Distance from tooth tip to Joint 0 (roller 0 center):
dist_to_j0 = math.hypot(tip_x - 0, tip_y - (-R0))
print(f"Distance from tooth tip to Joint 0 center: {dist_to_j0:.2f} mm")
print(f"Roller radius r_roller = {d1/2:.2f} mm")
print(f"Clearance to roller 0: {dist_to_j0 - d1/2:.2f} mm")

# Distance from tooth tip to Joint 1 (roller 1 center):
j1_x = -R0 * math.sin(alpha_rad)
j1_y = -R0 * math.cos(alpha_rad)
dist_to_j1 = math.hypot(tip_x - j1_x, tip_y - j1_y)
print(f"Distance from tooth tip to Joint 1 center: {dist_to_j1:.2f} mm")
print(f"Clearance to roller 1: {dist_to_j1 - d1/2:.2f} mm")
