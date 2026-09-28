# Phase 15C: Duplicate SHA Protocol

## The Challenge
Empirical extraction revealed 3,304 duplicate commit SHAs mapping to multiple distinct CI builds within the CIBench index. These duplicates arise from CI matrix builds (e.g., testing across different Java versions) or job retries.

Because the PTS representation (refactoring footprint) is identical for a given SHA, retaining multiple test-execution observations for the same SHA creates repeated-measures correlation.

## Frozen Strategy: OPTION B
We will **retain multiple builds** and explicitly model the hierarchical dependencies.

**Justification:**
1. **Outcome Variation:** Different CI environment builds for the same SHA often yield varying test outcomes (e.g., flakiness or environment-specific failures). Arbitrarily discarding one (Option A) throws away valid empirical variance and biases the sample towards whichever build index was arbitrarily chosen first.
2. **Statistical Compatibility:** The chosen E11 statistical model is a Hierarchical Mixed-Effects Logistic Regression. This architecture natively accommodates repeated measures.

## Formal Hierarchy
The observation hierarchy for inference is strictly ordered as:
**Repository $\rightarrow$ Commit SHA $\rightarrow$ CI Build (Job) $\rightarrow$ Test Class**

The random-effects structure of the final model MUST include intercepts for `Commit SHA` to correctly partition the variance and prevent the artificial inflation of statistical significance that would occur if duplicate SHAs were treated as independent observations.
