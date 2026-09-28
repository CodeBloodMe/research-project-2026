# Phase 14B: Outcome Analysis Specification (E11)

## 1. Core Variables
For every commit $d$ and test execution $t$ in the candidate test universe:

* **Failure Occurrence ($y(d,t)$)**: 
  $y(d,t) = 1$ if test $t$ actually failed during the CI execution of commit $d$, otherwise $y(d,t) = 0$.

* **PTS Selection ($s(d,t)$)**:
  $s(d,t) = 1$ if the PTS model selects test $t$ for execution, otherwise $s(d,t) = 0$.

* **Test-Level Miss ($m(d,t)$)**:
  $m(d,t) = 1$ iff $y(d,t) = 1$ AND $s(d,t) = 0$.
  $m(d,t) = 0$ iff $y(d,t) = 1$ AND $s(d,t) = 1$.
  $m(d,t)$ is **UNDEFINED** for passing tests ($y(d,t) = 0$).

## 2. Analysis Population
* **Primary Miss Analysis**: The primary statistical models (for RQ1, RQ2, RQ3) evaluating the `FailureMissRate` are computed **strictly conditional on $y(d,t) = 1$**. Only rows representing actual failing test instances enter this primary regression.
* **Secondary Analyses**: Passing tests ($y=0$) are used only to evaluate the secondary `SelectionRate` and `TestTimeSaved` outcomes, and to calibrate the PTS model threshold.

## 3. Secondary Build-Level Outcome
* **Build-level Regression Escape ($E_d$)**:
  $E_d = 1$ iff $\sum y(d,t) > 0$ AND $\sum (y(d,t) \times s(d,t)) = 0$.
  This represents a commit where a real regression occurred, but no selected test caught it. This is a separate, commit-level aggregation and must not be conflated with the primary test-level $m(d,t)$ estimand.
