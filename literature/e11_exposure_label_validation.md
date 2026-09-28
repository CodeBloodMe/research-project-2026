# Phase 16B: Exposure Label Validation

## Core Principle
A refactoring operation is NOT universally classified as "direct exposure". It is only a direct exposure if it modifies an identity (e.g., file path or class name) that the *frozen baseline ML-PTS model* relies upon as a predictive feature.

## Baseline Features (Machalica Option B)
- **Direct Identifiers**: File Paths, File Names.
- **Excluded**: Internal class structures, dependency graphs, token semantics (TF-IDF/CodeBERT).

## Classification Rules applied in Phase 16B
- **Direct Exposure**: Any refactoring that alters the File Path or File Name of a Java file.
  - *Examples*: Rename Class (if it triggers a file rename), Move Class (changes path), Rename Package (changes path of all classes within it).
- **Indirect Exposure**: Refactorings that alter internal class structures without changing the file path. The historical file path indexing remains intact, but the internal logic has shifted.
  - *Examples*: Rename Method, Move Method, Extract Method, Inline Method, Change Parameter Type, Change Return Type.

## Script Implementation
The extraction script evaluates the RefactoringMiner `type` strings against this logic:
- If `"Rename Class" in t` or `"Move Class" in t` or `"Rename Package" in t`, it flags `direct_exposure = True`.
- If `"Method" in t` or `"Parameter" in t` or `"Return Type" in t` or `"Attribute" in t`, it flags `indirect_exposure = True`.
- A single commit can exhibit both direct and indirect exposures simultaneously.

## Final Validation
*(To be completed empirically post-extraction)*
We will sample the resulting `data/e11_refactoring_exposure_labels.csv` to ensure no "Rename Method" operations were falsely flagged as direct exposure.
