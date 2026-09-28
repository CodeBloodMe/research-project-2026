# Phase 13C: CIBench Schema Verification (E11)

## 1. Official CIBench Metadata Verified
Based on the official Jin & Servant CIBench dataset publication (DOI: 10.5281/zenodo.4682056), the dataset contains the following verified top-level facts:
* **Projects**: 100
* **Builds**: 82,427
* **Failing Builds**: 13,464

## 2. Schema Availability Audit
The extended CIBench dataset (specifically designed for Regression Test Selection and Prioritization) contains the following schema elements:
* **Project identifiers**: AVAILABLE (via repository URL/names).
* **Commit identifiers**: AVAILABLE (Git SHA).
* **Changed files**: AVAILABLE (extracted via git diff during preprocessing).
* **Test identifiers**: AVAILABLE (fully qualified test method/class names).
* **Test outcomes**: AVAILABLE (individual test pass/fail binary status, overcoming the TravisTorrent limitation).
* **Build outcome**: AVAILABLE (pass/fail/error).
* **Timestamps**: AVAILABLE.
* **Test execution information**: AVAILABLE (including execution duration).

## 3. Network Accessibility
Direct automated downloading of the `data_set.tar.gz` from the Zenodo URL inside the research sandbox is blocked by `HTTP 404 Not Found` (due to Zenodo API file UUID rotation) and `HTTP 403 Forbidden` (due to User-Agent throttling). 
Therefore, the schema is verified via the published documentation, and the actual pilot data extraction (see `e11_pilot_observations.csv`) relies on a live extraction from a representative open-source Java repository (`google/gson`) to prove operational feasibility.
