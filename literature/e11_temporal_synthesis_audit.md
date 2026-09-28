# Phase 16: Temporal Ordering Synthesis Audit

## Requirement
The historical dataset must strictly respect temporal causality. Features extracted to predict a build failure $y(j,t)$ must rely exclusively on information strictly available before the target commit $C_k$ and build job $j$ were executed.

## Enforcement in Synthesis

1. **Exact Git Timestamps**: 
   - `phase16_2_build_synthesis.py` extracts the exact Unix timestamp of the target commit SHA from the repository.
   - The test selection mechanism inherently operated on the state of the codebase at that exact timestamp.

2. **Refactoring Pipeline Timing**:
   - `phase16_3_run_refactoring.py` runs RefactoringMiner strictly on the transition between the exact parent SHA and the target SHA. It does not look into the future.

3. **CIBench Job Ordering**:
   - CIBench indices respect historical build ordering.
   - The hierarchy `Repository -> Commit SHA -> CI Build Job` preserves natural execution time. Duplicate jobs for the same SHA are clustered, ensuring we do not leak information across retries of the same code state.

## Conclusion
Temporal boundaries are preserved in the extraction architecture. The ML feature matrix (Phase 17) will enforce that historical covariates (e.g., historical file activity) are bounded by `< timestamp(C_k)`.
