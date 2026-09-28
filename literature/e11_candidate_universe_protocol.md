# Phase 15: Candidate Universe Protocol (E11)

## 1. Candidate Test Availability
The empirical reality of mined continuous integration data (like CIBench) is that we often only observe tests that were *actually executed* during a build. Reconstructing the complete static test universe (all tests that *could* have been run) requires perfect compilation of historical snapshots, which is computationally prohibitive and prone to failure across 100 projects.

## 2. Empirical Definition of the Universe
Following the Phase 15 Empirical Data Gate inspection, the candidate universe is strictly defined by the raw CIBench Zenodo artifact. 

- **Total Commits**: 118,928 (listed across 100 projects in the `Abdalkareem19_git_result` directory).
- **Observable Executions**: Only 82,272 of these commits have corresponding parsed test execution logs in the `test_info_logs` directory.

We define the candidate universe for commit $d$, denoted $T_d$, exclusively as the set of tests that CIBench recorded as having been executed for that build within the 82,272 observable builds. Any commit without a corresponding test log file is strictly excluded from the study.

## 3. Implications for Estimands
Because we cannot observe the full theoretical suite, we strictly restrict our claims. We do NOT claim:
- "Full-suite test recall"
- "Exact total suite selection rate"

Instead, our estimands are formally defined as:
- **Test-level miss rate**: "Missed-failure rate among observable failing test executions."
- **Selection rate proxy**: "Proportion of observable executed tests selected by the model."

## 4. Verification Step
The raw CIBench dataset (CSV files, not SQLite) maps commit hashes to row numbers, and test execution outcomes are recorded per row number in `test_info_logs`. Tests marked as 'skipped' or 'N/A' in column 4 are excluded from the test-level evaluation universe unless their ground-truth pass/fail outcome is deterministically known from an adjacent build.
