#!/usr/bin/env python3
"""Capture a tracker release snapshot for the next deterministic diff.

This is an explicit release operation: canonical facts remain in research claims,
events, recovery rows and sources. The snapshot stores only stable public IDs and
headline metric values so a later build can say what changed without copying prose.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "tracker" / "data" / "tracker.json"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-id", required=True)
    parser.add_argument("--snapshot-date", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = json.loads(TRACKER.read_text(encoding="utf-8"))
    metrics = {}
    events = []
    recovery = []
    for program in data.get("programs", []):
        for metric in program.get("legal_metrics", []):
            metrics[metric["metric_id"]] = metric.get("value")
        events.extend(e["event_id"] for e in program.get("events", []) if e.get("event_id"))
        recovery.extend(r["entry_id"] for r in program.get("recovery", []) if r.get("entry_id"))

    snapshot = {
        "schema_version": 1,
        "snapshot_id": args.snapshot_id,
        "snapshot_date": args.snapshot_date,
        "commit_sha": args.commit_sha,
        "legal_metrics": dict(sorted(metrics.items())),
        "event_ids": sorted(set(events)),
        "recovery_entry_ids": sorted(set(recovery)),
        "note": "Derived release checkpoint only; canonical facts remain in source-linked research records.",
    }
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"snapshot captured: {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
