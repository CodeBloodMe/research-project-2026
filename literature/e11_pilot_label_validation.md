# Phase 13D: Pilot Label Validation (E11)

## 1. Issue with Previous Pilot Claims
In Phase 13B, the pilot execution on `google/gson` reported 99 commits as "mixed refactoring + functional commits" (`REF_MIXED`), and 0 as "pure refactoring commits" (`REF_ONLY`). This classification was based on a flawed heuristic (the absence of the word 'refactor' in the commit message or cursory inspection), rather than a rigorous AST differencing between the RefactoringMiner-detected operations and the raw Git diff.

## 2. Correction
* The `gson` pilot is now strictly downgraded and labeled as a **"single-project operational pilot"**. 
* The previous statistics (99/99, 41/99, 0 pure refactorings) are NO LONGER presented as evidence of population prevalence or statistical power. They merely prove that the pipeline (RefactoringMiner + Git) can execute operationally.
* The "Mixed Commits" count has been replaced with the label **"Refactoring-Containing; Mixed Status Unresolved"**, explicitly stating that the exact delta representing non-refactoring production changes was not computed for every commit.

## 3. Requirement for Full Implementation
In the final data extraction pipeline, a commit may only be labeled as `REF_MIXED` if the raw Git diff of production files contains AST changes that are *not* entirely covered by the bounds of the RefactoringMiner-detected operations. If all AST changes are fully accounted for by the refactorings, the commit is `REF_ONLY`. Until this diff-coverage pipeline is built, mixed status remains unresolved.
