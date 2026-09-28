# Phase 12B Design Change Log (E11)

This log documents the methodological corrections made to the E11 research design to ensure scientific rigor and avoid premature claims.

1. **Corrected Build-Level False Negative Definition**: Separated `test-level miss` from `build-level regression escape`. A build is not a regression escape if at least one selected test catches the regression. Conflating the two was inaccurate.
2. **Reframed RQ3**: Replaced the causal mediation question ("Is the difference explained by...") with an experimentally testable intervention question: "To what extent is the refactoring-associated change in PTS performance attenuated when historical code identity is preserved through structural mapping?"
3. **Narrowed PTS Claim**: Removed generalizations about "industrial PTS systems." Scoped the baseline strictly to "history-based tabular ML-PTS models using the specified feature family."
4. **Refined Pure Refactoring Definition**: Replaced "pure refactoring" with "candidate pure-refactoring commit" (RefactoringMiner detection + no non-refactoring code changes). Added a requirement for manual validation of a stratified sample to estimate labeling reliability, acknowledging that tool detection is not absolute proof of behavior preservation.
5. **Redefined Primary Outcome**: Changed from continuous FNR to a binary indicator `test_missed` (1 if an actual failing test was not selected, 0 if selected). Made build-level regression escape a distinct secondary outcome.
6. **Operating-Point Procedure**: Removed arbitrary probability thresholds. Implemented a strict Train/Validation/Test operating-point procedure where the execution threshold is tuned on the validation set based on a time-reduction budget and frozen for the test set evaluation.
7. **Revised Statistical Plan**: Removed the Mann-Whitney U test as the default. Acknowledged the hierarchical nature of the data (test → commit → repository) requiring clustered/mixed-effects models. Explicitly stated that the exact statistical test will not be finalized until a dataset census confirms failure prevalence and class imbalance.
8. **Specified Identity-Aware Interventions**: Clarified that RQ3 will be tested via Baseline PTS vs. Identity-Aware PTS using historical file identity mapping, moved-code mapping, and rename mapping.
9. **Revised Hypotheses**: Removed arbitrary numerical effect sizes (e.g., $RR \ge 3.0$). Rephrased H1–H3 to focus on associations, feature changes, and identity preservation without assuming outcomes.
10. **Narrowed External Validity**: Removed claims generalizing to all statically typed languages. Scoped strictly to mature open-source Java projects.
11. **Emphasized Data Power**: Highlighted that statistical power strictly depends on the conjunction of refactoring commits, actual failing tests, AND missed failing tests, necessitating a pilot data census before implementation.
