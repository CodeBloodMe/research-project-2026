# Phase 13E: Conditional Mechanism Model (E11)

This model delineates the hypothesized causal chain mapping a structural refactoring operation to a test-level missed regression in a history-based tabular PTS system. It explicitly distinguishes between refactorings that directly disrupt indexed history and those that merely generate code churn.

> **Note**: The arrows represent the *proposed mechanism* under study, not universally established causal facts.

```mermaid
flowchart TD
    A[Structural Refactoring Operation] --> B{Does it alter an identifier directly indexed by the PTS baseline?}
    
    B -->|YES (e.g., File/Class Rename)| C[Historical Representation Discontinuity]
    C --> D[Massive Feature Distribution Shift (Disrupted Historical Linkages)]
    
    B -->|NO (e.g., Local Variable Extract)| E[Primarily Code Churn / Secondary Feature Change]
    E --> F[Minor/Indirect Feature Distribution Shift]
    
    D --> G[Prediction Change in ML-PTS]
    F --> G
    
    G --> H[Test-Level Missed Failure]
```

## Model Explanation
1. **Structural Refactoring Operation**: Detected via RefactoringMiner.
2. **Direct Alteration Check**: Determines whether the operation acts on the `FILE/PATH` level (which is strictly utilized by the baseline) vs. the `METHOD`, `SIGNATURE`, or `LOCAL` level.
3. **Discontinuity vs. Churn**: Operations with direct exposure cause the historical link to break (discontinuity). Operations with indirect exposure simply register as modified lines (churn).
4. **Distribution Shift**: The magnitude of the shift in the input vector provided to the PTS model during inference.
5. **Prediction Change**: The resulting probability degradation from the PTS model.
6. **Missed Failure**: If the probability falls below the operating threshold for a test that will deterministically fail, a test-level miss occurs.
