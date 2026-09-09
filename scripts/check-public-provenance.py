#!/usr/bin/env python3
"""Fail fast when a public page cites an official source this corpus never captured.

The public pages (index.html, status/index.html, good/index.html, guide/index.html,
oversight/index.html, programs/index.html, money/index.html, authority/index.html) are
hand-authored HTML, not generated from research/. That is a deliberate, separate track
from The Record (research/viewer/build.py's manifest-gated corpus.json/corpus.js) -- but
it still makes consequential factual assertions and links to primary government sources
to back them. This script is the provenance floor for that hand-authored track: every
link this corpus makes to an official source domain (justice.gov, mn.gov DHS, etc.) on
a public page must have a matching archived source record under research/sources/, so
that (a) the underlying fact has a captured, retrieval-dated, quote-checked record in
the corpus rather than resting only on a live outbound link, and (b) if the official
page ever changes or disappears, this corpus still has what it said.

This does not verify the fact is accurately restated on the public page -- only that a
source record exists somewhere in research/sources/ whose text contains the cited URL
(as canonical_url, or noted as a same-content mirror in another field). Read the pages
and the sources yourself when reviewing this check's output.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = ROOT / "research" / "sources"

# Public HTML files that are expected to sometimes cite official sources.
# Add a page here once it starts linking out to a domain in OFFICIAL_DOMAINS.
PUBLIC_PAGES = [
    "index.html",
    "status/index.html",
    "good/index.html",
    "guide/index.html",
    "oversight/index.html",
    "programs/index.html",
    "money/index.html",
    "authority/index.html",
]

# Domains treated as "official primary source" for this check. A citation to one of
# these on a public page must be backed by a research/sources/*.json record.
OFFICIAL_DOMAINS = (
    "justice.gov",
    "oig.hhs.gov",
    "usda.gov",
    "gao.gov",
    "leg.mn.gov",
    "revisor.mn.gov",
    "mn.gov",
    "courtlistener.com",
    "auditor.leg.state.mn.us",
)

URL_RE = re.compile(
    r"https://(?:www\.)?(?:" + "|".join(re.escape(d) for d in OFFICIAL_DOMAINS) + r")[^\s\"'<>)]*"
)

# Known exceptions: URLs that are intentionally not backed by a research/sources
# record (e.g. a link to a live evergreen dashboard/index page rather than a
# point-in-time official statement of fact). Keep this list short and justified;
# it is a deliberate escape hatch, not a place to silence real gaps.
ALLOWED_UNSOURCED = {
    # Evergreen DHS program-integrity landing page, not a dated press release --
    # its content changes over time and it is not cited for a specific fact.
    "https://mn.gov/dhs/program-integrity/",
    # Evergreen DHS program-description page for the (now-terminated) Housing
    # Stabilization Services benefit -- background/definition, not a dated
    # factual citation.
    "https://mn.gov/dhs/housing-income/housing-services/programs-and-services/housing-stabilization-services/",
    # 2026-09-09 pass: live-fetched and confirmed to return only DHS's generic,
    # one-year-rolling news-index shell (no article body for this specific id),
    # and archive.org has no snapshot of this exact URL. The underlying fact
    # (HSS ended Oct. 31, 2025) is independently backed elsewhere in this
    # corpus's sources; this specific DHS press-release URL could not be
    # archived in this pass. Revisit if DHS's news CMS becomes fetchable.
    "https://mn.gov/dhs/about-us/legislative-media/media/news/?id=1053-711321",
}


def main() -> int:
    if not SOURCES_DIR.exists():
        print(f"missing sources directory: {SOURCES_DIR}", file=sys.stderr)
        return 1

    source_text = ""
    for path in sorted(SOURCES_DIR.glob("*.json")):
        source_text += path.read_text(encoding="utf-8", errors="ignore")

    errors: list[str] = []
    checked = 0

    for rel in PUBLIC_PAGES:
        path = ROOT / rel
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        urls = sorted(set(URL_RE.findall(html)))
        for url in urls:
            checked += 1
            if url in ALLOWED_UNSOURCED:
                continue
            if url not in source_text:
                errors.append(f"{rel} cites {url!r} with no matching research/sources/*.json record")

    if errors:
        print("Public-provenance check failed:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        print(
            "\nEvery official-source URL a public page cites must be backed by a "
            "research/sources/*.json record (as canonical_url, or explicitly noted as "
            "a same-content mirror). Capture the source, or add a justified entry to "
            "ALLOWED_UNSOURCED in scripts/check-public-provenance.py if it is genuinely "
            "an evergreen reference rather than a dated factual citation.",
            file=sys.stderr,
        )
        return 1

    print(f"Public provenance OK: {checked} official-source citations checked across {len(PUBLIC_PAGES)} pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
