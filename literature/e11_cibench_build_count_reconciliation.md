# Phase 15C: CIBench Build Count Reconciliation

## The Discrepancy
- **Published Count:** The CIBench paper (Jin & Servant) claims the dataset contains **82,427** CI builds with parsed test information.
- **Physical Count:** Our empirical audit of the extracted `data_set.tar.gz` archive reveals exactly **82,272** CSV files in the `test_info_logs` directory.
- **Difference:** 155 builds.

## Accounting for the Difference
The total number of commits listed in the root `Abdalkareem19_git_result` index files is 118,928. Not all of these commits produced test logs (due to build failures, cancellations, or lack of test execution).

The 155 "missing" builds represent a 0.18% delta from the published number. This discrepancy is attributed to:
1. **Empty Log Omission**: The dataset extraction pipeline likely discarded 155 builds that were initially flagged as "having test information" but upon final extraction yielded 0 parseable test rows.
2. **Author Post-Processing**: The published 82,427 figure likely refers to the intermediate database state *before* final export into the Zenodo archive, where some malformed CSVs failed to serialize.

## Frozen Strategy
We do not artificially inject or simulate 155 dummy builds to match the published count. 
The true, physically observable candidate universe is definitively **82,272** test execution logs. The E11 protocol operates exclusively on this empirical reality.
