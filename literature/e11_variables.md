# Phase 12B: Variables and Definitions for E11

## 1. Precise Definitions
* **commit**: A Git revision representing a single logical change recorded in the repository history.
* **REF_ONLY (pure-refactoring commit)**: A commit where RefactoringMiner detects structural operations, and NO non-refactoring production-code changes are detected.
* **NON_REF (non-refactoring commit)**: A commit with production-code changes where zero refactoring operations are detected by RefactoringMiner.
* **REF_MIXED (mixed commit)**: A commit containing both RefactoringMiner-detected refactoring operations and other feature/functional modifications. This is the primary treatment group.
* **selected test**: A test case predicted to have a failure probability above the defined execution threshold by the PTS model, thus scheduled for execution.
* **omitted test**: A test case predicted by the PTS model as likely to pass (below the execution threshold), and thus skipped during the CI run.
* **actual failing test**: A test case that fails during the ground-truth deterministic execution of the full test suite for a given commit.
* **test-level miss**: An instance where an *actual failing test* is *omitted* by the PTS model.
* **build-level regression escape**: An instance where the actual regression is not exposed by *any* selected failing test, so the PTS-selected execution as a whole would not reveal the failure to the developer.

## 2. Feature Groups (ML Baseline & Identity-Aware)
* **File Identity/Path**: Modified file names, file extensions, and directory paths (the primary representation mechanism for the tabular baseline).
* **Code Churn**: Number of lines added, lines deleted, and total files changed in the commit.
* **Historical Failure Relationships**: The failure rate of the test in recent history, and historical code-test co-occurrence.
* **Identity-Aware Information** *(For RQ3 Intervention)*: Historical file identity mapping, moved-code mapping, rename mapping, or structural refactoring indicators.

## 3. RQ2 Analytical Variables (Multi-Label Representation)
Because a single commit may contain multiple refactoring operations acting on different semantic levels, the structural alteration is represented via non-mutually exclusive binary indicators:
* `identity_file_change = 0/1`: Operations affecting file/path identity (e.g., Rename Class, Move Class).
* `identity_method_change = 0/1`: Operations affecting symbol/method identity but preserving the file (e.g., Rename Method, Move Method within same package/class).
* `identity_signature_change = 0/1`: Operations altering method signatures (e.g., Change Parameter Type).
* `local_structural_change = 0/1`: Operations affecting local AST tokens (e.g., Extract Variable, Rename Variable).

## 4. Outcomes
### Primary Outcome
* **Test Missed ($Y_{miss}$)**: A binary outcome defined at the test-execution level.
  * `test_missed = 1`: if an actual failing test was omitted by the PTS model.
  * `test_missed = 0`: if an actual failing test was selected by the PTS model.

### Secondary Outcomes
* **Build-Level Regression Escape**: A binary outcome indicating if the build failed to expose the regression.
* **Test-Time Reduction**: The percentage of test execution time saved by omitting tests (to ensure the threshold operating point is met).
* **Feature Distribution Shift**: Quantified comparing the distribution of PTS input features on feature commits versus refactoring commits.

## 4. Confounders
* **Commit Size**: Larger commits (more code churn) are inherently riskier. Must be controlled as a covariate.
* **Repository Hierarchy**: Commits and tests are nested within repositories, representing different engineering cultures and test structures. Must be controlled via hierarchical/clustering models.
* **Flaky Tests**: Tests failing for non-deterministic reasons introduce outcome noise. Must be strictly filtered.
