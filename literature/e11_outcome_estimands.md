# Phase 14: Outcome Estimands (E11)

To prevent ambiguity, the outcomes are strictly defined mathematically based on the ML predictions $\hat{y}(d,t)$ (where $1$ means selected) and ground truth $y(d,t)$ (where $1$ means actual failure).

## 1. TestRecall (True Positive Rate)
For a specific commit $d$:
$$TestRecall(d) = \frac{\sum_{t \in T_d} I(\hat{y}(d,t) = 1 \text{ and } y(d,t) = 1)}{\sum_{t \in T_d} I(y(d,t) = 1)}$$
*Condition*: Defined only when there is at least one actually failing test in commit $d$.

## 2. FailureMissRate (Test-Level FNR)
$$FailureMissRate(d) = 1 - TestRecall(d)$$
*Definition*: The proportion of *actually failing tests* that the PTS model incorrectly chose to omit. (Evaluated exclusively among tests where $y=1$).

## 3. SelectionRate
$$SelectionRate(d) = \frac{\sum_{t \in T_d} I(\hat{y}(d,t) = 1)}{|T_d|}$$
*Definition*: The fraction of the total candidate test suite executed.

## 4. TestTimeSaved
$$TestTimeSaved(d) = \frac{\sum_{t \in T_d, \hat{y}(d,t) = 0} Duration(t)}{\sum_{t \in T_d} Duration(t)}$$
*Definition*: The percentage of the raw test execution time avoided by the PTS model. (If CIBench lacks test-level duration, SelectionRate acts as a proxy).

## 5. Build-level Regression Escape
A binary outcome $E_d \in \{0,1\}$ for the entire commit $d$:
$$E_d = 1 \iff \left( \sum_{t \in T_d} I(y(d,t)=1) > 0 \right) \text{ and } \left( \sum_{t \in T_d} I(\hat{y}(d,t)=1 \text{ and } y(d,t)=1) = 0 \right)$$
*Definition*: A build-level regression escape occurs if the commit contains at least one actual failing test, but the PTS model failed to select *any* failing test, resulting in a green CI build despite a real regression.
