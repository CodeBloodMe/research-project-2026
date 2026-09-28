# Phase 15D: Refactoring Pilot Re-Audit

## The Invalid Phase 15C Pilot
In Phase 15C, the RefactoringMiner pilot used `git log -n 50` on the present-day `square/okhttp` repository to sample commits. This fundamentally invalidated the pilot for the following reasons:
1. **Timestamp Mismatch**: The sampled commits yielded timestamps from 2026, long after the CIBench dataset was constructed (circa 2019).
2. **Population Validity**: These recent commits are not part of the CIBench `Abdalkareem19_git_result` index. They have no corresponding test log outcomes in `test_info_logs` or `Machalica19_git_result`.
3. **Silent Shift**: Using present-day commits bypasses the actual empirical challenge of checking out historic SHAs which may have been rewritten, deleted, or force-pushed out of the repository.

## Cause of Error
The extraction script `scratch/run_phase15c_pilot.py` prioritized execution speed over empirical fidelity by invoking `git log -n 50` on the `HEAD` of the cloned repository rather than reading specific target SHAs directly from the CIBench `Abdalkareem19_git_result` CSV files.

## Correction Plan
The Phase 15C pilot is officially **INVALID_FOR_CIBENCH** and relegated to a tooling smoke test.

The corrected pipeline must:
1. Parse actual `commit_hash` values directly from `Abdalkareem19_git_result/[project].csv`.
2. Ensure the selected SHAs actually exist in the target repository.
3. Extract the genuine historical `git_timestamp` for that specific CIBench SHA.
4. Pass that historical SHA to RefactoringMiner for structural analysis.
