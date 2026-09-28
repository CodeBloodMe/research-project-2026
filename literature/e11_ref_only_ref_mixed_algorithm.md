# Phase 16: REF_ONLY / REF_MIXED Classification Algorithm

## The Suspicious Case (Phase 15D)
Commit `3e63e7a5e4234c8fd62d7ab1b5bd101390b9111e` was labeled `REF_MIXED` in the pilot despite having 0 changed production files, which raised a flag. Upon review, it appears the pilot script incorrectly classified it because of a naive condition (e.g., checking if `changed_file_count > 0` vs `changed_prod_files`). We must implement a mathematically rigorous algorithm to define pure refactorings.

## Definition

### REF_ONLY
A commit is classified as `REF_ONLY` (a pure refactoring commit) if and only if **all** production-code edits (modifications, additions, deletions within `src/main/java/` or equivalent) can be structurally explained by the refactoring operations detected by RefactoringMiner. If the AST difference exclusively maps to the refactoring transformations (e.g., a pure rename, or extract method with no other logic tweaks), it is pure.

### REF_MIXED
A commit is classified as `REF_MIXED` if at least one production-code change exists that is **outside** the bounds of the detected refactoring transformations. This means the developer tangled a structural refactoring with a bug fix, feature addition, or behavior modification in the same commit.

## Algorithmic Implementation (Post-RefactoringMiner)

1. **Extract Changed Files**: Query `git diff --name-only <parent> <commit>` for all production files.
2. **Extract Refactoring Footprint**: From the RefactoringMiner JSON output, extract the set of all file paths and line ranges involved in the refactoring operations (`leftSideLocations` and `rightSideLocations`).
3. **Diff Intersection**:
    - For each production file changed, calculate the unified diff (additions/deletions).
    - If any changed line falls outside the `rightSideLocations` or `leftSideLocations` bounding boxes of the refactorings, increment `unexplained_change_files`.
4. **Classification**:
    - If `unexplained_change_files == 0` AND `refactoring_count > 0`: **REF_ONLY**
    - If `unexplained_change_files > 0` AND `refactoring_count > 0`: **REF_MIXED**
    - If `refactoring_count == 0`: **NON_REF**

*Note: For the purposes of E11 dataset synthesis, any commit where the changed production file set is completely disjoint from the files modified in the RefactoringMiner footprint is immediately classified as REF_MIXED. Finer-grained line-level intersection will be applied where file sets overlap.*
