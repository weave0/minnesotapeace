#!/usr/bin/env python3
"""Build the public Accountability Brief from the tracker projection."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TRACKER=ROOT/"tracker"/"data"/"tracker.json"
OUT=ROOT/"accountability"/"data"/"brief.json"

def main():
    data=json.loads(TRACKER.read_text(encoding="utf-8"))
    source_map={s["source_id"]:s for s in data.get("sources",[])}
    changes=data.get("changes") or {}
    programs=[]
    used=set()

    for p in data.get("programs",[]):
        items=[]
        for m in changes.get("legal_metric_changes") or []:
            if p["program_id"]=="feeding-our-future" and m["metric_id"].startswith("fof-"):
                items.append({"kind":"LEGAL_METRIC","date":None,"title":m["metric_id"],"summary":f"{m['before']} → {m['after']}","source_ids":[]})
        for e in changes.get("new_events") or []:
            if e.get("program_id")!=p["program_id"]: continue
            sids=e.get("source_ids") or []
            used.update(sids)
            items.append({"kind":e.get("event_type"),"date":e.get("occurred_at"),"title":e.get("subject") or "Program update","summary":e.get("summary"),"source_ids":sids})
        for r in changes.get("new_recovery_entries") or []:
            if r.get("program_id")!=p["program_id"]: continue
            sids=r.get("source_ids") or []
            used.update(sids)
            items.append({"kind":r.get("category"),"date":r.get("event_date"),"title":r.get("subject") or "Recovery record","summary":r.get("interpretation"),"value":r.get("value"),"currency":r.get("currency"),"source_ids":sids})
        items.sort(key=lambda x:(x.get("date") or ""), reverse=True)
        programs.append({"program_id":p["program_id"],"name":p["name"],"items":items,"change_count":len(items)})

    sources=[]
    for sid in sorted(used):
        if sid not in source_map:
            raise SystemExit(f"brief references source missing from tracker projection: {sid}")
        sources.append(source_map[sid])

    out={
      "schema_version":1,
      "title":"Minnesota Public Accountability Brief",
      "since_snapshot":changes.get("since_snapshot"),
      "snapshot_date":changes.get("snapshot_date"),
      "last_verified":data.get("last_verified"),
      "change_count":sum(p["change_count"] for p in programs),
      "programs":programs,
      "sources":sources,
      "rules":[
        "No change is published without a canonical source or a reconciled tracker metric.",
        "Restitution ordered is not money collected.",
        "Assets seized are not automatically forfeited or recovered.",
        "Announced, implemented, measured and effective remain distinct states.",
        "No cross-category money total is calculated."
      ]
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"accountability brief built: {OUT.relative_to(ROOT)} ({out['change_count']} changes, {len(sources)} sources)")

if __name__=="__main__":
    main()
