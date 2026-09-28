# Research Question Candidates (Final Reformulated Set)

This document contains the finalized, publication-grade research question formulations resulting from Phase 10 (Reformulation Lab) and the final 2026 novelty audit.

---

## Candidate E02: Product Quantization / ANN under temporal distribution drift
**Status**: CLOSED (Novelty defeated by May 2026 preprints on codebook-free streaming vector search).

> **"Can streaming quantization residual statistics detect semantic concept drift and reliably predict ANN Recall@K degradation in Product Quantization before recall drops below a service-level agreement (SLA) threshold, while isolating index size growth, codebook aging, and query distribution drift?"**

---

## Candidate E05: Serverless/Disaggregated Database Micro-Burst Latency
**Status**: WEAK QUESTION (Saturated literature on cloud DB tail latency; borders on systems profiling rather than algorithmic discovery).

> **"In compute-storage disaggregated databases under sudden read micro-bursts, does P99 tail latency amplification stem primarily from remote network transport delay or from internal buffer pool latch contention (`LWLock:buffer_mapping` and `BufferContent`) during concurrent page fault resolution?"**

---

## Candidate E11: Predictive Test Selection under Refactoring Commits
**Status**: STRONG RESEARCH QUESTION (Underexplored empirical gap intersecting ML failure modes and deterministic AST analysis).

> **"How do specific categories of structural refactorings (class renames, method moves, and cross-module extractions) impact the False Negative Rate of Machine Learning-based Predictive Test Selection models across chronologically ordered continuous integration commit streams?"**
