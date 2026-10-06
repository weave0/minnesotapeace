#!/usr/bin/env python3
"""Build /tracker/ public data from canonical Minnesota Peace records.

The tracker is a projection, not a truth store. It consumes:
- manifest-gated /record/ corpus for charge-era cases and money rows,
- canonical research/claims for explicitly selected current metrics/claims,
- canonical accountability events,
- canonical Medicaid control timeline,
- canonical source records for every public fact.

It fails closed on missing sources, ambiguous legal metrics, duplicate events,
unknown money categories, and unsupported legal-stage transitions.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
RECORD = ROOT / "record" / "data" / "corpus.json"
PROGRAMS = RESEARCH / "programs" / "tracker-programs-v1.json"
EVENTS = RESEARCH / "events" / "accountability-events-v1.json"
CONTROLS = RESEARCH / "oversight" / "medicaid-control-timeline.json"
RECOVERY = RESEARCH / "money" / "tracker-recovery-v1.json"
SNAPSHOT = RESEARCH / "snapshots" / "tracker-v1-2026-09-30.json"
OUT = ROOT / "tracker" / "data" / "tracker.json"

LEGAL_EVENT_STAGES = {
    "CHARGED": "CHARGED",
    "PLEADED": "PLEADED",
    "CONVICTED": "CONVICTED",
    "SENTENCED": "SENTENCED",
    "CASE_APPEARANCE": "CHARGED",
}
LEGAL_STAGE_ORDER = {"CHARGED": 1, "PLEADED": 2, "CONVICTED": 2, "SENTENCED": 3}
MONEY_CATEGORIES = {
    "amount_billed", "amount_claimed", "amount_paid", "alleged_loss", "proven_loss",
    "restitution_ordered", "forfeiture_ordered", "recovered_amount",
    "identified_for_recovery", "cost_avoidance", "program_spend", "fraud_estimate",
    "assets_seized", "assets_recovered", "forfeiture_sought", "administrative_recoupment",
}
REFORM_STATE_MAP = {
    "state_program_review": "IMPLEMENTED",
    "program_termination_request": "ANNOUNCED",
    "administrative_controls": "IMPLEMENTED",
    "federal_corrective_action_request": "ANNOUNCED",
    "prepayment_review": "IMPLEMENTED",
    "state_cap_submission": "ANNOUNCED",
    "enhanced_screening": "IMPLEMENTED",
    "revalidation_notice": "IMPLEMENTED",
    "provider_enrollment_moratorium": "IMPLEMENTED",
    "state_revised_cap": "ANNOUNCED",
    "revalidation_target": "ANNOUNCED",
    "moratorium_extension": "IMPLEMENTED",
    "revalidation_snapshot": "MEASURED",
    "claims_review": "IMPLEMENTED",
    "service_access_impact": "MEASURED",
    "payment_integrity_report": "MEASURED",
    "improper_payment_measurement": "MEASURED",
    "federal_noncompliance_determination": "MEASURED",
}


# Evidence-basis model for recovery rows. A row is COURT_DOCUMENT-backed only when it
# declares primary_document_ids and every one is a court record of a document type that
# can actually establish that metric. A release, news report, or unrelated court filing
# (for example an indictment) never upgrades a restitution/forfeiture row.
COURT_DOC_TYPES_BY_METRIC = {
    "restitution_ordered": {"court_judgment", "court_amended_judgment", "court_restitution_order"},
    "forfeiture_ordered": {"court_forfeiture_order", "court_judgment", "court_amended_judgment"},
    "forfeiture_sought": {"court_forfeiture_motion", "court_forfeiture_order", "court_plea_agreement"},
    "assets_seized": {"court_forfeiture_order", "court_forfeiture_motion", "court_plea_agreement"},
    "assets_recovered": {"court_collection_accounting"},
    "recovered_amount": {"court_collection_accounting"},
}
COLLECTION_METRICS = {"recovered_amount", "assets_recovered", "administrative_recoupment"}
COLLECTION_EVIDENCE_TYPES = {"court_collection_accounting", "agency_collection_ledger"}
NEUTRAL_RECOVERY_STATUSES = {None, "", "UNKNOWN", "NOT_APPLICABLE"}
SECONDARY_PREFIXES = ("SECONDARY", "LEAD", "NEWS", "REPUTABLE")
COURT_CLASSES_NOT_ADJUDICATED_FOR = {"assets_seized", "forfeiture_sought", "forfeiture_ordered"}
BASIS_GAP = {
    "restitution_ordered": "Judgment or restitution order not yet captured; amount rests on the cited release.",
    "forfeiture_ordered": "Forfeiture order not yet captured; status rests on the cited release.",
    "assets_seized": "No court order or filing captured for this seizure; it rests on the cited release.",
}

class BuildError(SystemExit):
    pass

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def index_json(directory: Path, field: str):
    out = {}
    for path in sorted(directory.glob("*.json")):
        data = load(path)
        ident = data.get(field) if isinstance(data, dict) else None
        if not ident:
            continue
        if ident in out:
            raise BuildError(f"duplicate {field}: {ident}")
        out[ident] = data
    return out

def source_ids_for(obj):
    ids = []
    if isinstance(obj.get("source_id"), str):
        ids.append(obj["source_id"])
    if isinstance(obj.get("source_ids"), list):
        ids.extend(x for x in obj["source_ids"] if isinstance(x, str))
    return ids

def require_sources(ids, sources, context):
    ids = list(dict.fromkeys(ids))
    if not ids:
        raise BuildError(f"source-less tracker fact: {context}")
    missing = [sid for sid in ids if sid not in sources]
    if missing:
        raise BuildError(f"missing source record(s) for {context}: {missing}")
    return ids

def source_public(s):
    return {
        "source_id": s["source_id"],
        "title": s.get("title"),
        "issuing_body": s.get("issuing_body"),
        "publication_date": s.get("publication_date"),
        "retrieval_date": s.get("retrieval_date"),
        "canonical_url": s.get("canonical_url"),
        "evidence_class": s.get("evidence_class"),
    }

def normalize_money(amount, context):
    category = amount.get("metric_type") or amount.get("money_category")
    if category not in MONEY_CATEGORIES:
        raise BuildError(f"unclear money category for {context}: {category!r}")
    value = amount.get("value", amount.get("amount"))
    if not isinstance(value, (int, float)):
        raise BuildError(f"missing numeric money value for {context}")
    return {
        "value": value,
        "currency": amount.get("currency", "USD"),
        "category": category,
        "exact_or_approximate": amount.get("exact_or_approximate"),
        "period_start": amount.get("period_start"),
        "period_end": amount.get("period_end"),
        "overlap_group_id": amount.get("overlap_group_id"),
        "methodology": amount.get("methodology"),
        "evidence_class": amount.get("evidence_class"),
    }

def validate_legal_event(event):
    etype = event.get("event_type")
    stage = event.get("legal_stage")
    if etype in LEGAL_EVENT_STAGES:
        if stage != LEGAL_EVENT_STAGES[etype]:
            raise BuildError(f"legal event {event.get('event_id')} stage/type mismatch: {etype}/{stage}")
    elif stage:
        raise BuildError(f"non-legal event {event.get('event_id')} carries legal_stage {stage}")

def legal_transition(previous, newer):
    if previous is None:
        return True
    if previous not in LEGAL_STAGE_ORDER or newer not in LEGAL_STAGE_ORDER:
        return False
    return LEGAL_STAGE_ORDER[newer] >= LEGAL_STAGE_ORDER[previous]

def validate_event_sequence(events, sources):
    seen = set()
    subject_stage = {}
    by_program = {}
    for event in events:
        eid = event.get("event_id")
        if not eid or eid in seen:
            raise BuildError(f"duplicate or missing event_id: {eid!r}")
        seen.add(eid)
        require_sources(source_ids_for(event), sources, f"event {eid}")
        validate_legal_event(event)
        if event.get("legal_stage"):
            subject = event.get("subject")
            prev = subject_stage.get(subject)
            if not legal_transition(prev, event["legal_stage"]):
                raise BuildError(f"unsupported legal transition for {subject}: {prev} -> {event['legal_stage']}")
            subject_stage[subject] = event["legal_stage"]
        by_program.setdefault(event.get("program_id"), []).append(event)
    return by_program

def active_metric(metric_id, claims, sources):
    matches = [c for c in claims.values() if c.get("metric_id") == metric_id and not c.get("valid_until")]
    if len(matches) != 1:
        raise BuildError(f"metric {metric_id!r} must have exactly one active claim; found {len(matches)}")
    claim = matches[0]
    sids = require_sources(source_ids_for(claim), sources, f"metric {metric_id}")
    return {
        "metric_id": metric_id,
        "value": claim.get("metric_value"),
        "measurement_type": claim.get("measurement_type"),
        "status": claim.get("status"),
        "evidence_class": claim.get("evidence_class"),
        "as_of": claim.get("event_date") or claim.get("measurement_date") or claim.get("reviewed_at"),
        "explanation": claim.get("public_explanation") or claim.get("claim_text"),
        "source_ids": sids,
    }

def fact_from_claim(claim, sources):
    sids = require_sources(source_ids_for(claim), sources, f"claim {claim.get('claim_id')}")
    money = [normalize_money(a, f"claim {claim.get('claim_id')}") for a in claim.get("amounts") or []]
    return {
        "claim_id": claim.get("claim_id"),
        "text": claim.get("claim_text"),
        "claim_type": claim.get("claim_type"),
        "status": claim.get("status"),
        "evidence_class": claim.get("evidence_class"),
        "event_date": claim.get("event_date"),
        "is_allegation": bool(claim.get("is_allegation")),
        "qualifiers": claim.get("qualifiers") or [],
        "money": money,
        "source_ids": sids,
    }

def family_case_projection(family_id, corpus, sources):
    cases = [c for c in corpus.get("cases", []) if c.get("family") == family_id]
    docket_set = {c.get("docket") for c in cases if c.get("docket")}
    claim_map = {
        c.get("claim_id"): c for c in corpus.get("claims", [])
        if c.get("case_number") in docket_set and c.get("claim_id")
    }
    claim_ids = set(claim_map)
    money = []
    for row in corpus.get("money", []):
        if row.get("claim_id") not in claim_ids:
            continue
        claim = claim_map[row.get("claim_id")]
        sids = require_sources(source_ids_for(claim), sources, f"record money claim {row.get('claim_id')}")
        normalized = normalize_money(row, f"record money row {row.get('row_id')}")
        normalized.update({
            "row_id": row.get("row_id"),
            "claim_id": row.get("claim_id"),
            "case_number": row.get("case_number"),
            "status": row.get("status"),
            "qualifiers": row.get("qualifiers") or [],
            "source_ids": sids,
        })
        money.append(normalized)
    public_cases = []
    for case in cases:
        case_sids = case.get("source_ids") or []
        if not case_sids:
            continue
        require_sources(case_sids, sources, f"record case {case.get('id')}")
        public_cases.append({
            "case_id": case.get("id"),
            "docket": case.get("docket"),
            "short_name": case.get("short_name"),
            "instrument": case.get("instrument"),
            "filed": case.get("filed"),
            "defendants": case.get("defendants") or [],
            "count_n": case.get("count_n"),
            "evidentiary_status": case.get("evidentiary_status"),
            "source_ids": case_sids,
            "gap": bool(case.get("gap")),
        })
    return public_cases, money

def timeline_projection(controls, sources):
    out = []
    for idx, event in enumerate(controls.get("events", [])):
        state = REFORM_STATE_MAP.get(event.get("event_type"))
        if not state:
            continue
        sids = require_sources(source_ids_for(event), sources, f"control timeline event {idx}")
        out.append({
            "event_date": event.get("event_date"),
            "event_type": event.get("event_type"),
            "actor": event.get("actor"),
            "program": event.get("program"),
            "summary": event.get("summary"),
            "evidence_class": event.get("evidence_class"),
            "implementation_state": state,
            "effectiveness": "UNKNOWN",
            "qualification": event.get("qualification"),
            "source_ids": sids,
        })
    return out


def derive_evidence_basis(entry, sources, eid):
    """Return (basis, primary_ids, gap). Never infers court backing from a release."""
    metric = entry.get("metric_type")
    sids = source_ids_for(entry)
    declared = entry.get("primary_document_ids") or []
    if declared:
        allowed = COURT_DOC_TYPES_BY_METRIC.get(metric, set())
        for pid in declared:
            if pid not in sids:
                raise BuildError(f"recovery entry {eid}: primary document {pid} is not in source_ids")
            src = sources[pid]
            if src.get("source_status") != "PRIMARY_COURT_RECORD" or src.get("document_type") not in allowed:
                raise BuildError(
                    f"recovery entry {eid}: {pid} cannot establish {metric} "
                    f"(status={src.get('source_status')!r}, type={src.get('document_type')!r})"
                )
        return "COURT_DOCUMENT", list(declared), None
    statuses = {str(sources[sid].get("source_status") or "") for sid in sids}
    # A court record that was not declared as primary for this metric (an indictment, a docket
    # entry, a co-defendant's judgment) is corroboration only; it never makes the row court-backed.
    agency_like = {s for s in statuses if s.startswith("PRIMARY_") and "COURT" not in s}
    secondary_like = {s for s in statuses if s.startswith(SECONDARY_PREFIXES) or "JOURNALISM" in s or "ADVOCACY" in s}
    if agency_like:
        basis = "AGENCY_RELEASE_ONLY"
    elif secondary_like:
        basis = "SECONDARY_ONLY"
    else:
        basis = "UNRESOLVED"
    default = (
        "Rests on an agency or contractor publication; no independent record or collection ledger is captured."
        if basis == "AGENCY_RELEASE_ONLY"
        else "No primary record is captured for this row."
    )
    return basis, [], BASIS_GAP.get(metric, default)

def check_overlap_rules(rows):
    """Identical restitution amounts across subjects must be explicitly grouped (non-additive)."""
    by_value = {}
    for row in rows:
        if row["category"] == "restitution_ordered":
            by_value.setdefault((row["program_id"], row["value"]), []).append(row)
    for (_, value), group in by_value.items():
        subjects = {r["subject"] for r in group}
        if len(subjects) < 2:
            continue
        groups = {r.get("overlap_group_id") for r in group}
        if None in groups or len(groups) != 1:
            raise BuildError(
                f"identical restitution amount {value} for multiple subjects lacks a single overlap_group_id"
            )

def recovery_projection(doc, sources):
    seen = set()
    by_program = {}
    all_rows = []
    for entry in doc.get("entries", []):
        eid = entry.get("entry_id")
        if not eid or eid in seen:
            raise BuildError(f"duplicate or missing recovery entry_id: {eid!r}")
        seen.add(eid)
        sids = require_sources(source_ids_for(entry), sources, f"recovery entry {eid}")
        row = normalize_money(entry, f"recovery entry {eid}")
        metric = row["category"]
        basis, primary_ids, gap = derive_evidence_basis(entry, sources, eid)
        evidence_ids = entry.get("collection_evidence_source_ids") or []
        for cid in evidence_ids:
            if cid not in sids or sources[cid].get("document_type") not in COLLECTION_EVIDENCE_TYPES:
                raise BuildError(f"recovery entry {eid}: {cid} is not collection evidence")
        if metric in COLLECTION_METRICS and not evidence_ids:
            raise BuildError(f"recovery entry {eid}: {metric} requires collection_evidence_source_ids")
        claimed = {entry.get("collection_status"), entry.get("realization_status")} - NEUTRAL_RECOVERY_STATUSES
        if claimed and not evidence_ids:
            raise BuildError(f"recovery entry {eid}: {sorted(claimed)} asserted without collection evidence")
        evidence_class = str(entry.get("evidence_class") or "")
        if metric in COURT_CLASSES_NOT_ADJUDICATED_FOR and basis != "COURT_DOCUMENT" and evidence_class.startswith("ADJUDICATED"):
            raise BuildError(f"recovery entry {eid}: release-only {metric} cannot use adjudicated evidence class {evidence_class}")
        row.update({
            "entry_id": eid,
            "program_id": entry.get("program_id"),
            "subject": entry.get("subject"),
            "event_date": entry.get("event_date"),
            "evidence_class": entry.get("evidence_class"),
            "evidence_basis": basis,
            "primary_document_ids": primary_ids,
            "primary_document_gap": gap,
            "collection_evidence_source_ids": list(evidence_ids),
            "source_ids": sids,
            "interpretation": entry.get("interpretation"),
            "collection_status": entry.get("collection_status"),
            "realization_status": entry.get("realization_status"),
        })
        if not row["program_id"]:
            raise BuildError(f"recovery entry {eid} missing program_id")
        by_program.setdefault(row["program_id"], []).append(row)
        all_rows.append(row)
    check_overlap_rules(all_rows)
    return by_program, all_rows

def build_changes(baseline, programs, all_events, recovery_rows):
    current_metrics = {}
    for program in programs:
        for metric in program.get("legal_metrics") or []:
            current_metrics[metric["metric_id"]] = metric.get("value")

    metric_changes = []
    for metric_id, old_value in (baseline.get("legal_metrics") or {}).items():
        if metric_id not in current_metrics:
            raise BuildError(f"baseline metric disappeared from tracker: {metric_id}")
        new_value = current_metrics[metric_id]
        if new_value != old_value:
            metric_changes.append({
                "metric_id": metric_id,
                "before": old_value,
                "after": new_value,
            })

    baseline_events = set(baseline.get("event_ids") or [])
    new_events = [e for e in all_events if e.get("event_id") not in baseline_events]
    baseline_recovery = set(baseline.get("recovery_entry_ids") or [])
    new_recovery = [r for r in recovery_rows if r.get("entry_id") not in baseline_recovery]

    return {
        "since_snapshot": baseline.get("snapshot_id"),
        "snapshot_date": baseline.get("snapshot_date"),
        "legal_metric_changes": metric_changes,
        "new_events": new_events,
        "new_recovery_entries": new_recovery,
        "change_count": len(metric_changes) + len(new_events) + len(new_recovery),
    }

def main():
    corpus = load(RECORD)
    config = load(PROGRAMS)
    event_doc = load(EVENTS)
    controls = load(CONTROLS)
    recovery_doc = load(RECOVERY)
    baseline = load(SNAPSHOT)
    claims = index_json(RESEARCH / "claims", "claim_id")
    sources = index_json(RESEARCH / "sources", "source_id")

    events_by_program = validate_event_sequence(event_doc.get("events", []), sources)
    recovery_by_program, recovery_rows = recovery_projection(recovery_doc, sources)

    controls_public = timeline_projection(controls, sources)
    programs_out = []
    used_sources = set()

    for program in config.get("programs", []):
        pid = program["program_id"]
        purpose_sids = require_sources(program.get("purpose_source_ids") or [], sources, f"program purpose {pid}")
        used_sources.update(purpose_sids)

        facts = []
        for cid in program.get("claim_ids") or []:
            claim = claims.get(cid)
            if not claim:
                raise BuildError(f"tracker selects unknown claim {cid!r}")
            fact = fact_from_claim(claim, sources)
            used_sources.update(fact["source_ids"])
            facts.append(fact)

        metrics = []
        for mid in program.get("legal_metric_ids") or []:
            metric = active_metric(mid, claims, sources)
            used_sources.update(metric["source_ids"])
            metrics.append(metric)

        cases, family_money = ([], [])
        if program.get("family_id"):
            cases, family_money = family_case_projection(program["family_id"], corpus, sources)

        pevents = events_by_program.get(program.get("event_program_id"), [])
        for event in pevents:
            used_sources.update(source_ids_for(event))

        reform_events = []
        if pid in {"hss", "eidbi", "medicaid-program-integrity"}:
            for event in controls_public:
                p = (event.get("program") or "").lower()
                if pid == "hss" and "hss" not in p and "housing stabilization" not in p:
                    continue
                if pid == "eidbi" and "eidbi" not in p:
                    continue
                if pid == "medicaid-program-integrity" and event.get("program"):
                    continue
                reform_events.append(event)
                used_sources.update(event["source_ids"])
            if pid == "medicaid-program-integrity":
                for event in pevents:
                    if event.get("event_type") == "MEASUREMENT_PUBLISHED":
                        reform_events.append({
                            "event_date": event.get("occurred_at"),
                            "event_type": "measurement_published",
                            "actor": "Minnesota DHS",
                            "program": "Minnesota Medicaid",
                            "summary": event.get("summary"),
                            "evidence_class": "AGENCY_POSITION",
                            "implementation_state": "MEASURED",
                            "effectiveness": event.get("effectiveness", "UNKNOWN"),
                            "qualification": "Activity/output measures do not by themselves prove effectiveness.",
                            "source_ids": source_ids_for(event),
                            "measures": event.get("measures") or [],
                        })

        explicit_money = []
        for fact in facts:
            for amount in fact["money"]:
                row = dict(amount)
                row["claim_id"] = fact["claim_id"]
                row["status"] = fact["status"]
                row["source_ids"] = fact["source_ids"]
                explicit_money.append(row)
        for event in pevents:
            for measure in event.get("measures") or []:
                if measure.get("unit") != "USD":
                    continue
                row = normalize_money(measure, f"event measure {event.get('event_id')}")
                row["event_id"] = event.get("event_id")
                row["status"] = event.get("implementation_state") or event.get("event_type")
                row["source_ids"] = source_ids_for(event)
                explicit_money.append(row)

        for row in family_money:
            used_sources.update(row.get("source_ids") or [])
        for case in cases:
            used_sources.update(case.get("source_ids") or [])

        program_recovery = recovery_by_program.get(pid, [])
        for row in program_recovery:
            used_sources.update(row.get("source_ids") or [])

        programs_out.append({
            "program_id": pid,
            "name": program["name"],
            "purpose": program["purpose"],
            "purpose_source_ids": purpose_sids,
            "legal_metrics": metrics,
            "facts": facts,
            "cases": cases,
            "money": family_money + explicit_money,
            "events": pevents,
            "reform_events": reform_events,
            "recovery": program_recovery,
            "unknowns": {
                "charged_count": None if not any(m["metric_id"].endswith("charged-count") for m in metrics) else "SEE_METRIC",
                "convicted_count": None if not any(m["metric_id"].endswith("convicted-count") for m in metrics) else "SEE_METRIC",
                "sentenced_count": None if not any(m["metric_id"].endswith("sentenced-count") for m in metrics) else "SEE_METRIC",
                "recovery_total": None,
                "effectiveness": None,
            },
        })

    changes = build_changes(baseline, programs_out, event_doc.get("events", []), recovery_rows)
    source_list = [source_public(sources[sid]) for sid in sorted(used_sources)]
    verified_dates = [s.get("retrieval_date") for s in source_list if s.get("retrieval_date")]
    out = {
        "schema_version": 1,
        "generated_from": {
            "record_corpus_generated_at": corpus.get("generated_at"),
            "program_selection": "research/programs/tracker-programs-v1.json",
            "accountability_events": "research/events/accountability-events-v1.json",
            "control_timeline": "research/oversight/medicaid-control-timeline.json",
            "recovery_selection": "research/money/tracker-recovery-v1.json",
            "comparison_snapshot": "research/snapshots/tracker-v1-2026-09-30.json",
        },
        "last_verified": max(verified_dates) if verified_dates else None,
        "do_not_conflate": [
            "charged, pleaded, convicted, and sentenced",
            "alleged loss, program spending, adjudicated amount, restitution, forfeiture, recovery, cost avoidance",
            "announced, enacted, implemented, measured, and effective",
        ],
        "changes": changes,
        "recovery_rules": recovery_doc.get("rules") or [],
        "programs": programs_out,
        "sources": source_list,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"tracker built: {OUT.relative_to(ROOT)} ({len(programs_out)} programs, {len(source_list)} sources)")

if __name__ == "__main__":
    main()
