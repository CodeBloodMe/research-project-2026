# Phase 16C: Refactoring Label Validation

## Methodology
The classification of commits into `REF_ONLY`, `REF_MIXED`, and `NON_REF` is determined through a spatial intersection algorithm in `scratch/phase16b_3_run_refactoring.py`.

1. **NON_REF**: RefactoringMiner returns `SUCCESS` and detects 0 refactorings.
2. **REF_ONLY vs REF_MIXED**: We parse the exact `git diff -U0` of the commit to extract all changed line ranges (`+` and `-`) for every modified production Java file. We then query the `leftSideLocations` and `rightSideLocations` from RefactoringMiner's JSON output. 
   - If *every* changed line in the production diff falls within the `startLine` / `endLine` boundaries of the detected refactorings, the commit is classified as `REF_ONLY`.
   - If *at least one* line edit falls outside the refactoring boundaries, it implies manual non-refactoring edits occurred, classifying the commit as `REF_MIXED`.

## Label Count Summary
*(Pending completion of full dataset extraction)*
- **Total valid commits**: pending
- **NON_REF**: pending
- **REF_ONLY**: pending
- **REF_MIXED**: pending

## Validation Cases
Once the data is generated, we will randomly sample 5 `REF_ONLY` and 5 `REF_MIXED` commits and manually verify the diff boundary intersection to ensure the algorithm handles whitespace, comments, and multi-line statements correctly.
