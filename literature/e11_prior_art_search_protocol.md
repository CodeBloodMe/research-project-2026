# Phase 14B: Prior Art Search Protocol (E11)

## 1. Objective
To systematically verify the novelty claim that the specific intersection of history-based ML-PTS and structural code refactoring is underexplored.

## 2. Methodology
* **Databases/Search Engines**: Google Scholar, Semantic Scholar, OpenAlex, ACM Digital Library, IEEE Xplore, arXiv.
* **Date of Final Search**: September 2026.
* **Date Cutoff**: 2015 to 2026 (Modern ML-PTS era).
* **Exact Query Families**:
  - `("predictive test selection" OR "machine learning test selection") AND "refactoring"`
  - `"predictive test selection" AND ("code evolution" OR "structural change")`
  - `("regression test selection" OR "RTS") AND "machine learning" AND "refactoring"`
  - `"test selection" AND ("rename" OR "move method" OR "file rename") AND "continuous integration"`

## 3. Screening Procedure
1. **Deduplication**: Exact matches on title and DOI merged.
2. **Title/Abstract Screening**: Exclude papers not dealing with test selection, prioritization, or CI ML models.
3. **Full-Text Screening**: Retain papers that evaluate an ML model on CI histories.
4. **Data Extraction**: Extract the baseline model type (e.g., historical vs static), whether refactoring was isolated, and if empirical miss rates on refactored commits were calculated.

## 4. Closest Prior Art Summary
(See `e11_prior_art_matrix.csv` for the full table).
* **Machalica et al. (2019)**: Defines the PTS baseline; does not isolate structural refactoring disruption.
* **Wang et al. (2021)**: Re-evaluates ML-PTS broadly; does not isolate refactoring exposure.
* **Fazlalizadeh et al. (2009)**: Evaluates refactoring test prioritization; uses static heuristics, not ML CI histories.

## 5. Novelty Status
The specific mechanism of historical index disruption via identity-altering refactoring in ML-PTS remains **underexplored**. We make no claims of being the "first" or that the area is "unexplored entirely."
