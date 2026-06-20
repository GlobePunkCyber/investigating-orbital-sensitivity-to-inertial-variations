import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11
M_earth = 5.972e24
R_earth = 6371e3

# Satellite setup
altitude = 400e3
r0 = R_earth + altitude
v0 = np.sqrt(G * M_earth / r0)

# User inputs
lower_inertia = float(input("Enter lower inertia factor, example 0.999: "))
higher_inertia = float(input("Enter higher inertia factor, example 1.001: "))
days = float(input("Enter simulation length in days, example 30: "))

# Time setup
dt = 10
steps = int((days * 24 * 60 * 60) / dt)

def simulate_orbit(inertia_factor=1.0):
    pos = np.array([r0, 0.0])
    vel = np.array([0.0, v0])

    xs = []
    ys = []
    distances = []

    for _ in range(steps):
        r = np.linalg.norm(pos)

        if r < R_earth:
            print(f"Satellite hit Earth with inertia factor {inertia_factor}")
            break

        gravity_accel = -(G * M_earth / r**3) * pos
        accel = gravity_accel / inertia_factor

        vel += accel * dt
        pos += vel * dt

        xs.append(pos[0])
        ys.append(pos[1])
        distances.append(np.linalg.norm(pos))

    return np.array(xs), np.array(ys), np.array(distances)

cases = {
    "Normal inertia 100%": 1.0,
    f"Lower inertia {lower_inertia}": lower_inertia,
    f"Higher inertia {higher_inertia}": higher_inertia
}

results = {}

for label, factor in cases.items():
    x, y, distances = simulate_orbit(factor)
    results[label] = {
        "x": x,
        "y": y,
        "distances": distances
    }

baseline_label = "Normal inertia 100%"
baseline_x = results[baseline_label]["x"]
baseline_y = results[baseline_label]["y"]

plt.figure(figsize=(10, 5))

for label, data in results.items():
    if label == baseline_label:
        continue

    min_length = min(len(baseline_x), len(data["x"]))

    dx = data["x"][:min_length] - baseline_x[:min_length]
    dy = data["y"][:min_length] - baseline_y[:min_length]

    position_error = np.sqrt(dx**2 + dy**2)

    time_days = np.arange(min_length) * dt / (24 * 60 * 60)

    plt.plot(time_days, position_error / 1000, label=f"{label} position error")

    print()
    print(label)
    print(f"Maximum position error: {np.max(position_error) / 1000:.3f} km")
    print(f"Average position error: {np.mean(position_error) / 1000:.3f} km")
    print(f"Final position error: {position_error[-1] / 1000:.3f} km")

plt.xlabel("Time (days)")
plt.ylabel("Position Error From Normal Orbit (km)")
plt.title("Position Error Analysis")
plt.grid(True)
plt.legend()
plt.show()
