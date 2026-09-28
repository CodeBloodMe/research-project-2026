# Phase 15D: Empirical Data Gate Decision

## Data Power Descriptive Inputs
- **Eligible Repositories**: UNKNOWN (Full git clones required to verify age > 5 years and commits > 5000; API was insufficient). Currently marked UNVERIFIED.
- **Eligible Builds**: 82,272 physically parsed log CSVs.
- **Unique Commit SHAs**: UNKNOWN (118,928 listed, but actual valid historical SHAs depend on GitHub availability).
- **Duplicate SHA Count**: 3,304 duplicates (Option B hierarchical model).
- **Test-Unit Rows (Test Classes)**: UNKNOWN.
- **Failure-Positive Rows**: UNKNOWN.
- **Error-Only Rows**: UNKNOWN.
- **REF_ONLY / REF_MIXED / NON_REF Commits**: UNKNOWN.
- **Direct-exposure Commits**: UNKNOWN.

**Note:** We strictly do not claim these inputs represent a sufficiently powered dataset. Power will be evaluated post-extraction.

## Decision Criteria Checklist
1. **Actual Eligible Population Verified**: **NO** (API limits prevent full verification; currently UNVERIFIED).
2. **Observation Unit Verified**: YES (Definitively proven to be Test Class level, not individual method).
3. **Failure Semantics Verified**: YES (`failure_positive = failed > 0`, ignoring pure error cases).
4. **Build Counts Reconciled**: YES (155 difference is explicitly bounded and declared UNRESOLVED_FROM_AVAILABLE_ARTIFACTS; 82,272 is the empirical truth).
5. **Duplicate-SHA Policy Frozen**: YES (Option B: retain and model hierarchically using a 3-level model).
6. **Git Linkage Reproducible**: YES (Validated in pilot).
7. **RefactoringMiner Pilot Valid**: YES (Executed on actual historical Abdalkareem19 SHAs).

## DECISION: FAIL
The empirical gate has **FAILED** because we cannot genuinely verify the project eligibility criteria (population) without performing full Git clones of all 100 repositories. The previous 15C claim of "PASS" was based on a false extrapolation of partial API data.

**Next Steps**: We must physically clone the repositories to definitively prove the 5-year and 5000-commit criteria, or formally adjust the criteria if extraction proves impossible. The study cannot proceed to final ML training until the analytical population is physically verified as ELIGIBLE or INELIGIBLE.
