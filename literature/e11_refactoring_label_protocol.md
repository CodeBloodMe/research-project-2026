# Phase 14: Refactoring Label Protocol (E11)

## 1. Tool Version Freeze
The classification relies exclusively on **RefactoringMiner version 3.0** (or the latest stable release at the time of final execution, frozen and documented). Hand-invented operations or heuristic regexes on commit messages are strictly prohibited.

## 2. Label Definitions
* **NON_REF**: The raw git diff indicates modifications to production source code (`.java` files outside test directories), but RefactoringMiner detects 0 refactoring operations.
* **REF_MIXED**: RefactoringMiner detects at least one valid structural refactoring operation AND an AST diff/coverage analysis reveals production-code modifications that fall *outside* the bounds of the detected refactoring operations.
* **REF_ONLY**: RefactoringMiner detects at least one valid structural refactoring operation AND the AST diff/coverage analysis reveals that 100% of the production-code modifications are fully accounted for by the detected operations (i.e., pure structural transformation with no functional changes).

## 3. Labeling Pipeline
1. Clone the repository and checkout the commit.
2. Run RefactoringMiner on the commit.
3. If 0 operations: Assign `NON_REF`.
4. If > 0 operations: Compute the AST differencing bounds (e.g., using GumTree or RefactoringMiner's internal bounds mapping). 
5. Subtract the refactoring bounds from the total changed production code bounds.
6. If the remainder is non-empty: Assign `REF_MIXED`. Else: Assign `REF_ONLY`.

## 4. Manual Validation
To estimate the reliability of this automated pipeline, a stratified random sample of 50 `REF_MIXED` and 50 `REF_ONLY` commits will be manually reviewed by two independent coders. Disagreements will be resolved via discussion, and the inter-rater reliability (Cohen's Kappa) and error rate will be explicitly reported in the final manuscript. The previous 99-commit Gson pilot is explicitly excluded from these power and prevalence estimates.
