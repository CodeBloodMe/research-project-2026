# Phase 14: Final Research Design (E11)

## 1. Problem
Machine-learning-based Predictive Test Selection (ML-PTS) systems utilize historical code-test correlation data to probabilistically drop tests. Structural code refactorings alter the identities (e.g., file paths, method signatures) that these models use to index history, potentially causing silent degradation in prediction accuracy.

## 2. Motivation
If refactoring code systematically blinds the CI pipeline's test selection model, developers are disincentivized from maintaining code hygiene, as structural improvements will inadvertently allow regressions to escape into production.

## 3. Precise Gap
While traditional Regression Test Selection (RTS) has been evaluated for refactoring robustness, the specific failure mode where *history-based ML tabular features* lose their index linkages due to identity-altering refactorings remains underexplored.

## 4. Prior Art
The baseline model is derived from Machalica et al. (2019, ICSE-SEIP). Static RTS tools (Legunsen et al. 2016) and dynamic tools (Gligoric et al. 2015) handle structural changes differently and do not suffer from historical feature shift. Fazlalizadeh et al. (2009) examined refactoring prioritization using static heuristics, not ML-PTS. 

## 5. Population
History-based tabular ML-PTS models evaluated on the CI build histories of mature, open-source Java repositories.

## 6. Dataset
The study uses CIBench (Jin & Servant, 2021, DOI: 10.5281/zenodo.4682056). Descriptive dataset stats: 100 projects, 82,427 builds, 13,464 failing builds (before E11 filtering).

## 7. Observation Unit
A `(commit d, test t)` pair representing a specific candidate test execution. Ground truth $y(d,t) = 1$ if the test actually failed.

## 8. Treatment/Control
* **Treatment**: `REF_MIXED` (commits containing at least one RefactoringMiner operation + non-refactoring production changes).
* **Control**: `NON_REF` (commits with production changes but 0 refactoring operations).

## 9. Refactoring Labels
Computed via RefactoringMiner 3.0. `REF_ONLY` vs `REF_MIXED` is determined by an AST differencing check proving non-refactored code was modified. Manual validation on a stratified sample of 100 commits is required.

## 10. Baseline PTS
A reduced history-based LightGBM model derived from Machalica et al. (Option B), deliberately omitting internal dependency-graph features to isolate the historical representation vulnerability.

## 11. Feature Vector
File/Path Identity, Code Churn, Historical Test Failure Rate, Historical Code-Test Co-occurrence, Common Path Tokens. (TF-IDF/CodeBERT are explicitly excluded).

## 12. Ground Truth
The actual pass/fail test outcomes generated during the CIBench recorded CI build.

## 13. Outcomes
* **Primary**: `FailureMissRate` (proportion of actual failing tests missed by the model).
* **Secondary**: `Build-level Regression Escape`, `SelectionRate`, `TestTimeSaved`.

## 14. RQs
* **RQ1**: Do REF_MIXED commits exhibit different test-level missed-failure behavior in the specified history-based ML-PTS formulation than comparable NON_REF commits?
* **RQ2**: Are refactorings that alter representations directly used by the history-based PTS baseline associated with greater feature distribution shift and missed-failure behavior than refactorings without direct representation changes?
* **RQ3**: To what extent does preserving the affected historical representation through structural mapping attenuate the observed missed-failure behavior for refactoring commits?
* **RQ4**: (Secondary/Exploratory) Do AST/dependency structural features improve robustness on refactoring commits?

## 15. Hypotheses
* **H1**: REF_MIXED commits are associated with increased PTS test-level missed-failure rates compared to NON_REF commits.
* **H2**: Operations altering represented identity levels exhibit greater shift and miss behavior than non-altering operations.
* **H3**: Preserving disrupted historical representations reduces the elevated missed-failure behavior.

## 16. Estimands
Average Treatment Effects (ATE) evaluated via hierarchical mixed-effects regression models on test executions clustered within commits and repositories.

## 17. Confounders
Commit Size (churn), Temporal Window (project age), and Repository Culture. Controlled via mixed-effects modeling and a sensitivity PSM analysis.

## 18. Temporal Protocol
Strict boundaries: No information generated during or after commit $d$ may enter the historical feature vector $x(d,t)$.

## 19. Flakiness Protocol
Repeated builds use the outcome of the first run. Any tests known to be flaky in CIBench documentation are excluded from the candidate universe to minimize noise.

## 20. Calibration/Selection Policy
Test selection operates via a global or repository-specific probability threshold calibrated strictly on training/validation data to achieve a target historical recall (e.g., 95%).

## 21. Statistical Model
Hierarchical Mixed-Effects Logistic Regression predicting Failure Misses. 

## 22. RQ3 Intervention
Intercepting file renames/moves at prediction time to query the historical failure matrix using the old file path, injecting that history into the new file path's feature vector.

## 23. RQ4 Status
EXPLORATORY ANALYSIS. (Not required for the core causal claim, but useful context).

## 24. Threats to Validity
Construct validity (RefactoringMiner accuracy, AST diff mapping), External validity (Java/CIBench bias), Internal validity (unobserved confounders like developer skill).

## 25. Data-Power Gate
DATA NOT YET MEASURED. Power calculations will occur after the full CIBench metadata extraction.

## 26. Remaining Unknowns
The exact yield of `REF_MIXED` commits containing failing tests across the 100 repositories is unknown until the schema is parsed.

# FINAL STATUS
**DESIGN FROZEN WITH EMPIRICAL GATE**
