import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11
M_earth = 5.972e24
R_earth = 6371e3

altitude = 400e3
r0 = R_earth + altitude
v0 = np.sqrt(G * M_earth / r0)

dt = 10
days = 365

steps = int((days * 24 * 60 * 60) / dt)

test_values = [
    1.000001,
    1.00001,
    1.0001,
    1.001
]

def simulate(inertia_factor):

    pos = np.array([r0, 0.0])
    vel = np.array([0.0, v0])

    xs = []
    ys = []

    for _ in range(steps):

        r = np.linalg.norm(pos)

        gravity_accel = -(G * M_earth / r**3) * pos
        accel = gravity_accel / inertia_factor

        vel += accel * dt
        pos += vel * dt

        xs.append(pos[0])
        ys.append(pos[1])

    return np.array(xs), np.array(ys)

normal_x, normal_y = simulate(1.0)

final_errors = []

for inertia_factor in test_values:

    x, y = simulate(inertia_factor)

    error = np.sqrt(
        (x[-1] - normal_x[-1])**2 +
        (y[-1] - normal_y[-1])**2
    )

    final_errors.append(error / 1000)

    print(
        f"Inertia={inertia_factor} "
        f"Final Error={error/1000:.3f} km"
    )

plt.figure(figsize=(10,5))
plt.plot(test_values, final_errors, marker="o")

plt.xlabel("Inertia Factor")
plt.ylabel("Final Position Error (km)")
plt.title("Precision Threshold Analysis")
plt.grid(True)

plt.show()
