# Phase 13D: E11 Design Change Log

> **STATUS: HISTORICAL**
> *This document represents past design iterations. It may contain causal language or baseline specifications that have since been superseded by the `E11_FINAL_RESEARCH_DESIGN.md`.*

## 1. RQ1 Alignment
* **Previous State**: RQ1 broadly compared "refactoring-containing commits" to "non-refactoring commits," silently merging `REF_ONLY` (pure refactorings) into the primary treatment.
* **New State**: RQ1 now explicitly contrasts `REF_MIXED` against `NON_REF`. `REF_ONLY` is defined as a separately reported descriptive subgroup to prevent theoretical ambiguity.

## 2. Refactoring Taxonomy Rebuilt
* **Previous State**: The taxonomy abstracted operations loosely and made claims about TF-IDF or CodeBERT impacts.
* **New State**: The abstract taxonomy has been superseded by `e11_identity_representation_taxonomy.md`. Operations are now strictly classified by which *identity level* they alter relative to the defined history-based tabular PTS baseline (File/Path, Method/Symbol, Signature, Local/Token structure). Semantic embedding claims were purged.

## 3. RQ2 Analytical Variable Update
* **Previous State**: Grouping implied mutually exclusive categories for each commit.
* **New State**: Because a commit can have multiple operations affecting multiple identity levels, RQ2 employs a multi-label binary representation (`identity_file_change = 0/1`, `identity_method_change = 0/1`, `identity_signature_change = 0/1`, `local_structural_change = 0/1`). H2 has been updated to hypothesize directly on these represented identity levels.

## 4. Pilot Audited and Re-labeled
* **Previous State**: 99/99 commits from the `gson` pilot were declared `REF_MIXED`, acting as proof of population prevalence.
* **New State**: The pilot is explicitly downgraded to a "single-project operational pilot." The `REF_MIXED` count was reverted to "Refactoring-Containing; Mixed Status Unresolved" because a strict diff-coverage AST analysis was not performed. All assertions of statistical power relying on this subset were removed.

# Phase 13E: E11 Design Change Log (Representation Exposure)

## 1. Separation of Refactoring Effect vs PTS Exposure
* **Previous State**: The taxonomy evaluated refactoring operations by the structural property they altered (File, Method, Signature, Local) assuming all alterations were equally relevant.
* **New State**: The logic has been bifurcated. A refactoring operation changes an AST identity, but it only causes *historical representation discontinuity* if that identity is actually indexed by the baseline PTS model. This causal chain is codified in `e11_mechanism_model.md`.

## 2. Baseline Representation Freeze
* **Previous State**: The baseline representations were loosely described and left open the possibility of deep semantic embeddings (e.g., CodeBERT).
* **New State**: `e11_baseline_representation_spec.md` strictly limits the baseline to File/Path Identity, Code Churn, Historical Code-Test Co-occurrence, and Historical Test Failure Information, all primarily indexed at the File level.

## 3. RQ2 and RQ3 Rewrite
* **Previous State**: RQ2 explored specific structural classes. RQ3 proposed generic identity mapping.
* **New State**: RQ2 now directly tests the difference between operations with *Direct Exposure* (altering file/path) vs *Indirect Exposure* (altering local churn). RQ3 strictly limits the intervention to preserving the *affected* historical representation (e.g., file rename mapping).

## 4. Purge of Extraneous Claims
* References to RefactoringMiner 2.0 as an infallible or exclusive authority were removed.
* TF-IDF and CodeBERT were completely excised from the baseline definition documents.
