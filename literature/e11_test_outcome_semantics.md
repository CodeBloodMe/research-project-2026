# Phase 15B: Test Outcome Semantics Audit

This document describes the exact empirical semantics of the CIBench `test_info_logs` based on physical inspection of the Zenodo artifact.

## Physical Representation
- **One CSV per CI Build**: A single CSV file inside `test_info_logs/[project]/` (e.g., `1.csv`) corresponds to exactly one CI build. The file name integer matches the 1-indexed row number in the project's `Abdalkareem19_git_result` CSV.
- **Test Class Aggregation**: Each row in the CSV represents a **Test Class** (e.g., `com.squareup.okhttp.internal.http.URLConnectionTest`), NOT an individual test method.

## Column Semantics
Based on empirical samples (e.g., `okhtt,libcore.net.http.URLConnectionTest,113,N/A,1,0,0,6.082`):
1. **Project Prefix**: A string prefix indicating the project or module (e.g., `okhtt`).
2. **Test Class Name**: The fully qualified Java class name of the test suite.
3. **Total Tests**: An integer representing the total number of test methods within this test class.
4. **Unused / N/A**: Consistently recorded as `N/A`.
5. **Failed Tests**: An integer count of tests in the class that failed (assertion failures).
6. **Errored Tests**: An integer count of tests in the class that threw unexpected exceptions/errors.
7. **Skipped Tests**: An integer count of tests in the class that were skipped or explicitly unexecuted (e.g., `@Ignore`).
8. **Duration**: Execution time of the test class in seconds.

## Discoveries & Implications
- **Individual Test Identification is Impossible**: The dataset aggregates outcomes at the **Test Class** level. It is impossible to identify exactly which individual test method failed if a class contains multiple methods and `Failed=1`.
- **Machalica19 Aggregation**: The `Machalica19_git_result` data matches this aggregation perfectly. `failure_status = 1.0` means at least one test in the class failed/errored. The ML model is fundamentally a **Test-Class Selection Model**, not an individual test selection model.
- **Outcomes are Mutually Exclusive**: `Passed` tests are not explicitly recorded, but can be deterministically inferred as `Passed = Total - (Failed + Errors + Skipped)`.
- **Skipped Representation**: Skipped tests are explicitly represented as a count. These can be excluded from the effective "candidate universe" (as they were not run and cannot fail).
