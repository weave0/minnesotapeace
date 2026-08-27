# Court harvest gaps

Updated 2026-08-26 evening after authenticated RECAP pulls (no PACER purchases).

## Locally archived charging instruments (hashed)

| File | Docket | Instrument | SHA-256 | Pages |
|---|---|---|---|---|
| `0_22-cr-00223_ecf1_Indictment.pdf` | 0:22-cr-00223 Bock | Indictment | `060c069f751742405427ab4277ff30809d6724539d4e8b86e29b6dbbf393393a` | 58 |
| `0_22-cr-00124_ecf22_Indictment.pdf` | 0:22-cr-00124 Farah | Passport § 1542 only | `64b4c93a6aa721d741bbcd5afe98ff692de5daf6f6295e508618f5724e19d054` | 1 |
| `0_24-cr-00015_ecf1_mohamed.pdf` | 0:24-cr-00015 Mohamed | FOF indictment | `eb090e5e657fe64fff1819c26ed073aa934b689f0e1e49b0ac1df47b81df0d1f` | 37 |
| `0_25-cr-00349_ecf1_aden-hss.pdf` | 0:25-cr-00349 Aden | HSS indictment | `d1781deb0cabf59ba808078976349a2b4fb6074c5f790d63073408c0feaf9812` | 8 |
| `0_25-cr-00351_ecf1_falade-hss.pdf` | 0:25-cr-00351 Falade | HSS indictment | `c88b4ac7ebce8fd63a0974ca41a9d8bd272210596406b0b9375ab1b13debb0fe` | 7 |
| `0_25-cr-00353_ecf1_anwar-adow-hss.pdf` | 0:25-cr-00353 Anwar Adow | **Felony information** (not indictment) | `c449cde383c96511ad2b0b02c75e57673dc4f72cb9b12d02d9adf87c0f80d81f` | 6 |

## Still missing as local charging instruments

- **Empire/Farah 43-count superseding indictment is now locally archived** as `0_22-cr-00124_ecf57_Superseding-Indictment.pdf` (ECF 57, 48 pp., RECAP 201530.57). ECF 22 remains the earlier one-page passport count. The 201529 IA dump still lacks 57.0.pdf. First 20 docket entries are the May 2022 complaint path. A 16 MB FBI complaint affidavit (ECF 2-1, 34 pp.) is on disk locally and is **not** committed (size). That affidavit is not the superseding indictment.
- **`0:25-cr-00354` Asad Adow / Leo Human Services** felony information: docket identity confirmed (counts 1–4, filed 2025-09-18, waiver of indictment 2025-11-17). RECAP `is_available=false`. Still a local-document gap.
- Dispositive filings (judgments, plea agreements, restitution orders) to move facts from CHARGED_ALLEGED to ADJUDICATED, including Anwar Adow’s 2025-10-23 change-of-plea minute entry.

## Notes

Do not burn rate-limited CourtListener pulls merely to duplicate official-host facts. A docket identity is not a locally acquired PDF. `CHARGING-INSTRUMENTS.md` lists a PDF only after save + hash + ECF check.
