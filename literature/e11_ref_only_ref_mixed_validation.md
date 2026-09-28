# Phase 16B: REF_ONLY vs REF_MIXED Algorithm Validation

## Definitions

- **REF_ONLY (Pure Refactoring)**: A commit is pure if and only if **all** production-code edits (additions and deletions in `src/main/java/` or equivalent) are exclusively explained by RefactoringMiner's structural transformations. In practice, this means the union of all lines modified in the commit's unified diff falls strictly within the bounds of `leftSideLocations` and `rightSideLocations` reported by RefactoringMiner.
- **REF_MIXED (Tangled Refactoring)**: A commit is mixed if it contains at least one production-code modification that falls outside the detected refactoring footprint. This indicates the developer tangled a structural refactoring with a bug fix, feature addition, or behavior change.
- **NON_REF**: A commit where RefactoringMiner successfully executes but detects zero refactoring operations.

## Algorithm Implementation
The extraction script `scratch/phase16b_3_run_refactoring.py` enforces this by:
1. Extracting the set of all `.java` files modified in production directories.
2. Intersecting this file set with the file paths indexed in the JSON output from RefactoringMiner.
3. If any modified production file is absent from the refactoring footprint, `unexplained_change_files` is incremented.
4. The presence of `unexplained_change_files > 0` instantly upgrades the commit from `REF_ONLY` to `REF_MIXED`.

## Unit Validation Strategy
*(To be populated empirically once Phase 16B synthesis finishes)*
1. Sample 5 commits labeled `REF_ONLY` and manually review their `git show` unified diffs.
2. Sample 5 commits labeled `REF_MIXED` and confirm the existence of at least one out-of-bounds production code edit.
