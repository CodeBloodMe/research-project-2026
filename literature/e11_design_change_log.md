# Phase 13C: E11 Design Change Log

## 1. Unit of Analysis Update
* **Previous State**: The primary treatment was restricted to "Candidate pure-refactoring commits" (commits with absolutely no functional/feature code).
* **New State**: The primary treatment is now **"REFactoring-containing commit"** (any commit in which RefactoringMiner detects at least one structural refactoring operation).
* **Rationale**: Phase 13B proved empirically that pure-refactoring commits are extraordinarily rare (~0% of refactoring commits in the pilot), leading to artificial data sparsity. Moreover, mixed commits (refactoring + functional changes) are the realistic scenario where a refactoring might obscure a real functional regression from a PTS model. The updated definition establishes three groups (REF_ONLY, REF_MIXED, NON_REF) for strict reporting.

## 2. Refactoring Category Mapping (RQ2 vs H2 Alignment)
* **Previous State**: RQ2 asked an open-ended question about "which refactoring categories" cause issues, while H2 explicitly hypothesized that *identity-changing* refactorings cause the most shift, creating a mismatch between the inductive RQ and the deductive Hypothesis.
* **New State**: RQ2 and H2 have been explicitly aligned. RQ2 now asks: "Which classes of structural refactoring are associated with differences in missed-failure behavior...?", directly leveraging the new formal taxonomy of `IDENTITY-CHANGING` vs `IDENTITY-PRESERVING` operations. H2 maps perfectly to this by hypothesizing that `IDENTITY-CHANGING` operations yield significantly higher missed-failure rates than `IDENTITY-PRESERVING` operations.
* **Rationale**: Eliminates theoretical confusion and provides a scientifically coherent mapping from taxonomy to question to hypothesis.

## 3. Power Claims Removed
* **Previous State**: Documents made claims such as "RQ2 is adequately powered."
* **New State**: All definitive statements regarding statistical power have been deleted and replaced with "Power will be assessed after the empirical census."
* **Rationale**: Prevent hallucination or assumption of statistical power prior to processing the massive, final multi-project dataset.

## 4. CIBench Identity Corrected
* **Previous State**: Minor confusion regarding CIBench schema availability.
* **New State**: Standardized exactly on the Jin & Servant CIBench dataset (DOI: 10.5281/zenodo.4682056) recognizing its published facts (82,427 builds, 100 projects, 13,464 failing builds).
