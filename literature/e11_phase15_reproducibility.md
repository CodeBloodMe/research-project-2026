# Phase 15B: CIBench Empirical Data Gate Reproducibility Log

## Dataset Provenance
- **Dataset**: CIBench (Jin & Servant)
- **DOI / Zenodo ID**: 10.5281/zenodo.4682056
- **Filename**: `data_set.tar.gz`
- **Download Method**: Scripted `wget`/Python `urllib` from Zenodo record URL.
- **Archive Size**: ~850 MB (compressed)
- **Extraction Method**: Native Python `tarfile` extraction to `scratch/data_set/Extended_TravisTorrent`.

## Scripting and Software Versions
- **Git Linkage Audit (`scratch/git_linkage_audit.py`)**: Used native Python 3 with `subprocess` calling `git clone` and `git show -s --format=%ct`. Run on a random seed (`random_state=42`) on 10 sampled commits from `okhttp` and `picasso`.
- **RefactoringMiner Pilot (`scratch/run_refactoring_miner_pilot.py`)**: 
  - **Tool Version**: RefactoringMiner 3.0.7 (frozen in research design).
  - **Execution**: The pilot script executed `bin/RefactoringMiner.bat` over 5 randomly sampled commits from `okhttp` (`random_state=123`).
  - **Outcome/Errors**: All 5 commits logged an `ERROR_RM_FAILED` status. The batch file failed to produce the requested JSON file locally, likely due to Java environment configuration (`JAVA_HOME` or heap space) or execution timeouts within the terminal environment. The error status is explicitly preserved in the pilot CSV output.

## Sample Windows
- The Git Linkage and Refactoring Pilot utilized a small cross-sectional random sample (5-10 commits) from the full CIBench CSV history of `square/okhttp` and `square/picasso`, explicitly preserving random seeds for transparency.

## Missing or Corrupted Artifacts
- **Missing Commits**: `ba2c6acf059fe08f991c299dd7bfa23e888152cf` in `picasso` was verified missing from the modern upstream repository.
- **Duplicate Commits**: 3,304 duplicate SHAs were identified in the native `Abdalkareem19_git_result` directory.

## No Unjustified Repairs
In accordance with the stringent empirical protocol, missing timestamps were not simulated, and refactoring outcomes were not extrapolated from the failure of the pilot execution. Missing values and errors are strictly preserved as true observations of the extraction pipeline's reality.
