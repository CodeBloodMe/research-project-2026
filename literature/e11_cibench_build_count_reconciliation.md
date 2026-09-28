# Phase 15D: CIBench Build Count Reconciliation

## The Discrepancy
- **Published Count (CIBench Paper / Meta-data)**: 82,427 builds.
- **Physical Count (Extracted from test_info_logs)**: 82,272 builds.
- **Delta**: 155 builds (0.18%).

## Reconciliation Table

| Category | Count | Evidence Source |
| :--- | :--- | :--- |
| CIBench published meta-population | 82,427 | Jin & Servant (2021) paper / summary |
| Physically present test log CSVs | 82,272 | `test_info_logs/**/*.csv` |
| Records with missing/empty test logs | 155 | Calculated Delta |
| **Reason for Discrepancy** | **UNRESOLVED_FROM_AVAILABLE_ARTIFACTS** | The CIBench artifact does not contain an explicit error log for the 155 missing rows. |

## Decision
We cannot empirically prove *why* the 155 builds are missing (e.g., whether the CI job crashed before test execution, failed to produce an XML report, or the script failed to parse them). Therefore, we explicitly state this discrepancy is **UNRESOLVED_FROM_AVAILABLE_ARTIFACTS**.

Our dataset size is strictly defined by the **82,272 physically observable** build records. We will not use the 82,427 count in our calculations.
