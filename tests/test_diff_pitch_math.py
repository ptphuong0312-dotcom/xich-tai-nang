import math

# Catalog Page 50 parameters
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

print(f"z={z}, d0={d0:.2f}, df={df:.2f}, da={da:.2f}, ds={ds:.2f}")
print(f"theta1={math.degrees(theta1):.2f} deg, theta2={math.degrees(theta2):.2f} deg")
