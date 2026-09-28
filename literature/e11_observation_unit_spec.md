# Phase 14: Observation Unit Specification (E11)

## 1. Machine Learning Example
The fundamental unit of observation in the dataset is a **(commit, test)** pair. 

Let $d$ be a specific commit (change) triggered in Continuous Integration.
Let $t$ be a specific test case within the candidate test universe for that repository.

* **$x(d,t)$**: The feature vector representing the historical state of test $t$, the properties of commit $d$, and the historical correlation between the files changed in $d$ and the test $t$.
* **$y(d,t)$**: The ground-truth outcome label. $y(d,t) = 1$ if test $t$ deterministically failed when executed on the code at commit $d$; otherwise $y(d,t) = 0$.

## 2. Candidate Test Universe
Because E11 does not rely on a perfect static dependency graph (which cannot be reliably extracted from public CIBench data for all languages), the candidate test universe $T_d$ for a commit $d$ is defined as **all tests that were executed and recorded by CIBench during the CI build for commit $d$**. 

* **Deviation from Machalica**: Machalica restricts the candidate set using internal Buck dependency targets. E11 uses the empirical execution set provided by CIBench. 
* **Justification**: CIBench guarantees that these tests were run and that their pass/fail outcomes are known. Tests not executed in the CIBench history for that build are implicitly excluded, as their ground-truth $y$ label is unknown.
