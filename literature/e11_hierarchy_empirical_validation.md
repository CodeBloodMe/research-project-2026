# Phase 16C: Empirical Hierarchy Validation

## Theoretical Structure
The frozen statistical model dictates the following mixed-effects structure to account for duplication and retry environments in CIBench:
- **Level 3**: Repository
- **Level 2**: Commit SHA
- **Level 1**: CI Build Job
- **Observation Unit**: Test Class

## Empirical Counts
*(Actual quantities pending physical synthesis completion)*

- **Repositories**: pending
- **Commit SHAs**: pending
- **CI Build Jobs**: pending
- **Test Class Observations**: pending

## Diagnostics
Once the dataset is materialized, the following diagnostics must be run to determine if Level 1 (CI Build Job) collapses into singularity:
1. Average duplicate CI Build Jobs per Commit SHA.
2. Variance of failure outcomes across duplicate CI Build Jobs for identical Commit SHAs.
3. Solver convergence for the full 3-level GLMM.

If variance at Level 1 approaches 0 (i.e. retry environments almost always yield identical outcomes), the structure will be empirically downgraded to `Repository -> Commit SHA -> Test Class`.

*(Status: Pending background extraction)*
