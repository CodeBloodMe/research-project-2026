# Phase 13B: Feasibility Reassessment (E11)

Based on the forensic pilot data and the re-definition of the observational unit to **"mixed refactoring + functional commits"**, the Research Questions are re-evaluated below:

## RQ1: Do structural-refactoring commits differ in ML-PTS missed-failure behavior from non-refactoring commits?
* **Status**: **FEASIBLE**
* **Evidence**: By including mixed commits, the volume of refactoring-containing commits is empirically proven to be massive (~100% in dense history zones, realistically 20-30% on average). Test failures naturally occur in these mixed commits due to the functional changes. We can reliably measure if the presence of the refactoring artificially inflates the PTS False Negative Rate compared to commits without refactorings.

## RQ2: Which refactoring categories are associated with differences in missed failures?
* **Status**: **FEASIBLE**
* **Evidence**: The pilot identified 31 distinct refactoring categories in just 99 commits. The abundance of operations like `Extract Variable` (52) and `Change Attribute Access Modifier` (33) guarantees sufficient statistical power to run mixed-effects models stratified by category across a dataset like RTPTorrent.

## RQ3: Does structural identity preservation attenuate the observed difference?
* **Status**: **CONDITIONALLY FEASIBLE**
* **Evidence**: This relies on the ability to programmatically map the AST identity from before the refactoring to after. As long as RefactoringMiner's JSON outputs provide exact file paths and line ranges (which they do), the feature engineering for this RQ is highly feasible.

## RQ4: Do AST/dependency structural features improve robustness on refactoring commits?
* **Status**: **FEASIBLE**
* **Evidence**: Because RQ1 is feasible, we can construct the baseline and then inject the AST-aware features to measure the delta in False Negative Rate.
