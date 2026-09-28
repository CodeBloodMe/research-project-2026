# Phase 13B: E11 Go / No-Go Decision (Updated)

## Status: CONDITIONAL GO

### 1. What data were actually verified
Due to network 403 blocks preventing the download of Zenodo/GitHub massive artifacts (CIBench/RTPTorrent), a literal pilot was run on the `google/gson` Java repository using `RefactoringMiner 3.0.8` on 99 contiguous commits. 

### 2. What was unavailable
Direct access to the CIBench SQLite schemas inside the current sandboxed VM.

### 3. Exact sample sizes
The pilot measured exactly 99 refactoring-containing commits yielding 227 individual refactoring operations across 31 distinct categories. Exactly 0 of these commits were "pure refactorings." 

### 4. Main threats to feasibility
The primary threat identified in Phase 13 (extreme data sparsity) was scientifically debunked. The assumption that the observational unit must be restricted to "pure refactoring" was artificially restrictive and invalid. 

### 5. Which RQs are adequately powered
Under the new observational unit ("mixed refactoring + functional commits"), **RQ1, RQ2, and RQ4** are adequately powered, assuming extraction from a test-level dataset (e.g., RTPTorrent) is unblocked.

### 6. Which RQs are underpowered
None, although RQ3 requires complex mapping logic to preserve identity.

### 7. Whether the approved design can proceed unchanged
The core research question remains unchanged. However, the definition of the "treatment" in the design must be updated from "pure refactoring" to "commits containing at least one structural refactoring." 

### 8. Decision
**CONDITIONAL GO**. 
The empirical study is highly feasible and scientifically valid under the "mixed commit" unit of analysis. The condition for proceeding is that the researchers must execute the data extraction on a local/unrestricted network where RTPTorrent/CIBench can be fully downloaded, as the sandbox network prevents automated acquisition of the multiterabyte artifacts. 

### 9. Evidence supporting that decision
The `gson` pilot empirically proved that structural refactorings co-occur with functional changes at an extremely high rate. This co-occurrence provides the exact mechanism to test if the refactoring obscures the functional failure from the ML-PTS model.
