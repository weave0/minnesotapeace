#!/usr/bin/env python3
"""Fail if status/index.html's generated snapshot block is stale or hand-edited.

Runs scripts/build-status-snapshot.py into the real file, diffs against what was
actually committed, then restores the committed content -- this script only ever
reports whether the committed state *would* differ, mirroring
verify-public-corpus-fresh.py's pattern for the /record/ corpus.

Because build-status-snapshot.py's output has no volatile field (no generated_at
equivalent -- the one date it writes, "status checked", is itself computed
deterministically from canonical claims' last_swept_for_supersession), a plain
byte-for-byte comparison is sufficient: two correct runs against the same inputs
are identical, so any difference here is a real drift.

This also transitively re-runs every fail-closed check inside the generator
itself (missing source, non-primary source, unsupported stage, malformed value/
date, unresolved duplicate-active-claim, etc.) -- a validation failure there
surfaces here as a non-zero exit before any diff is even computed.

Run from repo root:  python3 scripts/check-status-snapshot-fresh.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-status-snapshot.py"
STATUS_HTML = ROOT / "status" / "index.html"


def main() -> int:
    committed = STATUS_HTML.read_text(encoding="utf-8")

    result = subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        # Restore before reporting -- a failed generator run may have left the file
        # untouched (it writes only after all validation passes), but be defensive.
        STATUS_HTML.write_text(committed, encoding="utf-8")
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return result.returncode

    fresh = STATUS_HTML.read_text(encoding="utf-8")

    # Restore committed content regardless of outcome -- this script only reports.
    STATUS_HTML.write_text(committed, encoding="utf-8")

    if committed != fresh:
        print("status/index.html's generated snapshot block is stale relative to canonical claims.", file=sys.stderr)
        print(
            "Either a canonical claim/source changed without rerunning the generator, "
            "or someone hand-edited a value, date, source URL, or label inside a "
            "STATUS-SNAPSHOT:GENERATED:* marker pair.",
            file=sys.stderr,
        )
        print("\nRun 'python3 scripts/build-status-snapshot.py' and commit the result.", file=sys.stderr)
        return 1

    print("status/index.html snapshot matches a fresh build.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
