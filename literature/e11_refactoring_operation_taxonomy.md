# Phase 13C: Refactoring Operation Taxonomy (E11)

This document defines the scientific treatment classes for structural refactoring operations detected by RefactoringMiner. It establishes a principled boundary between operations that obscure a file/function's identity in version history (and thus likely break history-based PTS models) versus operations that merely restructure internal code without severing top-level linkage.

## 1. IDENTITY-CHANGING
Operations in this class directly modify the structural identifiers (names, locations, namespaces) used by predictive test selection algorithms to map historical test failures to modified source files or methods.

* **Rename Class**
  * **Treatment Class**: Identity-Changing
  * **Scientific Rationale**: Modifies the primary token used to link the class file to its corresponding test file in historical co-occurrence matrices.
  * **Affects File Identity**: YES (usually involves a file rename).
  * **Affects Path Identity**: YES.
  * **Affects Code-Test Historical Linkage**: HIGH impact.

* **Rename Method**
  * **Treatment Class**: Identity-Changing
  * **Scientific Rationale**: Method-level PTS techniques track failure history by method signature. Renaming severs this link.
  * **Affects File Identity**: NO.
  * **Affects Path Identity**: YES (at the method AST level).
  * **Affects Code-Test Historical Linkage**: HIGH impact.

* **Rename Variable / Rename Parameter**
  * **Treatment Class**: Identity-Changing (Sub-method level)
  * **Scientific Rationale**: Alters token distribution within a method, potentially shifting TF-IDF or CodeBERT embeddings used by advanced PTS features.
  * **Affects File Identity**: NO.
  * **Affects Path Identity**: NO.
  * **Affects Code-Test Historical Linkage**: MODERATE impact.

* **Move Class**
  * **Treatment Class**: Identity-Changing
  * **Scientific Rationale**: Changes the package structure and directory path of the source file. Path-based PTS models will treat this as a brand-new file with zero historical failure probability.
  * **Affects File Identity**: YES.
  * **Affects Path Identity**: YES.
  * **Affects Code-Test Historical Linkage**: HIGH impact.

* **Move Method / Move Attribute**
  * **Treatment Class**: Identity-Changing
  * **Scientific Rationale**: Relocates a method/attribute to a different class. The historical failures associated with the old class are decoupled from the moved method.
  * **Affects File Identity**: NO (but moves logic between two different file identities).
  * **Affects Path Identity**: YES.
  * **Affects Code-Test Historical Linkage**: HIGH impact.

* **Extract Class / Extract Subclass / Extract Superclass**
  * **Treatment Class**: Identity-Changing
  * **Scientific Rationale**: Creates a new structural identity (a new class) and moves existing logic into it. The new class has no failure history.
  * **Affects File Identity**: YES.
  * **Affects Path Identity**: YES.
  * **Affects Code-Test Historical Linkage**: HIGH impact.

## 2. IDENTITY-PRESERVING / OTHER STRUCTURAL
Operations in this class change the structure of the AST (e.g., adding annotations, extracting local variables, changing modifiers) but do not alter the primary identifiers (file name, class name, method signature) that link to test history.

* **Extract Variable / Inline Variable**
  * **Treatment Class**: Identity-Preserving
  * **Scientific Rationale**: Localized to the method body. Does not sever the method-to-test link.
  * **Affects File Identity**: NO.
  * **Affects Path Identity**: NO.
  * **Affects Code-Test Historical Linkage**: LOW impact.

* **Extract Method / Inline Method**
  * **Treatment Class**: Identity-Preserving (mostly)
  * **Scientific Rationale**: While it creates a new method signature (Extract), the newly extracted method is typically called from the original method (whose identity is preserved). The original test mapping often survives via the unchanged caller.
  * **Affects File Identity**: NO.
  * **Affects Path Identity**: PARTIAL (creates a new sub-path).
  * **Affects Code-Test Historical Linkage**: LOW to MODERATE impact.

* **Change Access Modifier (Class/Method/Attribute)**
  * **Treatment Class**: Identity-Preserving
  * **Scientific Rationale**: Alters visibility (e.g., public to private) but the AST node identifier remains exactly the same.
  * **Affects File Identity**: NO.
  * **Affects Path Identity**: NO.
  * **Affects Code-Test Historical Linkage**: LOW impact.

* **Change Return Type / Change Parameter Type / Change Variable Type**
  * **Treatment Class**: Identity-Preserving
  * **Scientific Rationale**: Modifies type definitions without renaming the entity.
  * **Affects File Identity**: NO.
  * **Affects Path Identity**: NO.
  * **Affects Code-Test Historical Linkage**: LOW impact.

* **Add / Remove Annotation**
  * **Treatment Class**: Identity-Preserving
  * **Scientific Rationale**: Modifies metadata.
  * **Affects File Identity**: NO.
  * **Affects Path Identity**: NO.
  * **Affects Code-Test Historical Linkage**: LOW impact.
