# Phase 13E: RQ2 and RQ3 Revision Documentation

## 1. Separation of Refactoring Effect and PTS Exposure
Previous iterations of the research questions conflated the *effect* of a refactoring operation (e.g., renaming a method) with its *exposure* to the PTS baseline. Because the defined PTS baseline uses *file-level* historical co-occurrence and code churn, a method rename does not directly destroy the represented file identity; rather, it manifests indirectly as code churn.

## 2. Revised RQ2
* **Old**: "Which classes of structural refactoring (file/path, method/symbol, signature, local/token) are associated with differences in missed-failure behavior and/or PTS feature distribution?"
* **New**: "Are refactorings that alter representations directly used by the history-based PTS baseline associated with greater feature distribution shift and missed-failure behavior than refactorings without direct representation changes?"
* **Rationale**: This centers the investigation on the causal mechanism (baseline representation exposure). The specific structural operation-level analysis (e.g., Method Rename vs. Variable Extract) remains as a secondary descriptive analysis, but the primary scientific contrast is DIRECT vs. INDIRECT exposure.

## 3. Revised RQ3
* **Old**: "To what extent does preserving historical code identity through structural mapping attenuate any observed performance difference?"
* **New**: "To what extent does preserving the affected historical representation through structural mapping attenuate the observed missed-failure behavior for refactoring commits?"
* **Rationale**: The intervention is now explicitly bound to the representations actually disrupted. If a file is renamed, the mapping intervention must link the new file path to the old file path's history. It avoids promising interventions for method/symbol identities if the baseline PTS does not actually index them.

## 4. Updates Applied
These rewritten RQs have been synchronized across:
* `e11_research_design.md`
* `e11_rq_hypothesis_matrix.csv`
* `e11_design_change_log.md`
