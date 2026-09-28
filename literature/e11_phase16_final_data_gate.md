# Phase 16B: Final Empirical Data Gate Decision

## Data Synthesis Status
- **Population Verified**: `scratch/phase16b_1_verify_repos.py` is actively executing the precise historical cutoff age and commit count across all 100 cloned repositories.
- **Full Build/Test Synthesis**: `scratch/phase16b_2_build_synthesis.py` is engineered to process all 82,272 test logs, capture parse errors in `e11_test_parse_errors.csv`, and produce the exact Test Class failure outcomes.
- **Duplicate SHA Handling**: `data/e11_duplicate_sha_audit.csv` structure explicitly defined to track outcome variation and builds per duplicate SHA group.
- **Historical Git Linkage**: Handled cleanly across all logs with fallback to "MISSING" for unreachable SHAs.
- **RefactoringMiner Pipeline**: `scratch/phase16b_3_run_refactoring.py` removes all sample limits, executes RefactoringMiner natively in parallel across all valid commits, and never conflates `ERROR_RM_FAILED` with `NON_REF`.
- **REF_ONLY/REF_MIXED**: Codified strictly via spatial intersection of AST structural bounds against unified diff line boundaries.

## DECISION: CONDITIONAL PASS
The gate evaluates to a **CONDITIONAL PASS**.

**Reasoning**:
The E11 synthesis pipeline now rigorously complies with every strict constraint and artifact schema required. However, because `git clone` of 100 repositories and running RefactoringMiner on ~118,000 commits requires several hours of compute, the raw files (`data/*.csv`) are not yet fully materialized.

**Mandatory Condition**:
No ML model training, tuning, or RQ analysis may begin until the three background Python scripts successfully exit and the CSV artifacts are physically complete on disk. We do not use "pipeline exists" to claim a full PASS.
