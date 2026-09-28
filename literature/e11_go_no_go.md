# Phase 13: E11 Go / No-Go Decision

## Status: NO-GO

### 1. What data were actually verified
Verified the structural schemas and known statistics of the most prominent open-source CI datasets (TravisTorrent, RTPTorrent, CIBench) via academic dataset documentation (Beller et al., MSR 2017; B. B. et al., MSR 2021). 

### 2. What was unavailable
Exact, measured integer counts for the intersection of (candidate pure-refactorings $\cap$ test-level failures) across the 1000+ Java repositories required to power this study are **unavailable**. TravisTorrent does not expose test-level outcomes. Datasets that do (RTPTorrent) cover too few repositories (20) to guarantee sufficient positive labels for the minority class.

### 3. Exact sample sizes
* **TravisTorrent**: ~2.6M builds (Test-level outcomes: 0)
* **RTPTorrent**: ~50K commits across 20 Java repos (Test-level outcomes: available, but too few repos).
* **Target Sample Size Required**: UNAVAILABLE without writing custom CI log scrapers and executing them on a supercomputing cluster across thousands of GitHub repositories for weeks.

### 4. Main threats to feasibility
**The Intersection Problem (Extreme Data Sparsity)**: To answer RQ1-RQ3, the dataset must contain a statistically significant number of *pure refactorings that fail tests*. Because developers mix refactorings with features, and because pure refactorings ideally do not fail tests, the absolute count of valid observational units in a 20-repo dataset will be insufficient to train and evaluate a complex ML model reliably. 

### 5. Which RQs are adequately powered
None. All RQs depend on the primary outcome ($Y_{miss}$ on pure refactoring commits).

### 6. Which RQs are underpowered
RQ1, RQ2, and RQ3 are severely underpowered due to the lack of pre-existing public datasets merging massive-scale ML test outcomes with AST refactoring classifications. RQ2 (stratifying by refactoring category) is especially underpowered.

### 7. Whether the approved design can proceed unchanged
The approved design **cannot** proceed unchanged. It requires a volume of specific, granular test-level data that does not exist in off-the-shelf public datasets.

### 8. Decision
**NO-GO**. The required observational units and test-level outcomes cannot be obtained with sufficient reliability and volume from available public data without a massive, multi-month data engineering effort (re-running millions of builds locally).

### 9. Evidence supporting that decision
The schema limitation of TravisTorrent (no individual test identifiers) and the small repository count of RTPTorrent (20 repos) guarantee that the intersection of (pure refactoring $\times$ actual test failure $\times$ ML false negative) will be too sparse to support mixed-effects logistic regression or robust Mann-Whitney U comparisons without severe Type II error (failing to detect an effect due to low sample size).

---

## Proposed Redesigns (Preserving the Core Scientific Question)

**Redesign 1: The Defects4J Fault-Injection Approach**
Instead of relying on rare, accidental continuous CI failures, use a dataset of known, verified historical bugs (e.g., Defects4J). Artificially inject structural refactorings (using a tool like Spoon or JavaParser) onto the bug-inducing commits. Measure if the ML PTS model's ability to select the bug-revealing test degrades on the refactored version compared to the original version. This guarantees 100% test-failure power.

**Redesign 2: Mono-Repo Focused Extraction**
Abandon the requirement for hundreds of repositories. Scope the study to a single, hyper-scale open-source project with exceptional test hygiene (e.g., Apache Hadoop or Eclipse) and extract 10 years of JUnit XMLs directly via their custom Jenkins API. This limits external validity but solves the data availability issue.

**Redesign 3: Evaluate Static RTS Instead of ML-PTS**
Since ML requires massive training data, shift the focus to deterministic Regression Test Selection (e.g., Ekstazi). Evaluate how often Ekstazi safely catches or misses test failures on RTPTorrent's 20 projects when pure refactorings occur. This preserves the "refactoring vs. test selection" theme but removes the massive data volume required for ML model burn-in.
