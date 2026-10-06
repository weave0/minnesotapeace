#!/usr/bin/env python3
"""Regenerate research/money/RECOVERY-EVIDENCE-INVENTORY.md from the built tracker projection.

The row table is derived from tracker/data/tracker.json (run build-tracker.py first), so the
inventory cannot drift from what /tracker/ publishes. The per-defendant document checklist and
the acquisition gaps are maintained by hand below and must be edited when a document is captured.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "tracker" / "data" / "tracker.json"
OUT = ROOT / "research" / "money" / "RECOVERY-EVIDENCE-INVENTORY.md"

BASIS = {
    "COURT_DOCUMENT": "COURT_DOCUMENT",
    "AGENCY_RELEASE_ONLY": "DOJ / AGENCY_RELEASE_ONLY",
    "SECONDARY_ONLY": "SECONDARY_ONLY",
    "UNRESOLVED": "UNKNOWN / UNRESOLVED",
}
CATEGORY_ORDER = ["restitution_ordered", "forfeiture_ordered", "forfeiture_sought", "assets_seized",
                  "assets_recovered", "recovered_amount", "administrative_recoupment",
                  "identified_for_recovery", "cost_avoidance"]

# Y = captured in research/court (see source records); N = exists on the docket or is expected but not captured;
# n/a = not applicable to that defendant's posture; ? = not determined in this pass.
CHECKLIST = """
| Defendant (docket) | Judgment | Plea agr. | Prelim. forfeiture order | Final forfeiture order | Restitution order | Forfeiture realization | Actual collection |
|---|---|---|---|---|---|---|---|
| Bock (22-cr-223) | Y ECF 907 | n/a (trial) | N | N | Y (in judgment) | N | N |
| Shariff (22-cr-124) | Y ECF 789 | n/a (trial) | Y ECF 709 | N (judgment cites "final orders") | Y (in judgment) | N | N |
| Ross (23-cr-82) | Y ECF 68 | Y ECF 43 | Y ECF 55 | N | Y (in judgment) | N | N |
| A. Farah (22-cr-124) | N (ECF 851 / 858 amended; not on RECAP) | n/a (trial) | N (ECF 665 cited by ECF 952; not retrieved) | N (ECF 902 judgment of forfeiture; not on RECAP) | N | N (ECF 952 approves BBI third-party settlement; no dollars) | N |
| Ismail (22-cr-124) | N (ECF 690; not on RECAP) | n/a (trial) | ? | ? | N | N | N |
| Abdimajid Nur (22-cr-124) | N (ECF 939; not on RECAP) | N (24-cr-173 ECF 73 is the bribery plea) | ? | ? | N | N | N |
| Sahra Nur (22-cr-224) | N (not located) | ? | ? | ? | N | N | N |
| Jesow (22-cr-224) | N (not located) | N (ECF 392; not on RECAP) | ? | ? | N | N | N |
| Abdulkadir Salah (22-cr-223) | N | Y ECF 496 | N | N | N (agreed in plea only) | N | N |
| Abdi Salah (22-cr-223) | N | Y ECF 497 | N | N | N (agreed in plea only) | N | N |
| Ibrahim (22-cr-124) | N (not sentenced in this record) | N (ECF 842 on RECAP; not downloaded) | Y ECF 971 | N | n/a | N | N |
| Anwar Adow (25-cr-353, HSS) | N | Y ECF 9 | N | N | N (agreed in plea only) | N | N |
| Asad Adow (25-cr-354, HSS) | N | Y ECF 14 | N | N | N (agreed in plea only) | N | N |
"""

GAPS = """
## Court documents acquired in this tranche

Judgments: Bock (22-cr-223 ECF 907), Shariff (22-cr-124 ECF 789), Ross (23-cr-82 ECF 68).
Forfeiture orders: Shariff preliminary order (ECF 709), Ross preliminary order (ECF 55), Ibrahim preliminary order (ECF 971), Farah/BBI settlement judgment (ECF 952, no dollar amounts).
Plea agreements: Ross (ECF 43), Abdulkadir Salah (ECF 496), Abdi Salah (ECF 497), Anwar Adow (25-cr-353 ECF 9), Asad Adow (25-cr-354 ECF 14).
Every file carries a SHA-256 in its source record (`research/sources/src-courtlistener-mnd-*.json`). Scans above 1.5 MB are not committed; their OCR text and hash are, and the PDF is re-fetchable from the recorded RECAP URL. OCR-derived figures used by tracker rows were checked against the page images.

## Not obtainable from RECAP in this pass (recorded gaps, not placeholders)

- Judgments: Ismail (ECF 690), Farah (ECF 851, 858), Hayat Nur (ECF 869), Abdimajid Nur (ECF 939), Sahra Nur, Jesow. `is_available=false` on RECAP, or not located before the CourtListener search API rate-limited this client (429, Retry-After about 24 hours). They would need a PACER purchase or a later RECAP upload.
- Farah preliminary forfeiture order (ECF 665) and judgment of forfeiture (ECF 902); the BBI stipulation (ECF 945).
- Final orders of forfeiture for every defendant above.
- HSS: Aden (25-cr-349), Falade (25-cr-351), Hussein (25-cr-479), Sallah (25-cr-482) plea/judgment documents were not queried before the rate limit.

## Collection and realization gaps (no row is above "ordered")

No document captured in this tranche shows a dollar collected, an asset sold, or an administrative recoupment. Nothing in the tracker is `recovered_amount`, `assets_recovered` or `administrative_recoupment`, and the builder now refuses such a row without collection-accounting evidence.
Sources that could close this: Financial Litigation Unit / clerk restitution ledgers, final orders of forfeiture with disposition, USMS/AFMLS sale records, DHS recoupment ledgers, MFCU annual statistical reports.

## Priorities 4 and 5 (not tracker rows; classification of the existing money ledgers)

- EIDBI / autism: no adjudicated money outcome captured yet. Asha Hassan (autism FOF, plea 2025-12-18) has USAO releases only; docket not yet harvested.
- MFCU / DHS (research/money recovery ledgers, not published on /tracker/): DHS ">$56M identified for recovery" is AGENCY_RELEASE_ONLY and is published as `identified_for_recovery`; Optum $165M is a cost-avoidance claim; MFCU "$32M ordered / $3M collected" and FOX 9's 48-case sample are SECONDARY_ONLY (KSTP/FOX 9) and stay off the tracker; the Ibrahim CACFP civil judgment ($2,481,310.08, Hennepin County 27-CV-22-13107) is a court record but is a civil judgment not yet on the tracker.

## Findings that changed the model

1. `assets_seized` rows carried evidence class ADJUDICATED although they rested on a DOJ release. They now rest on the filed plea agreements and are labelled PLEA_AGREEMENT; the builder rejects a release-only seizure or forfeiture row labelled ADJUDICATED.
2. Recovery rows had no visible evidence basis. Each row now publishes `evidence_basis`, the court documents that establish it, and (when absent) the specific primary-document gap.
3. Non-additivity was a convention. The builder now fails if identical restitution amounts for different subjects are not in one overlap group.
4. Ross: the USAO release gave no forfeiture dollar value; her preliminary order enters a $1,241,455 money judgment (her plea consented to $2,837,491, so the order is used).
5. Shariff's judgment shows the Empire joint-and-several schedule also includes Hayat Nur (22-cr-124 defendant 8), who is not a tracker row.
6. Bock's $242,807,755 restitution order (ECF 907) was not in the corpus. It is payable to the same victim for the same program loss as other defendants' orders and has not been reconciled with them.

## Next highest-value acquisition target

Once the CourtListener rate limit clears (or via PACER): the Empire family judgments (Ismail ECF 690, Farah ECF 858, Nur ECF 939, Hayat Nur ECF 869), the Farah preliminary and judgment of forfeiture orders (ECF 665, 902), and the Bock preliminary and final forfeiture orders. Those convert the five remaining release-only restitution rows and unlock the largest forfeiture figures.
"""


def money(v):
    return f"${v:,.2f}".replace(".00", "")


def main() -> None:
    data = json.loads(TRACKER.read_text(encoding="utf-8"))
    rows = [r for p in data["programs"] for r in p["recovery"]]
    rows.sort(key=lambda r: (r["program_id"], CATEGORY_ORDER.index(r["category"]) if r["category"] in CATEGORY_ORDER else 99, r["subject"] or "", r["event_date"] or ""))
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["evidence_basis"]] = counts.get(r["evidence_basis"], 0) + 1

    lines = [
        "# Recovery evidence inventory",
        "",
        "Generated by `scripts/inventory-recovery-evidence.py` from the built tracker projection. Do not edit the row table by hand.",
        "",
        "Categories stay distinct: restitution ordered, restitution collected, forfeiture ordered, forfeiture realized, assets seized, assets recovered, identified for recovery, administrative recoupment, cost avoidance. An order is never evidence of collection; a seizure is never evidence of final forfeiture; overlapping or joint-and-several obligations are never summed.",
        "",
        "## Evidence basis of every published recovery row",
        "",
        "| Basis | Rows |",
        "|---|---|",
    ]
    for key in ("COURT_DOCUMENT", "AGENCY_RELEASE_ONLY", "SECONDARY_ONLY", "UNRESOLVED"):
        lines.append(f"| {BASIS[key]} | {counts.get(key, 0)} |")
    lines += ["", "| Program | Category | Subject | Amount | Basis | Court documents | Overlap group | Collection / realization |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        docs = ", ".join(i.replace("src-courtlistener-mnd-", "") for i in r["primary_document_ids"]) or "none (" + (r["primary_document_gap"] or "gap not stated") + ")"
        state = r.get("collection_status") or r.get("realization_status") or "not stated"
        lines.append(f"| {r['program_id']} | {r['category']} | {r['subject']} | {money(r['value'])} | {BASIS[r['evidence_basis']]} | {docs} | {r.get('overlap_group_id') or ''} | {state} |")
    lines += ["", "## Document checklist by defendant", CHECKLIST, GAPS]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"inventory written: {OUT.relative_to(ROOT)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
