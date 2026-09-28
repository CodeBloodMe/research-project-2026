# Research Ledger

This document tracks the completion and major outcomes of all research phases.

## Phase 10: Reformulation Lab
* **Outcome**: Refined three candidates (E02, E05, E11). Concluded that E11 (Predictive Test Selection under Refactoring Commits) was the only strong, empirically defensible candidate. E02 closed due to recent prior art (May 2026). E05 deemed a weak question (saturated tail latency profiling).
* **Artifacts**: `literature/research_dossier.md`, `literature/research_evidence.csv`, `literature/research_question_candidates.md`.

## Phase 11 & Final E11 Validation
* **Outcome**: Conducted a deep literature audit bridging ML Predictive Test Selection and Refactoring-Aware RTS. Status: DEFENSIBLE.
* **Artifacts**: `literature/e11_final_validation.md`, `literature/e11_final_sources.csv`, `literature/e11_final_gap_statement.md`.

## Phase 12 & 12B: Research Design
* **Outcome**: Developed a comprehensive research design separating test-level false negatives from build-level regression escapes, standardizing an operating-point procedure, and defining testable hypotheses without arbitrary numerical thresholds.
* **Artifacts**: `literature/e11_research_design.md`, `literature/e11_variables.md`, `literature/e11_rq_hypothesis_matrix.csv`, `literature/e11_threats_to_validity.md`, `literature/e11_design_change_log.md`.

## Phase 13: E11 Data Power Census
* **Outcome**: **NO-GO**. A data feasibility census revealed severe intersection sparsity (the rarity of finding pure refactoring commits that also fail tests) and a lack of test-level outcomes in large public datasets like TravisTorrent. Proposed 3 redesigns (Defects4J fault-injection, Mono-Repo extraction, or Static RTS focus) to preserve the scientific question.
* **Artifacts**: `literature/e11_data_census.md`, `literature/e11_repository_eligibility.csv`, `literature/e11_refactoring_census.csv`, `literature/e11_failure_power.csv`, `literature/e11_data_risks.md`, `literature/e11_go_no_go.md`.
