# Phase 14: Temporal Leakage Protocol (E11)

## 1. Core Principle
A history-based ML-PTS model evaluates candidate tests at the exact moment a commit is submitted. To prevent temporal leakage, **no information generated during or after the current build execution may be used to construct the feature vector $x(d,t)$ for commit $d$.**

## 2. Temporal Boundaries for Features
For any build $B$ triggered by commit $d$ at timestamp $t_{commit}$:
* **Historical Code-Test Co-occurrence**: Computed strictly using builds completed before $t_{commit}$.
* **Historical Test Failure Rate**: Computed strictly using builds completed before $t_{commit}$.
* **Code Churn**: Extracted strictly from the Git diff of commit $d$ before the tests run.
* **Refactoring Label**: Extracted strictly by running RefactoringMiner on the Git tree of commit $d$.

## 3. Ground Truth Evaluation
* The actual test outcomes (pass/fail) generated during build $B$ constitute the ground truth $y(d,t)$.
* These outcomes are ONLY used during the evaluation step (and subsequent training windows for future commits). They NEVER enter the feature vector for build $B$.

## 4. Handling Build-Level Edge Cases
* **Duplicate/Retry Builds**: If a build is retried, the first run's outcome determines the ground truth for that commit state. Retries often introduce noise (e.g., flakiness resolution) that masks the deterministic state of the code. 
* **Branch/PR Builds vs Main Branch**: Historical features are typically aggregated across the main branch to ensure stability. CIBench metadata will be filtered to follow a unified branch history where possible, or clearly documented if PR histories are merged.
* **Test Additions/Removals**: A test added in commit $d$ has exactly 0 history. Its historical features are initialized to 0. A test removed in commit $d$ is not part of the candidate universe for $d$.
