# Phase 13D: RQ1 Alignment Audit

## 1. Issue Addressed
The previous formulation of RQ1 asked whether "refactoring-containing commits" exhibit different behavior than "non-refactoring commits." However, "refactoring-containing" silently collapsed the `REF_ONLY` (pure refactoring) and `REF_MIXED` groups. Since `REF_ONLY` commits mathematically almost never contain failing tests (due to the behavior-preserving intent of pure refactoring), collapsing them into `REF_MIXED` creates theoretical ambiguity and dilutes the treatment definition.

## 2. Correction
RQ1 has been explicitly aligned to the primary experimental contrast:
* **New RQ1**: "Do REF_MIXED commits exhibit different test-level missed-failure behavior in the specified history-based ML-PTS formulation than comparable NON_REF commits?"

## 3. Subgroup Treatment
The `REF_ONLY` subgroup will be reported separately as a descriptive statistic. It is NOT silently merged into `REF_MIXED`.

## 4. Documents Updated
The primary contrast has been verified and updated across:
* `e11_research_design.md`
* `e11_rq_hypothesis_matrix.csv`
* `e11_variables.md`
* `e11_go_no_go.md`
