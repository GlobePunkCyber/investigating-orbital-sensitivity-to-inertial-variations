Experiment 007 – Broadcast vs Precise Orbit Analysis
Objective

Evaluate differences between GNSS broadcast ephemerides and precise orbit products using real-world satellite orbit data from NASA CDDIS and the International GNSS Service (IGS).

The goal is to establish a real-world orbital reference dataset for future orbital sensitivity and inertial variation studies.

Data Sources
Broadcast Ephemeris
File: brdc1850.22g
Source: NASA CDDIS
Date: Day 185, 2022
Constellation: GLONASS
Precise Orbit Product
File: COD0MGXFIN_20221850000_01D_05M_ORB.SP3
Source: IGS Final Orbit Product
Format: SP3
Sampling Interval: 5 minutes
Date: Day 185, 2022
Method
Load GLONASS broadcast ephemeris data.
Load corresponding IGS precise orbit product.
Match satellites and observation epochs where possible.
Compute:
Position differences
Orbital radius differences
Satellite-specific error statistics
Compare broadcast navigation products against precise orbit solutions.
Results
Dataset Summary
SP3 Records: 5,202
Broadcast Records: 131
Matched Records: 117
Observations
Direct position comparisons produced large discrepancies between broadcast and precise orbit solutions.
Orbital radius differences remained significantly smaller and showed consistent trends across satellites.
Results indicate that direct comparison of broadcast ephemerides and precise orbit products requires proper orbit propagation and epoch alignment.
Generated Outputs
exp007_position_error_vs_time.png
exp007_average_error_by_satellite.png
exp007_radius_difference.png
Conclusion

Experiment 007 successfully incorporated real-world GNSS orbit products into the orbital sensitivity project.

The analysis demonstrated that broadcast ephemerides and precise orbit products contain comparable orbital-scale information, but accurate position comparisons require proper propagation of the broadcast state vectors to common epochs.

This experiment established IGS SP3 precise orbit products as the preferred reference dataset for future investigations involving orbital stability, sensitivity analysis, and inertial perturbation studies.

Significance

This experiment represents the first use of operational GNSS orbit products within the project and provides a bridge between simulated orbital models and real satellite observations.

The resulting precise orbit dataset will serve as a baseline for future experiments investigating the sensitivity of orbital trajectories to changes in model parameters and inertial assumptions.