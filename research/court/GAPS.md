# Court harvest gaps

- `/dockets/`, `/docket-entries/`, `/recap-documents/` REST: **401** without a CourtListener API token.
- Public search **429** cut this continuation at `0:24-cr-00015` after 3 backoffs (12s / 24s / 48s). Indexed `0:24-cr-00173` (juror bribery).
- Still missing: `0:24-cr-00015`, `0:25-cr-00349`, `0:25-cr-00351`, `0:25-cr-00353`, `0:25-cr-00354`.
- No charging-instrument PDFs on disk yet.
- A free CL token (courtlistener.com account) would list RECAP filepaths without PACER fees for documents already uploaded.
