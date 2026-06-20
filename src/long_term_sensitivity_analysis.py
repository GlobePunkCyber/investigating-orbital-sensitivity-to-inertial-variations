import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11
M_earth = 5.972e24
R_earth = 6371e3

altitude = 400e3
r0 = R_earth + altitude
v0 = np.sqrt(G * M_earth / r0)

dt = 10

lower_inertia = float(input("Enter lower inertia factor, example 0.999: "))
higher_inertia = float(input("Enter higher inertia factor, example 1.001: "))

durations = [30, 90, 180, 365]

def simulate_orbit(inertia_factor, days):
    steps = int((days * 24 * 60 * 60) / dt)

    pos = np.array([r0, 0.0])
    vel = np.array([0.0, v0])

    xs = []
    ys = []

    for _ in range(steps):
        r = np.linalg.norm(pos)

        if r < R_earth:
            break

        gravity_accel = -(G * M_earth / r**3) * pos
        accel = gravity_accel / inertia_factor

        vel += accel * dt
        pos += vel * dt

        xs.append(pos[0])
        ys.append(pos[1])

    return np.array(xs), np.array(ys)

max_errors_lower = []
max_errors_higher = []
final_errors_lower = []
final_errors_higher = []

for days in durations:
    print(f"\nRunning {days}-day simulation...")

    normal_x, normal_y = simulate_orbit(1.0, days)
    lower_x, lower_y = simulate_orbit(lower_inertia, days)
    higher_x, higher_y = simulate_orbit(higher_inertia, days)

    min_len_lower = min(len(normal_x), len(lower_x))
    min_len_higher = min(len(normal_x), len(higher_x))

    lower_error = np.sqrt(
        (lower_x[:min_len_lower] - normal_x[:min_len_lower])**2 +
        (lower_y[:min_len_lower] - normal_y[:min_len_lower])**2
    )

    higher_error = np.sqrt(
        (higher_x[:min_len_higher] - normal_x[:min_len_higher])**2 +
        (higher_y[:min_len_higher] - normal_y[:min_len_higher])**2
    )

    max_errors_lower.append(np.max(lower_error) / 1000)
    max_errors_higher.append(np.max(higher_error) / 1000)

    final_errors_lower.append(lower_error[-1] / 1000)
    final_errors_higher.append(higher_error[-1] / 1000)

    print(f"Lower inertia {lower_inertia}")
    print(f"Max position error: {np.max(lower_error) / 1000:.3f} km")
    print(f"Final position error: {lower_error[-1] / 1000:.3f} km")

    print(f"Higher inertia {higher_inertia}")
    print(f"Max position error: {np.max(higher_error) / 1000:.3f} km")
    print(f"Final position error: {higher_error[-1] / 1000:.3f} km")

plt.figure(figsize=(10, 5))

plt.plot(durations, max_errors_lower, marker="o", label=f"Lower inertia {lower_inertia} max error")
plt.plot(durations, max_errors_higher, marker="o", label=f"Higher inertia {higher_inertia} max error")

plt.xlabel("Simulation Duration (days)")
plt.ylabel("Maximum Position Error (km)")
plt.title("Long-Term Sensitivity Analysis")
plt.grid(True)
plt.legend()
plt.show()

plt.figure(figsize=(10, 5))

plt.plot(durations, final_errors_lower, marker="o", label=f"Lower inertia {lower_inertia} final error")
plt.plot(durations, final_errors_higher, marker="o", label=f"Higher inertia {higher_inertia} final error")

plt.xlabel("Simulation Duration (days)")
plt.ylabel("Final Position Error (km)")
plt.title("Final Position Error Over Time")
plt.grid(True)
plt.legend()
plt.show()
