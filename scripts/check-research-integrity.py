#!/usr/bin/env python3
"""Fail fast on structural problems in the private research corpus.

This intentionally validates provenance plumbing, not factual truth. Factual review
still requires reading the cited primary source.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
SOURCES = RESEARCH / "sources"
SOURCE_ID_RE = re.compile(r"^src-[a-z0-9][a-z0-9._-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors: list[str] = []
parsed: dict[Path, object] = {}


def error(message: str) -> None:
    errors.append(message)


def valid_http_url(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed_url = urlparse(value)
    except ValueError:
        return False
    return parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc)


# 1. Every JSON research artifact must parse.
for path in sorted(RESEARCH.rglob("*.json")):
    try:
        parsed[path] = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report all parse failures together
        error(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")

# 2. Source records need stable identifiers and minimum citation metadata.
source_ids: dict[str, Path] = {}
for path in sorted(SOURCES.glob("src-*.json")):
    data = parsed.get(path)
    if not isinstance(data, dict):
        error(f"source record must be a JSON object: {path.relative_to(ROOT)}")
        continue

    source_id = data.get("source_id")
    if not isinstance(source_id, str) or not SOURCE_ID_RE.match(source_id):
        error(f"missing/invalid source_id in {path.relative_to(ROOT)}: {source_id!r}")
        continue

    if path.stem != source_id:
        error(
            f"source_id/filename mismatch: {path.relative_to(ROOT)} has {source_id!r}"
        )

    previous = source_ids.get(source_id)
    if previous:
        error(
            f"duplicate source_id {source_id!r}: "
            f"{previous.relative_to(ROOT)} and {path.relative_to(ROOT)}"
        )
    else:
        source_ids[source_id] = path

    if not valid_http_url(data.get("canonical_url")):
        error(f"missing/invalid canonical_url in {path.relative_to(ROOT)}")

    for field in ("title", "source_status"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            error(f"missing {field} in {path.relative_to(ROOT)}")

    retrieval_date = data.get("retrieval_date")
    if retrieval_date is not None and (
        not isinstance(retrieval_date, str) or not DATE_RE.match(retrieval_date)
    ):
        error(f"invalid retrieval_date in {path.relative_to(ROOT)}: {retrieval_date!r}")

# 3. Any structured src-* citation reference in key corpus layers must resolve.
def walk_refs(value: object, trail: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            child_trail = f"{trail}.{key}"
            if key == "source_id" and isinstance(child, str) and child.startswith("src-"):
                yield child, child_trail
            elif key == "source_ids" and isinstance(child, list):
                for idx, item in enumerate(child):
                    if isinstance(item, str) and item.startswith("src-"):
                        yield item, f"{child_trail}[{idx}]"
            else:
                yield from walk_refs(child, child_trail)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from walk_refs(child, f"{trail}[{idx}]")


for directory in (RESEARCH / "cases", RESEARCH / "money", RESEARCH / "oversight"):
    if not directory.exists():
        continue
    for path in sorted(directory.rglob("*.json")):
        data = parsed.get(path)
        if data is None:
            continue
        for source_id, trail in walk_refs(data):
            if source_id not in source_ids:
                error(
                    f"unresolved source reference {source_id!r} in "
                    f"{path.relative_to(ROOT)} at {trail}"
                )

# 4. Research remains a non-public substrate. The deployment workflow must retain
# an explicit research exclusion/guard before this gate passes.
deploy = ROOT / ".github" / "workflows" / "deploy.yml"
if not deploy.exists():
    error("missing .github/workflows/deploy.yml")
else:
    deploy_text = deploy.read_text(encoding="utf-8")
    if "research" not in deploy_text or "/research" not in deploy_text:
        error("deploy workflow no longer contains explicit research exclusion/public guard")

if errors:
    print("Research integrity check failed:", file=sys.stderr)
    for item in errors:
        print(f"- {item}", file=sys.stderr)
    sys.exit(1)

print(f"Research integrity OK: {len(parsed)} JSON files parsed; {len(source_ids)} source IDs unique.")
