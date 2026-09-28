# Phase 14: RQ3 Final Intervention Specification (E11)

## 1. The Core Vulnerability
The defined tabular baseline PTS uses File Identity (the path/name of a file) to look up historical failure rates and co-occurrences. When a refactoring alters the File Identity (e.g., `Rename Class` or `Move Class`), the historical link is severed. The new file appears to have zero history, despite logically being the same code.

## 2. The Intervention (Identity-Aware PTS)
The intervention is a specific, feature-engineering correction applied *prior* to prediction, independent of test outcomes.

**Mechanism: Historical File Path Mapping**
1. At prediction time $t_{commit}$ for commit $d$, detect if any file paths were altered by structural refactorings using RefactoringMiner.
2. If `OldPath` was renamed/moved to `NewPath`, intercept the feature construction for `NewPath`.
3. Query the historical code-test failure matrix using `OldPath`.
4. Inject the historical features (failure rate, co-occurrence) of `OldPath` into the feature vector for `NewPath`.

## 3. Experimental Controls
To isolate the effect of this mapping intervention:
* **Model Class**: The exact same GBDT model architecture and hyperparameters are used.
* **Train/Test Population**: Evaluated on the exact same set of test executions.
* **Operating Point**: The threshold selection procedure remains identical.
* **Evaluation**: Compare the $FailureMissRate$ of the Baseline PTS against the Identity-Aware PTS on the subset of `REF_MIXED` commits that contain directly exposed refactorings (file renames/moves). 

This directly tests H3: whether preserving the disrupted historical representation rescues the elevated miss rate.
