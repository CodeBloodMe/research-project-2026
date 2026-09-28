# Phase 16B: Historical Eligibility Protocol

## Core Principle
Repository eligibility (age, commit count, language, and test count) must be evaluated at the exact historical moment the dataset was extracted (the "CIBench Observation Cutoff"), not at the present-day state of the repository. Evaluating a project in 2026 for a dataset snapshotted in 2019 creates temporal data leakage and falsely validates projects that only met the criteria *after* the study period.

## 1. CIBench Observation Cutoff
- **Definition**: The specific commit SHA representing the most recent historical observation recorded for the project in `Abdalkareem19_git_result/<project>.csv`.
- **Extraction**: We will extract the last row from the project's Abdalkareem19 index to identify this cutoff SHA and query the repository for its exact timestamp.

## 2. Age and Commit-History Criteria
- **Earliest Commit Date**: Extracted via `git log --reverse`.
- **Age at Cutoff**: The duration between the earliest commit date and the cutoff timestamp. Must be > 5 years (1825 days).
- **Commit Count at Cutoff**: Computed via `git rev-list --count <cutoff_SHA>`. Must be > 5000 commits.

## 3. Java Status Criterion
- **Verification**: At the exact cutoff SHA, we will run `git ls-tree -r <cutoff_SHA>` to independently verify the presence of `.java` files. If the repository is completely devoid of Java files, or Java is clearly not the primary language (e.g., zero source files in `src/main/java`), it fails this criterion independently of CIBench metadata.

## 4. Test-History Criterion
- **Frozen Rule**: The E11 research design requires `>1,000 automated unit tests`.
- **Verification**: For each project, we will scan the physical `test_info_logs` for builds existing prior to the cutoff. We will sum the `total_tests` per build (or count unique test classes if `total_tests` is missing). The project must demonstrate at least one build containing > 1,000 executed test methods to satisfy the "mature test suite" requirement.

## Conclusion
This protocol guarantees that the empirical dataset is bounded exactly by the conditions of the open-source projects as they existed when the CIBench ground truth was finalized, preserving temporal validity.
