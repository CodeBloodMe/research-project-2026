# Novelty Audits

## Candidate C01
### Proposed Contribution
Low-latency cross-encoder filter prior to generation to reduce adversarial context poisoning in RAG.
### Verdict
REJECT
### Justification
Filtering retrieved documents with a cross-encoder or relevance classifier is already a standard baseline in robust RAG systems. The claim that "no lightweight real-time filter exists" is falsified by the literature.

## Candidate C02
### Proposed Contribution
Iterative static-analysis feedback loop to reduce API hallucinations in LLM code generation.
### Verdict
REJECT
### Justification
Recent papers (e.g., "Static Analysis as a Feedback Loop", arXiv:2508.14419) exactly propose this method. Combining LLMs with static analyzers like Bandit or CodeQL is now an active and crowded research space, not a novel gap.

## Candidate C03
### Proposed Contribution
Task-specific adapter-routing mechanism to prevent catastrophic forgetting in PECFT while maintaining parameter budget.
### Verdict
REJECT
### Justification
The literature (2025-2026) has already addressed this. C-LoRA introduces a learnable routing matrix, and ProCL uses dynamic routing of "programs" within LoRA adapters. The proposed gap has been decisively closed.
