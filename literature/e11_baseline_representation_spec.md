# Phase 13E: Baseline Representation Specification (E11)

This specification strictly freezes the feature representations used by the study's tabular history-based PTS model. Any refactoring effect must be evaluated exclusively against its exposure to this defined feature set.

## 1. File/Path Identity (Primary Linkage)
* **Description**: The fully qualified file path of the modified production code.
* **Unit of Indexing**: File level.
* **Role**: Used as the primary token to query historical code-test failure correlation matrices.
* **Exposure Pathway**: Refactorings that rename or move files directly sever this mapping, setting the historical correlation probability for that file path to zero.

## 2. Historical Code-Test Co-occurrence
* **Description**: The conditional probability that test $T_j$ failed in the past given that file $F_i$ was modified.
* **Unit of Indexing**: File-to-Test mapping.
* **Role**: The core associative signal identifying which tests are sensitive to changes in which areas of the codebase.
* **Exposure Pathway**: Relies entirely on File/Path Identity remaining stable over time.

## 3. Code Churn
* **Description**: The quantitative counts of lines added, lines deleted, and files modified within the commit.
* **Unit of Indexing**: Commit level and File level.
* **Role**: Acts as a proxy for risk/complexity.
* **Exposure Pathway**: Refactorings inherently generate structural churn (e.g., extracting a method adds and deletes lines). This is an *indirect* exposure; the identity is intact, but the churn metric is altered.

## 4. Historical Test Failure Information
* **Description**: The overall historical failure rate of test $T_j$, recent failure window, and time since last failure.
* **Unit of Indexing**: Test level.
* **Role**: Captures base rates of failure for tests independently of code modifications.
* **Exposure Pathway**: Refactoring production code does not alter test-level identifiers unless the test suite itself is concurrently refactored.

## Explicit Exclusions
* **Semantic Embeddings**: TF-IDF vectors, CodeBERT embeddings, or AST token sequence models are NOT part of this defined baseline.
* **Method-Level History**: The baseline aggregates history at the file level. Method-level tracking is excluded unless explicitly defined in a separate intervention phase.
