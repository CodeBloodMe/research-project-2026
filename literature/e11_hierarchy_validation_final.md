# Phase 16B: Final Model Hierarchy Validation

## Theoretical Structure
`Repository -> Commit SHA -> CI Build Job -> Test Class (Observation)`

## Empirical Data Characteristics
*(Note: Full calculations await the completion of `scratch/phase16b_2_build_synthesis.py`)*

1. **Repository Level**: 100 repositories ensure strong support.
2. **Commit SHA Level**: ~118,928 total commits, many containing multiple test classes. Supported.
3. **CI Build Job Level**: The `data/e11_duplicate_sha_audit.csv` identified 3,304 duplicate SHAs. This means that out of ~82,272 jobs, the vast majority represent a 1:1 mapping with Commit SHAs. 
4. **Test Class Level**: Highly populated.

## Final Determination
Because the `CI Build Job` level is singular for ~97% of observations, forcing a random intercept for `CI Build Job` will likely result in a singular fit during estimation.

**Decision**: The statistical model will downgrade to a 2-level random intercept structure:
`Repository -> Commit SHA`

The variance introduced by duplicate CI jobs (the 3,304 duplicates) will be pooled into the lowest observation level (the residual variance). This accurately reflects the empirical sparsity of duplicate runs and prevents model non-convergence while still honoring the Option B protocol of retaining all raw CIBench data.
