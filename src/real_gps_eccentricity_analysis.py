import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# DATA FOLDER
# --------------------------------------------------
DATA_DIR = Path(
    r"C:\Dev\investigating-orbital-sensitivity-to-inertial-variations\data"
)

# --------------------------------------------------
# GPS SATELLITE FILES
# --------------------------------------------------
files = {
    "GPS BIIRM-6 (32711)": "Orbit-Data-32711-GP.csv",
    "GPS BIIF-7 (40105)": "Orbit-Data-40105-SupGP.csv",
    "GPS BIIF-10 (40730)": "Orbit-Data-40730-GP.csv",
}

results = {}

# --------------------------------------------------
# READ FILES
# --------------------------------------------------
for sat_name, filename in files.items():

    file_path = DATA_DIR / filename

    print(f"\nLoading: {filename}")

    df = pd.read_csv(file_path)

    # Show available columns
    print("Columns:")
    print(df.columns.tolist())

    # Convert date column
    df["Date/Time (UTC)"] = pd.to_datetime(df["Date/Time (UTC)"])

    avg_ecc = df["Eccentricity"].mean()
    avg_sma = df["SMA"].mean()
    avg_inc = df["Inclination"].mean()

    results[sat_name] = {
        "df": df,
        "avg_ecc": avg_ecc,
        "avg_sma": avg_sma,
        "avg_inc": avg_inc,
    }

    print(f"\n{sat_name}")
    print(f"Average Eccentricity: {avg_ecc:.6f}")
    print(f"Average SMA: {avg_sma:.3f} km")
    print(f"Average Inclination: {avg_inc:.3f} deg")

# --------------------------------------------------
# FIGURE 1
# ECCENTRICITY COMPARISON
# --------------------------------------------------
plt.figure(figsize=(10, 5))

for sat_name, data in results.items():
    plt.plot(
        data["df"]["Date/Time (UTC)"],
        data["df"]["Eccentricity"],
        label=sat_name
    )

plt.title("GPS Satellite Eccentricity Comparison")
plt.xlabel("Date")
plt.ylabel("Eccentricity")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save figure
plt.savefig("exp005_eccentricity_comparison.png", dpi=300)

# --------------------------------------------------
# FIGURE 2
# SMA COMPARISON
# --------------------------------------------------
plt.figure(figsize=(10, 5))

for sat_name, data in results.items():
    plt.plot(
        data["df"]["Date/Time (UTC)"],
        data["df"]["SMA"],
        label=sat_name
    )

plt.title("GPS Satellite Semi-Major Axis Comparison")
plt.xlabel("Date")
plt.ylabel("Semi-Major Axis (km)")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("exp005_sma_comparison.png", dpi=300)

# --------------------------------------------------
# FIGURE 3
# AVERAGE ECCENTRICITY
# --------------------------------------------------
plt.figure(figsize=(8, 5))

names = list(results.keys())
ecc_values = [results[name]["avg_ecc"] for name in names]

plt.bar(names, ecc_values)

plt.title("Average GPS Orbit Eccentricity")
plt.ylabel("Average Eccentricity")
plt.grid(axis="y")

plt.tight_layout()

plt.savefig("exp005_average_eccentricity.png", dpi=300)

plt.show()
