# Phase 13D: Identity Representation Taxonomy (E11)

This taxonomy maps RefactoringMiner operations specifically to the representation levels utilized by the defined *tabular history-based ML-PTS baseline*. The baseline primarily utilizes file paths, historical failure rates, and code churn; it does *not* utilize deep semantic embeddings (e.g., TF-IDF, CodeBERT). 

The classification defines which level of historical identity the refactoring alters:
A. **FILE/PATH IDENTITY**: The physical file path or class name used as the primary indexing token for historical code-test co-occurrence matrices.
B. **METHOD/SYMBOL IDENTITY**: The name of the method/function, which may be used by finer-grained PTS formulations.
C. **SIGNATURE IDENTITY**: The parameter types or return types of a method, which may affect method resolution but not the primary symbol name.
D. **LOCAL/TOKEN STRUCTURE**: The AST nodes within a method body. These are entirely invisible to file-level tabular PTS models but affect code-churn metrics.

## 1. FILE/PATH IDENTITY ALTERING
Operations that destroy or change the primary file/path token used to query historical failure records.
* **Rename Class / Rename Package / Move Class / Move Package**
  * **Identity Level Affected**: FILE/PATH
  * **Scientific Rationale**: Directly alters the file path or top-level namespace. The tabular PTS model will treat this as a novel file with zero failure history.
  * **Expected Baseline Interaction**: Massive feature shift (historical co-occurrence drops to 0).

* **Extract Class**
  * **Identity Level Affected**: FILE/PATH
  * **Scientific Rationale**: Creates a new file/class containing existing logic. The new file lacks historical failure mapping.
  * **Expected Baseline Interaction**: Massive feature shift for the extracted logic.

## 2. METHOD/SYMBOL IDENTITY ALTERING
Operations that alter the method-level symbol but preserve the host file's identity.
* **Rename Method / Move Method (within same file/package) / Move Attribute**
  * **Identity Level Affected**: METHOD/SYMBOL
  * **Scientific Rationale**: If the PTS model aggregates history at the method level, this destroys the linkage. If the PTS model aggregates strictly at the file level, this may be somewhat insulated, though it registers as massive line churn.
  * **Expected Baseline Interaction**: Moderate-to-high feature shift depending on the aggregation level (file vs. method).

## 3. SIGNATURE IDENTITY ALTERING
Operations that change method interfaces but preserve the primary symbol name.
* **Change Parameter Type / Change Return Type / Add Parameter / Remove Parameter**
  * **Identity Level Affected**: SIGNATURE
  * **Scientific Rationale**: Preserves the method name, meaning coarse file/method-level history mapping often survives, but the exact signature token changes.
  * **Expected Baseline Interaction**: Low feature shift (primarily manifests as localized code churn).

## 4. LOCAL/TOKEN STRUCTURE ALTERING
Operations that strictly reorganize internal AST nodes within an intact method/file boundary.
* **Extract Variable / Rename Variable / Change Variable Type / Extract Method / Change Access Modifier / Annotations**
  * **Identity Level Affected**: LOCAL/TOKEN
  * **Scientific Rationale**: Tabular PTS models typically do not parse AST tokens. These operations simply register as lines added/deleted (code churn).
  * **Expected Baseline Interaction**: Negligible feature shift (beyond normal churn). Historical identity is perfectly preserved.

## Excluded Concepts
* Note: Interactions with textual semantic models (TF-IDF) or embeddings (CodeBERT) have been explicitly excluded, as the baseline is defined as a history-based tabular model.
