# Phase 15B: Build and Commit Relationships Audit

This document summarizes the exact, verified relationships between CIBench data indices, Git SHAs, and TravisCI builds.

## 1. Row Index = CI Build
The physical structure of the CIBench artifacts uses a 1-indexed line number in the `Abdalkareem19_git_result` project CSVs as the primary key. This row number uniquely maps to a single CI build output in `test_info_logs` and `Machalica19_git_result`.
- **Finding**: We have verified that a CSV (e.g., `10.csv`) in `test_info_logs` represents exactly one CI build attempt.

## 2. Duplicate Commits
A Python audit script (`scratch/audit_git_cibench.py`) verified the uniqueness of commit SHAs across the dataset.
- **Finding**: Out of 118,928 total rows, there are only 115,624 unique SHAs.
- **Conclusion**: There are exactly 3,304 duplicate SHAs in the dataset. Multiple CI builds can, and do, map to a single commit SHA. This is common in CI environments due to build retries, pull request syncs, or multi-environment matrix builds. 
- **Implication for E11**: The unit of analysis is the *CI Build* (the row index), not just the `commit_hash`. We must treat duplicate SHAs as separate builds, or explicitly deduplicate them prior to ML training.

## 3. Git Linkage
A random sample linkage audit (`scratch/git_linkage_audit.py`) was performed to map CIBench SHAs to fresh clones of `square/okhttp` and `square/picasso`.
- **Finding**: While most commits perfectly matched the current `main` branch of the repositories and successfully yielded standard Unix timestamps, **missing commits were detected** (e.g., `ba2c6acf...` in Picasso).
- **Conclusion**: The CIBench dataset contains SHAs that no longer exist in the upstream remote repositories (likely due to force-pushes, squashed PRs, or deleted branches after the CIBench snapshot was taken in 2019/2021). 
- **Implication for E11**: Any pipeline augmenting the dataset with timestamps or RefactoringMiner must handle missing/unresolved SHAs gracefully by dropping those builds from the candidate universe.
