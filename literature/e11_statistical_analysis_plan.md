# Phase 14B: Statistical Analysis Plan (E11)

## RQ1: Miss-Rate Association
* **Response**: $m(d,t)$ (binary, $1$ = test missed, $0$ = test selected), evaluated exclusively where actual failure $y(d,t) = 1$.
* **Exposure**: `REF_MIXED` vs `NON_REF` (binary).
* **Covariates**: Log code churn, Number of files changed, Historical file activity.
* **Grouping**: Random intercepts for `Repository` and `Commit`.
* **Effect Measure**: Adjusted Odds Ratio (aOR) or Risk Difference.
* **CI**: 95% Confidence Interval computed via profile likelihood or bootstrap.
* **Model Family**: Hierarchical Mixed-Effects Logistic Regression. (Mann-Whitney U is explicitly insufficient due to nested data).

## RQ2: Exposure Mechanisms
* **Direct vs Indirect Exposure**: Handled as multi-label binary indicators (`exposure_direct`, `exposure_indirect`).
* **Handling Multiple Indicators**: Commits containing both direct and indirect operations are coded with both indicators active. The regression models the marginal contribution of each exposure type.
* **Multiplicity Correction**: P-values for exploratory operation-level subcategories (e.g., Rename vs Move) will be adjusted using the Benjamini-Hochberg (FDR) procedure.

## RQ3: Identity-Aware Intervention
* **Comparison**: Paired comparison between Baseline PTS and Identity-Aware PTS on the exact same test instances.
* **Data Subset**: Restricted to `REF_MIXED` commits exhibiting `exposure_direct = 1` (where the intervention actually applies).
* **Effect Measure**: Absolute difference in $FailureMissRate$.
* **Clustering/Method**: Paired Hierarchical Mixed-Effects Logistic Regression (adding a random slope for the intervention effect per repository), or cluster-robust bootstrapping to account for non-independence.

## RQ4: Structural Features
* **Status**: Exploratory Analysis only. (Used to contextualize if providing the AST graph back to the ML model rescues performance, secondary to the main historical degradation claim).
