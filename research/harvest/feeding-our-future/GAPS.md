# Feeding Our Future — Gaps

What this collection could **not** verify in a primary source as of 2026-08-26. Journalism and ChatGPT claims are noted as leads, not as facts.

---

## 1. Latest official defendant count after the 77th (Nov 20, 2025)

- Verified: 77th defendant **Ousman Camara**, 2025-11-20 (IRS-CI / USAO announcement).
- USAO-MN URL exists for a **78th** defendant (`https://www.justice.gov/usao-mn/pr/78th-defendant-charged-feeding-our-future-fraud-scheme`) but returned an Akamai interstitial; body not captured.
- Journalism (KSTP, Star Tribune Aug 19, 2026) says **80 charged**. Not verified on a fetched .gov page.
- **76th defendant name** not captured on a readable IRS/DOJ page.

## 2. ChatGPT claim: 68 convictions as of July 24, 2026

- **Not verified** on a DOJ OPA or IRS-CI page retrieved in this collection.
- Last **verified** official conviction count: **65 on April 9, 2026** (DOJ OPA, S11).
- Prior verified: **63** on March 20, 2026; **56** on Sept 18, 2025.
- KSTP reported Abdirashid Bixi Dool as 68th conviction (plea July 13, 2026) and an editor’s note that DOJ first said 70th then corrected to 68th. That is a **lead**, not a captured primary.
- Star Tribune Aug 19, 2026: 69 convicted / 80 charged — **lead**.

## 3. July 2026 120-month juror-bribery sentence (Abdiaziz Farah)

- Requested: DOJ release for a defendant sentenced July 2026 to 120 months for juror bribery.
- **Not retrieved** from justice.gov or irs.gov.
- Journalism (Star Tribune, Fox 9, KSTP, Red Lake Nation News reprint) identifies **Abdiaziz Shafii Farah**, sentenced **July 22, 2026**, by Judge **Eric C. Tostrud**, 120 months consecutive to 28 years.
- What **is** on .gov:
  - Abdiaziz Farah **plea** June 17, 2025, bribery of a juror (IRS-CI).
  - **Abdulkarim** Farah sentenced **57 months** March 4, 2026 (DOJ OPA) — different person, different term.
  - Nur plea agreement case number **24-cr-173**.
- Likely USAO-MN page was blocked by Akamai in the same way as other 2026 MN PRs.

## 4. Full indictment PDFs (PACER)

- CourtListener/RECAP opinions and motions quoting the 61-count Bock indictment were fetched (S22, S24).
- The **original indictment PDFs** (ECF 1 in 22-CR-223, 22-CR-124, etc.) were not downloaded in full from PACER.
- Consequently **18 U.S.C. § 1349** was **not found** in fetched charging text. Conspiracy is charged in the documents we have as **§ 371 + § 1343**, plus § 666, § 1956(a), § 1957, and juror bribery **§ 201**. Passport false-statement statute number for Abdiaziz Farah was not captured.

## 5. First-trial (June 2024) complete verdict roster

- IRS-CI confirms Abdiaziz Farah and Abdimajid Nur were convicted after the seven-week trial that began April 22, 2024.
- No DOJ “jury verdict” press release listing all seven defendants’ guilty/not-guilty counts was captured.
- Journalism says two defendants were acquitted of the fraud (including Said Farah, later convicted of juror bribery). **Unverified** in a primary.

## 6. Complete plea/sentence status for the original 47

- DEFENDANTS.md leaves most wave-1 names at **charged** unless a later .gov PR was fetched.
- Many additional USAO-MN plea and sentencing releases exist (USAO-MN `/pr/` slugs) but were Akamai-blocked. IRS-CI republications were used where search found them; the IRS-CI press-release index was not exhaustively scraped.

## 7. USDA OIG work product on Minnesota FOF

- No USDA OIG audit report, investigation closeout, or press release specifically quantifying MN CACFP/SFSP FOF fraud was found. **Still true as of 2026-08-29 recheck.**
- OLA (p. 50) records that MDE told OLA it informed USDA OIG of suspected SFSP fraud in **October or November 2020**, and that USDA OIG had previously issued **general** warnings about nutrition-program fraud risk. OLA does not publish an OIG investigative finding.
- House Education and the Workforce subpoenaed USDA OIG (2024); the OIG’s production is not in this corpus. **Confirmed and dated (2026-08-29 pass):** Committee Chairwoman Virginia Foxx issued the subpoena to USDA Secretary Vilsack and USDA Inspector General Phyllis Fong on **2024-09-04**, with a **2024-09-18** compliance deadline (`src-edworkforce-house-2024-09-04-subpoena-walz-usda-oig`). No public record of USDA/USDA OIG’s response, production, or compliance with that subpoena was located; assume this requires a direct records/FOIA request or a committee-records search rather than further open-web search.
- New in this pass: HuffPost (2026-01-30, `src-huffpost-2026-01-30-usda-knew-did-nothing`), drawing on the 2024 OLA audit plus original reporting, adds specific detail MDE previously flagged to USDA — a **~252% vs. ~14%** reimbursement-growth disparity and a "perfect attendance" pattern USDA dismissed as consistent with pandemic waivers — and quotes an **anonymous** former USDA official describing internal recognition of likely fraud and a decision by superiors not to get involved. This deepens the MDE-side and journalistic account of the referral’s aftermath but is still not USDA/USDA-OIG’s own work product, and the anonymous quote should not be elevated above LEAD-tier confidence.
- FNS integrity rulemaking cites 2011/2013 OIG audits that are **national** and predate FOF.

## 8. Court-certified network loss / recovery totals

- No primary in this corpus publishes a single **proven_loss** for the entire FOF network, a cumulative **restitution_ordered** total, or a **recovered_amount** / **forfeiture_ordered** grand total.
- Official language varies: **$250 million** (2022 charging), **$250 million** or **$300 million** (later USAO/IRS), **>$240 million** “obtained and disbursed” through FOF (charging and Bock sentencing).
- Individual restitution (e.g., $47,920,514) may be joint-and-several; summing orders would double-count.
- **$9 billion** does not appear.

## 9. Civil recovery against Feeding Our Future / MDE legal-fee claim

- Journalism mentions MDE seeking legal fees from FOF after the civil case. The Ramsey County docket, Guthmann written orders (June 2021 contempt, $35,750 sanctions, etc.), and any civil judgment were **not** downloaded. Only the Sept 23, 2022 Judicial Branch **statement** was captured.

## 10. “Sponsor A”

- March 2023 USAO PR refers to a second sponsor as “Sponsor A.” Legal name not in the captured PR.

## 11. Technical access limits

- `justice.gov/usao-mn/pr/*` frequently returned Akamai “Powered and protected by” pages (403/empty) via WebFetch.
- IRS-CI pages sometimes returned “Historical Content” stubs (e.g., Abdiaziz Farah 28-year sentence page).
- mncourts.gov WebFetch timed out; curl succeeded.

## 12. What was successfully obtained (so this file is not only negative)

Local copies under `primary/`:
- `ola-2024-mdefof.pdf` (official OLA special review)
- `ola-2024-mdefof-sum.pdf`
- `ola-2024-mdefof.txt` (extracted text)
- `mncourts-guthmann-2022-09-23.html`
- `bock-said-order-acquittal-2025-08-22.pdf` (Brasel, Aug 22, 2025)
