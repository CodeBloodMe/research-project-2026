# Phase 14: E11 Defensible Novelty Statement

## Novelty Claim
We contribute an empirical evaluation of how structural code refactorings influence the performance and feature distribution of history-based Machine Learning Predictive Test Selection (ML-PTS) models. While existing literature extensively covers both ML-PTS accuracy in general CI settings (e.g., Machalica et al., 2019) and traditional Regression Test Selection (RTS) robustness to structural changes (e.g., Legunsen et al., 2016), the specific vulnerability of tabular historical features to identity-altering refactorings remains underexplored. This study formalizes the exposure mechanisms by which identity loss disrupts historical code-test correlation matrices and empirically quantifies the resulting test-level missed regressions.

## Limitations of Claim
* We do not claim to be the "first" to study test selection under refactoring.
* We do not claim this affects all forms of test selection; the claim is strictly bounded to *history-based ML* formulations.
* Novelty centers on identifying the representation discontinuity mechanism, not on inventing the baseline PTS architecture.
