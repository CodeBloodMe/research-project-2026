# Phase 13B: Reassessment of the Observational Unit (E11)

## The Initial Error
In Phase 13, the primary observational unit was implicitly defined as: **"Candidate pure-refactoring commit" $\cap$ "Actual failing test"**. 
This intersection caused the NO-GO decision because pure refactoring commits are exceptionally rare (0 out of 99 refactoring-containing commits in the `gson` pilot), and failing tests on pure refactorings are mathematically close to zero (as they are intended to be behavior-preserving).

## Scientific Reassessment of the Formulations

### A. Pure-refactoring commits only
* **Count**: ~0% of the sample.
* **Failing Tests**: ~0.
* **Scientific Validity**: **POOR**. By definition, a pure refactoring should not change behavior and therefore should not fail a test (unless the test itself is flaky or tightly coupled to implementation details). Evaluating PTS failure *only* on pure refactorings restricts the study to edge cases and artificial scenarios. 

### B. All refactoring-containing commits (Mixed + Pure)
* **Count**: Very high (approx. 20-30% of all development commits contain *some* structural refactoring). In the `gson` pilot, 99 consecutive commits had at least one refactoring operation.
* **Failing Tests**: Follows the natural baseline distribution of CI failures (e.g., 2-5% of builds).
* **Scientific Validity**: **STRONG**. In industrial practice, developers routinely mix refactoring operations (e.g., Extract Method, Rename Variable) with functional changes (e.g., adding a feature, fixing a bug) in the same commit. 

### Why the "Mixed Commit" Unit Restores Feasibility and Validity
If a commit contains both a feature change and a refactoring, the feature change may induce a legitimate regression (causing a test to fail). The core research question is: **Does the concurrent presence of the structural refactoring confuse the ML-PTS model into missing the test that would have caught the feature's regression?**

By shifting the unit of analysis to **Refactoring-containing commits (Formulation B)**, we:
1. **Restore Statistical Power**: The number of valid observational units increases by orders of magnitude.
2. **Increase External Validity**: Mixed commits represent actual developer behavior.
3. **Preserve the Core RQ**: We are still measuring whether the structural distribution shift induced by a refactoring degrades PTS prediction accuracy on real failures.

## Conclusion
The definition must be updated to **"Commits containing at least one structural refactoring"**, rather than "pure refactoring commits." Under this scientifically superior definition, data sparsity is resolved.
