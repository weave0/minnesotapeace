# MinnesotaPeace research-state report

**As of:** 26 August 2026, America/Chicago  
**Coverage state:** first harvest. Not complete. Active investigations continue.  
**Working copy:** `/workspace/minnesota-fraud-corpus/` (not yet committed; GitHub write still pending)  
**Repo branch to receive this:** `weave0/minnesotapeace` / `research/minnesota-fraud-corpus`

This report is an internal snapshot of what the record currently permits. It is not a homepage.

---

## 1. Corpus statistics (this pass)

| Category | Count / note |
|---|---|
| Investigation families opened | Feeding Our Future; Medicaid HCBS (HSS, EIDBI, ICS, high-risk list); oversight/law |
| Markdown source/claim files | 12 |
| Primary PDFs on disk | 14 unique documents (~28 MB; OLA FOF PDF stored twice) |
| FOF numbered primary sources (S-ids) | 31 |
| FOF structured claims | 15 |
| FOF named defendants in table | 79 (many still status=charged pending later .gov PRs) |
| Medicaid HCBS official PRs indexed | 6 DOJ + AG/DHS companions |
| Statute files | federal + Minnesota (Revisor / uscode locators) |
| Precedent opinions on disk | Escobar, Schutte, Ciminelli, Kousisis, plus 8th Cir. *Cairns* locators |
| Court records beyond press releases | Bock/Said post-trial order (2025-08-22); MN Judicial Branch Guthmann statement (2022-09-23) |
| PACER indictment PDFs | 0 (gap) |
| Journalism treated as ceiling | 0 |

---

## 2. Investigation coverage

### Feeding Our Future — deepest family, still incomplete

| Dimension | State |
|---|---|
| Source depth | Official charging/plea/sentencing PRs (DOJ OPA + IRS-CI republications of USAO-MN); OLA 2024 special review PDF + extracted text; one district-court order; Judicial Branch statement |
| Legal maturity | High on program structure and charged statutes as described in PRs; low on original indictment PDFs |
| Prosecution maturity | Mature. First wave 2022-09-20 (47 defendants). 77th defendant charged 2025-11-20 (Ousman Camara). Leader Aimee Bock sentenced 500 months (2026-05-22). Multiple restitution orders exist |
| Major missing records | PACER ECF 1 indictments; 78th+ charging PR body; official conviction count after 65 (2026-04-09); July 2026 juror-bribery sentence PR; USDA OIG MN work product; civil Ramsey County docket |

### Medicaid HCBS (HSS / EIDBI / ICS / high-risk list) — charging-PR deep, court-file shallow

| Dimension | State |
|---|---|
| Source depth | USAO-MN and DOJ OPA PRs; MN AG; DHS program-integrity page; CMS/MN CAP materials on disk |
| Legal maturity | Program-design and growth figures are in charging narratives (treat as government allegation of *spend*, not of *fraud*) |
| Prosecution maturity | First HSS wave 2025-09-18 (8 people). First EIDBI charge 2025-09-24 (Asha Farhan Hassan / Smart Therapy). Dec 18 2025 wave + ICS search. May 21 2026 takedown (15 defendants, “over $90M intended_loss”, mix of Medicaid and child-care — do not treat as all HCBS) |
| Major missing records | PACER informations/pleas; CMS Dec 5 2025 and Jan 6 2026 letters; Optum Phase 1 official host; House Oversight transcripts |

### Oversight / law — usable scaffold

OLA FOF 2024; OLA BHA grants 2021 and 2026; OLA CCAP 2019 (controls + fraud-allegations); HHS-OIG CCAP audit; HHS-OIG MFCU inspection; MN CAP response 2026-01-30; PERM RY2025 notification. Statutes and key SCOTUS/8th Cir. opinions located. **No primary charging document of a Minnesota elected official (bucket D/E empty).**

---

## 3. Most important verified findings (ranked by evidentiary strength)

1. **ADJUDICATED — Aimee Marie Bock.** Convicted at trial (all counts tried); post-trial motions denied 2025-08-22; sentenced **500 months** 2026-05-22. Actor class **A**.
2. **ADJUDICATED — Abdimajid Mohamed Nur.** Sentenced 2025-11-24 to **120 months**; restitution **$47,920,514** (`restitution_ordered`). Empire Cuisine group “stole more than $47 million” as characterized post-trial by USAO. Joint-and-several risk: Abdiaziz Farah’s restitution is the same figure — **do not add**.
3. **ADJUDICATED — Abdiaziz Shafii Farah (fraud).** Sentenced 2025-08-06 to **28 years**; restitution **$47,920,514**. Juror-bribery **plea** 2025-06-17 is on .gov. The July 22 2026 **120-month bribery sentence** is journalism-led, not yet a captured USAO PR.
4. **AUDIT_FINDING — OLA (13 June 2024).** MDE’s inadequate oversight “created opportunities for fraud.” Complaints 2018–2021 poorly handled, including asking Feeding Our Future to investigate itself. Supports **B** and **C**. Does **not** find that MDE officials stole the funds. Commissioner Jett’s response attributes the crime to private actors (**A**).
5. **AGENCY_POSITION / contradiction record — MN Judicial Branch, 23 Sept 2022.** Judge John Guthmann did **not** order MDE to resume Feeding Our Future reimbursements; MDE resumed them voluntarily. Any “the judge forced payments” public claim is contradicted by the court system’s own statement.
6. **CHARGED_ALLEGED — HSS first wave, 18 Sept 2025.** Eight defendants, four dockets (25-cr-349/351/353/354). Do not sum billed+paid across entities into an official “$8 million” total.
7. **CHARGED_ALLEGED then plea — EIDBI.** Asha Farhan Hassan / Smart Therapy: more than **$14 million** EIDBI reimbursement (`amount_paid` / `alleged_loss` at charging); separate FOF claim ~$465k. Pleaded guilty 2025-12-18. Later Smart+Star indictment figures **$46.6M billed / $21.2M paid** overlap the $14M — **not additive**.
8. **CHARGED_ALLEGED — Star Autism.** Abdinajib Hassan Yussuf: more than **$6 million** EIDBI obtained (Dec 18 2025 PR). Journalism of a March 2026 plea is **not** on a captured USAO PR.

---

## 4. Major unresolved questions

- What is the latest **official** FOF charged/convicted count after 77 charged (2025-11-20) and 65 convicted (2026-04-09)?
- What is the court-certified **network** loss for FOF, if any exists, as distinct from the $250M charging headline and overlapping restitution orders?
- What did USDA OIG actually do after MDE’s late-2020 referral?
- Exact OLA page-level quotes for the “≥30 complaints, June 2018–Dec 2021” claim (PDF is on disk; passage binding still needed).
- CMS’s own Dec 5 2025 / Jan 6 2026 letters (content currently known via MN DHS CAP correspondence).
- Optum Phase 1: ~$52.3M identified recoveries and >$1.7B “opportunities” — circulating as a KSTP-hosted PDF; not yet captured from mn.gov.
- Yussuf / Star Autism plea: PACER or USAO PR?
- Any **D/E** evidence: named official as criminal defendant? **None found this pass.**
- Transcript of Joseph H. Thompson’s 18 Dec 2025 press conference (source of the $9B arithmetic).

---

## 5. Major contradictions (do not silently reconcile)

| Topic | Version A | Version B |
|---|---|---|
| $9 billion | Oral estimate by AUSA Thompson, 18 Dec 2025: 14 high-risk programs billed ~$18B since 2018; “half or more” could be fraud; “but we’ll see.” **Not in the USAO PR that day.** | DHS IG James Clark: speculation “shocking”; Medicaid Director John Connolly: evidence in hand “tens of millions,” excluding FOF |
| FOF conviction count | Official: 65 on 2026-04-09 | Journalism: 68 (July 2026) / 69 (Aug 2026) |
| HSS start | USAO 2025-09-18: “dates back to July 2022” | Later USAO/DHS: July 2020 |
| HSS 2021 paid | USAO Sept/Dec 2025: >$21 million | OPA 2026-05-21: >$26 million |
| ICS cumulative paid | Dec 2025: >$400M since 2021 | May 2026: >$460M |
| 2025 payment withholds | DHS-PI Aug 2026: 490 | DHS CAP letter: “over 500” |
| EIDBI dollars | Hassan PR: Smart Therapy obtained >$14M | May 2026 indictment: Smart+Star billed $46.6M / paid $21.2M (overlap) |
| Guthmann payments | Public claim: judge ordered MDE to pay | Judicial Branch 2022-09-23: Guthmann did not; MDE resumed voluntarily |
| $90M takedown | OPA: “over $90 million in intended_loss” | Includes CCAP/GSCSPP child-care cases that are not Medicaid HCBS |

---

## 6. Money reconciliation (do not sum)

| Figure | Metric type | Status | Notes |
|---|---|---|---|
| $250 million FOF scheme | alleged_loss / fraud_estimate | charging headline 2022; repeated later | Not a restitution total |
| >$240 million obtained/disbursed through FOF | amount_paid / alleged_loss | DOJ charging + Bock sentencing PR | Pass-through, not net proven loss |
| $47,920,514 | restitution_ordered | Nur and Farah (same figure) | Likely joint-and-several; **do not add** |
| HSS program paid $21M→$104M (2021–2024) | program_spend / amount_paid | USAO charging narrative | Program outlays, including any legitimate care |
| ICS >$400M / >$460M since 2021 | program_spend | two USAO vintages | Not alleged_loss |
| Smart Therapy >$14M EIDBI | amount_paid / alleged_loss | charging, then plea | Overlaps later $46.6M/$21.2M |
| Star Autism >$6M | amount_paid / alleged_loss | charging | |
| “Over $90 million” May 2026 takedown | intended_loss | OPA | Mixed programs |
| ~$9 billion | fraud_estimate | oral prosecutor statement | Denominator = 14-program spend (~$18B); numerator = “half or more” judgment. **Not proven_loss.** Later journalism (KARE 11) updates denominator to ~$20.83B — still not proven fraud |
| DHS >$56 million identified for recovery | identified_for_recovery | AGENCY_POSITION (Aug 2026) | ≠ recovered_amount |
| 490 payment withholds (2025) | n/a (count) | AGENCY_POSITION | Conflicts with “over 500” in CAP letter |

**Rule in force:** billed ≠ paid ≠ stolen ≠ estimated ≠ identified-for-recovery ≠ recovered ≠ restitution-ordered ≠ restitution-collected. Overlapping case amounts are not added to program estimates.

---

## 7. Knowledge / oversight findings (warning → recipient → response)

Documented, not editorialized:

- **OLA 2024:** MDE received complaints about FOF/sites from at least June 2018 through December 2021; some not investigated, some inadequately investigated; at times FOF was asked to investigate itself. Payments continued. Later: federal prosecution of private actors; OLA finding of inadequate oversight.
- **OLA 2024:** MDE told OLA it informed USDA OIG of suspected SFSP fraud in Oct/Nov 2020. OIG work product not in this corpus.
- **Judicial Branch 2022-09-23:** After civil litigation, MDE resumed reimbursements **voluntarily**; Guthmann did not order it.
- **HSS/EIDBI/ICS:** USAO charging narratives describe explosive program-spend growth vs original cost predictions. That is **program_spend**, used by prosecutors as context. It is not by itself proof of official criminal participation.
- **DHS 2026:** high-risk designation of 14 Medicaid service categories; CAP with CMS; payment withholds and revalidation. **AGENCY_POSITION** on stats. High-risk ≠ charged fraud in each category (several of the 14 have no federal indictment found this pass).
- **Bucket D/E:** no primary charging document naming a Minnesota elected official, DHS commissioner, or CMS official as a criminal defendant.

Assertion ladder for “officials knowingly facilitated fraud”:

- Available: complaints existed; agency received them; some investigations inadequate; payments continued; audit criticized oversight.
- Missing: source demonstrating that a specified official knowingly joined a fraudulent scheme.
- Current assessment: **strong B/C; insufficient D/E.**

---

## 8. Recommended next acquisition (priority order)

1. PACER/RECAP: FOF 22-CR-223, 22-CR-124, 22-CR-224, 22-CR-226, 22-CR-222, 22-CR-225; HSS 25-cr-349/351/353/354; Hassan/Yussuf EIDBI dockets; juror-bribery 24-cr-173.
2. Capture USAO-MN PRs currently blocked by Akamai (78th defendant; July 2026 Farah bribery sentence; later FOF conviction-count PRs). IRS-CI republications where they exist.
3. Passage-bind OLA 2024 PDF (already on disk) for complaint counts, dates, and “investigate itself” language, with page numbers.
4. CMS Dec 5 2025 and Jan 6 2026 letters (FOIA or *Minnesota v. HHS* docket).
5. Official Optum Phase 1 (mn.gov or legislative record), not the KSTP copy alone.
6. House Oversight majority/minority reports and transcribed interviews — label `LEGISLATIVE_FINDING_OR_ALLEGATION`.
7. HHS-OIG MFCU annual statistical reports FFY 2024–2026.
8. DHS official 14-category list page + PI dashboard snapshot (3,068 intakes / 1,647 cases / $56M identified_for_recovery) as dated AGENCY_POSITION.
9. Ramsey County civil docket (FOF v. MDE / Guthmann orders).
10. Secretary of State / NPI / provider-enrollment extracts for FOF meal-site entities (entity resolution).

---

## 9. What this pass will not do

- Put a TOTAL FRAUD number on a homepage.
- Treat $9 billion as stolen.
- Collapse oversight failure into official criminality.
- Treat shared addresses, common attorneys, or community as conspiracy.
- Gut `main` or the live mediation site until this substrate can replace it.

**last_checked:** 2026-08-26  
**next_check:** continue PACER/USAO capture; harden schemas; normalize FOF as the reference case family.
