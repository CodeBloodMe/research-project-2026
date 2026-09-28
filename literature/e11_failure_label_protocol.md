# Phase 15D: CIBench/Machalica Operational Failure-Positive Label

## The Ambiguity
The `test_info_logs` natively split outcomes into: `skipped`, `failed`, `errors`, and `passed`.
We must strictly align the E11 primary failure outcome ($y(j,t) = 1$) with the exact semantics used in the CIBench ground-truth extraction (`Machalica19_git_result`'s `failure_status`).

## Empirical Resolution
We audited several CIBench builds and cross-referenced `test_info_logs` rows with `Machalica19_git_result` rows for the same Test Class.

**Observations:**
1. **Failed > 0 AND Errors > 0:** Yields `failure_status = 1.0` in Machalica.
2. **Failed = 0 AND Errors > 0:** Yields `failure_status = 0.0` in Machalica!
3. **Skipped:** Skipped tests are recorded as `nan` in Machalica or excluded, and do not contribute to positive failure status.

## Frozen E11 Failure Definition
To maintain strict fidelity to the CIBench baseline target, the frozen failure outcome is:

**`failure_positive = (failed > 0)`**

This is explicitly named the **CIBench/Machalica operational failure-positive label**.

### Explicit Classifications
- **assertion-failure-positive**: When `failed > 0`. This is the ONLY condition where `failure_positive = 1`.
- **error-only**: When `failed = 0` but `errors > 0` (e.g., compile errors or setup exceptions). This is explicitly defined as `failure_positive = 0` under the frozen operational definition. We do not call these "pass", but they are mapped to 0.
- **skipped**: Tests explicitly marked as skipped do not contribute to `failed`. They have `failure_positive = 0`.
- **zero-execution**: A test class with 0 executions (or missing total) is not part of the candidate universe.
- **missing observations**: Tests that were never run or omitted from the XML runner entirely are unobservable.
