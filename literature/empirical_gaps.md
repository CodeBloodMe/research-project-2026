# Empirical Gaps Analysis

This document details the specific experimental gaps identified during the empirical research discovery phase. These gaps focus on evaluating existing systems under stress conditions, edge cases, or intersections that have been overlooked in the literature.

### G01: BBRv3 vs Cubic on Shallow Buffers
Current evaluations of BBR often assume adequate buffer sizing or focus on WAN performance. The specific dynamics of BBRv3 pacing colliding with TCP Cubic's aggressive window behavior on edge ToR switches with extreme shallow buffers (<1MB) remains an empirical gap.

### G02: PQ Concept Drift Silent Failure
While vector database literature focuses on QPS and static recall, the operational reality of RAG systems involves continuous incremental updates. The point at which a fixed Product Quantization codebook catastrophically fails to approximate distances for out-of-domain vectors (without throwing errors) is an unmeasured vulnerability.

### G03: Pathological Memory Fragmentation via Fuzzing
Fuzzing literature optimizes for edge coverage and memory safety violations (ASan/Valgrind). Measuring a fuzzer's ability to act as a "fragmentation adversarial agent" against modern allocators (jemalloc) represents a gap in both testing and systems reliability research.

### G04: Trivial Evasion of ETA NIDS
Deep Learning NIDS research often trains and tests on the same pristine distribution (e.g., CICIDS2017). The gap lies in proving how extremely brittle these >95% accurate models are to the simplest forms of network obfuscation (fixed payload padding and minor randomized delay).

### G05: Serverless DB Micro-Burst Latency
The decoupling of compute and storage in serverless DBs is praised for scalability. However, the specific P99 tail latency degradation curve during un-cached micro-bursts (where compute nodes must synchronous fetch pages from the storage layer) is rarely benchmarked against monolithic equivalents.

### G06: Two-Tower Popularity Bias under Flooding
Recommender systems are known to have popularity bias. The gap is isolating the systemic penalty applied by Two-Tower architectures to bursty, high-velocity new items (flooding) before the model can properly fine-tune their embeddings.

### G07: FL Oscillation under Bimodal Temporal Shift
FL research heavily evaluates static non-IID distributions (e.g., Dirichlet splitting). The empirical gap is evaluating convergence stability when local client distributions experience periodic, bimodal temporal shifts (e.g., flipping 180 degrees every N rounds).

### G08: ZeRO Offload + Async Checkpoint PCIe Contention
ML Systems literature evaluates async checkpointing and ZeRO CPU-offloading independently. The gap is measuring the GPU starvation (idle time) caused by PCIe bus saturation when these two mechanisms are forced to operate simultaneously during large-scale training.

### G09: DP-SGD Clipping on Extreme Minorities
The fairness degradation of DP-SGD is known. The specific gap is isolating the gradient clipping operation and empirically proving that it acts as a "hard filter" that completely erases the gradients of extreme minority classes (<0.1%), forcing their recall to exactly zero regardless of the privacy budget epsilon.

### G10: Learned Index Boundary Insertions
ALEX and other learned indexes are evaluated on random inserts or standard Zipfian distributions. The gap is benchmarking the P99 latency spikes induced by continuous, sequential insertions specifically placed at the boundaries of the learned CDF segments, forcing pathological node splits.

### G11: PTS Failure on Refactoring
Predictive Test Selection (PTS) is evaluated on historical CI data. The gap is partitioning the evaluation set to isolate "structural refactoring" commits from "feature" commits to measure if PTS models exhibit a dangerously higher False Negative Rate (FNR) on structural changes due to feature overfitting.

### G12: CXL Spilling for Random-Access Graphs
CXL is evaluated for database caching and sequential workloads. The gap is measuring the extreme latency penalty of CXL memory expansion for highly random-access graph traversal workloads (e.g., PageRank), which cannot benefit from standard memory prefetching.
