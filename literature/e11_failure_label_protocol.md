# Phase 15C: Failure Label Protocol

## The Ambiguity
The `test_info_logs` natively split outcomes into: `skipped`, `failed`, `errors`, and `passed`.
We must strictly align the E11 primary failure outcome ($y(d,t) = 1$) with the exact semantics used in the CIBench ground-truth extraction (`Machalica19_git_result`'s `failure_status`).

## Empirical Resolution
We audited several CIBench builds and cross-referenced `test_info_logs` rows with `Machalica19_git_result` rows for the same Test Class.

**Observations:**
1. **Failed > 0 AND Errors > 0:** Yields `failure_status = 1.0` in Machalica. (e.g., `aws-sdk-java` build 388).
2. **Failed = 0 AND Errors > 0:** Yields `failure_status = 0.0` in Machalica! (e.g., `aws-sdk-java` build 505: `failed=0, errors=3`).
3. **Skipped:** Skipped tests are recorded as `nan` in Machalica or excluded, and do not contribute to positive failure status.

## Frozen E11 Failure Definition
To maintain strict fidelity to the CIBench baseline target, the frozen failure outcome is:

**`failure_positive = (failed > 0)`**

### Explicit Treatments
- **Error-only cases** (e.g., compile errors or setup exceptions causing test aborts but not assertion failures): Count as **Negative / Pass ($0$)**. Do NOT collapse errors into failures.
- **Skipped cases**: Skipped tests do not contribute to `failed` and remain Negative.
- **Zero-execution cases**: If `total_tests` is 0 or missing, it is not a valid observation unit for failure prediction.
