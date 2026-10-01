#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/"scripts"/"build-tracker.py")],check=True)
subprocess.run([sys.executable,str(ROOT/"scripts"/"build-accountability-brief.py")],check=True)
brief=json.loads((ROOT/"accountability"/"data"/"brief.json").read_text(encoding="utf-8"))
tracker=json.loads((ROOT/"tracker"/"data"/"tracker.json").read_text(encoding="utf-8"))
assert brief["since_snapshot"]=="tracker-v1-2026-09-30"
assert brief["change_count"]==sum(p["change_count"] for p in brief["programs"])
assert brief["change_count"]==tracker["changes"]["change_count"]
assert "recovery_total" not in brief
assert all(s.get("canonical_url") for s in brief["sources"])
kinds={i["kind"] for p in brief["programs"] for i in p["items"]}
assert "restitution_ordered" in kinds
assert "FORFEITURE_ORDERED" in kinds
for p in brief["programs"]:
    for i in p["items"]:
        if i["kind"]=="FORFEITURE_ORDERED":
            assert "value" not in i
print("accountability brief tests: passed")
