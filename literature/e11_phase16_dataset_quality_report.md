# Phase 16: Dataset Quality Report

## CIBench Population
- **CIBench Population**: 100 projects.
- **Verified E11 Population**: Currently being processed via `phase16_1_verify_repos.py`.
- **Observable Builds**: Approximately 82,272 physically parsed log CSVs.

## Test-Class Synthesis
- **Unique SHAs**: Expected ~118k.
- **Duplicate SHA Groups**: Tracked via `data/e11_duplicate_sha_audit.csv`.
- **Test-class observations**: Normalization script `phase16_2_build_synthesis.py` running.
- **Failure-positive observations**: (pending extraction completion)
- **Error-only observations**: (pending extraction completion)
- **Skipped observations**: (pending extraction completion)

## RefactoringMiner Pipeline
- **Git linkage rate**: Tracked via `data/e11_git_linkage_full.csv`.
- **RefactoringMiner success rate**: Subset processed in `phase16_3_run_refactoring.py`.
- **Refactoring commits**: (pending pipeline completion)
- **REF_ONLY**: (pending pipeline completion)
- **REF_MIXED**: (pending pipeline completion)
- **Direct exposure**: (pending pipeline completion)
- **Indirect exposure**: (pending pipeline completion)

## Unresolved Data
- **Missing data**: 155 builds explicitly excluded as `UNRESOLVED_FROM_AVAILABLE_ARTIFACTS`.
- **Power claim**: None yet. Pending full matrix materialization.
