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

    xs, ys, distances = [], [], []

    for _ in range(steps):
        r = np.linalg.norm(pos)

        if r < R_earth:
            print(f"Satellite hit Earth with inertia factor {inertia_factor}")
            break

        gravity_accel = -(G * M_earth / r**3) * pos

        # Artificial inertia variation
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

# Print summary
baseline = results["Normal inertia 100%"]["distances"]
baseline_avg = np.mean(baseline)

for label, data in results.items():
    distances = data["distances"]

    min_altitude = (np.min(distances) - R_earth) / 1000
    max_altitude = (np.max(distances) - R_earth) / 1000
    avg_radius = np.mean(distances) / 1000
    delta_radius = (np.mean(distances) - baseline_avg) / 1000

    print()
    print(label)
    print(f"Minimum altitude: {min_altitude:.3f} km")
    print(f"Maximum altitude: {max_altitude:.3f} km")
    print(f"Average orbital radius: {avg_radius:.3f} km")
    print(f"Difference from normal: {delta_radius:.3f} km")

# Plot 1: Orbit comparison
plt.figure(figsize=(8, 8))

earth = plt.Circle((0, 0), R_earth / 1000, fill=False, color="black")
plt.gca().add_patch(earth)

for label, data in results.items():
    plt.plot(data["x"] / 1000, data["y"] / 1000, label=label)

plt.xlabel("X position (km)")
plt.ylabel("Y position (km)")
plt.title("Orbital Sensitivity to Inertial Variations")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()

# Plot 2: Orbit drift analysis
baseline_distances = results["Normal inertia 100%"]["distances"]

plt.figure(figsize=(10, 5))

for label, data in results.items():
    if label == "Normal inertia 100%":
        continue

    min_length = min(len(baseline_distances), len(data["distances"]))
    difference = data["distances"][:min_length] - baseline_distances[:min_length]
    time_days = np.arange(min_length) * dt / (24 * 60 * 60)

    plt.plot(time_days, difference, label=f"{label} minus normal")

plt.xlabel("Time (days)")
plt.ylabel("Radius Difference (meters)")
plt.title("Orbit Drift Analysis")
plt.grid(True)
plt.legend()
plt.show()
