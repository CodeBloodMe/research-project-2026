# Research Gaps

## G01: RAG Adversarial Vulnerability
Current RAG systems retrieve contextual documents but do not intrinsically verify their integrity, leaving them vulnerable to prompt injection or poisoned corpus documents.

## G02: RAG Adaptive Depth
Standard RAG pipelines retrieve a fixed number of documents (k) regardless of query complexity, leading to unnecessary latency on simple queries and insufficient context on complex ones.

## G03: Contamination-Proof SE Benchmarks
Standard SE benchmarks (like HumanEval) are frequently ingested in the training data of new LLMs, making accurate zero-shot evaluation nearly impossible without entirely new, hidden test suites.

## G04: Long-Horizon SE Context Forgetting
When an LLM agent navigates a large codebase to fix an issue, it quickly exhausts its context window or forgets the original intent, leading to stalled resolutions on SWE-bench.

## G05: PECFT Catastrophic Forgetting
When a model is continually fine-tuned using parameter-efficient methods (PECFT) on a sequence of tasks, the updates destructively interfere, causing catastrophic forgetting of earlier tasks.

## G06: PEFT Adversarial Fragility
While PEFT achieves comparable standard accuracy to full fine-tuning, the low-rank nature of its updates may introduce specific vulnerabilities to adversarial perturbations that remain unexplored.

## G07: RAG Recall Ceiling from Hard Filtering
Aggressively filtering adversarial or poisoned documents in RAG causes a sharp drop in overall recall, as valid structural information embedded in those documents is permanently destroyed.

## G08: LLM Repo-Level Static Analysis Exhaustion
Iterative static analysis feedback loops for LLMs work on single files, but feeding multi-file, cross-module dependency warnings into a prompt exhausts the context window and causes severe hallucinations.

## G09: Task-Free C-LoRA Brittleness
Continual learning routing mechanisms (like C-LoRA) strictly rely on explicit task IDs. In task-free, continuous data streams, they suffer from information leakage and route to the wrong adapters, causing catastrophic forgetting.

## G10: Irreversible KV Cache Eviction Loss
Current infinite-context LLM optimizations (like SnapKV) use attention heuristics to permanently evict tokens. This destroys the model's ability to perform long-horizon multi-step reasoning when an evicted token is suddenly needed later.
