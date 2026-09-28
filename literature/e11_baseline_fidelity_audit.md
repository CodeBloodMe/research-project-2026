# Phase 14: Baseline Fidelity Audit (E11)

## 1. Reference Baseline
Machalica et al., "Predictive Test Selection" (ICSE-SEIP 2019). This work establishes the industrial standard for ML-PTS using a LightGBM/GBDT model trained on file histories, cross-features, and test failure rates.

## 2. Deviation Decision
**OPTION B is explicitly chosen.**
The E11 baseline is a deliberate, reduced, history-based ML-PTS model. It is *derived* from the core historical concepts of Machalica et al. but is not a full replication.

## 3. Justification for Deviation
Machalica's production model heavily relies on:
1. Deep dependency graph features (e.g., "minimal dependency-graph distance") derived from Facebook's internal build systems (Buck).
2. Developer identity and historical test-flake tracking which are not uniformly available or reliable in public CIBench data.
3. Test time/duration integration to optimize a specific hardware allocation metric.

Since CIBench provides rich file-level history and Git diffs but lacks universal internal dependency graphs across 100 disparate Java projects, the E11 baseline restricts itself strictly to the *tabular historical representations*.

## 4. Scientific Validity
The core scientific claim of E11—that structural refactorings disrupt history-based ML models by breaking identity tracking—remains perfectly valid. By stripping away static dependency features, the E11 baseline actually isolates the specific vulnerability of historical tracking. (RQ4 optionally explores adding structural features back to see if they rescue performance).
