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
assert len(empire) == 3
assert all(r["value"] == 47920514 for r in empire)
assert "recovery_total" not in data

# 13. Snapshot diff exposes new records without inventing a legal-stage change.
changes = data["changes"]
assert changes["since_snapshot"] == "tracker-v1-2026-09-30"
assert changes["legal_metric_changes"] == []
assert changes["new_events"] == []
assert len(changes["new_recovery_entries"]) == 10

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
