#!/usr/bin/env python3
"""Generate the "01 - Feeding Our Future snapshot" block in status/index.html
from canonical, primary-source-backed metric claims.

Canonical research records -> validation -> this generator -> status/index.html

Scope: exactly three headline measurements (fof-charged-count, fof-convicted-count,
fof-sentenced-count). Nothing else on /status/ is touched. This generator does not
read research/cases/feeding-our-future/defendants.json (journalism-derived
dispositions) and must never be extended to do so for these metrics -- see
research/README.md's source-priority list and this script's ADMITTED_SOURCE_STATUSES.

Fails closed (non-zero exit, no partial write) when:
  - a required metric has zero, or more than one unresolved active, claim
  - a metric's evidence_class does not match its expected procedural stage
  - a metric's source is not an admitted primary source
  - a metric's source text does not textually support the stated ordinal + stage
  - metric_value or event_date is malformed
  - required public-facing fields are missing

Run from repo root:  python3 scripts/build-status-snapshot.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "research" / "claims"
SOURCES_DIR = ROOT / "research" / "sources"
STATUS_HTML = ROOT / "status" / "index.html"

MEASUREMENT_TYPE = "OFFICIAL_ORDINAL_MILESTONE"

# Admitted primary-source statuses for an official ordinal milestone. Deliberately
# narrow: this generator must never accept a journalism source (e.g. Sahan Journal,
# Hiiraan Online, Center of the American Experiment) as authority for one of these
# three numbers, no matter how well-sourced that journalism is for other purposes.
ADMITTED_SOURCE_STATUSES = {"PRIMARY_GOVERNMENT_RELEASE"}
ADMITTED_SOURCE_TIER_MAX = 3

# metric_id -> (display order, expected evidence_class, stage word for the
# source-support textual check, month names for date formatting)
METRICS = [
    ("fof-charged-count", "CHARGED_ALLEGED", "charged"),
    ("fof-convicted-count", "ADJUDICATED", "convict"),
    ("fof-sentenced-count", "ADJUDICATED", "sentenc"),
]

MONTHS = [
    "Jan.", "Feb.", "March", "April", "May", "June",
    "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec.",
]

GENERATED_MARKERS = [
    ("STATUS-SNAPSHOT:GENERATED:HERO-DATE", "inline"),
    ("STATUS-SNAPSHOT:GENERATED:CARDS", "block"),
    ("STATUS-SNAPSHOT:GENERATED:FOOTER-DATE", "inline"),
]


class BuildError(SystemExit):
    def __init__(self, message: str):
        super().__init__("status-snapshot build failed: " + message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise BuildError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def fmt_date(iso: str) -> str:
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", iso or "")
    if not m:
        raise BuildError(f"malformed date {iso!r} (expected YYYY-MM-DD)")
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        date(y, mo, d)
    except ValueError as exc:
        raise BuildError(f"malformed calendar date {iso!r}: {exc}")
    return f"{MONTHS[mo - 1]} {d}, {y}"


def esc(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def load_all_claims() -> list[dict]:
    claims = []
    for path in sorted(CLAIMS_DIR.glob("*.json")):
        data = load_json(path)
        data["_path"] = path
        claims.append(data)
    return claims


def load_all_sources() -> dict[str, dict]:
    sources = {}
    for path in sorted(SOURCES_DIR.glob("*.json")):
        data = load_json(path)
        sid = data.get("source_id")
        if sid:
            sources[sid] = data
    return sources


def resolve_active_claim(metric_id: str, candidates: list[dict]) -> dict:
    if not candidates:
        raise BuildError(f"metric {metric_id!r} has no claim at all -- a required metric lacks a source record")

    active = [c for c in candidates if c.get("valid_until") is None]
    if len(active) == 1:
        return active[0]

    if len(active) == 0:
        raise BuildError(
            f"metric {metric_id!r} has {len(candidates)} claim(s) but none is active "
            f"(all have valid_until set) -- fix valid_until on the current record"
        )

    # More than one active candidate: try to resolve via a superseded_by chain
    # among just the active set. Exactly one must be the terminal (unreferenced) node.
    referenced = {c.get("superseded_by") for c in active if c.get("superseded_by")}
    terminal = [c for c in active if c["claim_id"] not in referenced]
    if len(terminal) == 1:
        return terminal[0]

    ids = ", ".join(c["claim_id"] for c in active)
    raise BuildError(
        f"metric {metric_id!r} has {len(active)} active claims with no resolving "
        f"supersession chain ({ids}) -- two active records claim to be the latest "
        f"measurement for the same metric; set valid_until/superseded_by to resolve"
    )


def validate_metric(metric_id: str, expected_evidence_class: str, stage_word: str,
                     claims_by_metric: dict[str, list[dict]], sources: dict[str, dict]) -> dict:
    claim = resolve_active_claim(metric_id, claims_by_metric.get(metric_id, []))

    if claim.get("measurement_type") != MEASUREMENT_TYPE:
        raise BuildError(
            f"{claim['claim_id']}: metric_id set but measurement_type is not "
            f"{MEASUREMENT_TYPE!r} -- refusing to treat an ordinary claim as an "
            f"official ordinal milestone"
        )

    value = claim.get("metric_value")
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0 or int(value) != value:
        raise BuildError(f"{claim['claim_id']}: metric_value {value!r} is not a positive integer")
    value = int(value)

    event_date = claim.get("event_date")
    display_date = fmt_date(event_date)  # raises BuildError if malformed

    if claim.get("evidence_class") != expected_evidence_class:
        raise BuildError(
            f"{claim['claim_id']}: evidence_class {claim.get('evidence_class')!r} does not "
            f"match the expected {expected_evidence_class!r} for metric {metric_id!r} -- "
            f"the source does not support the stated procedural stage"
        )

    source_ids = claim.get("source_ids") or []
    if not source_ids:
        raise BuildError(f"{claim['claim_id']}: no source_ids -- a required metric lacks a source record")

    primary_source = None
    for sid in source_ids:
        src = sources.get(sid)
        if src is None:
            raise BuildError(f"{claim['claim_id']}: cites source_id {sid!r} which does not exist in research/sources/")
        tier = src.get("source_tier")
        status = src.get("source_status")
        if not (isinstance(tier, int) and tier <= ADMITTED_SOURCE_TIER_MAX and status in ADMITTED_SOURCE_STATUSES):
            raise BuildError(
                f"{claim['claim_id']}: source {sid!r} (tier={tier!r}, status={status!r}) "
                f"is not an admitted primary source for an official ordinal milestone"
            )
        if primary_source is None:
            primary_source = src

    # Textual check: somewhere in this claim's own supporting-passage quotes, or the
    # cited source's own `supports` bullets / title, the ordinal + stage word must
    # actually appear -- catches a metric_value that doesn't match what the source
    # actually says, rather than trusting the claim author's arithmetic.
    haystack_parts = [claim.get("claim_text") or ""]
    for p in claim.get("supporting_passages") or []:
        haystack_parts.append(p.get("quote") or "")
    for sid in source_ids:
        src = sources[sid]
        haystack_parts.append(src.get("title") or "")
        haystack_parts.extend(src.get("supports") or [])
    haystack = " ".join(haystack_parts).lower()
    ordinal_pattern = re.compile(rf"\b{value}(st|nd|rd|th)\b.{{0,40}}{re.escape(stage_word)}", re.IGNORECASE | re.DOTALL)
    if not ordinal_pattern.search(haystack):
        raise BuildError(
            f"{claim['claim_id']}: could not find text matching '{value}(st|nd|rd|th) ... {stage_word}' "
            f"in the claim's own supporting passages or its source's stated text -- "
            f"the source does not appear to support the stated procedural stage/value"
        )

    for field in ("public_label", "public_explanation", "public_source_label"):
        if not (isinstance(claim.get(field), str) and claim[field].strip()):
            raise BuildError(f"{claim['claim_id']}: missing required {field!r}")

    swept = claim.get("last_swept_for_supersession")
    if not (isinstance(swept, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", swept)):
        raise BuildError(f"{claim['claim_id']}: missing/malformed last_swept_for_supersession")

    canonical_url = primary_source.get("canonical_url")
    if not (isinstance(canonical_url, str) and canonical_url.startswith("http")):
        raise BuildError(f"{claim['claim_id']}: source {source_ids[0]!r} has no usable canonical_url")

    return {
        "value": value,
        "display_date": display_date,
        "public_label": claim["public_label"],
        "public_explanation": claim["public_explanation"],
        "public_source_label": claim["public_source_label"],
        "canonical_url": canonical_url,
        "last_swept_for_supersession": swept,
        "claim_id": claim["claim_id"],
    }


def render_card(m: dict) -> str:
    return (
        '          <article class="snapshot-card">\n'
        f'            <p class="snapshot-value">{m["value"]}</p>\n'
        f'            <p class="snapshot-label">{esc(m["public_label"])}</p>\n'
        f'            <p class="snapshot-asof">DOJ count &middot; {esc(m["display_date"])}</p>\n'
        f'            <p>{esc(m["public_explanation"])}</p>\n'
        f'            <p class="source-line"><a href="{esc(m["canonical_url"])}">{esc(m["public_source_label"])}</a></p>\n'
        "          </article>"
    )


def splice_marker(html: str, marker: str, replacement: str) -> str:
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    si = html.find(start)
    ei = html.find(end)
    if si == -1 or ei == -1 or ei < si:
        raise BuildError(f"marker pair {marker} not found (or out of order) in {STATUS_HTML.relative_to(ROOT)}")
    si_end = si + len(start)
    return html[:si_end] + replacement + html[ei:]


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--check-markers-only":
        html = STATUS_HTML.read_text(encoding="utf-8")
        for marker, _ in GENERATED_MARKERS:
            if f"<!-- {marker}:START -->" not in html or f"<!-- {marker}:END -->" not in html:
                raise BuildError(f"marker pair {marker} missing")
        print("status-snapshot markers OK")
        return

    claims = load_all_claims()
    sources = load_all_sources()

    milestone_claims = [c for c in claims if c.get("measurement_type") == MEASUREMENT_TYPE]
    claims_by_metric: dict[str, list[dict]] = {}
    for c in milestone_claims:
        mid = c.get("metric_id")
        if not mid:
            raise BuildError(f"{c['claim_id']}: measurement_type is {MEASUREMENT_TYPE!r} but metric_id is not set")
        claims_by_metric.setdefault(mid, []).append(c)

    results = []
    for metric_id, expected_evidence_class, stage_word in METRICS:
        results.append(validate_metric(metric_id, expected_evidence_class, stage_word, claims_by_metric, sources))

    # The page must never claim to be more current than its least-recently-checked
    # input metric.
    status_checked_iso = min(r["last_swept_for_supersession"] for r in results)
    status_checked_display = fmt_date(status_checked_iso)

    cards_html = "\n".join(render_card(r) for r in results)
    cards_block = f"\n        <div class=\"status-snapshot\">\n{cards_html}\n        </div>\n        "

    html = STATUS_HTML.read_text(encoding="utf-8")
    html = splice_marker(html, "STATUS-SNAPSHOT:GENERATED:HERO-DATE", f"Status checked {status_checked_display}")
    html = splice_marker(html, "STATUS-SNAPSHOT:GENERATED:CARDS", cards_block)
    html = splice_marker(html, "STATUS-SNAPSHOT:GENERATED:FOOTER-DATE", f"Status checked {status_checked_display}")

    STATUS_HTML.write_text(html, encoding="utf-8")
    print(
        "wrote status/index.html snapshot: "
        + ", ".join(f"{r['claim_id']}={r['value']}" for r in results)
        + f", status_checked={status_checked_display}"
    )


if __name__ == "__main__":
    main()
