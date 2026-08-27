# Research viewer (v1)

Static, evidence-first HTML for the MinnesotaPeace public-program fraud corpus. This layer is The Record inside MN Peace — not a fraud-total dashboard.


## Open

The public route is `/record` (Cases by default). `research/viewer/index.html` redirects there and keeps the hash.

Relative data paths stay under `research/viewer/` so the bundle can load from `/record`.

Rebuild the data bundle after claim/extract/source/entity edits:

```bash
python3 research/viewer/build.py
```

That writes `research/viewer/data/corpus.json`, `research/viewer/data/corpus.js` (the JS file is what the page loads, so `file://` works), and `research/viewer/data/stats.js` for the MN Peace homepage counters.

## What is in the bundle

- Canonical `research/claims/claim-*.json`
- Count-mapped extracts under `research/court/extracts/` (skips leftover stub `farah-22-cr-124-ecf57-superseding.json`)
- `research/sources/src-*.json`
- `research/entities/org-*.json`
- Asad Adow `0:25-cr-00354` as a gap card (RECAP information missing)

## Editorial

No TOTAL FRAUD number. No $9 billion on the index. Every displayed dollar keeps `metric_type` and evidence class. Overlap groups are preserved and not summed.
