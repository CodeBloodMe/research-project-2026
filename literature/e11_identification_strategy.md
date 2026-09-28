# Phase 14B: Identification Strategy (E11)

## 1. Observational Comparison for RQ1
We conduct a hierarchical observational comparison. We do not claim `REF_MIXED` "causes" higher miss rates; rather, we estimate the adjusted association between the presence of structural refactoring and PTS omission behavior.

## 2. Primary Analysis Model
The primary analysis is a **Hierarchical Mixed-Effects Logistic Regression**.

* **Outcome**: Test-level miss ($m(d,t)$) modeled strictly among actual failing test instances ($y(d,t) = 1$).
* **Exposure**: `REF_MIXED` vs `NON_REF`.
* **Fixed Covariates (Pre-specified)**: 
  - Log code churn (lines added + deleted)
  - Number of files changed
  - Historical file activity/age
* **Random Effects / Clustering**:
  - Random intercept for `Repository` to account for heterogeneous test suites and project cultures.
  - Random intercept for `Commit` to group test executions triggered by the same codebase state.

* **Estimand Reporting**: We report an adjusted Odds Ratio (or Risk Difference derived via marginal standardization) representing the associational difference in miss probability, accompanied by confidence intervals and variance components for repository heterogeneity.

## 3. Sensitivity Analysis
* **Within-Repository Stratification**: To test robustness, we will perform a stratified analysis matching/comparing `REF_MIXED` to `NON_REF` commits exclusively within the same repository and within identical time windows, thereby implicitly controlling for unobserved project-level confounders.
