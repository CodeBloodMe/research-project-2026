# Deep Prior-Art Due Diligence (Phase 8B)

This document contains the critical review and novelty decomposition for candidates F01–F10 following a rigorous publication-level search of 2024–2026 literature.

## F01 — DiskANN Predictive Prefetching
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** VeloANN (predictive prefetching coroutines) and Learned Prefetching for ANN.
*   **Strongest Novelty Threat:** The exact mechanism of using ML/predictive coroutines to fetch SSD nodes ahead of graph traversal in DiskANN already exists in recent DB literature (e.g., VeloANN).
*   **What Remains Distinct:** Nothing substantial at the algorithmic level.
*   **Research vs Engineering:** Engineering contribution (re-implementing known learned prefetching).

## F02 — Federated Gradient Sparsification
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** "Semantic-aware gradient sparsification for heterogeneous FL" and feature-aware SHAP pruning.
*   **Strongest Novelty Threat:** Dropping standard magnitude pruning in favor of semantic-aware or feature-aware pruning to combat client drift in non-IID FL is a heavily saturated sub-field in 2024-2025.
*   **What Remains Distinct:** Nothing.
*   **Research vs Engineering:** Trivial parameter tuning / Application of known FL sparsification.

## F03 — Serverless Deterministic Transactions
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** FaunaDB (commercial Calvin) and Remora (deterministic FaaS execution).
*   **Strongest Novelty Threat:** Applying Calvin-style pre-sequenced deterministic execution to eliminate 2PC in distributed/serverless environments is precisely the architectural foundation of FaunaDB and academic systems like Remora.
*   **What Remains Distinct:** Nothing.
*   **Research vs Engineering:** Engineering (implementing a known protocol in a new FaaS framework).

## F04 — Neural Surrogate for SMT in Fuzzing
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** NeuroSCA (Neuro-Symbolic Constraint Abstraction, 2025) and NEUEX.
*   **Strongest Novelty Threat:** NeuroSCA explicitly uses LLMs/neural layers to abstract semantic noise to prevent SMT solver timeouts during hybrid fuzzing. NEUEX uses gradient-guided neural solvers. 
*   **What Remains Distinct:** Nothing algorithmic.
*   **Research vs Engineering:** Engineering replication.

## F05 — Selective SGX ORAM
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** Obelix, Constantine, and DynPTA.
*   **Strongest Novelty Threat:** Using compiler passes (LLVM) and dynamic taint tracking to identify data-dependent branches and *selectively* apply ORAM/obfuscation in SGX to save performance is a completely saturated approach (Obelix/Constantine).
*   **What Remains Distinct:** Nothing.
*   **Research vs Engineering:** Engineering wrapper.

## F06 — Streaming Metadata Cold-Start
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** MARec (Metadata Alignment for cold-start Recommendation, RecSys 2024).
*   **Strongest Novelty Threat:** MARec and similar zero-shot embedding models already solve the problem of embedding new items using purely metadata before interaction streams arrive.
*   **What Remains Distinct:** Nothing.
*   **Research vs Engineering:** Application to a new dataset.

## F07 — Phase-Aware GPU DVFS
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** BiScale (2026), EcoInfer, GreenLLM.
*   **Strongest Novelty Threat:** BiScale explicitly proposes two-tier phase-aware DVFS specifically separating the compute-bound prefill phase and the memory-bound decode phase to save energy without violating TTFT SLOs. 
*   **What Remains Distinct:** Nothing.
*   **Research vs Engineering:** Pure re-implementation.

## F08 — P4 Single-Pass Bloom Filter
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** Standard P4 register array implementations (e.g., Lucid framework).
*   **Strongest Novelty Threat:** Implementing probabilistic data structures (Bloom filters, Count-Min Sketches) in a single pass using atomic register arrays is the de facto standard for P4 programming to avoid recirculation. It is covered in basic Tofino tutorials.
*   **What Remains Distinct:** Nothing.
*   **Research vs Engineering:** Trivial implementation.

## F09 — Conflict Graph Dynamic Consistency
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** cc-pipe (NSDI 2025) and Disciplined Inconsistency.
*   **Strongest Novelty Threat:** Building local predictive conflict graphs to safely schedule concurrent execution while preserving strict consistency is exactly the contribution of cc-pipe. Dynamic consistency models are also highly established.
*   **What Remains Distinct:** Nothing fundamentally novel in the distributed systems theory.
*   **Research vs Engineering:** Engineering adaptation.

## F10 — DLRM HBM Embedding Cache
*   **Status:** CLEARLY NOVELTY-THREATENED
*   **Closest Prior Work:** NVIDIA Merlin HugeCTR, Colossal-AI CachedEmbedding.
*   **Strongest Novelty Threat:** Utilizing GPU HBM as a software-managed cache for the hottest (Zipfian) embeddings while offloading the rest to CPU/PCIe is a standard, built-in feature of state-of-the-art DLRM frameworks (e.g., Colossal-AI, HugeCTR).
*   **What Remains Distinct:** Nothing.
*   **Research vs Engineering:** API Wrapper / Dashboarding.
