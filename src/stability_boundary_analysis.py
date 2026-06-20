import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11
M_earth = 5.972e24
R_earth = 6371e3

altitude = 400e3
r0 = R_earth + altitude
v0 = np.sqrt(G * M_earth / r0)

dt = 10
days = 30
steps = int((days * 24 * 60 * 60) / dt)

inertia_values = [
    1.0,
    0.9,
    0.8,
    0.7,
    0.6,
    0.5,
    0.4,
    0.3,
    0.2,
    0.125
]

survival_times = []

for inertia_factor in inertia_values:

    pos = np.array([r0, 0.0])
    vel = np.array([0.0, v0])

    survived_days = days

    for step in range(steps):

        r = np.linalg.norm(pos)

        if r < R_earth:
            survived_days = step * dt / (24 * 60 * 60)
            break

        gravity_accel = -(G * M_earth / r**3) * pos
        accel = gravity_accel / inertia_factor

        vel += accel * dt
        pos += vel * dt

    survival_times.append(survived_days)

    print(
        f"Inertia={inertia_factor:.3f} "
        f"Survival={survived_days:.2f} days"
    )

plt.figure(figsize=(10,5))
plt.plot(inertia_values, survival_times, marker="o")
plt.xlabel("Inertia Factor")
plt.ylabel("Survival Time (days)")
plt.title("Stability Boundary Analysis")
plt.grid(True)
plt.show()
