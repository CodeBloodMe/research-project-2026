# Phase 13: Data Sources Census

## 1. TravisTorrent
* **URL/DOI**: 10.1109/MSR.2017.24 (Beller et al., 2017)
* **Time Period**: 2011–2017
* **Repositories**: 1,283 (Ruby and Java)
* **Commits/Builds**: ~2.6 million builds
* **Individual test outcomes available?**: **NO**. The schema provides `tr_tests_ran`, `tr_tests_failed`, `tr_tests_errored`, `tr_tests_skipped`, but does not provide individual test names or binary pass/fail statuses for specific test cases.
* **Commit SHA available?**: YES
* **Build outcome available?**: YES (passed, failed, errored, canceled)
* **Changed-file information available?**: YES (via GitHub API linking)
* **Test-level outcomes recoverable?**: NO, without re-running the build or scraping archived raw text logs with regex (highly error-prone).
* **Licensing**: Creative Commons
* **Preprocessing**: Joined Travis CI API data with GitHub GHTorrent data.

## 2. RTPTorrent
* **URL/DOI**: 10.1145/3468264.3473140 (B. B. et al., 2021)
* **Time Period**: Up to 2020
* **Repositories**: 20 (Java only)
* **Commits/Builds**: ~50,000 commits
* **Individual test outcomes available?**: **YES**. Extracted from Travis CI logs and Maven Surefire reports.
* **Commit SHA available?**: YES
* **Build outcome available?**: YES
* **Changed-file information available?**: YES
* **Licensing**: Open Access
* **Preprocessing**: Specifically built for Regression Test Prioritization (RTP). Contains parsed test execution times and outcomes.

## 3. CIBench
* **URL/DOI**: 10.1145/3540250.3549094 (2022)
* **Repositories**: ~10 Java projects (specifically curated for CI testing).
* **Individual test outcomes available?**: **YES**.
* **Commit SHA available?**: YES
* **Changed-file information available?**: YES

## Conclusion on Population Criteria
The target population is "mature open-source Java projects with >5000 commits and individual test outcomes."
* **TravisTorrent** has the volume but lacks the schema (no test-level data).
* **RTPTorrent and CIBench** have the schema but lack the volume (only 10-20 repositories, many with <5000 commits).
* Extracting this data from scratch across 100+ GitHub repositories requires re-executing millions of Maven test suites locally to generate JUnit XMLs, which is computationally prohibitive.
