# Phase 13C: E11 Design Consistency Audit

## 1. Unit of Analysis Alignment
* **Issue**: Earlier documents conflated "pure refactoring commits" with the sole viable treatment. 
* **Resolution**: All core documents (`e11_research_design.md`, `e11_variables.md`, `e11_rq_hypothesis_matrix.csv`, `e11_go_no_go.md`) have been strictly aligned to the defined categories: `REF_ONLY`, `REF_MIXED`, and `NON_REF`. The primary experimental contrast for RQ1 is now `REF_MIXED` vs `NON_REF`.

## 2. Refactoring Category Mapping (RQ2 vs H2)
* **Issue**: The hypothesis matrix had a structural misalignment where RQ2 asked an open question about categories, but H2 assumed a specific identity-changing mechanism.
* **Resolution**: The taxonomy document (`e11_refactoring_operation_taxonomy.md`) explicitly formalizes `IDENTITY-CHANGING` vs `IDENTITY-PRESERVING` operations. RQ2 has been rewritten to explicitly query these classes, perfectly aligning with H2.

## 3. Power Claims Audit
* **Issue**: Unsupported assertions of statistical power were present in the feasibility documents based only on the subset pilot.
* **Resolution**: Replaced with explicit statements in `e11_research_design.md` that power will only be asserted *after* the full dataset extraction is complete.

## 4. CIBench Dataset Identity
* **Issue**: Confusion existed between the LLM CIBench benchmark and the regression testing CIBench dataset.
* **Resolution**: Explicitly anchored to Jin & Servant (DOI: 10.5281/zenodo.4682056) in `e11_cibench_schema_verification.md`, logging its exact published descriptive statistics.

## 5. Next Phase Guardrails
* **Action**: No ML model training, feature extraction, or full statistical inference is to be attempted until the final complete schema extraction of the massive CIBench/RTPTorrent datasets is successfully unblocked and downloaded. The current state is purely a validated, operational research design.
