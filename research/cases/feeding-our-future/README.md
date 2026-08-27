# Feeding Our Future — MinnesotaPeace reference case family

Investigation family `inv-feeding-our-future`. Normalized 2026-08-26 from the first-harvest markdown under `feeding-our-future/` (SOURCES.md, CLAIMS.md, DEFENDANTS.md, GAPS.md) plus SHA-256 of local files in `feeding-our-future/primary/`.

This directory is the structured JSON view. **Do not invent facts beyond those four files.** Coverage is `first_harvest`: press-release-plus-OLA-PDF depth; high on PRs, low on indictment PDFs. Prosecution is mature (dozens of pleas/trial convictions/sentences) but many original-47 statuses are still `charged` only because later USAO-MN pages were not fetched.

## How to read the files

| File | What it is |
|---|---|
| `family.json` | Family record, coverage flags, missing_records from GAPS.md, proposition classes A/B/C supported and D/E not supported |
| `sources.json` | Array of S01–S31 official/primary sources and L01–L05 journalism leads (`id`, `title`, `publisher`, `url`, `date`, `type`, `evidence_class`; local PDFs/HTML have `sha256`) |
| `claims.json` | One object per claim (`fof-c-001` …). Required: claim_id, claim_text, evidence_class, status, source_ids, confidence, is_allegation, is_inference, reviewed_at. OLA findings include page numbers in `supporting_passages` (p. 37, 49–51, 53, 55, 57, S-1) |
| `defendants.json` | One object per named defendant in DEFENDANTS.md. Status is **not** upgraded from journalism |
| `money.json` | Distinct dollar figures with `metric_type` and overlap notes. **$9 billion is not in this family** |
| `contradictions.json` | Guthmann vs “judge ordered payments”; 65 vs 68 convictions; $250M vs $300M; S&S $18M vs $17.4M |
| `events.json` | Dated chronology (charging waves, OLA report, sentences, Guthmann statement, juror-bribery plea). Lead-only events are tagged `LEAD_UNVERIFIED` |

Actor classes (do not collapse B/C into D):

- **A** — private actors defrauded programs (supported: charging, pleas, trial convictions)
- **B** — agency failed to detect/prevent (supported: OLA)
- **C** — negligence / incompetence / ill-prepared investigations (supported: OLA)
- **D** — officials knowingly committed crimes (**not supported** in collected sources)
- **E** — not defined in the source files (**not supported**)

## Do not sum restitution

Restitution orders can be **joint-and-several**. Especially:

- **$47,920,514** appears for both **Abdimajid Mohamed Nur** (S06, sentenced 2025-11-24) and **Abdiaziz Shafii Farah** (S07/S21, sentenced 2025-08-06). Treat as `MAY_OVERLAP` / likely joint-and-several on the Empire Cuisine loss. **Do not count two $47.9 million recoveries.**
- Mukhtar Mohamed Shariff “almost $50 million” (S21) may overlap the same Empire loss.
- S&S Catering individual restitutions (Sahra Mohamed Nur $5,000,240; Jesow $866,458) sit inside group alleged-loss figures. Do not add them to the group total.
- Mohamed-group (24-cr-15) site receipts and agreed restitutions sit inside the $14.6 million group alleged_loss.

There is **no** court-certified network `proven_loss`, cumulative `restitution_ordered` total, or `recovered_amount` in this harvest. Summing `money.json` will double-count.

## $250 million is alleged_loss, not proven_loss

- Charging headline **$250 million** (S01) = `alleged_loss` / `fraud_estimate`.
- “More than $240 million” obtained and disbursed (S01, repeated as “proven at trial” in S12) is still **not** a published court-certified net-loss judgment for the whole network.
- IRS Pub 3583 “over **$300 million**” (S21) is `AGENCY_POSITION`, not a court finding. See `contradictions.json` fof-x-003.
- FOF pass-through **~$3.4 million (2019) → nearly $200 million (2021)** is `amount_paid` / `program_spend`, not a loss total.
- **Do not put $9 billion in this family.** It does not appear in S01–S28. Claim `fof-c-022` records the negative finding only.

## Journalism leads are not a ceiling

`L01`–`L05` are `LEAD_UNVERIFIED`. Do not treat them as DOJ-verified:

- **68 convictions as of July 24, 2026** is **not verified** here (`fof-c-004`, status `unresolved`). Last verified official conviction count is **65 on 2026-04-09** (S11). KSTP’s Dool “68th” / “70th then 68th” note is a lead.
- **July 22, 2026 120-month** juror-bribery sentence attributed to Abdiaziz Farah is a lead (L03). What **is** on .gov: his **plea** 2025-06-17 and **Abdulkarim** Farah’s **57-month** sentence 2026-03-04. Do not confuse the two people or terms.
- Abdinasir Mahamed Abshir remains **charged** in this family even though L02 reports a 6.5-year sentence.
- Said Shafii Farah’s reported fraud-trial **acquittal** is journalism only; status is **pleaded** (juror bribery). Do not mark acquitted.
- Running totals of 78–80 charged are unverified; last verified official charged count in a captured .gov page is the **77th** (Ousman Camara, 2025-11-20).

If a defendant’s status is only `charged`, read `coverage_note`: later plea/sentence PRs often exist but were Akamai-blocked and were **not** fetched. Do not fill them from memory or news.

## Local primary files (hashed)

SHA-256 of files under `feeding-our-future/primary/`:

- `ola-2024-mdefof.pdf` — OLA full special review (S26)
- `ola-2024-mdefof-sum.pdf` — OLA summary (S27)
- `bock-said-order-acquittal-2025-08-22.pdf` — Brasel order (S22)
- `mncourts-guthmann-2022-09-23.html` — Judicial Branch statement (S28)
- `ola-2024-mdefof.txt` — extracted text of the full OLA report (companion to S26)

## OLA page map (claims)

Use these page cites; they come from CLAIMS.md, not from re-reading the PDF for new facts:

- **S-1** — summary headline: inadequate oversight created opportunities for fraud (`fof-c-012`)
- **p. 37** — 2018 CACFP administrative review, no follow-up (`fof-c-014`)
- **p. 49** — ≥30 complaints June 2018–Dec 2021 (`fof-c-015`); FOF asked to investigate itself / trustworthiness (`fof-c-016`)
- **pp. 49, 51, 55** — asked FOF to investigate itself (`fof-c-016`)
- **p. 50** — USDA OIG general warnings; MDE not prepared; Oct/Nov 2020 referral (`fof-c-018`, `fof-c-019`)
- **pp. 53, 57** — some complaints not investigated; investigations inadequate (`fof-c-017`)

MDE disputes the adequacy characterization (Jett letter 2024-06-07, `fof-c-025`). That is an `AGENCY_POSITION` rebuttal, not a withdrawal of the audit.

## Proposition classes in public write-ups

Supported: **A, B, C**. Not supported: **D, E**. Guthmann (S28) and OLA (S26/S27) are about oversight and civil procedure, not about MDE officials stealing funds. Keep that distinction.

## Local charging instrument: United States v. Mohamed, 0:24-cr-00015 ECF 1

Count-mapped 2026-08-27 from the face of the 37-page scan (`court/extracts/mohamed-24-cr-015-ecf1.json`). Feeding Our Future family, **not HSS**.

- 47 counts: Count 1 §§ 371/1343 (all 7); Counts 2–20 § 1343 (all 7); Count 21 § 371 bribery conspiracy (**not** Gandi Yusuf Mohamed); Counts 22–37 § 666 (Ikram on every row); Count 38 § 1956(h) (all 7); Counts 39–47 § 1957.
- Family **received** more than **$12 million** (`amount_paid`, para 91). Site receipts and Star Distribution ~$10 million **overlap** that figure. Do not add them to each other, to Bock $250 million, or to HSS.
- FOF-sponsor recitals (~$3.4 million 2019 / nearly $200 million 2021 / nearly $18 million admin fees) are sponsor-wide `amount_paid`, not this family's loss.
- CHARGED_ALLEGED only. Not a judgment.

## Local charging instrument: United States v. Farah, 0:22-cr-00124 ECF 57

Count-mapped 2026-08-27 from the face of the 48-page superseding indictment (`court/extracts/farah-22-cr-124-ecf57.json`). Empire / Feeding Our Future family, **not HSS**, not the Mohamed 24-cr-015 family.

- 43 counts: Count 1 §§ 371/1343 (all 8); Counts 2–12 § 1343 (Aftin on none of those rows); Count 13 § 371 bribery conspiracy (Abdiaziz, Said, Mukhtar only); Counts 14–19 § 666; Count 20 § 1956(h) (**Hayat omitted**); Counts 21–42 § 1957; Count 43 § 1542 (Abdiaziz only, same theory as ECF 22). Forfeiture is Counts 1–42, not 43.
- **$40 million** “scheme to defraud” (para 1, `alleged_loss`) is the same figure as para 47 “fraudulently received approximately $40 million” (`amount_paid`). Do **not** add to Bock **$250 million**. Empire Cuisine >$28M, ThinkTechAct, and shell receipts are subsets.
- FOF ~$3.4M (2019) / nearly $200M (2021) / nearly $18M admin, and Sponsor A recitals, are sponsor-wide `amount_paid`, not this indictment’s extra loss.
- CHARGED_ALLEGED only. Not a judgment. Count 17 table date Aug 13 vs para 146 Aug 17 is the same $10,000 check.

