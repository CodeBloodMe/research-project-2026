#!/usr/bin/env python3
"""
Phase 16D — E11 Empirical Data Gate

Fail-closed controller for the frozen E11 design.
This script performs only empirical-data integrity/adequacy checks.
It does NOT train, tune, evaluate, or import any ML model.

Exit code:
  0 = empirical gate PASS
  1 = empirical gate FAIL
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LIT = ROOT / "literature"

REQUIRED_FILES = {
    "eligibility": LIT / "e11_actual_project_eligibility.csv",
    "test_class": DATA / "e11_test_class_dataset.csv",
    "git_linkage": DATA / "e11_git_linkage_full.csv",
    "duplicate_sha": DATA / "e11_duplicate_sha_audit.csv",
    "parse_errors": DATA / "e11_test_parse_errors.csv",
    "rm_raw": DATA / "e11_refactoring_raw.csv",
    "rm_labels": DATA / "e11_refactoring_labels.csv",
}

EXPECTED_ELIGIBILITY_STATUSES = {"ELIGIBLE", "INELIGIBLE"}
REQUIRED_TEST_COLUMNS = {
    "project", "cibench_row", "commit_sha", "ci_build_id", "timestamp",
    "parent_sha", "test_class", "total_tests", "failed", "errors",
    "skipped", "executed_tests", "failure_positive", "duration_seconds",
}
REQUIRED_LINK_COLUMNS = {
    "project", "cibench_row", "commit_sha", "git_status", "timestamp",
    "parent_sha", "repository_url",
}
REQUIRED_RM_RAW_COLUMNS = {
    "project", "commit_sha", "parent_sha", "timestamp",
    "analysis_status", "refactoring_count",
}
REQUIRED_RM_LABEL_COLUMNS = {
    "project", "commit_sha", "REF_ONLY_or_REF_MIXED",
    "direct_exposure", "indirect_exposure",
}


def _safe_read_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception as exc:
        raise RuntimeError(f"Cannot parse {path}: {exc}") from exc


def _fail(checks: list[str], message: str) -> None:
    checks.append(f"FAIL: {message}")


def _pass(checks: list[str], message: str) -> None:
    checks.append(f"PASS: {message}")


def _normalise_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    # 1. Physical materialisation
    missing = [name for name, path in REQUIRED_FILES.items() if not path.is_file()]
    if missing:
        _fail(checks, "Required empirical artifacts missing: " + ", ".join(missing))
        failures.extend(missing)
        return _write_result(checks, failures)

    # 2. Eligibility population
    try:
        elig = _safe_read_csv(REQUIRED_FILES["eligibility"])
        missing_cols = {"project_identifier", "eligible_for_E11", "Java_status",
                        "E11_age_criterion", "E11_commit_history_criterion",
                        "E11_test_history_criterion"} - set(elig.columns)
        if missing_cols:
            _fail(checks, f"Eligibility schema missing columns: {sorted(missing_cols)}")
        else:
            if len(elig) != 100:
                _fail(checks, f"Eligibility table has {len(elig)} projects; frozen CIBench population is 100")
            else:
                _pass(checks, "Eligibility table covers exactly 100 CIBench projects")

            if elig["project_identifier"].duplicated().any():
                _fail(checks, "Eligibility table contains duplicate project identifiers")
            else:
                _pass(checks, "Eligibility project identifiers are unique")

            states = set(elig["eligible_for_E11"].dropna().astype(str))
            unexpected = states - EXPECTED_ELIGIBILITY_STATUSES
            if unexpected:
                _fail(checks, f"Eligibility contains unresolved/non-terminal statuses: {sorted(unexpected)}")
            else:
                _pass(checks, "Every project is terminally classified as ELIGIBLE or INELIGIBLE")

            eligible = elig[elig["eligible_for_E11"] == "ELIGIBLE"].copy()
            if len(eligible) == 0:
                _fail(checks, "No empirically eligible projects remain")
            else:
                _pass(checks, f"Non-empty analytical population: {len(eligible)} eligible projects")

            for col in [
                "Java_status", "E11_age_criterion",
                "E11_commit_history_criterion", "E11_test_history_criterion"
            ]:
                bad = eligible[eligible[col] != "PASS"]
                if len(bad):
                    _fail(checks, f"Eligible rows violate {col}: {len(bad)}")
                else:
                    _pass(checks, f"All eligible rows satisfy {col}")
    except Exception as exc:
        _fail(checks, str(exc))

    # Do not continue into derived-data claims when population validation failed.
    if failures or any(x.startswith("FAIL:") for x in checks):
        return _write_result(checks, failures)

    # 3. Derived empirical tables
    try:
        tests = _safe_read_csv(REQUIRED_FILES["test_class"])
        link = _safe_read_csv(REQUIRED_FILES["git_linkage"])
        dup = _safe_read_csv(REQUIRED_FILES["duplicate_sha"])
        parse_errors = _safe_read_csv(REQUIRED_FILES["parse_errors"])
        rm_raw = _safe_read_csv(REQUIRED_FILES["rm_raw"])
        rm_labels = _safe_read_csv(REQUIRED_FILES["rm_labels"])

        schemas = [
            ("test-class dataset", tests, REQUIRED_TEST_COLUMNS),
            ("Git linkage", link, REQUIRED_LINK_COLUMNS),
            ("RefactoringMiner raw", rm_raw, REQUIRED_RM_RAW_COLUMNS),
            ("RefactoringMiner labels", rm_labels, REQUIRED_RM_LABEL_COLUMNS),
        ]
        for name, frame, cols in schemas:
            missing = cols - set(frame.columns)
            if missing:
                _fail(checks, f"{name} schema missing columns: {sorted(missing)}")
            elif len(frame) == 0:
                _fail(checks, f"{name} is physically present but empty")
            else:
                _pass(checks, f"{name} is populated and schema-complete")

        if any(x.startswith("FAIL:") for x in checks):
            return _write_result(checks, failures)

        # 4. No placeholder/unknown analytical values
        placeholder_tokens = {"UNKNOWN", "pending", "PENDING", "UNVERIFIED"}
        for name, frame in [
            ("test-class dataset", tests),
            ("Git linkage", link),
            ("RefactoringMiner raw", rm_raw),
            ("RefactoringMiner labels", rm_labels),
        ]:
            found = set()
            for col in frame.columns:
                if frame[col].dtype == object:
                    vals = set(frame[col].dropna().astype(str))
                    found |= vals & placeholder_tokens
            if found:
                _fail(checks, f"{name} contains placeholder values: {sorted(found)}")
            else:
                _pass(checks, f"{name} contains no placeholder analytical values")

        # 5. Git linkage integrity
        found_link = link[link["git_status"] == "FOUND"].copy()
        missing_link = link[link["git_status"] != "FOUND"]
        if len(missing_link):
            _fail(checks, f"{len(missing_link)} build rows are not Git-linked to a verified commit")
        else:
            _pass(checks, "All synthesized build rows link to Git commits")

        if len(found_link):
            for col in ["timestamp", "parent_sha"]:
                if found_link[col].isna().any():
                    _fail(checks, f"Git linkage has missing {col} values")
            bad_ts = pd.to_numeric(found_link["timestamp"], errors="coerce").isna()
            if bad_ts.any():
                _fail(checks, f"Git linkage has {int(bad_ts.sum())} non-numeric timestamps")
            else:
                _pass(checks, "Git timestamps are numeric for all linked builds")

        # 6. Test outcome semantics
        numeric_cols = ["total_tests", "failed", "errors", "skipped", "executed_tests"]
        for col in numeric_cols:
            if pd.to_numeric(tests[col], errors="coerce").isna().any():
                _fail(checks, f"Non-numeric values found in test column {col}")

        expected_failure = pd.to_numeric(tests["failed"], errors="coerce") > 0
        observed_failure = tests["failure_positive"].map(_normalise_bool)
        if not (expected_failure.reset_index(drop=True) == observed_failure.reset_index(drop=True)).all():
            _fail(checks, "failure_positive is inconsistent with failed > 0")
        else:
            _pass(checks, "Ground-truth failure semantics match failed > 0")

        # 7. Commit-level refactoring labeling
        raw_status = set(rm_raw["analysis_status"].astype(str))
        errors = sorted(x for x in raw_status if x.startswith("ERROR"))
        if errors:
            _fail(checks, f"RefactoringMiner contains error statuses: {errors}")
        else:
            _pass(checks, "No RefactoringMiner execution errors remain")

        valid_labels = {"NON_REF", "REF_ONLY", "REF_MIXED"}
        label_values = set(rm_labels["REF_ONLY_or_REF_MIXED"].astype(str))
        unexpected_labels = label_values - valid_labels
        if unexpected_labels:
            _fail(checks, f"Unexpected refactoring labels: {sorted(unexpected_labels)}")
        else:
            _pass(checks, "Refactoring labels are restricted to NON_REF/REF_ONLY/REF_MIXED")

        key_cols = ["project", "commit_sha"]
        if rm_labels.duplicated(key_cols).any():
            _fail(checks, "Refactoring label table contains duplicate project/commit keys")
        else:
            _pass(checks, "Refactoring labels are unique at project/commit level")

        # 8. Treatment/control support and empirical failure support
        eligible_projects = set(
            elig.loc[elig["eligible_for_E11"] == "ELIGIBLE", "project_identifier"]
        )
        linked_projects = set(link["project"].astype(str))
        if not linked_projects <= eligible_projects:
            _fail(checks, "Derived build data contains projects outside the verified E11 population")
        else:
            _pass(checks, "Derived build data is bounded by the verified E11 population")

        joined = tests.merge(
            rm_labels[key_cols + ["REF_ONLY_or_REF_MIXED", "direct_exposure", "indirect_exposure"]],
            on=key_cols,
            how="inner",
            validate="many_to_one",
        )
        if len(joined) == 0:
            _fail(checks, "No test observations link to labeled commits")
        else:
            _pass(checks, f"{len(joined)} test observations link to refactoring labels")

        failing = joined[joined["failure_positive"].map(_normalise_bool)]
        control = failing[failing["REF_ONLY_or_REF_MIXED"] == "NON_REF"]
        treatment = failing[failing["REF_ONLY_or_REF_MIXED"] == "REF_MIXED"]

        if len(control) == 0:
            _fail(checks, "No failure-positive NON_REF observations exist")
        else:
            _pass(checks, f"Failure-positive NON_REF observations: {len(control)}")

        if len(treatment) == 0:
            _fail(checks, "No failure-positive REF_MIXED observations exist")
        else:
            _pass(checks, f"Failure-positive REF_MIXED observations: {len(treatment)}")

        direct_fail = failing[failing["direct_exposure"].map(_normalise_bool)]
        if len(direct_fail) == 0:
            _fail(checks, "No direct-exposure failure-positive observations exist; RQ2/RQ3 subset is empty")
        else:
            _pass(checks, f"Direct-exposure failure-positive observations: {len(direct_fail)}")

        # 9. Parse errors are evidence, not something to silently hide.
        if len(parse_errors):
            _fail(checks, f"Parser error table contains {len(parse_errors)} rows; gate remains closed until resolved/explicitly excluded")
        else:
            _pass(checks, "No parser-error rows remain")

        # 10. Basic hierarchy support, without fitting an ML model.
        repo_n = tests["project"].nunique()
        commit_n = tests[["project", "commit_sha"]].drop_duplicates().shape[0]
        build_n = tests[["project", "cibench_row"]].drop_duplicates().shape[0]
        test_n = len(tests)
        if repo_n < 2:
            _fail(checks, f"Only {repo_n} repositories in test data; hierarchical analysis is not supported")
        else:
            _pass(checks, f"Repository clusters present: {repo_n}")

        if commit_n == 0 or build_n == 0 or test_n == 0:
            _fail(checks, "One or more empirical hierarchy levels are empty")
        else:
            _pass(checks, f"Hierarchy populated: {repo_n} repositories / {commit_n} commits / {build_n} builds / {test_n} test rows")

        # 11. Do not turn this into a power conclusion.
        _pass(checks, "No statistical power conclusion is inferred by this gate; power remains a separate empirical analysis")

    except Exception as exc:
        _fail(checks, f"Derived-data audit error: {exc}")

    return _write_result(checks, failures)


def _write_result(checks: list[str], failures: list[str]) -> int:
    failed = [x for x in checks if x.startswith("FAIL:")]
    passed = [x for x in checks if x.startswith("PASS:")]
    gate_pass = len(failed) == 0

    report_lines = [
        "# Phase 16D: Empirical Data Gate",
        "",
        f"**Decision: {'PASS' if gate_pass else 'FAIL'}**",
        "",
        "This gate is fail-closed. It does not train, tune, evaluate, or import an ML model.",
        "",
        "## Checks",
        "",
        *checks,
        "",
        "## Enforcement",
        "",
        "- ML/model work remains blocked while this decision is FAIL.",
        "- A PASS requires physically materialized empirical artifacts with no unresolved placeholders, parser errors, Git-link failures, or refactoring-analysis errors.",
        "- A PASS is not a claim of statistical power; power is evaluated separately from the materialized empirical counts.",
        "",
    ]

    LIT.mkdir(parents=True, exist_ok=True)
    (LIT / "e11_phase16d_empirical_gate.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Phase 16D empirical gate: {'PASS' if gate_pass else 'FAIL'}")
    for line in passed:
        print(line)
    for line in failed:
        print(line)

    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
