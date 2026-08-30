#!/usr/bin/env python3
"""Fail if the committed public corpus is stale relative to research/ + the manifest.

Runs research/viewer/build.py into a scratch copy and compares it against what's
actually committed, ignoring `generated_at` (which legitimately changes on every
run and is not a content difference). A real difference means someone edited
research/ (or the publication manifest) without regenerating record/data and
research/viewer/data, or edited those generated files by hand instead of through
build.py -- either way the committed public corpus no longer matches what
canonical research and the manifest actually approve.

Run from repo root:  python3 scripts/verify-public-corpus-fresh.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "research" / "viewer" / "build.py"

TRACKED_OUTPUTS = [
    ROOT / "record" / "data" / "corpus.json",
    ROOT / "record" / "data" / "corpus.js",
    ROOT / "record" / "data" / "stats.js",
    ROOT / "research" / "viewer" / "data" / "corpus.json",
    ROOT / "research" / "viewer" / "data" / "corpus.js",
    ROOT / "research" / "viewer" / "data" / "stats.js",
]


def strip_generated_at(text: str) -> str:
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        # corpus.js / stats.js: window.__X__ = {...}; -- strip the JSON payload out,
        # normalize, and put it back so a byte-identical wrapper still compares equal.
        prefix, _, rest = text.partition("= ")
        payload, _, suffix = rest.rpartition(";")
        try:
            obj = json.loads(payload)
        except json.JSONDecodeError:
            return text
        obj.pop("generated_at", None)
        return prefix + "= " + json.dumps(obj, ensure_ascii=False) + ";" + suffix
    obj.pop("generated_at", None)
    return json.dumps(obj, indent=2, ensure_ascii=False)


def main() -> int:
    committed = {p: (p.read_text(encoding="utf-8") if p.exists() else None) for p in TRACKED_OUTPUTS}

    # Run the real builder against the real repo (it writes to fixed relative
    # paths, not a scratch dir -- build.py has no "output elsewhere" mode), then
    # diff against what was committed, then restore the committed files. This
    # script must never leave the working tree in the freshly-built state; it
    # only ever reports whether the committed state *would* differ.
    result = subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return result.returncode

    mismatches = []
    for p in TRACKED_OUTPUTS:
        fresh = p.read_text(encoding="utf-8") if p.exists() else None
        old = committed[p]
        if old is None or fresh is None:
            if old != fresh:
                mismatches.append(str(p.relative_to(ROOT)))
            continue
        if strip_generated_at(old) != strip_generated_at(fresh):
            mismatches.append(str(p.relative_to(ROOT)))

    # Restore committed content regardless of outcome -- this script only reports.
    for p in TRACKED_OUTPUTS:
        if committed[p] is None:
            if p.exists():
                p.unlink()
        else:
            p.write_text(committed[p], encoding="utf-8")

    if mismatches:
        print("The committed public corpus is stale relative to research/ + the publication manifest.")
        print("Files that differ (ignoring generated_at):")
        for m in mismatches:
            print(" -", m)
        print("\nRun 'python3 research/viewer/build.py' and commit the result.")
        return 1

    print("record/data and research/viewer/data match a fresh build (ignoring generated_at).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
