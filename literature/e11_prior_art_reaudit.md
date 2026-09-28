# Phase 14: Prior Art Reaudit (E11)

## 1. Scope of Search
A comprehensive search was re-evaluated against the intersection of "machine learning", "test selection / prioritization", "refactoring", and "continuous integration".

## 2. Findings
* **Predictive Test Selection (ML-PTS)**: The baseline is firmly established by Machalica et al. (2019). Subsequent work (e.g., Wang et al., 2021) evaluates ML-PTS under various architectural conditions but does not isolate structural refactoring as a causal disruption to historical feature representations.
* **Regression Test Selection (RTS)**: Static and dynamic RTS solutions (e.g., Ekstazi, STARTS) are well documented. They construct graphs or traces that are naturally resistant to simple renames (if tracked) or safely conservative (they re-test everything touching a changed symbol). They do not rely on historical failure matrices.
* **Refactoring and Testing**: Fazlalizadeh et al. (2009) evaluated test prioritization for refactoring but used static impact heuristics, not machine learning or historical CI traces.

## 3. Conclusion
The intersection of *history-based ML test selection* and *structural refactoring* is underexplored. The specific failure mode—where a refactoring breaks historical file linkage, causing a silent prediction degradation—is not directly evaluated in the identified PTS literature.
