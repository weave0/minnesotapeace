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
  - a required metric has zero, or more than one unresolved (live) claim
  - a metric's evidence_class does not match its expected procedural stage
  - a metric's source is not an admitted primary source
  - the cited SOURCE record's own title/supports text does not textually support
    the stated ordinal + stage (claim_text and supporting_passages quotes are
    deliberately excluded from this check -- a claim must not be able to prove
    itself)
  - metric_value, event_date, or last_swept_for_supersession is malformed or not
    a real calendar date
  - last_swept_for_supersession is later than today's America/Chicago date
  - required public-facing fields are missing

All HTML interpolation (including href attribute values) goes through esc(),
which is html.escape(..., quote=True) -- safe against a value containing a
double quote breaking out of an attribute.

Run from repo root:  python3 scripts/build-status-snapshot.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "research" / "claims"
SOURCES_DIR = ROOT / "research" / "sources"
STATUS_HTML = ROOT / "status" / "index.html"

MEASUREMENT_TYPE = "OFFICIAL_ORDINAL_MILESTONE"

# This product reports "status checked" dates as Minnesota (America/Chicago) local
# calendar days, not UTC. A sweep run late in the day US-side can already be
# tomorrow in UTC; comparing against UTC "today" would then wrongly reject a
# same-day sweep date, or (worse) silently accept a genuinely future one.
LOCAL_TZ = ZoneInfo("America/Chicago")

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


def parse_calendar_date(iso: str, field_label: str = "date") -> date:
    """Parse a YYYY-MM-DD string into a real calendar date, rejecting both bad
    formatting and impossible dates (e.g. 2026-02-31) that a bare regex would miss."""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", iso or "")
    if not m:
        raise BuildError(f"malformed {field_label} {iso!r} (expected YYYY-MM-DD)")
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        return date(y, mo, d)
    except ValueError as exc:
        raise BuildError(f"malformed {field_label} {iso!r}: not a real calendar date ({exc})")


def fmt_date(iso: str) -> str:
    d = parse_calendar_date(iso, "date")
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def today_local() -> date:
    return datetime.now(timezone.utc).astimezone(LOCAL_TZ).date()


def esc(value) -> str:
    # quote=True also escapes " and ' so this is safe to interpolate inside a
    # double-quoted HTML attribute (e.g. href="...") as well as in text content.
    return html.escape(str(value), quote=True)


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

    # A claim is "live" (the current measurement) only if it is BOTH still valid
    # (valid_until is None) AND not itself marked as replaced (superseded_by is
    # None). Treating superseded_by as authoritative regardless of valid_until is
    # what makes chain resolution select the *successor*, never the predecessor:
    # if old.superseded_by = "new" but someone forgot to also set old.valid_until,
    # old is still correctly excluded here because it names its own replacement.
    live = [c for c in candidates if c.get("valid_until") is None and c.get("superseded_by") is None]

    if len(live) == 1:
        return live[0]

    if len(live) == 0:
        raise BuildError(
            f"metric {metric_id!r} has {len(candidates)} claim(s) but none is live "
            f"(every candidate has valid_until and/or superseded_by set) -- fix the "
            f"current record so exactly one candidate has neither set"
        )

    # More than one candidate with neither valid_until nor superseded_by set: this
    # is a genuinely ambiguous "which one is current" state. This generator does
    # not guess a newest-by-date or any other heuristic here -- it fails closed,
    # since the canonical corpus has not explicitly resolved the ambiguity via
    # supersession.
    ids = ", ".join(c["claim_id"] for c in live)
    raise BuildError(
        f"metric {metric_id!r} has {len(live)} claims with neither valid_until nor "
        f"superseded_by set ({ids}) -- two active records claim to be the latest "
        f"measurement for the same metric with no supersession chain resolving it; "
        f"set valid_until and/or superseded_by on all but the true current record"
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

    # Textual check: the ordinal + stage word must actually appear in the cited
    # SOURCE record's own archived text (title / `supports` bullets) -- and only
    # there. A claim must not be able to prove itself: claim_text and
    # supporting_passages[].quote are authored by whoever wrote the claim, so
    # including them here would let a wrong metric_value pass validation merely
    # by also writing matching (but unverified, possibly fabricated) prose into
    # the claim. Grounding this check exclusively in the independently-archived
    # source record is what makes it a real check rather than the claim
    # confirming itself.
    haystack_parts = []
    for sid in source_ids:
        src = sources[sid]
        haystack_parts.append(src.get("title") or "")
        haystack_parts.extend(src.get("supports") or [])
    haystack = " ".join(haystack_parts).lower()
    ordinal_pattern = re.compile(rf"\b{value}(st|nd|rd|th)\b.{{0,40}}{re.escape(stage_word)}", re.IGNORECASE | re.DOTALL)
    if not ordinal_pattern.search(haystack):
        raise BuildError(
            f"{claim['claim_id']}: could not find text matching '{value}(st|nd|rd|th) ... {stage_word}' "
            f"in the cited source record's own title/supports text -- "
            f"the source does not appear to support the stated procedural stage/value"
        )

    for field in ("public_label", "public_explanation", "public_source_label"):
        if not (isinstance(claim.get(field), str) and claim[field].strip()):
            raise BuildError(f"{claim['claim_id']}: missing required {field!r}")

    swept = claim.get("last_swept_for_supersession")
    if not isinstance(swept, str):
        raise BuildError(f"{claim['claim_id']}: missing last_swept_for_supersession")
    swept_date = parse_calendar_date(swept, "last_swept_for_supersession")
    today = today_local()
    if swept_date > today:
        raise BuildError(
            f"{claim['claim_id']}: last_swept_for_supersession {swept!r} is after "
            f"today's America/Chicago date ({today.isoformat()}) -- a sweep cannot "
            f"have happened in the future"
        )

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


def splice_marker(html_text: str, marker: str, replacement: str) -> str:
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    si = html_text.find(start)
    ei = html_text.find(end)
    if si == -1 or ei == -1 or ei < si:
        raise BuildError(f"marker pair {marker} not found (or out of order) in {STATUS_HTML.relative_to(ROOT)}")
    si_end = si + len(start)
    return html_text[:si_end] + replacement + html_text[ei:]


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--check-markers-only":
        html_text = STATUS_HTML.read_text(encoding="utf-8")
        for marker, _ in GENERATED_MARKERS:
            if f"<!-- {marker}:START -->" not in html_text or f"<!-- {marker}:END -->" not in html_text:
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

    html_text = STATUS_HTML.read_text(encoding="utf-8")
    html_text = splice_marker(html_text, "STATUS-SNAPSHOT:GENERATED:HERO-DATE", f"Status checked {status_checked_display}")
    html_text = splice_marker(html_text, "STATUS-SNAPSHOT:GENERATED:CARDS", cards_block)
    html_text = splice_marker(html_text, "STATUS-SNAPSHOT:GENERATED:FOOTER-DATE", f"Status checked {status_checked_display}")

    STATUS_HTML.write_text(html_text, encoding="utf-8")
    print(
        "wrote status/index.html snapshot: "
        + ", ".join(f"{r['claim_id']}={r['value']}" for r in results)
        + f", status_checked={status_checked_display}"
    )


if __name__ == "__main__":
    main()
