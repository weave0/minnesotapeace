#!/usr/bin/env python3
"""Build research/viewer/data/corpus.json from canonical claims, extracts, sources, entities.

Research is a non-public substrate. A claim, source, or entity existing under research/
does not make it public. Only artifacts listed -- by ID and exact content hash -- in the
publication manifest (research/publication/record-v1.json) are emitted to corpus["claims"],
corpus["sources"], corpus["entities"], or corpus["money"]. Everything else in research/
claims, research/sources, research/entities is loaded only to validate the manifest against
it (existence, hash match, referential integrity) and is otherwise invisible to the output.

Does not invent claims. Does not sum overlapping dollars. Skips the leftover Farah
ECF 57 stub (empty count map). Asad 0:25-cr-00354 is emitted as a gap card.

Run from repo root:  python3 research/viewer/build.py
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAIMS_DIR = ROOT / "research" / "claims"
EXTRACTS_DIR = ROOT / "research" / "court" / "extracts"
SOURCES_DIR = ROOT / "research" / "sources"
ENTITIES_DIR = ROOT / "research" / "entities"
MANIFEST_PATH = ROOT / "research" / "publication" / "record-v1.json"
OUT_DIR = Path(__file__).resolve().parent / "data"
PUBLIC_DATA_DIR = ROOT / "record" / "data"
SKIP_EXTRACTS = {"farah-22-cr-124-ecf57-superseding.json"}

# Catalog of charging instruments this viewer exposes. Metadata describes documents
# already in the corpus; it does not add dollar figures that are not in claims/.
CASES = [
    {
        "id": "bock-22cr223",
        "family": "feeding-our-future",
        "docket": "0:22-cr-00223",
        "short_name": "Bock",
        "extract_file": "bock-22-cr-223-ecf1.json",
        "source_ids": [],
        "primary_claim_ids": [],
        "count_n": 61,
        "count_label": "61 counts (ECF 1 indictment)",
        "instrument": "indictment",
        "ecf": 1,
        "gap": False,
        "primary_dollar_note": "This extract maps counts; it does not isolate a case-level billed or paid total. The $250 million Feeding Our Future charging headline is a DOJ press-release alleged_loss / fraud_estimate in the family harvest, not a claim-*.json taken from the face of this indictment. Do not display it here as proven_loss.",
    },
    {
        "id": "farah-22cr124",
        "family": "feeding-our-future",
        "docket": "0:22-cr-00124",
        "short_name": "Farah / Empire",
        "extract_file": "farah-22-cr-124-ecf57.json",
        "related_extract_files": ["farah-22-cr-124-ecf22-passport.json"],
        "source_ids": ["src-mnd-22-cr-00124-ecf57-farah-superseding"],
        "primary_claim_ids": ["claim-farah-22cr124-ecf57-40m-scheme"],
        "count_n": 43,
        "count_label": "43 counts (ECF 57 superseding indictment)",
        "instrument": "superseding_indictment",
        "ecf": 57,
        "gap": False,
        "related_instruments": [
            {
                "ecf": 22,
                "instrument": "indictment",
                "note": "One-count 18 U.S.C. § 1542 passport application (Abdiaziz Shafii Farah only). Not the Feeding Our Future / Empire fraud charging instrument. The fraud counts are ECF 57.",
            }
        ],
    },
    {
        "id": "mohamed-24cr015",
        "family": "feeding-our-future",
        "docket": "0:24-cr-00015",
        "short_name": "Mohamed family",
        "extract_file": "mohamed-24-cr-015-ecf1.json",
        "source_ids": ["src-mnd-24-cr-00015-ecf1-mohamed-indictment"],
        "primary_claim_ids": ["claim-mohamed-24cr015-ecf1-family-received-12m"],
        "count_n": 47,
        "count_label": "47 counts (ECF 1 indictment)",
        "instrument": "indictment",
        "ecf": 1,
        "gap": False,
    },
    {
        "id": "aden-25cr349",
        "family": "hss",
        "docket": "0:25-cr-00349",
        "short_name": "Aden / Brilliant Minds",
        "extract_file": "aden-25-cr-349-ecf1.json",
        "source_ids": ["src-mnd-25-cr-00349-ecf1-aden-indictment"],
        "primary_claim_ids": ["claim-aden-25cr349-brilliant-minds-amount-billed"],
        "count_n": 6,
        "count_label": "6 counts, 18 U.S.C. § 1343 (wire fraud)",
        "instrument": "indictment",
        "ecf": 1,
        "gap": False,
    },
    {
        "id": "falade-25cr351",
        "family": "hss",
        "docket": "0:25-cr-00351",
        "short_name": "Falade / Faladcare",
        "extract_file": "falade-25-cr-351-ecf1.json",
        "source_ids": ["src-mnd-25-cr-00351-ecf1-falade-indictment"],
        "primary_claim_ids": ["claim-falade-25cr351-faladcare-amount-billed"],
        "count_n": 4,
        "count_label": "4 counts, 18 U.S.C. § 1343 (wire fraud)",
        "instrument": "indictment",
        "ecf": 1,
        "gap": False,
    },
    {
        "id": "anwar-adow-25cr353",
        "family": "hss",
        "docket": "0:25-cr-00353",
        "short_name": "Anwar Adow / Liberty Plus",
        "extract_file": "anwar-adow-25-cr-353-ecf1.json",
        "source_ids": ["src-us-v-adow-anwar-25cr353-ecf1"],
        "primary_claim_ids": ["claim-adow-anwar-liberty-plus-received-1.2m"],
        "count_n": 4,
        "count_label": "4 counts, 18 U.S.C. § 1343 (felony information, not an indictment)",
        "instrument": "felony_information",
        "ecf": 1,
        "gap": False,
        "plea_note": "CourtListener docket minute ECF 7 (2025-10-23): guilty as to Count 1 of the information. That is a docket-minute fact, not a judgment. Plea agreement ECF 9 is not on RECAP. Do not mark ADJUDICATED.",
    },
    {
        "id": "asad-adow-25cr354",
        "family": "hss",
        "docket": "0:25-cr-00354",
        "short_name": "Asad Adow / Leo Human Services",
        "extract_file": None,
        "source_ids": ["src-mnd-25-cr-00354-adow-asad-recap-gap"],
        "primary_claim_ids": [],
        "count_n": None,
        "count_label": "Counts not mapped — felony information not on RECAP",
        "instrument": "felony_information",
        "ecf": 1,
        "gap": True,
        "gap_kind": "recap_missing_information",
        "caption": "United States v. Asad Ahmed Adow",
        "defendants": ["Asad Ahmed Adow"],
        "provider": "Leo Human Services LLC",
        "entity_ids": ["org-leo-human-services"],
        "courtlistener_url": "https://www.courtlistener.com/docket/71379215/united-states-v-adow/",
        "gap_notes": [
            "Felony information ECF 1 is needed, not nonexistent. CourtListener docket 71379215 exists. RECAP is_available=false as of 2026-08-27 (no PACER purchase).",
            "Waiver ECF 13 and plea agreement ECF 14 are also unavailable on RECAP.",
            "Docket minute ECF 12 (2025-11-17) records guilty as to Count 1. That is not a judgment. Do not mark ADJUDICATED.",
            "No local count map. No claim-*.json dollar from the face of the information, because the information is not in the corpus.",
            "Related-case notices point at 25-cr-479 and 25-cr-482; those are separate charging instruments, not charges against Asad.",
        ],
    },
    {
        "id": "hussein-25cr479",
        "family": "hss",
        "docket": "0:25-cr-00479",
        "short_name": "Hussein / Pristine Health",
        "extract_file": "hussein-25-cr-479-ecf1.json",
        "source_ids": ["src-mnd-25-cr-00479-ecf1-hussein-indictment"],
        "primary_claim_ids": ["claim-hussein-25cr479-pristine-amount-claimed"],
        "count_n": 5,
        "count_label": "5 counts, 18 U.S.C. § 1343 (wire fraud)",
        "instrument": "indictment",
        "ecf": 1,
        "gap": False,
    },
    {
        "id": "sallah-25cr482",
        "family": "hss",
        "docket": "0:25-cr-00482",
        "short_name": "Sallah / SafeLodgings",
        "extract_file": "sallah-25-cr-482-ecf1.json",
        "source_ids": ["src-mnd-25-cr-00482-ecf1-sallah-indictment"],
        "primary_claim_ids": ["claim-sallah-25cr482-safelodgings-claimed-and-received"],
        "count_n": 4,
        "count_label": "4 counts, 18 U.S.C. § 1343 (wire fraud)",
        "instrument": "indictment",
        "ecf": 1,
        "gap": False,
    },
]

GAPS = [
    {
        "id": "asad-354-recap",
        "title": "Asad Adow 0:25-cr-00354 felony information is off RECAP",
        "detail": "Docket identity is confirmed (counts 1–4, filed 2025-09-18, waiver of indictment 2025-11-17). RECAP is_available=false. Needed, not nonexistent. No local count map.",
        "case_id": "asad-adow-25cr354",
    },
    {
        "id": "judgments-missing",
        "title": "Judgments and plea-agreement PDFs are mostly missing",
        "detail": "Guilty-plea docket minutes are not judgments. Anwar Adow 25-cr-353 ECF 7 (2025-10-23) and Asad Adow 25-cr-354 ECF 12 (2025-11-17) record Count 1 guilt as court-minute facts. Plea agreements (353 ECF 9, 354 ECF 14) are not on RECAP. Do not upgrade charged → pleaded → sentenced from journalism.",
        "case_id": None,
    },
    {
        "id": "bock-bribe-ocr",
        "title": "Bock 0:22-cr-00223 bribe-table OCR gaps",
        "detail": "ECF 1 count map is in the corpus. Bribe-table row numbers 23–24, 30, 32, 34, and 37 are garbled on OCR. Forfeiture property list is not itemized. The extract does not isolate a case-level billed/paid total.",
        "case_id": "bock-22cr223",
    },
    {
        "id": "anwar-cl-url",
        "title": "Anwar Adow 0:25-cr-00353 source record has no CourtListener URL",
        "detail": "The felony information is locally archived and count-mapped. src-us-v-adow-anwar-25cr353-ecf1 has canonical_url null. Local PDF + SHA-256 remain the durable copy.",
        "case_id": "anwar-adow-25cr353",
    },
]

FAMILIES = [
    {
        "id": "feeding-our-future",
        "name": "Feeding Our Future / child nutrition",
        "blurb": "Federal Child Nutrition Program (CACFP/SFSP) prosecutions in D. Minnesota. Charging instruments in this viewer: Bock 0:22-cr-00223, Farah/Empire 0:22-cr-00124 ECF 57, Mohamed family 0:24-cr-00015. Feeding Our Future II is a separate SOS nonprofit and is not merged into Feeding Our Future.",
    },
    {
        "id": "hss",
        "name": "Housing Stabilization Services (HSS)",
        "blurb": "Minnesota Medicaid Housing Stabilization Services. First-wave dockets 25-cr-349 / 351 / 353 / 354, plus later 25-cr-479 and 25-cr-482. Statewide program_spend recitals ($21M / $42M / $74M / $104M / $61M) are background on charging documents, not case alleged_loss.",
    },
]

SLIM_DROP = {
    "ocr_corrections",
    "ocr_engine",
    "ocr_dpi",
    "ocr_text",
    "bytes",
    "recap_path",
    "pacer_case_id_note",
    "gaps",  # some extracts still say Empire ECF 57 is missing; that is stale
}


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    """Hash file content, not file bytes.

    Approval must not flap depending on whether the working tree currently
    has CRLF or LF line endings (Windows vs. Linux CI, or a local
    core.autocrlf setting) when nothing about the JSON content changed.
    Normalize line endings before hashing so the same logical content
    always produces the same approval hash on every platform.
    """
    normalized = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def index_by_field(directory: Path, glob: str, id_field: str, kind: str) -> dict[str, Path]:
    """Glob directory for files matching glob and index by their internal id_field.

    Filenames in this corpus do not reliably match their internal IDs (e.g.
    research/claims/claim-fof-990-officers.json has claim_id
    "claim-fof-990-fy2020-officers"), so the manifest must be checked against
    internal IDs discovered by reading every file, not against guessed paths.
    """
    by_id: dict[str, Path] = {}
    for path in sorted(directory.glob(glob)):
        try:
            obj = load_json(path)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        ident = obj.get(id_field)
        if not ident:
            raise SystemExit(f"{path.relative_to(ROOT)} has no {id_field}")
        if ident in by_id:
            raise SystemExit(
                f"duplicate {kind} id {ident!r} in research/: "
                f"{by_id[ident].relative_to(ROOT)} and {path.relative_to(ROOT)}"
            )
        by_id[ident] = path
    return by_id


# Every manifest section (claims, sources, entities) uses the same shape:
# a list of {<id_field>: ..., "sha256": ...}. Approval attaches to a specific
# reviewed byte-for-byte version of the file, not merely to its identity --
# a plain ID allowlist would let someone materially rewrite an
# already-approved source or entity (including its `notes` field) and have
# it keep publishing unreviewed, since only the ID would need to still match.
MANIFEST_SECTIONS = {
    "claims": "claim_id",
    "sources": "source_id",
    "entities": "entity_id",
}


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        raise SystemExit(
            f"publication manifest missing: {MANIFEST_PATH.relative_to(ROOT)}. "
            "Research is a non-public substrate -- nothing publishes without an explicit, "
            "hash-pinned manifest entry."
        )
    manifest = load_json(MANIFEST_PATH)
    if manifest.get("schema_version") != 1:
        raise SystemExit(f"unsupported publication manifest schema_version: {manifest.get('schema_version')!r}")

    for section, id_field in MANIFEST_SECTIONS.items():
        seen: set[str] = set()
        for entry in manifest.get(section, []):
            ident = entry.get(id_field) if isinstance(entry, dict) else None
            sha = entry.get("sha256") if isinstance(entry, dict) else None
            if not ident or not sha:
                raise SystemExit(
                    f"malformed manifest {section} entry (expected {{{id_field!r}, 'sha256'}}): {entry!r}"
                )
            if ident in seen:
                raise SystemExit(f"duplicate {id_field} in publication manifest {section}: {ident}")
            seen.add(ident)

    return manifest


def resolve_approved(
    section: str, manifest: dict, index: dict[str, Path], dir_name: str
) -> tuple[list[dict], set[str]]:
    """Validate one manifest section against the files it names.

    Returns (loaded JSON objects in manifest order, set of approved ids).
    Fatal on: unknown id (manifest names something research/ doesn't have),
    or hash mismatch (the file changed since it was approved).
    """
    id_field = MANIFEST_SECTIONS[section]
    approved_objs: list[dict] = []
    approved_ids: set[str] = set()
    for entry in manifest.get(section, []):
        ident = entry[id_field]
        path = index.get(ident)
        if path is None:
            raise SystemExit(
                f"publication manifest approves {section[:-1]} {ident!r}, but no matching "
                f"research/{dir_name}/*.json file declares that {id_field}. Unknown manifest id."
            )
        actual_hash = sha256_file(path)
        if actual_hash != entry["sha256"]:
            raise SystemExit(
                f"publication manifest hash mismatch for {section[:-1]} {ident!r} ({path.relative_to(ROOT)}).\n"
                f"  manifest sha256: {entry['sha256']}\n"
                f"  actual   sha256: {actual_hash}\n"
                f"The canonical {section[:-1]} file changed since it was approved for publication. "
                "Re-review it and update its sha256 in "
                f"{MANIFEST_PATH.relative_to(ROOT)} to renew approval, or revert the file."
            )
        approved_objs.append(load_json(path))
        approved_ids.add(ident)
    return approved_objs, approved_ids


def collect_source_references(claims: list[dict], entities: list[dict], cases_specs: list[dict]) -> dict[str, list[str]]:
    """Every place a source_id can survive slimming into public output.

    Returns {source_id: [human-readable locations citing it]}, so an
    unapproved reference can be reported with enough context to fix it
    instead of just failing with a bare id.
    """
    refs: dict[str, list[str]] = {}

    def add(source_id: str | None, where: str) -> None:
        if not source_id:
            return
        refs.setdefault(source_id, []).append(where)

    for claim in claims:
        cid = claim.get("claim_id", "?")
        for sid in claim.get("source_ids") or []:
            add(sid, f"claim {cid!r} source_ids")
        for passage in claim.get("supporting_passages") or []:
            add(passage.get("source_id"), f"claim {cid!r} supporting_passages")

    for entity in entities:
        eid = entity.get("entity_id", "?")
        for sid in entity.get("source_ids") or []:
            add(sid, f"entity {eid!r} source_ids")
        for officer in entity.get("officers") or []:
            for sid in officer.get("source_ids") or []:
                add(sid, f"entity {eid!r} officer {officer.get('name')!r} source_ids")

    for spec in cases_specs:
        for sid in spec.get("source_ids") or []:
            add(sid, f"case {spec.get('id')!r} source_ids")

    return refs


def enforce_source_referential_closure(refs: dict[str, list[str]], approved_source_ids: set[str]) -> None:
    unapproved = {sid: where for sid, where in refs.items() if sid not in approved_source_ids}
    if not unapproved:
        return
    lines = [
        "publication references source id(s) that are not (or no longer) approved in "
        f"{MANIFEST_PATH.relative_to(ROOT)}:"
    ]
    for sid, where in sorted(unapproved.items()):
        lines.append(f"  {sid!r} cited by: {', '.join(where)}")
    lines.append(
        "Add each source to the manifest's sources section (with its content sha256), "
        "or remove the citation."
    )
    raise SystemExit("\n".join(lines))


def docket_key(value: str | None) -> str | None:
    if not value:
        return None
    m = re.search(r"(0:\d{2}-cr-\d+)", value, re.I)
    return m.group(1).lower() if m else None


def defendant_names(extract: dict | None, case: dict) -> list[str]:
    if case.get("gap"):
        return list(case.get("defendants") or [])
    if not extract:
        return []
    cap = extract.get("defendants_caption")
    names: list[str] = []
    if isinstance(cap, list):
        for item in cap:
            if isinstance(item, str):
                names.append(item)
            elif isinstance(item, dict) and item.get("name"):
                names.append(item["name"])
    elif extract.get("defendant"):
        names.append(extract["defendant"])
    return names


def provider_names(extract: dict | None, case: dict) -> list[dict]:
    if case.get("gap"):
        name = case.get("provider")
        return [{"name": name, "entity_id": (case.get("entity_ids") or [None])[0]}] if name else []
    if not extract:
        return []
    providers = extract.get("providers")
    out = []
    if isinstance(providers, list):
        for p in providers:
            if isinstance(p, dict):
                out.append(
                    {
                        "name": p.get("name"),
                        "entity_id": p.get("entity_id"),
                        "role_on_face": p.get("role_on_face"),
                    }
                )
            elif isinstance(p, str):
                out.append({"name": p, "entity_id": None, "role_on_face": None})
    elif extract.get("provider"):
        out.append({"name": extract["provider"], "entity_id": None, "role_on_face": None})
    return out


def slim_extract(extract: dict) -> dict:
    slim = {k: v for k, v in extract.items() if k not in SLIM_DROP}
    forfeiture = slim.get("forfeiture")
    if isinstance(forfeiture, dict):
        keep = {k: forfeiture[k] for k in ("pages", "starts_page", "statutes", "notes") if k in forfeiture}
        slim["forfeiture"] = keep
    # Farah uses dollar_figures; expose as amounts for the UI.
    if "amounts" not in slim and isinstance(slim.get("dollar_figures"), list):
        slim["amounts"] = slim["dollar_figures"]
    return slim


def flatten_counts(extract: dict | None) -> list[dict]:
    if not extract:
        return []
    rows: list[dict] = []
    for block in extract.get("counts") or []:
        if not isinstance(block, dict):
            continue
        nested = block.get("rows") or block.get("bribe_rows_ocr")
        if isinstance(nested, list) and nested:
            for row in nested:
                if not isinstance(row, dict):
                    continue
                rows.append(
                    {
                        "count": row.get("count", block.get("count")),
                        "statute": block.get("statute"),
                        "title": block.get("title"),
                        "date": row.get("date_on_or_about") or row.get("date"),
                        "wire": row.get("wire"),
                        "named_defendants": row.get("defendants_ocr")
                        or row.get("named_defendants")
                        or block.get("named_defendants"),
                        "amount_usd": row.get("amount_usd"),
                        "from": row.get("from"),
                        "to": row.get("to"),
                        "page": row.get("page") or block.get("page"),
                        "notes": row.get("ocr_note") or row.get("notes"),
                    }
                )
        else:
            rows.append(
                {
                    "count": block.get("count"),
                    "statute": block.get("statute"),
                    "title": block.get("title"),
                    "date": block.get("date_on_or_about") or block.get("period"),
                    "wire": block.get("wire") or block.get("wires"),
                    "named_defendants": block.get("named_defendants"),
                    "page": block.get("page") or block.get("pages"),
                    "notes": block.get("notes") or block.get("allegation"),
                }
            )
    return rows


def slim_source(src: dict) -> dict:
    keys = (
        "source_id",
        "title",
        "canonical_url",
        "archive_url",
        "issuing_body",
        "document_type",
        "document_date",
        "publication_date",
        "retrieval_date",
        "case_number",
        "court",
        "docket_id",
        "local_path",
        "sha256",
        "page_count",
        "access_status",
        "source_tier",
        "source_status",
        "notes",
    )
    return {k: src.get(k) for k in keys}


def slim_entity(ent: dict) -> dict:
    keys = (
        "entity_id",
        "entity_type",
        "canonical_name",
        "aliases",
        "former_names",
        "dba",
        "ein",
        "business_reg_ids",
        "officers",
        "addresses",
        "notes",
        "source_ids",
    )
    return {k: ent.get(k) for k in keys if k in ent}


def slim_claim(claim: dict) -> dict:
    keys = (
        "claim_id",
        "claim_text",
        "normalized_claim",
        "claim_type",
        "status",
        "evidence_class",
        "proposition_class",
        "source_ids",
        "supporting_passages",
        "amounts",
        "qualifiers",
        "editorial_notes",
        "case_number",
        "subject_ids",
        "organizations",
        "persons",
        "jurisdiction",
        "confidence",
        "is_allegation",
        "is_inference",
        "date_start",
        "date_end",
        "event_date",
        "reviewed_at",
    )
    return {k: claim.get(k) for k in keys if k in claim}


def overlap_label(group_id: str) -> str:
    labels = {
        "aden-brilliant-minds-2.3m-claims": "Aden — Brilliant Minds ~$2.3M claims (do not sum restatements)",
        "aden-brilliant-minds-personal-pocketing-range": "Aden — personal pocketing range (overlaps billed $2.3M; do not ×4)",
        "aden-brilliant-minds-amex-charges": "Aden — Amex charges from Brilliant Minds accounts (overlaps billed)",
        "aden-foundation-first-222k-claims": "Aden — Foundation First ~$222k claims (separate provider; do not silently add to $2.3M as one loss)",
        "falade-faladcare-2.2m-claims": "Falade — Faladcare >$2.2M claims (do not sum restatements)",
        "hss-adow-liberty-plus": "Anwar Adow — Liberty Plus >$1.2M received",
        "hss-statewide-program-payouts-2021-2025h1-indictment-recital": "HSS statewide program_spend recital (not case alleged_loss; identical boilerplate)",
        "hss-program-spend-adow-para8": "Anwar information ¶8 — HSS statewide program_spend (not Liberty Plus $1.2M)",
        "hussein-pristine-health-750k-claims": "Hussein — Pristine Health ~$750k claimed (do not sum restatements)",
        "sallah-safelodgings-1.4m-claimed-1.3m-received": "Sallah — $1.4M claimed and $1.3M received (same overlap group; do not add)",
        "empire-22cr124-40m-scheme": "Farah ECF 57 — Empire-group $40M (do not add to Bock $250M)",
        "fof-network-scheme-size": "FOF sponsor-wide recitals (overlap Bock network headline; not extra loss)",
        "sponsor-a-network-scheme-size": "Sponsor A recitals (not Empire $40M; not FOF $200M)",
        "mohamed-24cr015-family-receipts": "Mohamed family receipts (>$12M; site receipts are subsets)",
        "mohamed-24cr015-star-distribution": "Mohamed — Star Distribution ~$10M (overlaps family $12M)",
        "mohamed-24cr015-afrique-ikram": "Mohamed — Afrique / Ikram (overlaps family receipts)",
        "pin-990-fy2021": "Partners In Nutrition FY2021 Form 990 as-filed (not FOF loss)",
    }
    if group_id in labels:
        return labels[group_id]
    return group_id.replace("-", " ")


def build_money_rows(claims: list[dict]) -> list[dict]:
    rows = []
    for claim in claims:
        for i, amt in enumerate(claim.get("amounts") or []):
            if not isinstance(amt, dict) or amt.get("value") is None:
                continue
            if not amt.get("metric_type"):
                raise SystemExit(f"amount missing metric_type on {claim.get('claim_id')}")
            overlap = amt.get("overlap_group_id") or f"ungrouped:{claim['claim_id']}:{i}"
            rows.append(
                {
                    "row_id": f"{claim['claim_id']}#{i}",
                    "claim_id": claim["claim_id"],
                    "case_number": claim.get("case_number"),
                    "value": amt["value"],
                    "currency": amt.get("currency") or "USD",
                    "metric_type": amt["metric_type"],
                    "exact_or_approximate": amt.get("exact_or_approximate"),
                    "period_start": amt.get("period_start"),
                    "period_end": amt.get("period_end"),
                    "overlap_group_id": overlap,
                    "overlap_label": overlap_label(overlap) if amt.get("overlap_group_id") else "Ungrouped (single-claim figure)",
                    "methodology": amt.get("methodology"),
                    "evidence_class": claim.get("evidence_class"),
                    "status": claim.get("status"),
                    "qualifiers": claim.get("qualifiers") or [],
                }
            )
    return rows


def main() -> None:
    manifest = load_manifest()

    claim_index = index_by_field(CLAIMS_DIR, "claim-*.json", "claim_id", "claim")
    source_index = index_by_field(SOURCES_DIR, "src-*.json", "source_id", "source")
    entity_index = index_by_field(ENTITIES_DIR, "org-*.json", "entity_id", "entity")

    approved_claims_raw, _ = resolve_approved("claims", manifest, claim_index, "claims")
    approved_sources_raw, approved_source_ids = resolve_approved("sources", manifest, source_index, "sources")
    approved_entities_raw, approved_entity_ids = resolve_approved("entities", manifest, entity_index, "entities")

    claims = [slim_claim(c) for c in approved_claims_raw]
    claims_by_id = {c["claim_id"]: c for c in claims}
    entities = [slim_entity(e) for e in approved_entities_raw]

    # Referential closure: a published claim, entity (including its officers),
    # or hardcoded case spec may not cite a source that isn't itself approved
    # for publication -- at its currently-approved hash. Research-only
    # sources (and whatever is in their `notes`) must not leak into the
    # public record just because something approved points at them.
    source_refs = collect_source_references(claims, entities, CASES)
    enforce_source_referential_closure(source_refs, approved_source_ids)

    sources = {
        src["source_id"]: slim_source(src)
        for src in approved_sources_raw
    }

    extracts: dict[str, dict] = {}
    for path in sorted(EXTRACTS_DIR.glob("*.json")):
        if path.name in SKIP_EXTRACTS:
            continue
        extracts[path.name] = load_json(path)

    cases_out = []
    for spec in CASES:
        extract = None
        if spec.get("extract_file"):
            extract = extracts.get(spec["extract_file"])
            if extract is None:
                raise SystemExit(f"missing extract {spec['extract_file']}")
        related = []
        for rel in spec.get("related_extract_files") or []:
            related.append(slim_extract(extracts[rel]))

        docket = spec["docket"]
        dkey = docket_key(docket)
        linked_claims = [
            c["claim_id"]
            for c in claims
            if docket_key(c.get("case_number")) == dkey
        ]
        # Also attach claims that name this docket only in text? No — stick to case_number.

        primary_amounts = []
        for cid in spec.get("primary_claim_ids") or []:
            claim = claims_by_id.get(cid)
            if not claim:
                raise SystemExit(f"primary claim missing: {cid}")
            for amt in claim.get("amounts") or []:
                primary_amounts.append(
                    {
                        "claim_id": cid,
                        "value": amt.get("value"),
                        "metric_type": amt.get("metric_type"),
                        "exact_or_approximate": amt.get("exact_or_approximate"),
                        "overlap_group_id": amt.get("overlap_group_id"),
                        "methodology": amt.get("methodology"),
                        "evidence_class": claim.get("evidence_class"),
                    }
                )

        caption = None
        if extract:
            caption = extract.get("caption") or extract.get("short_caption")
        elif spec.get("caption"):
            caption = spec["caption"]

        case_obj = {
            "id": spec["id"],
            "family": spec["family"],
            "docket": docket,
            "short_name": spec["short_name"],
            "caption": caption,
            "instrument": spec["instrument"],
            "ecf": spec.get("ecf"),
            "filed": (extract or {}).get("filed"),
            "court": (extract or {}).get("court") or "United States District Court, District of Minnesota",
            "header_case_id": (extract or {}).get("header_case_id"),
            "pages": (extract or {}).get("pages"),
            "sha256": (extract or {}).get("sha256"),
            "source_pdf": (extract or {}).get("source_pdf"),
            "evidence_class": (extract or {}).get("evidence_class") or "CHARGED_ALLEGED",
            "evidentiary_status": (extract or {}).get("evidentiary_status") or "CHARGED_ALLEGED",
            "not_adjudicated": True if spec.get("gap") else (extract or {}).get("not_adjudicated", True),
            "count_n": spec.get("count_n"),
            "count_label": spec.get("count_label"),
            "defendants": defendant_names(extract, spec),
            "providers": provider_names(extract, spec),
            "source_ids": spec.get("source_ids") or [],
            "claim_ids": linked_claims,
            "primary_claim_ids": spec.get("primary_claim_ids") or [],
            "primary_amounts": primary_amounts,
            "primary_dollar_note": spec.get("primary_dollar_note"),
            "plea_note": spec.get("plea_note") or (extract or {}).get("docket_plea_lead"),
            "do_not": (extract or {}).get("do_not") or [],
            "counts": flatten_counts(extract),
            "extract_amounts": (slim_extract(extract).get("amounts") if extract else []) or [],
            "statewide_recital": (extract or {}).get("statewide_hss_program_payouts_recital"),
            "related_instruments": spec.get("related_instruments") or [],
            "related_extracts": related,
            "gap": spec.get("gap", False),
            "gap_kind": spec.get("gap_kind"),
            "gap_notes": spec.get("gap_notes") or [],
            "courtlistener_url": spec.get("courtlistener_url"),
            "editorial": (extract or {}).get("editorial"),
            "quotes": (extract or {}).get("quotes"),
        }
        cases_out.append(case_obj)

    money_rows = build_money_rows(claims)

    # Sanity: never emit a 9e9 fraud total; never emit a homepage_total field.
    forbidden = [r for r in money_rows if r["value"] == 9_000_000_000]
    if forbidden:
        raise SystemExit("refusing to emit a $9 billion money row")

    corpus = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "corpus_name": "MinnesotaPeace public-program fraud research corpus",
        "viewer": "research/viewer v1",
        "mandate": "Citation-rich investigative corpus. The atomic unit is a claim, not an article. This viewer is The Record inside MinnesotaPeace.com — not a fraud-total dashboard.",
        "editorial_rules": [
            "Never show a TOTAL FRAUD number. Never sum overlapping dollars.",
            "Every displayed dollar carries metric_type and evidence_class.",
            "Do not treat circulating press-conference estimates as proven_loss or as a homepage total.",
            "Shared address is not conspiracy. Do not draw guilt edges from SOS street overlap.",
            "Actor classes: (A) private fraud against programs, (B) agency oversight failure, (C) negligence, (D) official knowing duty violation, (E) official knowing crime. v1 does not claim D/E.",
            "Do not upgrade charged → pleaded → sentenced from journalism. Guilty-plea docket minutes are not judgments.",
            "AI-generated statements are not sources. Cite the JSON claim’s source_ids.",
        ],
        "families": FAMILIES,
        "gaps": GAPS,
        "cases": cases_out,
        "claims": claims,
        "sources": sources,
        "entities": entities,
        "money": money_rows,
        "skipped_extracts": sorted(SKIP_EXTRACTS),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "corpus.json"
    json_path.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    js_path = OUT_DIR / "corpus.js"
    js_path.write_text(
        "window.__CORPUS__ = " + json.dumps(corpus, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    stats = {
        "generated_at": corpus["generated_at"],
        "documents": len(sources),
        "claims": len(claims),
        "mapped_cases": len(cases_out),
        "gaps": len(GAPS),
        "entities": len(entities),
        "money_rows": len(money_rows),
        "families": len(FAMILIES),
    }
    stats_js = OUT_DIR / "stats.js"
    stats_js.write_text(
        "window.__CORPUS_STATS__ = " + json.dumps(stats, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    PUBLIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    public_json = PUBLIC_DATA_DIR / "corpus.json"
    public_js = PUBLIC_DATA_DIR / "corpus.js"
    public_stats = PUBLIC_DATA_DIR / "stats.js"
    public_json.write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    public_js.write_text(js_path.read_text(encoding="utf-8"), encoding="utf-8")
    public_stats.write_text(stats_js.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"wrote {json_path.relative_to(ROOT)} ({json_path.stat().st_size} bytes)")
    print(f"wrote {js_path.relative_to(ROOT)} ({js_path.stat().st_size} bytes)")
    print(f"wrote {stats_js.relative_to(ROOT)}")
    print(f"wrote {public_json.relative_to(ROOT)}")
    print(f"wrote {public_js.relative_to(ROOT)}")
    print(f"wrote {public_stats.relative_to(ROOT)}")
    print(f"claims={len(claims)} cases={len(cases_out)} money_rows={len(money_rows)} entities={len(entities)}")


if __name__ == "__main__":
    main()
