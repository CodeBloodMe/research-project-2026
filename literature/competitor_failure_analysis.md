# Competitor Failure Analysis (Phase 7B)

## 1. RAG Cross-Encoder Filtering (C01 Competitors)
**Recent Solutions:** Using rerankers, cross-encoders, and relevance classifiers (e.g., ScoreGate, ReliableRAG) to filter out poisoned or irrelevant documents.
**Actual Failure Mode:** *Recall Degradation & The Recall Ceiling.* Aggressive filtering strategies lead to severe recall drops. If a chunk is filtered out because it contains an adversarial trigger, the generator loses the valid information embedded in that same chunk.
**Second-Order Gap:** How to neutralize adversarial triggers within a retrieved chunk without irreversibly destroying the structural and semantic utility of the surrounding text for the generator.

## 2. LLM + Static Analysis Feedback (C02 Competitors)
**Recent Solutions:** AdaTaint, etc., which feed Bandit/CodeQL static analysis reports back into the LLM context window to iteratively refine code.
**Actual Failure Mode:** *Repository-Level Context Exhaustion.* These feedback loops work well on single files, but scaling them to enterprise repositories fails. The LLM cannot digest a multi-file dependency graph alongside hundreds of static analysis warnings without blowing out the context window and hallucinating.
**Second-Order Gap:** How to compress repository-wide static analysis warnings into a minimal dependency-graph representation that guides the LLM without exhausting context.

## 3. PEFT Adapter Routing (C03 Competitors)
**Recent Solutions:** C-LoRA, ProCL (2026), PEARL (2026) which use dynamic routing matrices to allocate tasks to different LoRA adapters, preventing catastrophic forgetting.
**Actual Failure Mode:** *Task-Identifier Brittleness.* These methods strictly rely on known task boundaries or explicit task IDs during training and inference. In "task-free" or online continuous data streams where boundaries are blurry, the routing matrix suffers from "Information Leakage" and chooses the wrong adapter, destroying accuracy.
**Second-Order Gap:** How to achieve task-free dynamic LoRA routing by implicitly inferring task boundaries without explicit labels.

## 4. KV Cache Eviction for Infinite Context (New Domain Exploration)
**Recent Solutions:** StreamingLLM, SnapKV, H2O which evict tokens from the KV cache based on attention heuristics (heavy hitters).
**Actual Failure Mode:** *Irreversible Information Loss.* Eviction is permanent. When multi-step logic requires a token that was evicted 10k steps ago because it had low attention *at the time*, the reasoning chain collapses.
**Second-Order Gap:** How to dynamically re-fetch evicted KV tokens from cheap CPU memory only when the LLM realizes it is missing context.
