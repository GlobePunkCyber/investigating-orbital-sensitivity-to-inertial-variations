# Investigating Orbital Sensitivity to Inertial Variations

## Project Overview

This project explores how artificial changes to the gravity–inertia balance affect satellite orbital behavior within a simplified orbital mechanics simulation.

The purpose of this study is not to challenge established physics, but to investigate how sensitive orbital trajectories are to small and large parameter variations.

The repository demonstrates numerical modeling, sensitivity analysis, scientific experiment design, and data visualization using Python.

---

## Research Question

How sensitive are orbital trajectories to changes in the modeled relationship between gravity and inertia?

---

## Methodology

A simplified Earth-orbit model is used to compare a baseline orbit against modified inertia factors.

The simulation evaluates:

* Orbital shape changes
* Orbital radius changes
* Position error accumulation
* Long-term trajectory divergence
* Stability boundaries
* Precision sensitivity

All experiments maintain identical initial conditions unless otherwise stated.

---

# Experiment 001 – Orbital Sensitivity Analysis

## Objective

Determine how changing the inertia factor affects orbital shape and radius.

## Method

Compare:

* Baseline inertia = 1.000
* Lower inertia = 0.999
* Higher inertia = 1.001

over a 30-day simulation.

## Results

* Small inertia changes produced measurable orbit differences.
* Higher inertia produced a larger average orbital radius.
* Lower inertia produced a smaller average orbital radius.

## Conclusion

Orbital trajectories are sensitive to changes in the gravity–inertia balance.

### Figure

`exp001_orbital_sensitivity.png`

---

# Experiment 002 – Position Error Analysis

## Objective

Measure accumulated position error relative to the baseline orbit.

## Method

Track position differences between modified and baseline trajectories over time.

## Results

* Position error increased steadily.
* Even small inertia changes produced large positional offsets after extended periods.

## Conclusion

Small perturbations accumulate into significant orbital position errors.

### Figure

`exp002_position_error_analysis.png`

---

# Experiment 003 – Long-Term Sensitivity Analysis

## Objective

Investigate how position error evolves over longer simulation periods.

## Method

Run simulations for:

* 30 days
* 90 days
* 180 days
* 365 days

## Results

Approximate maximum position errors:

| Duration | Position Error |
| -------- | -------------- |
| 30 Days  | ~2,700 km      |
| 90 Days  | ~7,800 km      |
| 180 Days | ~12,700 km     |
| 365 Days | ~12,500 km     |

## Conclusion

Position error grows substantially but does not increase indefinitely under the current model assumptions.

### Figure

`exp003_long_term_sensitivity.png`

---

# Experiment 004 – Stability Boundary Analysis

## Objective

Determine whether large inertia changes destabilize orbit.

## Method

Test progressively lower inertia factors while maintaining the same initial orbital velocity.

## Results

| Inertia Factor | Result   |
| -------------- | -------- |
| 1.00           | Stable   |
| 0.90           | Unstable |
| 0.80           | Unstable |
| 0.70           | Unstable |

## Conclusion

Large deviations from the baseline parameter can destroy orbital stability under current simulation assumptions.

### Important Note

The initial orbital velocity remains fixed throughout the experiment.

This experiment measures sensitivity to gravity–inertia balance changes and does not determine whether alternative stable orbits could exist with optimized starting velocities.

### Figure

`exp004_stability_boundary.png`

---

# Experiment 005 – Precision Threshold Analysis

## Objective

Investigate whether extremely small parameter changes produce measurable long-term effects.

## Method

Test:

* 1.000001
* 1.000010
* 1.000100
* 1.001000

over a one-year simulation.

## Results

Approximate final position errors:

| Inertia Factor | Position Error |
| -------------- | -------------- |
| 1.000001       | ~500 km        |
| 1.000010       | ~4,700 km      |
| 1.000100       | ~5,700 km      |
| 1.001000       | ~12,300 km     |

## Conclusion

Tiny parameter variations can accumulate into measurable long-term orbital differences.

### Figure

`exp005_precision_threshold.png`

---

# Overall Findings

The experiments consistently demonstrate:

### Small Changes Matter

Small inertia variations alter orbital trajectories.

### Error Accumulation

Small differences grow into large position errors over time.

### Long-Term Divergence

Position errors increase significantly over months and years.

### Stability Limits

Large parameter changes can destabilize the orbit.

### Precision Sensitivity

Even extremely small parameter variations can produce measurable effects over long durations.

---

# Key Interpretation

This project does not demonstrate new physics.

Instead, it demonstrates that orbital trajectories are highly sensitive to changes in the modeled relationship between gravity and inertia.

The repository should be viewed as a computational sensitivity study rather than a challenge to established orbital mechanics.

---

# Skills Demonstrated

* Python Simulation Development
* Numerical Modeling
* Orbital Mechanics Fundamentals
* Sensitivity Analysis
* Scientific Experiment Design
* Data Visualization
* Research Documentation
* GitHub Project Organization

---

# Repository Status

## Completed

* Experiment 001
* Experiment 002
* Experiment 003
* Experiment 004
* Experiment 005

## Future Work

Potential future studies:

* Velocity Compensation Analysis
* Inclined Orbit Sensitivity
* Eccentric Orbit Sensitivity
* Numerical Integrator Comparison
* Multi-Body Sensitivity Analysis

---

## Disclaimer

This repository is intended for educational and computational research purposes. The experiments use simplified orbital models to investigate parameter sensitivity and should not be interpreted as evidence against established gravitational or orbital theories.
