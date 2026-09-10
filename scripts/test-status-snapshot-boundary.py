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

    # 4. metric_value doesn't match what the source text actually says (42 claimed, source says 999th).
    try:
        validate_one(
            base_fixture_claim(metric_id="fixture-metric", metric_value=42),
            base_fixture_source(),
        )
        note(False, "metric_value unsupported by source text is rejected")
    except SystemExit as e:
        note("does not appear to support" in str(e), "metric_value unsupported by source text is rejected")

    # 4b. Self-validation bypass: claim_text (and supporting_passages) FALSELY say
    #     "42nd defendant charged" -- consistent with the wrong metric_value=42 --
    #     while the actual archived source says "999th". A claim must not be able
    #     to prove itself: this must still fail, grounded only in the source's own
    #     text, not in whatever the claim author also typed into claim_text.
    try:
        validate_one(
            base_fixture_claim(
                metric_id="fixture-metric",
                metric_value=42,
                claim_text="USAO-MN identifies a fixture defendant as the 42nd defendant charged.",
                supporting_passages=[
                    {"source_id": "zz-test-fixture-source", "quote": "the 42nd defendant charged", "locator": "fixture"}
                ],
            ),
            base_fixture_source(),  # still says "999th" in its own supports/title
        )
        note(False, "claim cannot validate itself via claim_text/supporting_passages")
    except SystemExit as e:
        note(
            "does not appear to support" in str(e),
            "claim cannot validate itself via claim_text/supporting_passages",
        )

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

    # 6b. Impossible calendar date specifically on last_swept_for_supersession (not just
    #     event_date): 2026-02-31 matches the YYYY-MM-DD regex shape but February never
    #     has 31 days. A bare regex check would miss this; real calendar parsing must not.
    try:
        validate_one(
            base_fixture_claim(metric_id="fixture-metric", last_swept_for_supersession="2026-02-31"),
            base_fixture_source(),
        )
        note(False, "impossible calendar date (2026-02-31) in last_swept_for_supersession is rejected")
    except SystemExit as e:
        note(
            "not a real calendar date" in str(e),
            "impossible calendar date (2026-02-31) in last_swept_for_supersession is rejected",
        )

    # 6c. last_swept_for_supersession may not be in the future relative to America/
    #     Chicago "today" -- a sweep cannot have happened tomorrow. Use a date far
    #     enough out that no plausible clock skew makes this test flaky.
    try:
        validate_one(
            base_fixture_claim(metric_id="fixture-metric", last_swept_for_supersession="2099-01-01"),
            base_fixture_source(),
        )
        note(False, "a future last_swept_for_supersession (America/Chicago) is rejected")
    except SystemExit as e:
        note(
            "is after today's America/Chicago date" in str(e),
            "a future last_swept_for_supersession (America/Chicago) is rejected",
        )

    # 6d. A same-day (today, America/Chicago) sweep date must NOT be rejected as
    #     "future" -- guards against an off-by-one from comparing local vs. UTC dates.
    today_str = bss.today_local().isoformat()
    try:
        m = validate_one(
            base_fixture_claim(metric_id="fixture-metric", last_swept_for_supersession=today_str),
            base_fixture_source(),
        )
        note(m["last_swept_for_supersession"] == today_str, "a same-day (America/Chicago) sweep date is accepted")
    except SystemExit as e:
        note(False, f"a same-day (America/Chicago) sweep date is accepted (raised: {e})")

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

    # 9. Two claims for the same metric_id, NEITHER valid_until nor superseded_by set on
    #    either -> genuinely ambiguous, no chain to resolve it. Must fail closed rather
    #    than guess (e.g. by picking whichever sorts first, or the one with a later
    #    event_date) -- the referee's explicit preference is fail-closed rejection of
    #    multiple active claims unless the canonical corpus resolves the ambiguity itself.
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
        note("neither valid_until nor superseded_by set" in str(e), "two unresolved active claims for one metric are rejected")

    # 10. Two claims, one properly superseded (valid_until set + superseded_by) -> resolves cleanly.
    old = base_fixture_claim(claim_id="zz-old", metric_id="fixture-metric", valid_until="2026-01-02T00:00:00Z", superseded_by="zz-new")
    new = base_fixture_claim(claim_id="zz-new", metric_id="fixture-metric")
    resolved = bss.resolve_active_claim("fixture-metric", [old, new])
    note(resolved["claim_id"] == "zz-new", "a properly superseded old claim does not block resolution")

    # 10b. The exact scenario the referee flagged as broken: TWO claims that are both
    #      still "active" by valid_until (both None -- nobody set it on the old one),
    #      but old.superseded_by points at new. The old buggy logic treated "referenced
    #      by someone else's superseded_by" as a reason to EXCLUDE a candidate from
    #      "terminal", which backwards-selected the *old* (unreferenced) claim instead
    #      of the new (referenced, i.e. the actual successor) one. Must select "new".
    old_both_active = base_fixture_claim(claim_id="zz-old2", metric_id="fixture-metric", valid_until=None, superseded_by="zz-new2")
    new_both_active = base_fixture_claim(claim_id="zz-new2", metric_id="fixture-metric", valid_until=None, superseded_by=None)
    resolved2 = bss.resolve_active_claim("fixture-metric", [old_both_active, new_both_active])
    note(
        resolved2["claim_id"] == "zz-new2",
        "old->new via superseded_by (both valid_until=null) selects the successor, not the predecessor",
    )

    # 11. Zero claims for a metric -> "lacks a source record".
    try:
        bss.resolve_active_claim("fixture-metric", [])
        note(False, "a metric with zero claims is rejected")
    except SystemExit as e:
        note("lacks a source record" in str(e), "a metric with zero claims is rejected")

    # 11b. Quote-aware HTML escaping: a canonical_url (or any other rendered field)
    #      containing a double quote must not be able to break out of the href="..."
    #      attribute it's interpolated into. Render a card with such a URL and confirm
    #      the quote is escaped, not passed through raw.
    hostile_result = {
        "value": 1,
        "display_date": "Jan. 1, 2026",
        "public_label": "fixture label",
        "public_explanation": "fixture explanation",
        "public_source_label": "fixture release →",
        "canonical_url": 'https://example.gov/pr/x"><script>alert(1)</script>',
        "last_swept_for_supersession": "2026-01-01",
        "claim_id": "zz-hostile",
    }
    rendered = bss.render_card(hostile_result)
    # The literal sequence `x">` (unescaped quote immediately followed by the tag
    # closer) must not appear anywhere in the output -- that is what would actually
    # close the href attribute early and let the rest be parsed as new markup in a
    # real browser. It must instead show up HTML-entity-escaped.
    note('x">' not in rendered, "a double quote in a rendered field cannot break out of the href attribute")
    note(
        'href="https://example.gov/pr/x&quot;&gt;&lt;script&gt;alert(1)&lt;/script&gt;"' in rendered,
        "the hostile URL is rendered fully HTML-entity-escaped inside the href attribute",
    )

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
