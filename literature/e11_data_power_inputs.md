# Phase 15B: Descriptive Data Power Inputs

The following metrics were empirically extracted from the raw CIBench dataset for future power analysis. **No claim is made that the study is sufficiently powered at this stage.**

- **Number of eligible projects**: 100 (from `e11_actual_project_eligibility.csv`)
- **Observable builds**: 82,272
- **Observable test rows (Test Classes)**: Unknown (Requires full database parse; computationally intensive local python run interrupted)
- **Failing test instances (Test Classes with >0 failures)**: Unknown (Requires full database parse)
- **Refactoring commits**: Unknown (Requires full RefactoringMiner execution on Git clones)
- **REF_MIXED commits**: Unknown (Requires full RefactoringMiner execution on Git clones)
- **Direct-exposure commits**: Unknown (Requires full RefactoringMiner execution on Git clones)
- **Clustering**: Hierarchical (Test Classes nested within Builds/Commits nested within Repositories)
