# Phase 13D: E11 Design Change Log

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
