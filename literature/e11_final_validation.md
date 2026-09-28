# Final E11 Validation

**STATUS**: DEFENSIBLE

## RESEARCH PROBLEM
Machine-learning-based Predictive Test Selection (PTS) models rely heavily on historical file-path change frequencies and code-test co-occurrence matrices. When structural refactorings (such as class renames, method moves, or cross-module relocations) occur, these historical file identities are altered or destroyed. This identity loss potentially induces a distribution shift in the ML features, blinding the model to historical failure correlations and causing it to silently skip necessary tests (false negatives / missed regressions).

## RESEARCH GAP
While the vulnerability of deterministic/static Regression Test Selection (RTS) to refactorings is well-studied (e.g., Refactoring-Aware RTS), and industry practitioners intuitively acknowledge that code churn causes "model drift" in ML-based PTS, there is no peer-reviewed empirical study that systematically quantifies the False Negative Rate (FNR) degradation of ML PTS models stratified by specific AST-level structural refactorings using continuous CI commit streams.

## RESEARCH QUESTION
To what extent do structural refactoring transformations induce distribution shift in the features used by machine-learning-based predictive test-selection models, and does that shift increase the probability of missed regression tests?

### RQ1
Do structural refactoring commits exhibit a statistically significantly higher False Negative Rate (missed regressions) in ML-based PTS models compared to standard feature-addition commits?

### RQ2
Which specific categories of refactoring (e.g., class renames, method moves, cross-module extractions) are most strongly associated with PTS false negatives?

### RQ3
Is the degradation in predictive performance explained by the loss of historical file-path identity and the resulting feature distribution shift?

### RQ4
Can augmenting ML PTS models with explicit AST/structural transformation features (e.g., tracking moved code back to its original file identity) mitigate the increase in false negatives?

## HYPOTHESES
* **H1**: Structural refactoring categories are associated with statistically significant differences in PTS false-negative behavior compared to non-refactoring commits.
* **H2**: Identity-changing and cross-module transformations produce larger feature-distribution changes (model drift) than refactorings that preserve file/symbol identity, leading to higher missed regression risk.
* **H3**: Adding structural identity-mapping information to the PTS feature set reduces false-negative behavior on refactoring commits, provided the observed failures are primarily caused by representation shift rather than underlying logical changes.

## EXPECTED SCIENTIFIC CONTRIBUTION
**New empirical finding and failure characterization.** 
The study will provide the first rigorous empirical measurement of ML PTS failure modes bounded to AST-level structural changes. It will expose and quantify a critical "silent regression risk" in modern ML-driven CI pipelines, establishing a baseline for refactoring-aware ML test selection.

## CLOSEST PRIOR WORK
1. **Machalica et al., "Predictive Test Selection" (ICSE-SEIP 2019)**: Establishes the baseline for ML-based PTS but evaluates overall performance in aggregate.
2. **Wang et al., "Towards refactoring-aware regression test selection" (ICSE 2018)**: Investigates refactoring entirely in the context of static, dependency-based RTS, not machine learning.
3. **Industry technical blogs (BrowserStack, Meta, Launchable, 2023-2024)**: Acknowledge that "model drift" requires scheduled retraining and manual heuristics to handle deep refactoring safely.

## EXACT DIFFERENCE FROM PRIOR WORK
E11 bridges the gap between static AST refactoring analysis and ML-based test selection. 
- Prior ML PTS work evaluates performance in aggregate, ignoring structural refactoring classifications.
- Prior Refactoring-Aware RTS work evaluates deterministic dependency graphs, ignoring ML feature drift.
E11 specifically audits the False Negative Rate of ML models under the stress condition of identity-modifying refactorings.

## THREATS TO VALIDITY
1. **Temporal Leakage**: Evaluating PTS models requires strict chronological splits; random cross-validation invalidates results.
2. **Flaky Tests**: Tests failing for non-deterministic reasons could be misattributed to refactoring-induced model failure.
3. **Confounding Commits**: "Mixed" commits that contain both deep logical changes and refactorings might obscure whether a false negative was caused by the structural shift or the logical bug.

---

### What evidence would still be required before implementation?
Before committing to implementation, we must verify that public continuous CI datasets (e.g., TravisTorrent, GitHub Actions logs) contain a statistically sufficient volume of *failing builds* that isolate pure structural refactorings. If open-source refactoring commits rarely fail CI checks, there will be insufficient positive examples (missed regressions) to achieve statistical significance for the False Negative Rate.
