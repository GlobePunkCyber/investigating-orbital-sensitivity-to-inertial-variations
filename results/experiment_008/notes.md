# Experiment 008 – Real Orbit Inertial Sensitivity Analysis

## Objective

Test whether small artificial inertia perturbations produce measurable divergence when applied to a real GNSS precise orbit.

## Data Source

* **File:** `COD0MGXFIN_20221850000_01D_05M_ORB.SP3`
* **Source:** IGS Final Multi-GNSS Precise Orbit Product
* **Date:** Day 185, 2022
* **Satellite Analyzed:** `R01`

## Method

A precise SP3 orbit was used as the reference trajectory. Satellite position history was extracted from the precise orbit product, and velocity was estimated between observation epochs.

Three inertia factors were evaluated:

```text
0.999
1.000
1.001
```

Modified trajectories were generated and compared against the original SP3 reference orbit.

## Results

* Inertia factor **1.000** remained aligned with the SP3 reference trajectory.
* Inertia factors **0.999** and **1.001** produced measurable divergence from the reference orbit.
* Maximum position divergence reached approximately **50 km** over a one-day period.
* Orbital radius error reached approximately **±50 km**.
* The perturbed trajectories remained stable while gradually separating from the reference orbit.

## Discussion

The experiment demonstrated that small modifications to the modeled motion response can produce measurable changes in orbital evolution when compared to a real GNSS precise orbit.

The results indicate that satellite trajectories are sensitive to small parameter variations, with divergence accumulating over time despite the perturbations remaining relatively small.

While the experiment does not demonstrate new physics or deviations from established gravitational theory, it provides a quantitative measure of orbital sensitivity using real-world satellite orbit data.

## Conclusion

Experiment 008 showed that a ±0.1% artificial inertia perturbation applied to a real GNSS precise orbit produced approximately 50 km of trajectory divergence over a one-day period.

These findings support the conclusion that orbital trajectories are highly sensitive to small changes in modeled motion parameters and establish a foundation for future studies involving direct perturbations to orbital acceleration models.

## Figures

```text
exp008_position_error_vs_time.png
exp008_radius_error_vs_time.png
exp008_max_error_by_inertia_factor.png
```
