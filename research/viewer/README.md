# Research viewer (v1)

Static, evidence-first HTML for the MinnesotaPeace public-program fraud corpus. It is not the live mediation site and is not a homepage fraud dashboard.

## Open

Open `research/viewer/index.html` (GitHub Pages-style static hosting, or any local static server). Relative paths only.

Rebuild the data bundle after claim/extract/source/entity edits:

```bash
python3 research/viewer/build.py
```

That writes `research/viewer/data/corpus.json` and `research/viewer/data/corpus.js` (the JS file is what the page loads, so `file://` works).

## What is in the bundle

- Canonical `research/claims/claim-*.json`
- Count-mapped extracts under `research/court/extracts/` (skips leftover stub `farah-22-cr-124-ecf57-superseding.json`)
- `research/sources/src-*.json`
- `research/entities/org-*.json`
- Asad Adow `0:25-cr-00354` as a gap card (RECAP information missing)

## Editorial

No TOTAL FRAUD number. No $9 billion on the index. Every displayed dollar keeps `metric_type` and evidence class. Overlap groups are preserved and not summed.
