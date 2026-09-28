# Candidate Research Questions

## Candidate C01
### Research Area
Information Retrieval / RAG
### Problem
RAG systems retrieve documents from external corpora without verifying their integrity, making them highly susceptible to adversarial poisoning or conflicting information.
### Existing Work
Standard RAG, Self-RAG.
### Gap
Lack of lightweight, real-time adversarial filtering during the retrieval integration phase.
### Research Question
Does applying a low-latency cross-encoder filter prior to generation significantly reduce the success rate of adversarial context poisoning in RAG without harming accuracy on clean data?
### Hypothesis
A lightweight validation layer will reject poisoned contexts, maintaining baseline exact-match scores while dropping adversarial success rates by >40%.
### Potential Contribution
A novel, efficient filtering pipeline for secure RAG.
### Datasets
HotpotQA with artificially injected adversarial paragraphs.
### Baselines
Standard DPR + Llama-3, Self-RAG.
### Metrics
Exact Match, Faithfulness, Adversarial Success Rate, Latency.
### Compute Requirement
MEDIUM
### Main Risk
The filter might increase latency too much for real-time applications or falsely reject valid documents.
### Evidence
Surveys emphasize security and adversarial robustness as an open frontier.
### Gap Confidence
[HIGH]

## Candidate C02
### Research Area
Software Engineering (LLM4SE)
### Problem
LLMs frequently hallucinate API calls or use deprecated functions when generating code for specialized libraries.
### Existing Work
Instruction tuning, RAG for code.
### Gap
Prompt engineering alone cannot guarantee semantic correctness of API usage without external compiler/static analysis feedback.
### Research Question
How does tightly coupling an LLM generator with an iterative static-analysis feedback loop compare to standard few-shot prompting for reducing API hallucinations in specialized domains?
### Hypothesis
Iterative static analysis feedback will reduce API hallucination rates by >50% compared to standard zero-shot or few-shot baselines.
### Potential Contribution
A hybrid symbolic-neural framework for code generation.
### Datasets
Custom dataset of recent (post-2023) API documentation and tasks (to avoid contamination).
### Baselines
GPT-4/CodeLlama with standard prompting.
### Metrics
Compilation Success Rate, API Hallucination Rate.
### Compute Requirement
LOW (API based) / MEDIUM (local LLMs)
### Main Risk
Building the static analysis harness for multiple languages is highly engineering-intensive.
### Evidence
ICSE-FoSE survey calls for hybridizing LLMs with traditional SE tools.
### Gap Confidence
[HIGH]

## Candidate C03
### Research Area
Parameter-Efficient Fine-Tuning (PEFT)
### Problem
Continual learning using PEFT (PECFT) leads to catastrophic forgetting as the same low-rank matrices are updated for new tasks.
### Existing Work
Standard LoRA, Elastic Weight Consolidation (EWC).
### Gap
Existing dynamic routing methods are too memory-intensive, and standard PEFT overwrites previous task knowledge.
### Research Question
Can a task-specific adapter-routing mechanism prevent catastrophic forgetting in sequence-task learning while maintaining the same parameter budget as standard LoRA?
### Hypothesis
Task-specific routing will retain >90% of base accuracy on previous tasks compared to standard LoRA which drops below 50%.
### Potential Contribution
A novel routing architecture for PECFT.
### Datasets
GLUE benchmark (learned sequentially).
### Baselines
Standard LoRA, AdapterFusion.
### Metrics
Average Accuracy, Forgetting Measure (FM).
### Compute Requirement
MEDIUM (single GPU is sufficient for small models like BERT/Llama-8B).
### Main Risk
Adapter routing might struggle to automatically identify task boundaries without explicit task IDs.
### Evidence
Multiple arXiv surveys highlight PECFT forgetting as a major limitation.
### Gap Confidence
[HIGH]

## Candidate C04
### Research Area
IR/RAG
### Problem
Filtering adversarial RAG chunks destroys valid surrounding information (recall ceiling).
### Existing Work
ReliableRAG, ScoreGate.
### Gap
Hard-filtering causes severe recall degradation.
### Research Question
Can compressed ambient context preserve recall while neutralizing adversarial triggers in RAG?
### Hypothesis
Passing filtered chunks through a heavy autoencoder destroys triggers but retains semantic utility.
### Potential Contribution
Novel defense mechanism preserving recall.
### Datasets
HotpotQA + Adversarial.
### Baselines
Standard Filtering, ScoreGate.
### Metrics
Recall, Adversarial Success.
### Compute Requirement
MEDIUM
### Main Risk
Autoencoder might not destroy advanced triggers.
### Evidence
2025 RAG Recall surveys.
### Gap Confidence
[HIGH]

## Candidate C05
### Research Area
LLM4SE
### Problem
File-level LLM static analysis feedback fails on large repositories due to context exhaustion.
### Existing Work
AdaTaint, arXiv:2508.14419.
### Gap
Cannot scale to multi-file repos.
### Research Question
Can dependency graph summarization scale iterative static-analysis feedback to repository-level generation?
### Hypothesis
Summarizing cross-module SA warnings via dependency graphs reduces context use by 70% while maintaining fix rate.
### Potential Contribution
Repo-level SA feedback framework.
### Datasets
SWE-bench.
### Baselines
Standard File-level SA feedback.
### Metrics
Patch Resolution Rate, Context Tokens.
### Compute Requirement
HIGH
### Main Risk
Graph summarization might lose critical bug context.
### Evidence
2025 Repo-level LLM surveys.
### Gap Confidence
[HIGH]

## Candidate C06
### Research Area
PEFT
### Problem
C-LoRA routing requires explicit task IDs and fails in task-free continuous streams.
### Existing Work
C-LoRA (2025), ProCL (2026).
### Gap
Brittle without explicit task boundaries.
### Research Question
Can base-model activation clustering unsupervisedly infer task boundaries for task-free C-LoRA routing?
### Hypothesis
Clustering intermediate activations of the frozen base model accurately infers boundaries for routing.
### Potential Contribution
Task-free dynamic routing architecture.
### Datasets
Task-Free GLUE.
### Baselines
C-LoRA, Task-Free Continual Learning.
### Metrics
Accuracy, Forgetting Measure.
### Compute Requirement
MEDIUM
### Main Risk
Activations might drift regardless of task.
### Evidence
2026 PECL limitation surveys.
### Gap Confidence
[HIGH]

## Candidate C07
### Research Area
ML Systems
### Problem
Attention-based KV eviction permanently deletes tokens needed for multi-step reasoning.
### Existing Work
SnapKV, StreamingLLM.
### Gap
Irreversible loss of long-horizon dependencies.
### Research Question
Can entropy-driven CPU re-fetching mitigate irreversible information loss in KV cache eviction?
### Hypothesis
Re-fetching evicted KV blocks from CPU when generation entropy spikes restores reasoning accuracy.
### Potential Contribution
Compute vs Memory adaptive systems tradeoff.
### Datasets
LongBench.
### Baselines
SnapKV.
### Metrics
Accuracy, Memory, Latency.
### Compute Requirement
HIGH
### Main Risk
PCIe transfer latency might outweigh generation benefits.
### Evidence
2025 Long-context KV eviction surveys.
### Gap Confidence
[HIGH]

## Candidate C08
### Research Area
LLM4SE
### Problem
Unclear if new reasoning models benefit from static analysis loops as much as standard LLMs.
### Existing Work
arXiv:2606.06633.
### Gap
Focuses heavily on standard LLMs.
### Research Question
Do latent chain-of-thought models render external compiler feedback redundant?
### Hypothesis
Reasoning models self-correct better internally making external compiler feedback marginally useful.
### Potential Contribution
Empirical analysis of reasoning vs external tools.
### Datasets
HumanEval / Custom Bugs.
### Baselines
o1 / DeepSeek-R1 + Compiler Feedback.
### Metrics
Fix Rate, Inference Compute.
### Compute Requirement
MEDIUM
### Main Risk
Reasoning models still make basic syntax errors.
### Evidence
2026 Reasoning model empirical studies.
### Gap Confidence
[MEDIUM]

## Candidate C09
### Research Area
Federated PEFT
### Problem
Federated PEFT suffers from client drift when data is non-IID.
### Existing Work
PEARL (2026), FedRoLE.
### Gap
Data heterogeneity disrupts fixed-rank PEFT updates.
### Research Question
Can dynamic rank allocation mitigate client-drift in Federated PEFT under extreme data heterogeneity?
### Hypothesis
Allocating higher LoRA ranks to clients with higher data entropy reduces global drift.
### Potential Contribution
Novel Federated PEFT aggregation method.
### Datasets
FedGLUE.
### Baselines
FedIT, Standard FedLoRA.
### Metrics
Global Accuracy, Communication Cost.
### Compute Requirement
MEDIUM
### Main Risk
Dynamic ranks complicate server aggregation.
### Evidence
2025 Federated PEFT surveys.
### Gap Confidence
[HIGH]

## Candidate C10
### Research Area
RAG Eval
### Problem
Joint RAG metrics fail to penalize a perfect retriever paired with a hallucinating generator.
### Existing Work
RAGAS, ARES.
### Gap
Cannot easily isolate the 'Recall Conversion Rate'.
### Research Question
How to computationally isolate retrieval success from generator reasoning failure?
### Hypothesis
A counterfactual evaluation metric isolating reasoning drops provides stronger diagnostic signals.
### Potential Contribution
New RAG diagnostic metric framework.
### Datasets
TriviaQA.
### Baselines
RAGAS.
### Metrics
Correlation with Human Judgement.
### Compute Requirement
LOW
### Main Risk
Difficult to define 'perfect' reasoning.
### Evidence
2025 RAG Evaluation Surveys.
### Gap Confidence
[MEDIUM]

## Candidate C11
### Research Area
Multi-Modal RAG
### Problem
Text-based RAG filters fail on multi-modal documents where images contain deceptive visual context.
### Existing Work
ScoreGate.
### Gap
Unexplored in Vision-Language Models.
### Research Question
Does dual-score fusion mitigate visual false-positives in VLM RAG?
### Hypothesis
Visual-semantic dual-scoring filters out adversarial image retrieval.
### Potential Contribution
Multi-modal robust RAG pipeline.
### Datasets
WebQA, VisualQA.
### Baselines
Standard VLM RAG.
### Metrics
Visual EM, Adversarial Success.
### Compute Requirement
HIGH
### Main Risk
VLMs are highly sensitive to prompt structure.
### Evidence
2025 VLM RAG surveys.
### Gap Confidence
[MEDIUM]
