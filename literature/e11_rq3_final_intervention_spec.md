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

## 3. Experimental Controls and Train/Inference Consistency
To isolate the effect of this mapping intervention and avoid representation mismatch:
* **Baseline PTS**: Standard frozen baseline feature construction for training, validation, and test sets.
* **Identity-Aware PTS**: Uses the exact same model family and is trained on the exact same training population. The historical identity mapping is applied consistently whenever the affected representation can be determined from information available *before* prediction.
  - *Training Feature Construction*: Applies the mapping to historical renames that occurred prior to the training build.
  - *Validation Feature Construction*: Applies the mapping to renames prior to the validation build.
  - *Test Feature Construction*: Applies the mapping to renames in the current commit using ONLY information available by the prediction timestamp. No future test outcome may enter the mapping.
* **Evaluation**: Compare the $FailureMissRate$ of the Baseline PTS against the Identity-Aware PTS on the subset of `REF_MIXED` commits that contain directly exposed refactorings (file renames/moves).

This directly tests H3: whether preserving the disrupted historical representation rescues the elevated miss rate.
