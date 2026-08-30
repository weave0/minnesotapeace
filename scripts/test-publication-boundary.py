#!/usr/bin/env python3
"""Regression test for the research/viewer/build.py publication boundary.

Confirms the specific defect this test exists to prevent: a claim that lives
under research/claims/ but is NOT listed in research/publication/record-v1.json
must never appear in the built public corpus, and its dollar amounts must
never appear in the public money view -- regardless of how well-formed or
well-sourced the claim is.

Also confirms the two fail-closed guarantees the manifest is supposed to give:
  - editing an already-approved claim's content invalidates its approval
    (sha256 mismatch) until the manifest is deliberately updated.
  - approving a claim that cites a source the manifest does not also approve
    is a build error, not a silent drop.

This script makes no permanent changes: every planted fixture file is removed,
and any real output written to record/data or research/viewer/data during the
test is restored to its pre-test (committed) state before exiting, pass or fail.

Run from repo root:  python3 scripts/test-publication-boundary.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "research" / "viewer" / "build.py"
CLAIMS_DIR = ROOT / "research" / "claims"
MANIFEST_PATH = ROOT / "research" / "publication" / "record-v1.json"
PUBLIC_CORPUS = ROOT / "record" / "data" / "corpus.json"

TRACKED_OUTPUTS = [
    ROOT / "record" / "data" / "corpus.json",
    ROOT / "record" / "data" / "corpus.js",
    ROOT / "record" / "data" / "stats.js",
    ROOT / "research" / "viewer" / "data" / "corpus.json",
    ROOT / "research" / "viewer" / "data" / "corpus.js",
    ROOT / "research" / "viewer" / "data" / "stats.js",
]

FIXTURE_CLAIM_ID = "claim-test-publication-boundary-unapproved"
FIXTURE_PATH = CLAIMS_DIR / "claim-test-publication-boundary-fixture.json"

failures: list[str] = []


def note(ok: bool, label: str) -> None:
    print(("PASS" if ok else "FAIL") + " -- " + label)
    if not ok:
        failures.append(label)


def snapshot(paths: list[Path]) -> dict[Path, bytes | None]:
    return {p: (p.read_bytes() if p.exists() else None) for p in paths}


def restore(snap: dict[Path, bytes | None]) -> None:
    for p, content in snap.items():
        if content is None:
            if p.exists():
                p.unlink()
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(content)


def run_build() -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def write_fixture_claim(amount_value: int = 999_999_999) -> None:
    FIXTURE_PATH.write_text(
        json.dumps(
            {
                "claim_id": FIXTURE_CLAIM_ID,
                "claim_text": "Fixture claim for the publication-boundary regression test. Not a real finding.",
                "claim_type": "AMOUNT",
                "status": "confirmed",
                "evidence_class": "SECONDARY_VERIFIED",
                "proposition_class": "B_OVERSIGHT_FAILURE",
                "source_ids": [],
                "supporting_passages": [],
                "amounts": [
                    {
                        "value": amount_value,
                        "currency": "USD",
                        "metric_type": "test_fixture_amount",
                        "exact_or_approximate": "exact",
                        "overlap_group_id": None,
                        "methodology": "Test fixture only.",
                    }
                ],
                "qualifiers": ["This is a test fixture. It must never appear in the public record."],
                "subject_ids": [],
                "organizations": [],
                "jurisdiction": None,
                "confidence": "HIGH",
                "is_allegation": False,
                "is_inference": False,
                "reviewed_at": "2026-08-30T00:00:00Z",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> int:
    output_snapshot = snapshot(TRACKED_OUTPUTS)
    manifest_snapshot = snapshot([MANIFEST_PATH])
    fixture_existed_before = FIXTURE_PATH.exists()

    try:
        # --- Test 1: an unapproved claim must not reach the public corpus ---
        write_fixture_claim()
        result = run_build()
        note(result.returncode == 0, "build.py succeeds with an unapproved claim present")
        if result.returncode != 0:
            print(result.stdout, result.stderr)

        corpus = json.loads(PUBLIC_CORPUS.read_text(encoding="utf-8"))
        claim_ids = {c["claim_id"] for c in corpus["claims"]}
        note(FIXTURE_CLAIM_ID not in claim_ids, "unapproved claim is absent from corpus.json claims")

        money_claim_ids = {row["claim_id"] for row in corpus["money"]}
        note(FIXTURE_CLAIM_ID not in money_claim_ids, "unapproved claim's amounts are absent from corpus.json money[]")

        amount_values = {row["value"] for row in corpus["money"]}
        note(999_999_999 not in amount_values, "unapproved claim's dollar value does not appear anywhere in money[]")

        FIXTURE_PATH.unlink()

        # --- Test 2: editing an approved claim invalidates its approval ---
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        first_claim_id = manifest["claims"][0]["claim_id"]
        # Find the real file for this claim_id (filenames don't always match ids).
        target_path = None
        for path in CLAIMS_DIR.glob("claim-*.json"):
            obj = json.loads(path.read_text(encoding="utf-8"))
            if obj.get("claim_id") == first_claim_id:
                target_path = path
                break
        note(target_path is not None, "located the canonical file for the first approved manifest claim")

        if target_path is not None:
            original_bytes = target_path.read_bytes()
            try:
                tampered = json.loads(original_bytes)
                tampered["claim_text"] = tampered.get("claim_text", "") + " (tampered by regression test)"
                target_path.write_text(json.dumps(tampered, indent=2), encoding="utf-8")
                result = run_build()
                note(
                    result.returncode != 0 and "hash mismatch" in (result.stdout + result.stderr).lower(),
                    "build.py fails closed when an approved claim's content changes without renewing its manifest hash",
                )
            finally:
                target_path.write_bytes(original_bytes)

        # --- Test 3: approving a claim that cites an unapproved source is a build error ---
        write_fixture_claim()
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        fixture["source_ids"] = ["src-this-source-id-does-not-exist-anywhere"]
        FIXTURE_PATH.write_text(json.dumps(fixture, indent=2), encoding="utf-8")

        # Use build.py's own hash function (line-ending-normalized), not a raw
        # hashlib.sha256 of the file bytes -- otherwise this step of the test
        # would fail on a hash mismatch instead of exercising the check it's
        # meant to exercise (an approved claim citing an unapproved source).
        sys.path.insert(0, str(BUILD_SCRIPT.parent))
        import build as build_module  # noqa: E402

        fixture_hash = build_module.sha256_file(FIXTURE_PATH)
        manifest_with_fixture = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest_with_fixture["claims"].append({"claim_id": FIXTURE_CLAIM_ID, "sha256": fixture_hash})
        MANIFEST_PATH.write_text(json.dumps(manifest_with_fixture, indent=2), encoding="utf-8")

        result = run_build()
        note(
            result.returncode != 0
            and "not (or no longer) approved" in (result.stdout + result.stderr).lower(),
            "build.py refuses to publish a claim that cites an unapproved source",
        )

        # --- Test 4: editing an approved SOURCE invalidates its approval (mirrors Test 2 for claims) ---
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        first_source_id = manifest["sources"][0]["source_id"]
        source_path = None
        for path in (ROOT / "research" / "sources").glob("src-*.json"):
            obj = json.loads(path.read_text(encoding="utf-8"))
            if obj.get("source_id") == first_source_id:
                source_path = path
                break
        note(source_path is not None, "located the canonical file for the first approved manifest source")

        if source_path is not None:
            original_bytes = source_path.read_bytes()
            try:
                tampered = json.loads(original_bytes)
                tampered["notes"] = (tampered.get("notes") or "") + " (tampered by regression test)"
                source_path.write_text(json.dumps(tampered, indent=2), encoding="utf-8")
                result = run_build()
                note(
                    result.returncode != 0 and "hash mismatch" in (result.stdout + result.stderr).lower(),
                    "build.py fails closed when an approved source's content changes without renewing its manifest hash",
                )
            finally:
                source_path.write_bytes(original_bytes)

        # --- Test 5: editing an approved ENTITY invalidates its approval (mirrors Test 2 for claims) ---
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        first_entity_id = manifest["entities"][0]["entity_id"]
        entity_path = None
        for path in (ROOT / "research" / "entities").glob("org-*.json"):
            obj = json.loads(path.read_text(encoding="utf-8"))
            if obj.get("entity_id") == first_entity_id:
                entity_path = path
                break
        note(entity_path is not None, "located the canonical file for the first approved manifest entity")

        if entity_path is not None:
            original_bytes = entity_path.read_bytes()
            try:
                tampered = json.loads(original_bytes)
                tampered["notes"] = (tampered.get("notes") or "") + " (tampered by regression test)"
                entity_path.write_text(json.dumps(tampered, indent=2), encoding="utf-8")
                result = run_build()
                note(
                    result.returncode != 0 and "hash mismatch" in (result.stdout + result.stderr).lower(),
                    "build.py fails closed when an approved entity's content changes without renewing its manifest hash",
                )
            finally:
                entity_path.write_bytes(original_bytes)

    finally:
        if FIXTURE_PATH.exists() and not fixture_existed_before:
            FIXTURE_PATH.unlink()
        restore(manifest_snapshot)
        restore(output_snapshot)

    if failures:
        print(f"\n{len(failures)} publication-boundary regression check(s) failed:")
        for f in failures:
            print(" -", f)
        return 1
    print("\nAll publication-boundary regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
