# E11 Current Research State

This document acts as the single authoritative entry point for the E11 research program ("Predictive Test Selection under Structural Refactoring"). All other design documents must agree with the state declared in `E11_FINAL_RESEARCH_DESIGN.md`.

## Master Document
* **E11_FINAL_RESEARCH_DESIGN.md**: The complete, consolidated, authoritative research design encompassing the problem statement, RQs, hypotheses, baseline, treatment definition, exposure definition, outcomes, data source, statistical design, RQ3 intervention, and novelty/gap statement.

## Authoritative Sub-Specifications
* **`e11_document_status_inventory.csv`**: Tracks the status (ACTIVE, HISTORICAL, SUPERSEDED, IRRELEVANT) of all documents in the repository to prevent reliance on stale claims.
* **`e11_claim_integrity_audit.csv`**: Audit log of removed obsolete/overclaiming statements.
* **`e11_prior_art_reaudit.md` / `e11_prior_art_matrix.csv`**: The authoritative prior art analysis.
* **`e11_novelty_claim.md`**: The defensible novelty statement.
* **`e11_baseline_fidelity_audit.md` / `e11_baseline_feature_spec.csv`**: The exact definition of the history-based PTS baseline (reduced from Machalica et al. 2019).
* **`e11_observation_unit_spec.md`**: The exact test-level dataset unit (x, y) definition.
* **`e11_outcome_estimands.md`**: The formal definitions of test recall, miss rate, selection rate, time saved, and build-level regression escape.
* **`e11_refactoring_label_protocol.md`**: Protocol for differentiating REF_ONLY, REF_MIXED, and NON_REF via AST diffing.
* **`e11_refactoring_pts_exposure_matrix.csv`**: The explicit mapping of refactoring operations to DIRECT vs. INDIRECT exposure against the defined baseline.
* **`e11_rq_estimand_matrix.csv`**: The integrated RQs, hypotheses, and estimands.
* **`e11_identification_dag.md`**: Causal DAG and adjustment strategy for RQ1.
* **`e11_temporal_leakage_protocol.md`**: The strict temporal boundaries for historical features.
* **`e11_cibench_provenance.md` / `e11_cibench_required_fields.csv`**: Documentation of the CIBench data source (Jin & Servant, DOI: 10.5281/zenodo.4682056).
* **`e11_rq3_final_intervention_spec.md`**: The exact mechanism of the RQ3 representation-preserving intervention.
* **`e11_master_audit_checklist.csv`**: Proof of resolution for all previously identified methodological inconsistencies.

> **Status**: Refer to `E11_FINAL_RESEARCH_DESIGN.md` for the current overall phase status (e.g., DESIGN FROZEN WITH EMPIRICAL GATE).
