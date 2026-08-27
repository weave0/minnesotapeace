# Court harvest gaps

- `/dockets/`, `/docket-entries/`, `/recap-documents/` REST: **401** without a CourtListener API token.
- Public search previously **429** cut the CourtListener continuation after 3 backoffs (12s / 24s / 48s). Indexed `0:24-cr-00173` (juror bribery).
- `0:24-cr-00015` is now **identified and externally located** as *United States v. Mohamed et al.* ECF 1, a 37-page indictment filed 2024-01-24. DOJ's official January 2024 release corroborates the docket number, defendants, factual theory, and charge families. A public PDF copy is indexed outside an official host, but it has **not yet been archived/hashed in this corpus**, so it remains a local-document acquisition gap rather than an identity/content gap.
- Still missing as local charging instruments: `0:24-cr-00015` ECF 1; `0:25-cr-00349`; `0:25-cr-00351`; `0:25-cr-00353`; `0:25-cr-00354`.
- HSS docket identities are externally corroborated: `0:25-cr-00349` (*USA v. Aden et al.*), `0:25-cr-00351` (*USA v. Falade et al.*), and `0:25-cr-00353` / `0:25-cr-00354` (*USA v. Adow* matters). Charging PDFs still need primary-document acquisition and hashing before count-level extraction.
- A free CourtListener token can list RECAP filepaths without PACER fees for documents already uploaded. Do not burn rate-limited pulls merely to duplicate official-host facts; prioritize missing charging instruments and dispositive filings.

## Verification discipline

A docket identity, DOJ charge summary, or third-party-hosted image of a court filing is enough to narrow a research gap, but not enough to mark a charging instrument as locally acquired. `CHARGING-INSTRUMENTS.md` should only call a PDF downloaded once the exact file is saved, hashed, and its ECF metadata checked.
