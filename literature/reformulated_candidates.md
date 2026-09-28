# Phase 10: Reformulation Lab

## Executive Summary

Phase 10 takes the three surviving empirical candidates from Phase 9B that required deep structural redesign and reformulates them into publication-grade, experimentally rigorous computer science research questions.

Each candidate has been redesigned with:
1. A valid, publicly accessible dataset or workload.
2. A controlled, falsifiable experimental methodology.
3. Separation of confounding variables.
4. Concrete student hardware feasibility.
5. Strict verification of prior art boundaries (2024–2026).

---

## 1. Candidate E02: Product Quantization under Semantic Drift

### 1.1 Original Flaws & Diagnostic
* **Original Formulation**: *"How resilient are fixed PQ codebooks to semantic concept drift?"*
* **Fatal Flaws in Phase 9**:
  1. *Dataset Invalidity*: Pairing SQuAD with MSMARCO is not concept drift; it is an arbitrary cross-domain covariate shift between two disparate QA corpora.
  2. *Hypothesis Tautology*: Asking whether fixed K-means centroids lose recall when out-of-distribution vectors are inserted is mathematically trivial (quantization error $\mathbb{E}[\|x - q(x)\|^2]$ increases by definition).
  3. *Uncontrolled Confounders*: Previous setups failed to separate genuine semantic drift from index size growth ($N \rightarrow 10N$), codebook aging, and query distribution drift.

### 1.2 Reformulated Research Question
> **"Can streaming quantization residual statistics detect semantic concept drift and reliably predict ANN Recall@K degradation in Product Quantization before recall drops below a service-level agreement (SLA) threshold, while isolating index size growth, codebook aging, and query distribution drift?"**

### 1.3 Mathematical & Theoretical Grounding
Let vector $x \in \mathbb{R}^d$ be partitioned into $m$ orthogonal sub-vectors $x = [x^{(1)}, \dots, x^{(m)}]$. A Product Quantizer maps each sub-vector $x^{(j)}$ to its nearest centroid $c_k^{(j)}$ in codebook $\mathcal{C}^{(j)}$. The reconstructed vector is $q(x) = [c_{k_1}^{(1)}, \dots, c_{k_m}^{(m)}]$, with residual vector $r(x) = x - q(x)$ and residual squared norm $\|r(x)\|_2^2 = \sum_{j=1}^m \|x^{(j)} - c_{k_j}^{(j)}\|_2^2$.

Under stationary conditions, residual norms follow an empirical distribution $\mathcal{P}_0(\|r\|_2)$. As incoming vectors stream in chronologically, semantic drift causes new vectors to populate peripheral, under-represented regions of the embedding space, shifting the empirical distribution to $\mathcal{P}_t(\|r\|_2)$.

We compute two online, $O(1)$-per-vector statistics over a sliding window $W$:
1. **Exponential Moving Average Residual Error (EMA-RE)**:
   $$\bar{E}_t = \alpha \|x_t - q(x_t)\|_2^2 + (1-\alpha) \bar{E}_{t-1}$$
2. **Streaming Wasserstein Distance of Residual Norms ($\mathcal{W}_1$)**:
   $$\mathcal{W}_1(\mathcal{P}_0, \mathcal{P}_t) = \int_0^\infty |F_0(z) - F_t(z)| dz$$
   where $F_0$ and $F_t$ are empirical cumulative distribution functions of the residual norms.

### 1.4 Dataset & Workload Construction
* **Corpus**: ArXiv Open Access Dataset (Cornell University via Kaggle/ArXiv API).
* **Time Span**: 2018–2024 (1.5 million paper titles and abstracts).
* **Embedding Model**: `BGE-large-en-v1.5` (1024-dim) or `all-MiniLM-L6-v2` (384-dim).
* **Chronological Structure**:
  - *Initialization / Training Period* ($T_0$): Papers published in 2018–2019 (train initial PQ codebook with $m=16$, $b=8$, and IVF-1024).
  - *Streaming Insertion Period* ($T_1 \dots T_{\text{end}}$): Sequential insertion of papers ordered strictly by publication date from 2020 to 2024.
* **Anchor Queries**: A fixed benchmark set of 1,000 queries sampled from 2018–2019 topics to measure retrieval fidelity on historical knowledge, alongside a parallel sliding set of 1,000 queries sampled from current streaming windows.

### 1.5 Confounder Isolation Protocol
To ensure observed recall drops are caused strictly by semantic drift:
1. **Index Size Growth vs. Semantic Drift**: Maintain a parallel **I.I.D. Control Index**. The control index starts with the same 2018–2019 codebook but receives incoming vectors sampled randomly (I.I.D.) from a stationary held-out 2018–2019 pool. At any insertion count $N_t$, both indices have identical vector counts, isolating capacity growth from distributional movement.
2. **Query Drift vs. Document Drift**: Measure Recall@K separately against (a) static anchor queries and (b) temporally aligned queries.
3. **Codebook Aging**: Track per-cluster residual variances to determine whether drift affects all clusters uniformly or concentrates in fast-evolving semantic subfields (e.g., generative AI, LLMs).

### 1.6 Scientific Question Test (E02)
1. *What is already known?* Static PQ codebooks lose recall when indexing out-of-distribution embeddings; online/incremental PQ can retrain codebooks at high computational expense (He et al., TPAMI 2018).
2. *What exactly remains uncertain?* Whether inexpensive online residual tracking during insertion ($O(1)$ overhead) can accurately forecast downstream Recall@K failure with sufficient lead time to trigger asynchronous retraining *before* an SLA breach (e.g., Recall@10 falling below 90%).
3. *Why does that uncertainty matter?* Brute-force ground truth recall evaluation requires $O(N \cdot d)$ exact KNN computation, which is computationally prohibitive in production vector databases. An accurate, zero-overhead residual early-warning trigger eliminates both unneeded periodic retraining and silent retrieval failures.
4. *What observation would falsify the hypothesis?* If residual statistics ($\bar{E}_t$, $\mathcal{W}_1$) exhibit weak correlation with Recall@10 ($r < 0.40$), or if recall collapses abruptly without any preceding shift in residual distribution, or if the I.I.D. control index produces residual alarms identical to the drifting index.
5. *What experiment isolates the phenomenon?* Feeding a timestamped ArXiv stream into a static index vs. an I.I.D. control index, logging residual statistics at every insertion, and taking periodic ground-truth Recall@10 snapshots every 10,000 vectors.
6. *What confounders must be controlled?* Index size expansion, query distribution changes, and embedding norm variations (normalized via $L_2$ unit sphere projection).
7. *What is the closest prior experiment?* He et al. (TPAMI 2018) on Online PQ, and Tacnode Technical Report (2024) noting residual increases under OOD data.
8. *Has the exact experiment already been done?* No. Prior works either propose complex online retraining algorithms or evaluate static OOD recall drops; none systematically evaluate residual divergence as a calibrated predictive early-warning sensor with lead-time metrics on a multi-year temporal corpus.
9. *Can a student reproduce it?* Yes. Uses standard Python, FAISS (`faiss-cpu`), HuggingFace embeddings, and public ArXiv metadata on a standard student laptop (16GB RAM, ~2 hours execution time for 1M vectors).

* **Status**: `READY_FOR_NOVELTY_AUDIT`

---

## 2. Candidate E05: Serverless/Disaggregated Database Micro-Burst Latency

### 2.1 Original Flaws & Diagnostic
* **Original Formulation**: *"What is the tail latency penalty of compute/storage decoupling under micro-bursts?"*
* **Fatal Flaws in Phase 9**:
  1. *Localhost Invalidation*: Deploying Neon or Aurora locally over `localhost` reduces network latency to 0–20 $\mu\text{s}$ (local IPC), eliminating the 1–5 $\text{ms}$ cloud storage network RTT that defines compute-storage disaggregation. Measured P99 latency reflects local CPU scheduling, not storage decoupling.
  2. *Literature Saturation*: The generic phenomenon—that idle periods cause cold caches and sudden bursts incur a "cold-fetch tax" resulting in P99 spikes—has been extensively published in VLDB 2023–2024 (Neon, Gopher, BurScale).

### 2.2 Reformulated Research Question
> **"In compute-storage disaggregated databases under sudden read micro-bursts, does P99 tail latency amplification stem primarily from remote network transport delay or from internal buffer pool latch contention (`LWLock:buffer_mapping` and `BufferContent`) during concurrent page fault resolution?"**

### 2.3 Experimental Testbed Design (Containerized Network Emulation)
To make this experiment scientifically valid on student hardware without relying on cloud credits or invalid localhost sockets:
* **Architecture**: Two Docker/Podman containers running on a Linux host:
  - *Container Compute*: PostgreSQL compute engine with Neon or remote buffer-pool storage extensions.
  - *Container Storage*: Open-source Pageserver / remote storage daemon managing persistent table pages.
* **Network Interconnect**: A dedicated Linux virtual Ethernet pair (`veth0` $\leftrightarrow$ `veth1`) bridging the two containers.
* **Controlled Network Impairments**: Use Linux Traffic Control (`tc`) with `netem`:
  ```bash
  tc qdisc add dev veth0 root netem delay 5ms 1.5ms distribution pareto loss 0.1%
  ```
  This injects true Pareto-distributed data center network jitter and latency directly into kernel packet queues between compute and storage.
* **Buffer Cache Invalidation**: Explicitly flush the compute container's buffer pool (`DISCARD ALL`, `pg_drop_caches`) or implement variable idle sleep intervals to simulate auto-suspend memory reclamation.

### 2.4 Workload & Concurrency Scaling
* **Benchmark**: YCSB Read-Heavy Workload (Workload B: 95% reads, 5% updates; 10M records).
* **Burst Pattern**: 30-second idle periods followed by sudden step-function bursts of 500–2,000 queries over 2 seconds across variable client thread pools ($C \in \{1, 4, 16, 64, 128, 256\}$).
* **Telemetry**: Instrument PostgreSQL wait events using `pg_stat_activity` and `pg_stat_database` to decompose latency into:
  - `IO:DataFileRead` (time spent awaiting network page transit).
  - `LWLock:buffer_mapping` (time worker threads spend waiting for shared buffer table locks).
  - `LWLock:BufferContent` (time spent waiting to acquire page buffer read/write pins).

### 2.5 Scientific Question Test (E05)
1. *What is already known?* Disaggregated databases experience severe P99 latency degradation on un-cached reads due to remote storage fetches across network fabrics (Neon VLDB 2023, Gopher VLDB 2024).
2. *What exactly remains uncertain?* Whether tail latency explosions under high-concurrency micro-bursts scale linearly with network RTT or scale quadratically due to internal buffer lock serialization in the database kernel while threads await pending remote I/O.
3. *Why does that uncertainty matter?* If network latency dominates, database architects must invest in faster network cards (RDMA, CXL). If buffer latch contention dominates, database architects must redesign PostgreSQL's buffer mapping hash tables for asynchronous multi-page prefetching.
4. *What observation would falsify the hypothesis?* If the percentage of total tail latency attributed to `LWLock:buffer_mapping` remains flat ($<10\%$) as concurrency scales from 1 to 128 threads, with network transit time explaining $>90\%$ of P99 growth.
5. *What experiment isolates the phenomenon?* Comparing micro-burst P99 latency across concurrency levels under constant network delay vs. varying network delay under constant concurrency.
6. *What confounders must be controlled?* Host OS page cache (bypass via `O_DIRECT`), TCP connection establishment (use persistent `pgbouncer` connection pooling), CPU saturation (pin containers to isolated CPU cores).
7. *What is the closest prior experiment?* VLDB 2024 Gopher paper evaluating cache hits vs. remote fetches, and ICDE 2024 BurScale.
8. *Has the exact experiment already been done?* The generic tail latency experiment is closed; the internal lock-contention breakdown under Pareto-jittered container networks is technically open but borders on systems engineering profiling.
9. *Can a student reproduce it?* Moderately complex: requires Linux root privileges (`tc netem`), Docker container networking, and compiling Neon/PostgreSQL from source on an 8-core Linux workstation.

* **Status**: `REFORMULATED` (Viable as an empirical systems study, but high execution complexity and partial prior-art saturation in database literature).

---

## 3. Candidate E11: Predictive Test Selection under Refactoring Commits

### 3.1 Original Flaws & Diagnostic
* **Original Formulation**: *"Do PTS models exhibit dangerously high false-negative rates on refactoring commits?"*
* **Fatal Flaws in Phase 9**:
  1. *Dataset Invalidation*: Defects4J is a curated database of isolated bug-fix pairs; it contains **zero** sequential CI commit histories, passing builds, or general refactorings. Using Defects4J for test selection evaluation is methodologically impossible.
  2. *Vague Question*: Asking whether PTS has "higher false negatives" is too generic; it does not isolate the exact structural properties that break machine learning test predictors.

### 3.2 Reformulated Research Question
> **"How do specific categories of structural refactorings (class renames, method moves, and cross-module extractions) impact the False Negative Rate of ML-based Predictive Test Selection models across chronologically ordered continuous integration commit streams?"**

### 3.3 Novelty & Prior-Art Boundary
* *Industrial Recognition*: Industry engineering teams (Meta, BrowserStack 2024, Launchable 2023) hypothesize that renames and method moves weaken historical file-to-test correlations, creating "silent regression risks."
* *Academic Gap*: While deterministic, rule-based "Refactoring-Aware Regression Test Selection" has been investigated (Silva et al., TOSEM 2023; Tsantalis et al., TSE 2024), **no open-science academic empirical study has systematically quantified the False Negative Rate (missed failing builds) of Machine Learning Predictive Test Selection (PTS) stratified by AST refactoring categories across real continuous CI commit streams**.

### 3.4 Valid Dataset Construction (No Temporal Leakage)
To completely replace Defects4J with a methodologically impeccable, chronologically valid dataset:
* **Primary Data Sources**:
  1. **TravisTorrent**: Comprehensive, publicly mined CI database capturing continuous build logs and test execution outcomes across major open-source Java projects.
  2. **Active GitHub Actions Repositories**: 15 mature open-source Java repositories with multi-year CI histories and extensive test suites (e.g., `commons-lang`, `commons-io`, `jackson-databind`, `spring-boot`, `mockito`, `retrofit`, `guava`).
* **Sequential Commit Pipeline**:
  ```
  Repository Git History
          ↓
  Filter commits with associated CI build & test outcome (Pass / Fail)
          ↓
  Run RefactoringMiner 2.0 on each commit diff
          ↓
  Tag commit with deterministic AST refactoring types:
    - Pure Refactoring (100% of modified AST nodes are refactorings)
    - Feature / Logic Change (0% refactorings)
    - Mixed Commit (>0% refactorings + functional changes)
          ↓
  Categorize refactoring operations:
    - Class Rename
    - Move Method / Field across files
    - Extract Method (in-file)
    - Cross-Module Refactoring (moving classes across Maven/Gradle modules)
  ```
* **Strict Chronological Splitting (Zero Temporal Leakage)**:
  For each project, sort commits chronologically:
  - **Training Set ($\mathcal{D}_{\text{train}}$)**: First 70% of chronological commits (e.g., Jan 2020 – Dec 2022).
  - **Validation Set ($\mathcal{D}_{\text{val}}$)**: Next 10% of commits (e.g., Jan 2023 – Apr 2023) for threshold tuning.
  - **Test Evaluation Set ($\mathcal{D}_{\text{test}}$)**: Final 20% of commits (e.g., May 2023 – Dec 2023).
  - *Strict Rule*: Zero random shuffling across time or projects. Models train strictly on the past and predict the future.

### 3.5 Predictive Test Selection Model & Baselines
* **Evaluated Model**: Industry-standard Gradient Boosted Decision Tree (GBDT / LightGBM) modeled on Meta's PTS (Machalica et al., ICSE-SEIP 2019):
  - *Features*: Modified file paths, line change counts, file extension counts, author commit frequency, historical test failure co-occurrence matrix ($P(\text{Test}_j \text{ fails} \mid \text{File}_i \text{ modified})$).
* **Baselines**:
  1. *Retest-All*: Executes 100% of tests (Upper bound: FNR = 0.0%, Time Saved = 0.0%).
  2. *Deterministic Dependency RTS* (Ekstazi / STARTS): File checksum-based test selection.
  3. *Random Test Selection*: Selects tests randomly up to the same compute budget as PTS.
  4. *AST-Augmented PTS*: A reformulated variant where modified file-path features are augmented with RefactoringMiner source/target mappings (tracing moved code back to its original historical file identity).

### 3.6 Dependent Variables & Core Metrics
* **False Negative Rate (FNR / Missed Regressions)**:
  $$\text{FNR} = \frac{\text{Number of Failing Tests Incorrectly Skipped by PTS}}{\text{Total Number of Truly Failing Tests in Commit}}$$
* **False Omission Rate (FOR)**: Proportion of commits predicted clean that actually had failing builds.
* **Test Time Reduction (TTR)**: Percentage of test execution time saved.
* **Stratified Risk Ratio ($RR$)**:
  $$RR = \frac{\text{FNR}(\text{Structural Refactoring Commits})}{\text{FNR}(\text{Feature Commits})}$$

### 3.7 Scientific Question Test (E11)
1. *What is already known?* ML-based PTS achieves $\approx 99.9\%$ recall on general industrial commit streams (Machalica et al. 2019). Refactoring-aware static RTS exists (TOSEM 2023).
2. *What exactly remains uncertain?* Whether identity-modifying refactorings (renames, method moves, cross-module relocations) cause a statistically significant spike in false negatives in standard file-path-based PTS models, and by what magnitude compared to regular feature commits.
3. *Why does that uncertainty matter?* A false negative in test selection is the worst possible failure: a regression silently passes CI and merges into the production release branch. If refactorings induce systematic false negatives, CI systems must automatically bypass PTS or use refactoring-aware feature mapping.
4. *What observation would falsify the hypothesis?* If the False Negative Rate on structural refactoring commits is statistically indistinguishable from or lower than feature commits ($RR \le 1.0$, $p > 0.05$).
5. *What experiment isolates the phenomenon?* Evaluating a trained GBDT PTS model on chronologically held-out commits partitioned into pure refactorings, feature commits, and mixed commits, while controlling for test suite size and failure rates.
6. *What confounders must be controlled?* Flaky tests (filter tests that fail and pass on the exact same commit hash), co-occurring test updates (separate commits that refactor tests simultaneously from production-only refactorings), build environment failures (exclude non-test Maven/Gradle compilation errors).
7. *What is the closest prior experiment?* Machalica et al. (ICSE 2019) evaluating overall PTS performance; Silva et al. (TOSEM 2023) evaluating static RTS on refactorings.
8. *Has the exact experiment already been done?* No. No prior peer-reviewed study has systematically evaluated ML-based PTS false negative rates stratified by AST refactoring categories using continuous open-source CI datasets.
9. *Can a student reproduce it?* Yes. Uses public Git repositories, public TravisTorrent/GitHub logs, open-source RefactoringMiner, and scikit-learn/LightGBM. Completely executable on a personal computer (CPU-only, 16GB RAM).

* **Status**: `READY_FOR_NOVELTY_AUDIT`

---

## 4. Reformulation Comparison Matrix

| Candidate ID | Area | Original Problem | Reformulated Core Hypothesis | Dataset / Workload | Baseline | Confounder Controls | Feasibility | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **E02** | Vector Databases | SQuAD$\rightarrow$MSMARCO was invalid domain shift; static recall drop is tautological. | Streaming residual statistics ($\bar{E}_t, \mathcal{W}_1$) can predict Recall@K degradation before SLA breach under temporal drift. | 1.5M ArXiv metadata embeddings (2018–2024), chronological. | Static PQ, Periodic Retraining, Exact KNN. | I.I.D. parallel control index, static anchor queries, unit norm. | High (FAISS on Laptop) | `READY_FOR_NOVELTY_AUDIT` |
| **E05** | Cloud Databases | Localhost eliminates cloud network RTT; general cold-fetch tail latency is closed. | P99 tail latency in micro-bursts is dominated by internal `LWLock:buffer_mapping` contention rather than network transit time. | YCSB read-heavy bursts (10M keys) on containerized PostgreSQL + Pageserver. | Monolithic PG, Non-jittered disaggregated, Single-threaded. | `tc netem` Pareto delay injection, `veth` isolation, `drop_caches`. | Medium (Docker + Linux root) | `REFORMULATED` |
| **E11** | Software Engineering | Defects4J lacks continuous CI streams; hypothesis was too generic. | Structural refactorings (renames, method moves) exhibit $\ge 3\times$ higher FNR in ML PTS due to path-feature decoupling. | 15 open-source Java repos from TravisTorrent & GitHub Actions ($>20k$ builds). | Retest-All, Standard GBDT PTS, Deterministic RTS (Ekstazi). | Chronological train/test split, RefactoringMiner tagging, flaky test filtering. | High (LightGBM on Laptop) | `READY_FOR_NOVELTY_AUDIT` |

---

## 5. Summary and Recommended Next Steps

1. **E02 (Vector DB / Product Quantization Drift Early Warning)** has been successfully converted into an actionable, statistically rigorous experimental question with a verified chronological dataset (ArXiv 2018–2024) and clear confounder controls.
2. **E05 (Disaggregated DB Buffer Lock Contention)** has been provided with a containerized network emulation methodology using `tc netem`, but remains threatened by substantial prior-art profiling in VLDB/SIGMOD cloud database literature.
3. **E11 (Predictive Test Selection under AST Refactorings)** has been fundamentally redesigned, replacing the invalid Defects4J source with continuous CI commit histories from TravisTorrent and GitHub Actions, labeled via RefactoringMiner 2.0 with strict chronological train/test partitioning.

Both **E02** and **E11** have reached `READY_FOR_NOVELTY_AUDIT` status with verified datasets, testable hypotheses, and high student execution feasibility.
