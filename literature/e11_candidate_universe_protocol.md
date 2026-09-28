# Phase 15B: Candidate Universe Protocol (E11)

## 1. Empirical Definition of the Universe
Following the physical inspection of the CIBench artifacts, the candidate universe is strictly bounded by what is recorded in the `test_info_logs` and `Machalica19_git_result` directories.

- **Total Commits**: 118,928 (listed across 100 projects in the `Abdalkareem19_git_result` directory).
- **Observable Executions**: 82,272 test logs corresponding to unique CI builds.

## 2. Unit of Analysis and Observability
- **Primary Unit ($t$)**: The data aggregates test executions at the **Test Class** level, NOT the individual test method level. Therefore, the unit of analysis $t$ is a Test Class (e.g., `libcore.net.http.HttpResponseCacheTest`).
- **What is Observable**: We can observe the total number of test methods within a class, and the aggregate counts of how many failed, errored, or were explicitly skipped in a specific build. We can infer the number of passed tests.
- **What is NOT Observable**: It is structurally impossible to identify which specific test method failed within a class. Furthermore, tests that were not compiled or explicitly reported by the CI runner as "skipped" are completely absent from the log and unobservable.
- **Support for (commit, test)**: The primary unit (commit, test method) is **NOT** genuinely supported. The study must operate on the unit of (commit, test class).

## 3. Candidate Universe ($T_d$)
We define the candidate universe for a commit $d$, denoted $T_d$, exclusively as the set of **Test Classes** that CIBench recorded as having been executed for that build. 
A Test Class is considered "executed" and part of $T_d$ if the sum of its passed, failed, and errored tests is greater than zero (i.e., Total - Skipped > 0).

## 4. Population and Estimand
Because we cannot observe individual test methods or theoretical test classes, our estimands are formally defined at the Test Class level:
- $m(d,t)$ refers to the event that the PTS model omits Test Class $t$ on commit $d$, given that the Test Class actually experienced $\ge 1$ failure/error in reality.
- **Test-class-level miss rate**: "Missed-failure rate among observable failing test classes."
- **Selection rate proxy**: "Proportion of observable executed test classes selected by the model."
