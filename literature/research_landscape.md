# Research Landscape

## Information Retrieval / RAG

### Major Problems
- Integration of retrieved noisy/adversarial inputs.
- Performance trade-offs (latency vs. faithfulness).
- Multi-hop reasoning and structured knowledge integration.
- Lack of robust evaluation frameworks for the hybrid nature of RAG.

### Existing Approaches
- Dense passage retrieval (DPR) + standard generation.
- Graph-based retrieval (GraphRAG).
- Iterative and adaptive retrieval techniques.

### Important Recent Work
- "Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers"
- "Evaluation of Retrieval-Augmented Generation: A Survey"

### Common Datasets
- NaturalQuestions, TriviaQA, MS MARCO, HotpotQA.

### Common Metrics
- F1, Exact Match (EM), ROUGE, BLEU, Answer Faithfulness, Context Relevance.

### Repeated Limitations
- Difficulty reasoning over disjointed or multi-hop evidence.
- High computational overhead for dynamic retrieval.
- Vulnerability to adversarial context.

### Unresolved Questions
- How to seamlessly integrate structural graphs into vector retrieval in real-time?
- How to measure grounding fidelity without relying solely on LLM-as-a-judge?

## Software Engineering (LLMs for Code)

### Major Problems
- Lack of standardized, uncontaminated evaluation datasets.
- Data scarcity for specialized, safety-critical domains.
- Context-window limitations for long-horizon repository-level maintenance.

### Existing Approaches
- Instruction tuning on code (CodeAlpaca, Magicoder).
- Agent-based frameworks (SWE-agent, AutoCodeRover).

### Important Recent Work
- "Large Language Models for Software Engineering: A Systematic Literature Review" (arXiv:2308.10620)
- "Large Language Models for Software Engineering: Survey and Open Problems"

### Common Datasets
- HumanEval, MBPP, SWE-bench, CodeSearchNet.

### Common Metrics
- Pass@k, Exact Match, Compilation Success Rate, Patch Resolution Rate.

### Repeated Limitations
- Severe risk of data contamination in benchmarks.
- Inability to handle deeply interdependent, multi-file software evolution.
- Hallucination of non-existent APIs (semantic misunderstandings).

### Unresolved Questions
- How to hybridize LLMs with traditional static analysis tools efficiently?
- How does LLM reliance impact long-term technical debt?

## Parameter-Efficient Fine-Tuning (PEFT)

### Major Problems
- Catastrophic forgetting in continual learning scenarios (PECFT).
- Generalization gap compared to full fine-tuning on complex tasks.
- Lack of understanding regarding adversarial robustness of PEFT.

### Existing Approaches
- LoRA, QLoRA, Prefix Tuning, Adapters, Prompt Tuning.

### Important Recent Work
- Surveys on Parameter-Efficient Continual Fine-Tuning (PECFT).
- "Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey"

### Common Datasets
- GLUE, SuperGLUE, domain-specific instruction sets.

### Common Metrics
- Accuracy, Perplexity, Parameter Count, GPU Memory footprint.

### Repeated Limitations
- Sequential task learning completely overwrites prior task adapters.
- Complex selection of hyper-parameters and PEFT combinations.
- Communication bottlenecks in Federated Learning.

### Unresolved Questions
- How to dynamically merge or route adapters to prevent forgetting?
- Does PEFT inherently increase vulnerability to adversarial data?
