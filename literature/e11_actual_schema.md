# CIBench Actual Artifact Schema

This document details the exact physical schema of the CIBench Zenodo dataset (`data_set.tar.gz`), uncompressed to the `Extended_TravisTorrent` directory.

## Directory Structure
The dataset consists of four subdirectories under `Extended_TravisTorrent`:
1. `Abdalkareem19_git_result`
2. `Machalica19_git_result`
3. `test_info_logs`
4. `dependency`

### 1. Abdalkareem19_git_result
Contains a CSV file for each of the 100 projects (e.g., `okhttp.csv`).
- **Format**: `commit_hash`, `commit_message`, `is_skipped`
- **Purpose**: Maps commit hashes to a line index (1-indexed). The row index serves as the primary key (`build_id`) for files in the other directories.

### 2. Machalica19_git_result
Contains subdirectories for each project (e.g., `square_okhttp`). Inside are CSV files named by the row index from the Abdalkareem19 CSV (e.g., `1.csv`).
- **Format**: `test_name`, `total_runs_in_class`, `failure_status`, `changed_files_json_array`, `feature_array_1`, `feature_array_2`, `integer_val`
- **Purpose**: Contains the list of changed files for the commit, the test failure status (0.0 or 1.0), and the feature vectors used by Machalica et al.

### 3. test_info_logs
Contains subdirectories for each project (e.g., `square_okhttp`). Inside are CSV files named by the row index from the Abdalkareem19 CSV (e.g., `1.csv`).
- **Format**: `project_prefix`, `test_name`, `total_tests`, `skipped`, `failed`, `errors`, `passed`, `duration_seconds`
- **Purpose**: Contains the raw, parsed test execution outcomes for the specific CI build.
- **Coverage**: Only 82,272 test log CSVs exist across the 118,928 total commits, meaning the observable test universe is strictly limited to these 82k builds.

### 4. dependency
Contains file-level dependency matrices for each project.

## Relationship Mapping
To retrieve a complete test-execution record for a commit:
1. Lookup the `commit_hash` in `Abdalkareem19_git_result/[project].csv`. The line number is `L`.
2. Open `test_info_logs/[project]/[L].csv` to retrieve test outcomes (pass/fail) and durations.
3. Open `Machalica19_git_result/[project]/[L].csv` to retrieve the `changed_files` list.
4. Timestamps are **not** present in the dataset and must be retrieved via `git log` using the `commit_hash`.
