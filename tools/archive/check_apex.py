import math

z = 8
alpha_deg = 360.0 / z
alpha_rad = math.radians(alpha_deg)
half_alpha = alpha_rad / 2.0

beta_deg = 74.0
beta_rad = math.radians(beta_deg)
half_beta = beta_rad / 2.0

gamma_deg = beta_deg / 2.0 - alpha_deg / 2.0
gamma_rad = math.radians(gamma_deg)

# Let's say d1 = 15, p = 40 (like in image 2: FVT 40, p=40, z=8, d1=15)
d1 = 15.0
p = 40.0
d0 = p / math.sin(math.pi / z)
R0 = d0 / 2.0
df = d0 - d1
Rf = df / 2.0
Ra = (d0 + 0.8 * d1) / 2.0

u = 0.02 * p # 0.8
r1 = 0.51 * d1 # 7.65
h3 = 0.3 * d1 # 4.50

# P1 in gap coordinates:
# P0 = (u/2, Rf) = (0.4, Rf)
# C1 center is at: C1.x = u/2 + r1 * sin(half_beta), C1.y = Rf + r1 - r1 * cos(half_beta) ?
# Let's check how P1 is computed in index.html for KWN_017
