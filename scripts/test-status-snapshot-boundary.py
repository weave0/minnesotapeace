#!/usr/bin/env python3
"""Hostile-case regression tests for scripts/build-status-snapshot.py.

Plants deliberately broken fixture claims/sources (missing source, non-primary
source, wrong evidence_class, malformed value/date, unresolved duplicate-active
records) and confirms the generator refuses to run rather than silently emitting
a wrong or unsupported number. Also confirms the freshness checker catches a
direct hand-edit of a generated value, and that the generator's own code never
combines the three metrics arithmetically.

Every fixture is planted under research/claims/ or research/sources/ with a
distinctive zz-test- prefix and removed in a finally block; status/index.html
is snapshotted and restored around every case. This script makes no permanent
changes regardless of pass/fail.

Run from repo root:  python3 scripts/test-status-snapshot-boundary.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-status-snapshot.py"
GENERATOR_SRC = BUILD_SCRIPT.read_text(encoding="utf-8")
STATUS_HTML = ROOT / "status" / "index.html"

failures: list[str] = []


def note(ok: bool, label: str) -> None:
    print(("PASS" if ok else "FAIL") + " -- " + label)
    if not ok:
        failures.append(label)


def run_generator() -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)], cwd=ROOT, capture_output=True, text=True
    )


def base_fixture_source(**overrides) -> dict:
    src = {
        "source_id": "zz-test-fixture-source",
        "canonical_url": "https://www.justice.gov/usao-mn/pr/zz-test-fixture",
        "issuing_body": "U.S. Attorney's Office, District of Minnesota",
        "title": "ZZ Test Fixture: 999th Defendant Charged in Feeding Our Future Fraud Scheme",
        "publication_date": "2026-01-01",
        "retrieval_date": "2026-01-01",
        "document_type": "press_release",
        "jurisdiction": "D. Minn.",
        "source_tier": 3,
        "source_status": "PRIMARY_GOVERNMENT_RELEASE",
        "evidence_class": "CHARGED_ALLEGED",
        "supports": ["USAO-MN identifies a fixture defendant as the 999th defendant charged."],
    }
    src.update(overrides)
    return src


def base_fixture_claim(**overrides) -> dict:
    claim = {
        "claim_id": "zz-test-fixture-claim",
        "claim_text": "Fixture claim for hostile testing.",
        "claim_type": "COUNT",
        "measurement_type": "OFFICIAL_ORDINAL_MILESTONE",
        "metric_id": "fof-charged-count",
        "metric_value": 999,
        "evidence_class": "CHARGED_ALLEGED",
        "status": "CHARGED",
        "confidence": "VERY_HIGH",
        "is_allegation": False,
        "is_inference": False,
        "event_date": "2026-01-01",
        "source_ids": ["zz-test-fixture-source"],
        "supporting_passages": [
            {"source_id": "zz-test-fixture-source", "quote": "the 999th defendant charged", "locator": "fixture"}
        ],
        "qualifiers": [],
        "public_label": "fixture label",
        "public_explanation": "fixture explanation",
        "public_source_label": "fixture release →",
        "last_swept_for_supersession": "2026-01-01",
        "valid_from": "2026-01-01T00:00:00Z",
        "valid_until": None,
        "superseded_by": None,
        "reviewed_at": "2026-01-01T00:00:00Z",
    }
    claim.update(overrides)
    return claim


def main() -> int:
    print("Each case below calls the generator's own validate_metric/resolve_active_claim")
    print("functions directly against a fixture claim using a private metric_id ('fixture-")
    print("metric') that the real corpus never uses, so no case can collide with or be")
    print("masked by the real charged/convicted/sentenced claims.\n")

    # importlib can't import a hyphenated filename as a plain module path; load it
    # directly from its file location instead.
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_status_snapshot", BUILD_SCRIPT)
    bss = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bss)  # type: ignore[union-attr]

    def validate_one(claim: dict, source: dict, metric_id="fixture-metric", expected_evidence_class="CHARGED_ALLEGED", stage_word="charged"):
        claims_by_metric = {metric_id: [claim]}
        sources = {source["source_id"]: source}
        return bss.validate_metric(metric_id, expected_evidence_class, stage_word, claims_by_metric, sources)

    # 1. Missing source record entirely.
    try:
        validate_one(
            base_fixture_claim(metric_id="fixture-metric", source_ids=["zz-nonexistent-source"]),
            base_fixture_source(),
        )
        note(False, "missing source record is rejected")
    except SystemExit as e:
        note("does not exist" in str(e), "missing source record is rejected")

    # 2. Source is not an admitted primary source (journalism tier).
    try:
        validate_one(
            base_fixture_claim(metric_id="fixture-metric"),
            base_fixture_source(source_tier=8, source_status="REPUTABLE_JOURNALISM"),
        )
        note(False, "non-primary (journalism) source is rejected")
    except SystemExit as e:
        note("not an admitted primary source" in str(e), "non-primary (journalism) source is rejected")

    # 3. evidence_class mismatch (source/claim says ADJUDICATED but metric expects CHARGED_ALLEGED).
    try:
        validate_one(
            base_fixture_claim(metric_id="fixture-metric", evidence_class="ADJUDICATED"),
            base_fixture_source(),
        )
        note(False, "evidence_class/procedural-stage mismatch is rejected")
    except SystemExit as e:
        note("procedural stage" in str(e), "evidence_class/procedural-stage mismatch is rejected")

    # 4. metric_value doesn't match what the source text actually says (999 claimed, source says 1st).
    try:
        validate_one(
            base_fixture_claim(metric_id="fixture-metric", metric_value=42),
            base_fixture_source(),
        )
        note(False, "metric_value unsupported by source text is rejected")
    except SystemExit as e:
        note("does not appear to support" in str(e), "metric_value unsupported by source text is rejected")

    # 5. Malformed metric_value (not a positive integer).
    try:
        validate_one(base_fixture_claim(metric_id="fixture-metric", metric_value="seventy-eight"), base_fixture_source())
        note(False, "non-numeric metric_value is rejected")
    except SystemExit as e:
        note("not a positive integer" in str(e), "non-numeric metric_value is rejected")

    try:
        validate_one(base_fixture_claim(metric_id="fixture-metric", metric_value=-5), base_fixture_source())
        note(False, "negative metric_value is rejected")
    except SystemExit as e:
        note("not a positive integer" in str(e), "negative metric_value is rejected")

    # 6. Malformed event_date.
    try:
        validate_one(base_fixture_claim(metric_id="fixture-metric", event_date="2026-13-40"), base_fixture_source())
        note(False, "malformed calendar date is rejected")
    except SystemExit as e:
        note("malformed" in str(e), "malformed calendar date is rejected")

    try:
        validate_one(base_fixture_claim(metric_id="fixture-metric", event_date="not-a-date"), base_fixture_source())
        note(False, "non-date event_date string is rejected")
    except SystemExit as e:
        note("malformed" in str(e), "non-date event_date string is rejected")

    # 7. measurement_type not set to the sentinel even though metric_id is present.
    try:
        validate_one(base_fixture_claim(metric_id="fixture-metric", measurement_type=None), base_fixture_source())
        note(False, "metric_id without measurement_type sentinel is rejected")
    except SystemExit as e:
        note("measurement_type" in str(e), "metric_id without measurement_type sentinel is rejected")

    # 8. Missing public-facing fields.
    try:
        validate_one(base_fixture_claim(metric_id="fixture-metric", public_label=""), base_fixture_source())
        note(False, "empty public_label is rejected")
    except SystemExit as e:
        note("public_label" in str(e), "empty public_label is rejected")

    # 9. Two active claims for the same metric_id, no supersession chain -> ambiguous.
    try:
        claims_by_metric = {
            "fixture-metric": [
                base_fixture_claim(claim_id="zz-a", metric_id="fixture-metric"),
                base_fixture_claim(claim_id="zz-b", metric_id="fixture-metric"),
            ]
        }
        bss.resolve_active_claim("fixture-metric", claims_by_metric["fixture-metric"])
        note(False, "two unresolved active claims for one metric are rejected")
    except SystemExit as e:
        note("no resolving supersession chain" in str(e), "two unresolved active claims for one metric are rejected")

    # 10. Two claims, one properly superseded (valid_until set + superseded_by) -> resolves cleanly.
    old = base_fixture_claim(claim_id="zz-old", metric_id="fixture-metric", valid_until="2026-01-02T00:00:00Z", superseded_by="zz-new")
    new = base_fixture_claim(claim_id="zz-new", metric_id="fixture-metric")
    resolved = bss.resolve_active_claim("fixture-metric", [old, new])
    note(resolved["claim_id"] == "zz-new", "a properly superseded old claim does not block resolution")

    # 11. Zero claims for a metric -> "lacks a source record".
    try:
        bss.resolve_active_claim("fixture-metric", [])
        note(False, "a metric with zero claims is rejected")
    except SystemExit as e:
        note("lacks a source record" in str(e), "a metric with zero claims is rejected")

    # 12. Structural: the generator's own source code never adds/subtracts metric values
    #     across different metrics (the "do not calculate 28 by adding two to 26" rule).
    #     Look for any arithmetic operator applied to something referencing metric_value
    #     or the per-metric result dicts, outside of this comment/docstring text itself.
    arithmetic_on_metrics = re.search(
        r'r\[["\']value["\']\]\s*[+\-]|result\[.*\]\s*[+\-]\s*result|value\s*\+\s*value|\bsum\(',
        GENERATOR_SRC,
    )
    note(arithmetic_on_metrics is None, "generator source contains no arithmetic combining metric values")

    # 13. Hand-edit drift detection: change a rendered number directly in status/index.html
    #     without touching any canonical record, then confirm the freshness checker (not
    #     just the generator) flags it.
    committed = STATUS_HTML.read_text(encoding="utf-8")
    try:
        tampered = committed.replace('<p class="snapshot-value">78</p>', '<p class="snapshot-value">79</p>', 1)
        if tampered == committed:
            note(False, "hand-edited snapshot value is caught by the freshness checker (setup failed to tamper)")
        else:
            STATUS_HTML.write_text(tampered, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "check-status-snapshot-fresh.py")],
                cwd=ROOT, capture_output=True, text=True,
            )
            note(result.returncode != 0, "hand-edited snapshot value is caught by the freshness checker")
    finally:
        STATUS_HTML.write_text(committed, encoding="utf-8")

    # 14. Happy path sanity: the real, committed claims still validate end to end.
    result = run_generator()
    note(result.returncode == 0, "the real committed claims still build successfully (sanity check)")
    # Restore in case the real generator run above changed anything (it shouldn't,
    # since the committed file already matches a fresh build, but be defensive).
    STATUS_HTML.write_text(committed, encoding="utf-8")

    if failures:
        print(f"\n{len(failures)} hostile-case check(s) failed:")
        for f in failures:
            print(" -", f)
        return 1
    print("\nAll status-snapshot hostile-case checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
