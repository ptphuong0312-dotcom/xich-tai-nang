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

# Let's inspect the tooth between two rollers at phi = -theta1/2 and phi = +theta1/2
# Roller 1 center: (R0 * sin(-theta1/2), R0 * cos(-theta1/2))
# Roller 2 center: (R0 * sin(theta1/2), R0 * cos(theta1/2))
print("Distance between roller centers:", math.hypot(
    R0 * math.sin(theta1/2) - R0 * math.sin(-theta1/2),
    R0 * math.cos(theta1/2) - R0 * math.cos(-theta1/2)
))
print("Expected p1:", p1)
