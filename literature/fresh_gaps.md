# Fresh CS Gaps (Phase 8)

## F01: DiskANN NVMe Latency Bottleneck
In vector databases, offloading HNSW graphs to SSDs solves RAM constraints but introduces severe I/O read latency during graph traversal that cannot be easily prefetched due to the algorithm's unpredictability.

## F02: Edge FL Pruning Client Drift
Pruning model updates in Federated Learning reduces communication for edge stragglers, but blindly pruning non-IID data causes global models to forget unique, localized client features.

## F03: Serverless 2PC Overhead
Stateful serverless functions using shared disaggregated logs suffer massive latency overheads due to the reliance on traditional Two-Phase Commit (2PC) protocols across stateless invocations.

## F04: Hybrid Fuzzing SMT Timeouts
Hybrid fuzzers rely on Symbolic Execution to solve complex branches, but underlying SMT solvers (like Z3) consistently time out on cryptographic, non-linear, or state-heavy constraints, stalling coverage.

## F05: SGX ORAM Overhead
Implementing side-channel protections like Oblivious RAM (ORAM) in Intel SGX Trusted Execution Environments incurs such extreme performance penalties that protecting ML inference becomes practically infeasible.

## F06: Streaming RecSys Cold-Start
Online streaming recommender systems cannot afford the latency of waiting for collaborative interaction data to arrive and trigger a model retraining, leaving newly ingested items entirely un-recommendable.

## F07: GPU DVFS SLO Violations
Energy-efficient GPU schedulers that rely on dynamic frequency scaling (DVFS) inadvertently violate strict Time-To-First-Token (TTFT) Service Level Objectives during LLM inference due to phase-agnostic throttling.

## F08: P4 Recirculation Throughput Drop
Complex stateful flow monitoring in P4 programmable switches requires packet recirculation due to SRAM/TCAM and ALU constraints, which inherently halves line-rate throughput on Tofino ASICs.

## F09: Paxos/Raft Tail Latency
Strict global consensus protocols in geo-replicated databases incur multi-round-trip WAN latencies, penalizing commutative or non-conflicting transactions unnecessarily.

## F10: DLRM PCIe Bottleneck
Offloading Deep Learning Recommendation Model embedding tables to CPU RAM solves the GPU capacity limit but introduces a severe PCIe transfer bottleneck during the forward pass.
