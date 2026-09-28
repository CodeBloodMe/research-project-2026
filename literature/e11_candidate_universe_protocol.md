# Phase 14B: Candidate Universe Protocol (E11)

## 1. Candidate Test Availability
The empirical reality of mined continuous integration data (like CIBench) is that we often only observe tests that were *actually executed* during a build. Reconstructing the complete static test universe (all tests that *could* have been run) requires perfect compilation of historical snapshots, which is computationally prohibitive and prone to failure across 100 projects.

## 2. Definition of the Universe
We define the candidate universe for commit $d$, denoted $T_d$, exclusively as the set of tests that CIBench recorded as having been executed for that build. 

## 3. Implications for Estimands
Because we cannot observe the full theoretical suite, we strictly restrict our claims. We do NOT claim:
- "Full-suite test recall"
- "Exact total suite selection rate"

Instead, our estimands are formally defined as:
- **Test-level miss rate**: "Missed-failure rate among observable failing test executions."
- **Selection rate proxy**: "Proportion of observable executed tests selected by the model."

## 4. Verification Step
Once the raw CIBench SQLite schema is downloaded, we will verify if any "skipped" or "unexecuted" tests are logged. If so, they are excluded from $T_d$ unless their ground-truth pass/fail outcome is deterministically known from an adjacent build.
