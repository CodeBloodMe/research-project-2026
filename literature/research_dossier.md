# Final Research Dossier

This document provides the final novelty audit for the three reformulated candidates (E02, E05, E11) against 2024–2026 literature.

---

## Candidate E02: Product Quantization / ANN under temporal distribution drift

**STATUS**: CLOSED

**RESEARCH PROBLEM**: Identifying when streaming Product Quantization (PQ) approximate nearest neighbor (ANN) indexes degrade in Recall@K due to semantic drift, without computing exact KNN.

**WHAT IS KNOWN**: Static PQ codebooks lose recall when indexing out-of-distribution embeddings. Retraining codebooks online is computationally expensive.

**WHAT IS UNKNOWN**: (Hypothesized gap) Can inexpensive online residual tracking predict Recall@K degradation with sufficient lead time?

**CLOSEST PRIOR WORK**: 
- *IVF-TQ: Calibration-Free Streaming Vector Search via a Codebook-Free Residual Layer* (arXiv:2605.17415, May 2026).
- *The Undetected Damage of Quantization on Retrieval and How to Fix It* (arXiv:2509.XXXX).

**NOVELTY THREAT**: FATAL. The 2026 IVF-TQ paper directly addresses the phenomenon where streaming ANN indexes using PQ lose recall over time. It specifically demonstrates that PQ methods can degrade even without semantic distribution shift simply due to reliance on static codebooks fitted to initial samples, and it proposes residual layers to solve this. This completely overtakes the novelty of E02's residual-statistics early-warning mechanism.

**RESEARCH QUESTION**: Can streaming quantization residual statistics detect semantic concept drift and reliably predict ANN Recall@K degradation before recall drops below an SLA threshold?

**HYPOTHESIS**: Streaming residual statistics ($\bar{E}_t, \mathcal{W}_1$) accurately predict downstream Recall@K failure under temporal concept drift.

**SCIENTIFIC CONTRIBUTION**: Would have been an $O(1)$ overhead early-warning trigger for vector DBs.

**MAIN THREAT TO VALIDITY**: The phenomenon is already solved by calibration-free / codebook-free streaming vector search methods published in early 2026.

**EVIDENCE QUALITY**: Strong. Web search returned highly specific arXiv preprints from 2025/2026 exactly in this subdomain.

### WHAT WE STILL NEED TO KNOW
Nothing for this specific question. The vector database community has already moved past detecting static codebook drift to implementing inherently drift-resistant (codebook-free) indexing structures.

---

## Candidate E05: Serverless/Disaggregated Database Micro-Burst Latency

**STATUS**: WEAK QUESTION

**RESEARCH PROBLEM**: Understanding the exact internal mechanisms driving P99 tail latency in compute-storage disaggregated databases during read micro-bursts.

**WHAT IS KNOWN**: Disaggregated databases experience severe P99 latency degradation on un-cached reads due to remote storage fetches across network fabrics (e.g., Neon VLDB 2023, Gopher VLDB 2024).

**WHAT IS UNKNOWN**: Whether tail latency explosions under high-concurrency micro-bursts stem linearly from network RTT, or quadratically from internal buffer pool latch contention (`LWLock:buffer_mapping`).

**CLOSEST PRIOR WORK**: 
- *Gopher: A disaggregated DBMS* (VLDB 2024).
- Papers investigating micro-bursts in data center networks and buffer management in cloud-native DBs.

**NOVELTY THREAT**: HIGH. While the exact breakdown of `LWLock` contention under Pareto network delay isn't explicitly the title of a paper, the general cloud DB space is overwhelmingly saturated with latency profiling studies. Identifying a bottleneck in PostgreSQL's buffer mapping under network latency is primarily a performance engineering / systems profiling task, not a foundational scientific contribution.

**RESEARCH QUESTION**: In compute-storage disaggregated databases under sudden read micro-bursts, does P99 tail latency amplification stem primarily from remote network transport delay or from internal buffer pool latch contention?

**HYPOTHESIS**: Buffer pool latch serialization scales quadratically under concurrency micro-bursts when threads await pending remote I/O, dominating network transit time.

**SCIENTIFIC CONTRIBUTION**: A detailed profiling breakdown of PostgreSQL wait events under simulated network disaggregation.

**MAIN THREAT TO VALIDITY**: Lack of theoretical novelty. It is a measurement study of an implementation artifact (PostgreSQL buffer locks) rather than a novel conceptual discovery.

**EVIDENCE QUALITY**: Moderate. Literature on disaggregated DBs (Neon, Aurora, Serverless) is vast, and handling bursty workloads is a known solved problem via various autoscaling and prefetching heuristics.

### WHAT WE STILL NEED TO KNOW
We need to know if there is a fundamental algorithmic gap in distributed buffer management that cannot be solved by existing RDMA/CXL network upgrades or standard lock-free data structures. The current formulation does not point to a new algorithm, only a measurement.

---

## Candidate E11: Predictive Test Selection under structural refactoring

**STATUS**: STRONG RESEARCH QUESTION

**RESEARCH PROBLEM**: Predictive Test Selection (PTS) models rely heavily on file-path modifications to predict test failures. When structural refactorings (renames, method moves) occur, these file identities change, potentially causing the ML model to miss critical test failures.

**WHAT IS KNOWN**: 
- Industry standard ML PTS (Machalica et al., ICSE-SEIP 2019) achieves high general recall. 
- Deterministic, rule-based Refactoring-Aware Regression Test Selection exists (Silva et al., TOSEM 2023).

**WHAT IS UNKNOWN**: How specific categories of structural refactorings (class renames, method moves, cross-module extractions) quantitatively impact the False Negative Rate (FNR) of ML-based PTS models in real-world continuous integration streams.

**CLOSEST PRIOR WORK**: 
- *Machalica et al. (ICSE 2019)* - Baseline ML PTS.
- *Silva et al. (TOSEM 2023)* - Static RTS for refactorings.
- Literature broadly addresses ML for test selection and AST for dynamic analysis, but these have not been crossed to empirically audit ML-PTS failure modes.

**NOVELTY THREAT**: LOW. Searches across arXiv and academic indexes (2024–2026) confirm that while "refactoring-aware regression test selection" is a known phrase, it strictly refers to static, deterministic graph-based analysis. No peer-reviewed paper has isolated refactoring commits in continuous CI streams to audit the blind spots of Machine Learning (GBDT) PTS models.

**RESEARCH QUESTION**: How do specific categories of structural refactorings (class renames, method moves, and cross-module extractions) impact the False Negative Rate of ML-based Predictive Test Selection models across chronologically ordered continuous integration commit streams?

**HYPOTHESIS**: Identity-modifying refactorings will exhibit a statistically significant Stratified Risk Ratio ($RR \ge 3.0$) for False Negatives compared to feature-only commits, because standard PTS path-features lose historical correlation.

**SCIENTIFIC CONTRIBUTION**: The first empirical measurement of ML PTS failure modes bounded to AST-level structural changes, exposing a critical "silent regression risk" in modern CI pipelines.

**MAIN THREAT TO VALIDITY**: Dataset temporal leakage and flaky tests. This is solved by the reformulated strict chronological split using TravisTorrent / GitHub Actions and filtering tests with inconsistent pass/fail rates on the same hash.

**EVIDENCE QUALITY**: High. The gap is clearly visible between the ML-PTS papers (which ignore refactoring types) and the static-RTS papers (which ignore Machine Learning).

### WHAT WE STILL NEED TO KNOW
We need to confirm if we can successfully map RefactoringMiner 2.0 AST outputs to a large enough corpus of failing CI builds in TravisTorrent to achieve statistical significance. We also need to build the baseline GBDT model to verify it achieves the standard 99% recall on non-refactoring commits.
