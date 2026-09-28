# Empirical Research Landscape

This landscape maps the transition from "algorithm invention" to "empirical failure-mode discovery". Instead of inventing new methods, these gaps represent poorly understood, poorly measured, or untested stress conditions on existing state-of-the-art systems.

## 1. Computer Networks (Congestion Control)
*   **System:** BBRv3 / TCP Cubic
*   **Gap:** The interaction of rate-based (BBR) and loss-based (Cubic) congestion control is well-studied in deep buffers, but the destructive synchronization and bandwidth underestimation of BBRv3 in shallow-buffered ToR switches remains under-evaluated.

## 2. Vector Databases (Approximate Nearest Neighbors)
*   **System:** Product Quantization (FAISS / DiskANN)
*   **Gap:** PQ relies on fixed codebooks. The silent degradation (recall collapse) of these codebooks under continuous "semantic concept drift" (incremental OOD insertions) without expensive retraining is poorly measured.

## 3. Software Testing (Fuzzing)
*   **System:** Coverage-guided Fuzzing (AFL++)
*   **Gap:** Fuzzers are evaluated on finding memory *safety* bugs (UAF, overflows). Their ability to discover deterministic, pathological *fragmentation* sequences in stateful memory allocators (jemalloc) leading to DoS/OOM is untested.

## 4. Cybersecurity (Intrusion Detection)
*   **System:** Encrypted Traffic Analysis (ETA) NIDS
*   **Gap:** DL-based ETA models boast >95% accuracy on standard datasets. Their extreme brittleness to trivial obfuscation (uniform packet delay jitter and MTU padding) is a critical empirical blind spot.

## 5. Distributed Systems (Serverless Databases)
*   **System:** Compute/Storage Decoupled DBs (Aurora, Neon)
*   **Gap:** The tail latency penalty (P99) of page cache invalidation during "thundering herd" micro-bursts—where the prefetcher cannot anticipate the read spike—is not systematically compared against monolithic baselines.

## 6. Recommender Systems (Retrieval)
*   **System:** Two-Tower Retrieval Models
*   **Gap:** The systemic algorithmic penalty applied to newly injected items during high-velocity "cold-start flooding" (due to heuristic embedding initialization) is not isolated from general popularity bias.

## 7. Edge Computing (Federated Learning)
*   **System:** FedAvg / FedProx
*   **Gap:** FL algorithms are heavily tested against static spatial non-IID data (label skew). Their convergence behavior under periodic bimodal temporal shifts (e.g., day/night cycles flipping local distributions) is largely unknown.

## 8. ML Systems (Hardware/Software Co-design)
*   **System:** Async Checkpointing + ZeRO Optimizer Offloading
*   **Gap:** The PCIe bandwidth contention when asynchronous model checkpointing overlaps with ZeRO-Infinity CPU-offloaded optimizer state updates, potentially causing massive GPU starvation, is uncharacterized.

## 9. Privacy-Preserving ML
*   **System:** Differentially Private SGD (DP-SGD)
*   **Gap:** The disparate impact of DP-SGD on fairness is known, but the specific mechanism by which gradient clipping completely erases sparse updates for *extreme* minority classes (<0.1%), collapsing their recall to zero, needs rigorous empirical validation.

## 10. Database Systems (Learned Indexes)
*   **System:** Updatable Learned Indexes (ALEX)
*   **Gap:** While B-Trees handle sequential inserts seamlessly, the P99 latency spikes in Learned Indexes caused by adversarial sequential inserts at the exact boundary of the learned CDF (forcing continuous retraining) is a critical robustness gap.

## 11. Software Engineering (CI/CD)
*   **System:** Predictive Test Selection (PTS)
*   **Gap:** PTS models are evaluated on overall time saved and false negative rate (FNR). Evaluating FNR specifically on structural refactoring commits versus feature logic commits will reveal if these models dangerously overfit to file paths.

## 12. Hardware / Architecture
*   **System:** CXL Memory Expansion
*   **Gap:** The performance penalty of spilling memory to CXL (which lacks aggressive hardware prefetching and has higher bus latency) specifically for random-access graph traversal workloads (PageRank) is an essential benchmark.
