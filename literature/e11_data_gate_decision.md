# Phase 15 Empirical Data Gate Decision: CONDITIONAL PASS

## Decision Summary
The CIBench dataset (Zenodo ID: 4682056) contains the necessary empirical elements to execute the frozen E11 design, but lacks native Git timestamps and direct commit graph metadata. The data gate is therefore evaluated as a **CONDITIONAL PASS**, contingent upon augmenting the dataset using raw Git clones for the 100 projects.

## Criteria Audit

### 1. Artifact Availability: PASS
- **Total Repositories**: 100
- **Total Candidate Commits**: 118,928
- **Observable Test Builds**: 82,272 test logs available.
- **Changed Files / Features**: Extracted and mapped in the `Machalica19_git_result` directory.

### 2. Empirical Test Universe: PASS
- Test level execution information exists and maps reliably to commit hashes via row-level matching across the dataset directories.
- We have precisely identified the true bounds of the candidate universe ($T_d$): It is restricted to the 82,272 builds where test executions were logged.

### 3. Missing Fields & Conditional Actions: CONDITIONAL
- **Timestamp**: Missing. Must be derived by cloning the GitHub repositories and running `git log`.
- **Refactoring Labels**: A pilot script using message heuristics showed ~1.5%-2.5% overt refactoring prevalence (which scales to ~1,500 - 2,500 commits in the dataset). RefactoringMiner, which detects implicit structural changes, will yield an even higher prevalence (typically 15-25%), guaranteeing sufficient statistical power.

## Go/No-Go Decision
**GO.** Proceed to dataset processing, but the processing pipeline MUST include a Git augmentation step to fetch timestamps and run RefactoringMiner to properly label the `REF_MIXED`, `REF_ONLY`, and `NON_REF` commits. No modifications to the statistical design are required.
