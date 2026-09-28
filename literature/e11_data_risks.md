# Phase 13: Data Risks (E11)

## 1. The Intersection Sparsity Risk
The core scientific unit of this study requires the conjunction of three conditions on a single commit:
1. It must be a **candidate pure-refactoring commit** (no feature changes).
2. It must have **at least one actual failing test** in the continuous CI ground truth.
3. The failing test must be a **test-level miss** by the PTS model.

**Analysis**:
* Pure refactoring commits are statistically rare in continuous integration streams ($< 5\%$ of all commits, as developers typically mix refactorings with feature additions).
* Test failures are the minority class in CI ($~2-5\%$ of test executions).
* Pure refactorings, by definition, preserve behavior, meaning their true test failure rate should approach $0\%$. When they do fail, it is a rare edge case.
* The probability of finding a sufficient sample of (Pure Refactoring $\cap$ Actual Failure $\cap$ Test Miss) is extremely low in publicly available datasets (like the 20 Java repositories in RTPTorrent).

## 2. Incomplete Public Datasets
The massive CI datasets typically used to power ML models (e.g., TravisTorrent, 2.6 million builds) **do not contain individual test outcomes**. They only track aggregate counts (`tests_ran`, `tests_failed`). Without the exact name of the failed test, it is impossible to evaluate a Predictive Test Selection model's test-level False Negative Rate.
Datasets that *do* contain parsed test-level outcomes (e.g., RTPTorrent, CIBench) are significantly smaller (10–20 repositories). This compounds the sparsity risk identified above.

## 3. Temporal Leakage in Feature Construction
Constructing the historical co-occurrence matrix $P(\text{Test}_j \text{ fails} \mid \text{File}_i \text{ modified})$ requires sliding-window parsing of past test failures. In smaller datasets, the "burn-in" period required to populate this matrix consumes a massive portion of the chronological history, leaving even fewer commits for the validation and test phases.

## 4. Refactoring Category Attrition (RQ2 Risk)
RQ2 requires stratifying the false negatives by refactoring category (e.g., Rename vs. Move Method). Given the sparsity of the top-level outcome, stratifying it further into 4-5 categories will almost certainly result in single-digit counts for specific operations, rendering statistical inference (mixed-effects models) severely underpowered and unreliable.
