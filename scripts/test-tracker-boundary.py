#!/usr/bin/env python3
"""Hostile regression tests for /tracker/ publication boundaries."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_tracker", ROOT / "scripts" / "build-tracker.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)

def expect_error(fn, label):
    try:
        fn()
    except mod.BuildError:
        return
    raise AssertionError(label)

# Minimal source registry fixture for hostile event tests.
SOURCES = {"src-fixture": {"source_id": "src-fixture"}}

# 1. charged cannot render as convicted.
expect_error(
    lambda: mod.validate_legal_event({
        "event_id": "e1", "event_type": "CHARGED", "legal_stage": "CONVICTED"
    }),
    "charged event accepted convicted stage",
)

# 2. convicted cannot render as sentenced without sentence evidence.
assert not mod.legal_transition("SENTENCED", "CONVICTED")
expect_error(
    lambda: mod.validate_legal_event({
        "event_id": "e2", "event_type": "CONVICTED", "legal_stage": "SENTENCED"
    }),
    "conviction event accepted sentenced stage",
)

# 3. alleged dollars cannot render as restitution/recovery.
alleged = mod.normalize_money(
    {"value": 100, "metric_type": "alleged_loss"}, "fixture alleged"
)
assert alleged["category"] == "alleged_loss"
assert alleged["category"] not in {"restitution_ordered", "recovered_amount"}

# 4. source-less tracker facts fail publication.
expect_error(
    lambda: mod.require_sources([], SOURCES, "fixture"),
    "source-less fact published",
)

# 5. duplicate events do not double-count.
duplicate = [
    {"event_id": "same", "event_type": "CHARGED", "legal_stage": "CHARGED", "program_id": "p", "subject": "A", "source_ids": ["src-fixture"]},
    {"event_id": "same", "event_type": "CHARGED", "legal_stage": "CHARGED", "program_id": "p", "subject": "A", "source_ids": ["src-fixture"]},
]
expect_error(
    lambda: mod.validate_event_sequence(duplicate, SOURCES),
    "duplicate event accepted",
)

# 6. newer event can advance status only through supported legal transition.
forward = [
    {"event_id": "a", "event_type": "CHARGED", "legal_stage": "CHARGED", "program_id": "p", "subject": "A", "source_ids": ["src-fixture"]},
    {"event_id": "b", "event_type": "PLEADED", "legal_stage": "PLEADED", "program_id": "p", "subject": "A", "source_ids": ["src-fixture"]},
    {"event_id": "c", "event_type": "SENTENCED", "legal_stage": "SENTENCED", "program_id": "p", "subject": "A", "source_ids": ["src-fixture"]},
]
mod.validate_event_sequence(forward, SOURCES)
backward = forward + [
    {"event_id": "d", "event_type": "CONVICTED", "legal_stage": "CONVICTED", "program_id": "p", "subject": "A", "source_ids": ["src-fixture"]},
]
expect_error(
    lambda: mod.validate_event_sequence(backward, SOURCES),
    "backward legal transition accepted",
)

# 7. unknown aggregate stays unknown instead of being guessed.
subprocess.run([sys.executable, str(ROOT / "scripts" / "build-tracker.py")], check=True)
data = json.loads((ROOT / "tracker" / "data" / "tracker.json").read_text(encoding="utf-8"))
hss = next(p for p in data["programs"] if p["program_id"] == "hss")
assert hss["unknowns"]["charged_count"] is None
assert hss["unknowns"]["convicted_count"] is None
assert hss["unknowns"]["sentenced_count"] is None

# 8. reform announced does not become implemented.
assert mod.REFORM_STATE_MAP["state_revised_cap"] == "ANNOUNCED"
assert mod.REFORM_STATE_MAP["revalidation_target"] == "ANNOUNCED"

# 9. implemented does not become effective.
medicaid = next(p for p in data["programs"] if p["program_id"] == "medicaid-program-integrity")
implemented = [e for e in medicaid["reform_events"] if e["implementation_state"] == "IMPLEMENTED"]
assert implemented
assert all(e.get("effectiveness") == "UNKNOWN" for e in implemented)

# 10. displayed dates and source links survive projection.
assert data["last_verified"]
assert data["sources"]
assert all(s.get("canonical_url") for s in data["sources"])
assert all(s.get("publication_date") or s.get("retrieval_date") for s in data["sources"])
fof = next(p for p in data["programs"] if p["program_id"] == "feeding-our-future")
assert all(m.get("as_of") for m in fof["legal_metrics"])
assert all(m.get("source_ids") for m in fof["legal_metrics"])

# 11. Recovery categories stay distinct and are never silently converted to collected cash.
fof_recovery = next(p for p in data["programs"] if p["program_id"] == "feeding-our-future")["recovery"]
assert fof_recovery
assert any(r["category"] == "restitution_ordered" for r in fof_recovery)
assert any(r["category"] == "assets_seized" for r in fof_recovery)
assert all(r["category"] != "recovered_amount" for r in fof_recovery)

# 12. Matching restitution orders remain individual rows with an overlap group, not a summed total.
empire = [r for r in fof_recovery if r.get("overlap_group_id") == "fof-empire-47920514-restitution"]
assert len(empire) == 4
assert all(r["value"] == 47920514 for r in empire)
assert "recovery_total" not in data

# 13. Snapshot diff exposes new records without inventing a legal-stage change.
changes = data["changes"]
assert changes["since_snapshot"] == "tracker-v1-2026-09-30"
assert changes["legal_metric_changes"] == []
assert {e["event_id"] for e in changes["new_events"]} == {
    "evt-fof-ross-forfeiture-ordered-2025-02-07",
    "evt-fof-ibrahim-forfeiture-ordered-2026-04-03",
}
assert all(e["event_type"] == "FORFEITURE_ORDERED" for e in changes["new_events"])
assert len(changes["new_recovery_entries"]) == 27

# 14. Source-less or duplicate recovery entries fail closed.
expect_error(
    lambda: mod.recovery_projection(
        {"entries": [{"entry_id": "r1", "program_id": "p", "amount": 1, "metric_type": "recovered_amount", "source_ids": []}]},
        SOURCES,
    ),
    "source-less recovery row published",
)
expect_error(
    lambda: mod.recovery_projection(
        {"entries": [
            {"entry_id": "r1", "program_id": "p", "amount": 1, "metric_type": "recovered_amount", "source_ids": ["src-fixture"]},
            {"entry_id": "r1", "program_id": "p", "amount": 2, "metric_type": "recovered_amount", "source_ids": ["src-fixture"]},
        ]},
        SOURCES,
    ),
    "duplicate recovery row accepted",
)

print("tracker boundary tests: 14/14 passed")

# ---- Primary judgment / collection acquisition regressions (tests 15-21) ----
RS = {
    "src-release": {"source_id": "src-release", "source_status": "PRIMARY_GOVERNMENT_RELEASE", "document_type": "press_release"},
    "src-news": {"source_id": "src-news", "source_status": "SECONDARY_VERIFIED", "document_type": "news_report"},
    "src-judgment": {"source_id": "src-judgment", "source_status": "PRIMARY_COURT_RECORD", "document_type": "court_judgment"},
    "src-indictment": {"source_id": "src-indictment", "source_status": "PRIMARY_COURT_RECORD", "document_type": "court_indictment"},
    "src-prelim-forfeiture": {"source_id": "src-prelim-forfeiture", "source_status": "PRIMARY_COURT_RECORD", "document_type": "court_forfeiture_order"},
    "src-accounting": {"source_id": "src-accounting", "source_status": "PRIMARY_COURT_RECORD", "document_type": "court_collection_accounting"},
}

def entry(**kw):
    base = {"entry_id": "r1", "program_id": "p", "subject": "A", "amount": 100, "currency": "USD",
            "metric_type": "restitution_ordered", "event_date": "2025-01-01", "evidence_class": "ADJUDICATED",
            "source_ids": ["src-release"], "interpretation": "fixture"}
    base.update(kw)
    return base

def project(*entries):
    return mod.recovery_projection({"entries": list(entries)}, RS)[1]

# 15. court-backed restitution replaces release-only provenance without changing the amount.
release_only = project(entry())[0]
court_backed = project(entry(source_ids=["src-judgment", "src-release"], primary_document_ids=["src-judgment"]))[0]
assert release_only["evidence_basis"] == "AGENCY_RELEASE_ONLY" and release_only["primary_document_gap"]
assert court_backed["evidence_basis"] == "COURT_DOCUMENT" and court_backed["primary_document_gap"] is None
assert court_backed["value"] == release_only["value"] == 100
assert "src-release" in court_backed["source_ids"]  # release kept as corroboration

# 16. joint-and-several / overlapping restitution stays non-additive and must be grouped.
expect_error(
    lambda: project(entry(entry_id="a", subject="A", amount=5), entry(entry_id="b", subject="B", amount=5)),
    "identical restitution for two subjects accepted without overlap group",
)
expect_error(
    lambda: project(
        entry(entry_id="a", subject="A", amount=5, overlap_group_id="g1"),
        entry(entry_id="b", subject="B", amount=5, overlap_group_id="g2"),
    ),
    "identical restitution split across different overlap groups accepted",
)
grouped = project(
    entry(entry_id="a", subject="A", amount=5, overlap_group_id="g"),
    entry(entry_id="b", subject="B", amount=5, overlap_group_id="g"),
)
assert {r["overlap_group_id"] for r in grouped} == {"g"} and "recovery_total" not in data
live_groups = {}
for r in fof_recovery:
    if r.get("overlap_group_id"):
        live_groups.setdefault(r["overlap_group_id"], []).append(r)
assert all(len({x["value"] for x in rows}) == 1 for rows in live_groups.values() if rows[0]["category"] == "restitution_ordered")

# 17. forfeiture order without realization stays unrecovered.
fo = project(entry(metric_type="forfeiture_ordered", source_ids=["src-prelim-forfeiture"],
                   primary_document_ids=["src-prelim-forfeiture"], collection_status=None))[0]
assert fo["category"] == "forfeiture_ordered" and fo["evidence_basis"] == "COURT_DOCUMENT"
assert fo["category"] not in {"recovered_amount", "assets_recovered"}
expect_error(
    lambda: project(entry(metric_type="forfeiture_ordered", source_ids=["src-prelim-forfeiture"],
                          primary_document_ids=["src-prelim-forfeiture"], realization_status="REALIZED")),
    "forfeiture order marked realized without collection evidence",
)

# 18. seizure without final forfeiture stays seized and cannot be labelled adjudicated from a release.
seized = project(entry(metric_type="assets_seized", evidence_class="AGENCY_POSITION"))[0]
assert seized["category"] == "assets_seized" and seized["evidence_basis"] == "AGENCY_RELEASE_ONLY"
expect_error(
    lambda: project(entry(metric_type="assets_seized", evidence_class="ADJUDICATED")),
    "release-only seizure labelled ADJUDICATED",
)
expect_error(
    lambda: project(entry(metric_type="assets_seized", evidence_class="ADJUDICATED_PRELIMINARY_ORDER")),
    "release-only seizure labelled with adjudicated variant",
)

# 19. collection evidence is required before recovered_amount (and other collection metrics).
for metric in ("recovered_amount", "assets_recovered", "administrative_recoupment"):
    expect_error(lambda m=metric: project(entry(metric_type=m)), f"{metric} without collection evidence")
expect_error(
    lambda: project(entry(metric_type="recovered_amount", source_ids=["src-release"],
                          collection_evidence_source_ids=["src-release"])),
    "press release accepted as collection evidence",
)
recovered = project(entry(metric_type="recovered_amount", source_ids=["src-accounting"],
                          primary_document_ids=["src-accounting"],
                          collection_evidence_source_ids=["src-accounting"], collection_status="COLLECTED"))[0]
assert recovered["category"] == "recovered_amount"
expect_error(
    lambda: project(entry(collection_status="COLLECTED")),
    "restitution order flipped to COLLECTED without evidence",
)
expect_error(
    lambda: project(entry(collection_status="FULLY_COLLECTED")),
    "unknown non-neutral collection status bypassed collection evidence gate",
)

# 20. a missing primary judgment is never silently treated as judgment-backed.
for src in (["src-release"], ["src-news"], ["src-indictment"]):
    row = project(entry(source_ids=src))[0]
    assert row["evidence_basis"] != "COURT_DOCUMENT", src
expect_error(
    lambda: project(entry(source_ids=["src-indictment"], primary_document_ids=["src-indictment"])),
    "indictment accepted as restitution judgment",
)
expect_error(
    lambda: project(entry(source_ids=["src-release"], primary_document_ids=["src-release"])),
    "press release accepted as primary court document",
)
expect_error(
    lambda: project(entry(source_ids=["src-judgment"], primary_document_ids=["src-judgment", "src-release"])),
    "primary document outside source_ids accepted",
)
assert project(entry(source_ids=["src-news"]))[0]["evidence_basis"] == "SECONDARY_ONLY"

# 21. every published recovery row declares its evidence basis; court rows resolve to court records.
for prog in data["programs"]:
    for r in prog["recovery"]:
        assert r["evidence_basis"] in {"COURT_DOCUMENT", "AGENCY_RELEASE_ONLY", "SECONDARY_ONLY", "UNRESOLVED"}
        if r["evidence_basis"] == "COURT_DOCUMENT":
            assert r["primary_document_ids"] and r["primary_document_gap"] is None
        else:
            assert not r["primary_document_ids"] and r["primary_document_gap"] or r["category"] in {"identified_for_recovery", "cost_avoidance"}

print("tracker boundary tests (acquisition regressions 15-21): passed")
