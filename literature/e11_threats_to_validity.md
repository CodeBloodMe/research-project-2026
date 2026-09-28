# Phase 12B: Threats to Validity (E11)

## Internal Validity
1. **Flaky Tests Misattribution**: Tests that fail non-deterministically may be incorrectly attributed as "test-level misses" caused by refactoring. 
   * *Mitigation*: Strict exclusion of tests that exhibit flakiness on the same commit hash or across identical branch states.
2. **Confounding Logical Changes**: A commit may contain both a structural refactoring and a deep logical bug. If the logical bug causes the test failure, attributing the test miss to the refactoring introduces omitted variable bias.
   * *Mitigation*: The primary experimental comparison isolates "candidate pure-refactoring commits" from feature commits, and includes manual validation of a stratified sample to estimate labeling reliability (ensuring they truly preserve behavior).
3. **Commit Size**: Refactoring commits often touch more files and lines of code than standard feature commits. Larger commits are inherently riskier. 
   * *Mitigation*: Regression analysis must control for commit size (lines added/deleted, files modified) as a covariate.

## External Validity (Generalizability)
1. **Tool and Language Scoping**: The experimental design relies on RefactoringMiner 2.0 and targets Java repositories. The results do not automatically generalize to all statically typed languages or dynamic languages, where refactoring patterns and ML-PTS feature representations behave differently.
   * *Mitigation*: Explicitly scope the scientific claims and conclusions to mature open-source Java projects.
2. **Open-Source vs. Industrial CI**: Open-source Java projects (even mature ones) might have different testing dynamics compared to proprietary industrial PTS systems.
   * *Mitigation*: Explicitly define the baseline as a "history-based tabular ML-PTS model using the specified feature family," rather than claiming it represents all proprietary industrial PTS systems.

## Construct Validity
1. **Refactoring Label Reliability**: RefactoringMiner detects structural operations, but detection does not guarantee absolute behavior preservation.
   * *Mitigation*: Require manual validation of a stratified sample of candidate pure-refactoring commits to estimate the noise/reliability of the labels.
2. **Evaluation Threshold Tuning**: Setting arbitrary probability thresholds during evaluation misrepresents how PTS systems are deployed in reality, where thresholds are tuned to a budget.
   * *Mitigation*: Use a strict Train/Validation/Test operating-point procedure, freezing the threshold based on a selection budget on the validation set.

## Conclusion Validity
1. **Statistical Power & Sparsity**: The statistical power of the primary outcome strictly depends on the conjunction of three sparse events: the number of pure refactoring commits, the number of actual failing tests, AND the number of test-level misses.
   * *Mitigation*: A dataset census must be conducted before the full study to ensure sufficient sample sizes and event prevalence.
2. **Hierarchical Data Structure**: Treating every test or commit as completely independent ignores the nested reality of software (tests belong to commits, commits belong to repositories).
   * *Mitigation*: The statistical plan must account for hierarchy (e.g., using repository clustering or mixed-effects models) to avoid artificially inflated significance levels.
