# Harvest report — 26 August 2026 (evening, America/Chicago)

**Working copy:** `/workspace/minnesota-fraud-corpus/`  
**This pass:** primary-source gap fill. No GitHub write. No CourtListener. No PACER buys. No tokens.  
**Editorial rules in force:** A–E not collapsed; journalism is a lead; `$9B` remains AUSA Thompson oral estimate 2025-12-18 (not in USAO PR); overlapping dollars not summed.

Companion harvest notes (do not duplicate this file’s full table):

- `feeding-our-future/HARVEST-2026-08-26-evening.md`
- `medicaid-hcbs/HARVEST-2026-08-26-evening.md`
- `oversight-law/HARVEST-2026-08-26-evening.md`
- Claim stubs: `cases/_inbox/claims-new.json` (8 records; does **not** overwrite existing `claims.json`)

PDFs landed in `oversight-law/pdfs/`.

---

## 1. Sources captured this evening

### A. CMS / HHS — Federal Register (official host)

| ID | Title | URL | Date | evidence_class | What it proves (one sentence) |
|---|---|---|---|---|---|
| **FR-2026-00512** | Notice of Opportunity for Hearing on Compliance of Minnesota State Plan Provisions Concerning Program Integrity and Fraud, Waste, and Abuse With Title XIX | Canonical HTML: https://www.federalregister.gov/documents/2026/01/14/2026-00512/notice-of-opportunity-for-hearing-on-compliance-of-minnesota-state-plan-provisions-concerning ; govinfo PDF: https://www.govinfo.gov/content/pkg/FR-2026-01-14/pdf/2026-00512.pdf ; API: https://www.federalregister.gov/api/v1/documents/2026-00512.json | Published **2026-01-14**; letter dated **2026-01-06**; FR citation **91 FR 1539–1542**; FR Doc. **2026-00512** | `AGENCY_POSITION` | Official CMS/HHS publication of Administrator Oz’s SSA § 1904 finding that Minnesota Medicaid is substantially out of compliance with SSA § 1902(a)(64) and 42 C.F.R. part 455 subpart A, reproducing the Jan. 6 letter that had previously been known only via KSTP/DocumentCloud. |
| (same document) | Jan. 6 letter to Gov. Walz (embedded) | Same | 2026-01-06 | `AGENCY_POSITION` | CMS directed a CAP after a **Dec. 5, 2025** notice to the Minnesota Medicaid Director; deemed the Dec. 31 CAP deficient; estimated quarterly FFP withhold **$515,154,947.56** (14 high-risk services); stated those 14 programs consume **$3.75 billion** federal+state resources; announced a focused CMS-64 review. **Not proven_loss.** |

Local copy: `oversight-law/pdfs/cms-fr-2026-00512-1904-hearing.pdf`  
SHA-256: `130fe15b667755bd24e84f5f83bef3fc52d820d44e65aee83ccc37645152c9ee`

**Still missing on cms.gov as standalone PDFs:** Dec. 5, 2025 letter; the original Jan. 6 letter file (text is now in the FR); March 19, 2026 CAP-approval letter (still DocumentCloud / state-hosted).

### B. CMS Newsroom (already indexed; re-fetched body)

| ID | Title | URL | Date | evidence_class | What it proves |
|---|---|---|---|---|---|
| **CMS-CRACK** | Trump Administration Prioritizes Affordability by Announcing Major Crackdown on Health Care Fraud | https://www.cms.gov/newsroom/press-releases/trump-administration-prioritizes-affordability-announcing-major-crackdown-health-care-fraud | 2026-02-25 | `AGENCY_POSITION` | CMS deferred **$259,505,491** FFP on Minnesota Q4 FY2025 claims ($243.8M “unsupported or potentially fraudulent” + $15.4M immigration-status documentation). Deferral ≠ disallowance ≠ stolen. |

### C. Optum Phase 1 — official Minnesota hosts (not KSTP)

| ID | Title | URL | Date | evidence_class | What it proves |
|---|---|---|---|---|---|
| **OPTUM-P1** | Minnesota Payment Integrity: Phase 1 Summary Report – Achievements, Findings and Recommendations | Minnesota Legislative Reference Library (official): https://www.lrl.mn.gov/docs/2026/other/260346/mn-pi-phase-1-summary-report-13026-final-redacted.pdf ; catalog: https://www.lrl.mn.gov/edocs/edocs?oclcnumber=1573848035 | Face date **2026-01-30** (Final); PDF metadata created 2026-01-30 | `AGENCY_POSITION` (contractor report for DHS) | Over **$52.3 million** “direct recoveries” (policy-violation recoupment opportunities on paid FFS claims); **>$1.7 billion** “potential recoveries” (missing/vague policy; may need medical-necessity review); **>$165 million** cost avoidance Q3→Q4 2025; **>$21 million** provider findings; **>$2.9 million** pre-pay warrant-cycle findings; 192 analytics; 46 months FFS; **MCO out of scope**. |
| **OPTUM-VA** | MN PI RRT Vulnerability Assessment (redacted) | https://www.lrl.mn.gov/docs/2026/other/260346/mn-pi-rrt-vulnerability-assessment-13126-redacted.pdf and House committee copy https://www.house.mn.gov/comm/docs/9KYnKlWAY0iCn0UO2gciNA.pdf | 2026-01-31 / House copy 2026-02-06 | `AGENCY_POSITION` | Companion deliverable quantifying MMIS edits and 14-program FWA evaluation; Phase 1 of a one-year contract. |
| **DHS-OPTUM-206** | Minnesota advances work on Medicaid anti-fraud systems | https://mn.gov/dhs/media/news/?id=1053-723194 | 2026-02-06 | `AGENCY_POSITION` | Medicaid Director John Connolly: “This is not a measure of fraud, waste and abuse.” |

Local: `oversight-law/pdfs/mn-pi-phase-1-summary-report-13026-final-redacted.pdf`  
SHA-256: `edb4af6d7cd44e5bdde683b82759bcd6feccbe20723aa30208190a9b83cc47b1`  
Also: `oversight-law/pdfs/mn-pi-rrt-vulnerability-assessment-13126-redacted.pdf`

**Do not publish $1.7B as stolen.** It overlaps $52.3M; MCO excluded; DHS disclaims it as a fraud measure.

### D. House Oversight — oversight.house.gov primary

| ID | Title | URL | Date | evidence_class | What it proves |
|---|---|---|---|---|---|
| **HO-HEAR-P2** | Oversight of Fraud and Misuse of Federal Funds in Minnesota: Part II (hearing page) | https://oversight.house.gov/hearing/oversight-of-fraud-and-misuse-of-federal-funds-in-minnesota-part-ii/ | Hearing **2026-03-04** 09:00 HVC-210 | hearing record locator | Witnesses: Gov. Tim Walz; AG Keith Ellison; Rev. Mariah Tollgaard (minority). **Official GPO transcript still not retrieved.** |
| **HO-STAFF-0304** | *The Cost of Doing Nothing: How Tim Walz and Keith Ellison Fueled Minnesota’s Fraud Explosion* (interim majority staff report, 53 pp.) | https://oversight.house.gov/wp-content/uploads/2026/03/The-Cost-of-Doing-Nothing_How-Tim-Walz-and-Keith-Ellison-Fueled-Minnesotas-Fraud-Explosion_3.4.26_FINAL.pdf | 2026-03-04 | `LEGISLATIVE_FINDING_OR_ALLEGATION` | Majority staff **alleges** official knowledge as early as 2019 (DHS) / April 2020 (MDE), unused stop-pay authority, and retaliation; **repeats** “potentially $9 billion in Medicaid-related funds” — not an independent measurement. |
| **HO-COMER-REL** | Oversight Committee Releases Explosive Testimony… | https://oversight.house.gov/release/oversight-committee-releases-explosive-testimony-revealing-minnesota-fraud-cover-up-by-governor-walz-and-attorney-general-ellison/ | 2026-03-04 | `LEGISLATIVE_FINDING_OR_ALLEGATION` | Majority press wrap of the same report. |
| **HO-VANCE-LTR** | Letter to VP Vance accompanying MN report | https://oversight.house.gov/wp-content/uploads/2026/06/Letter-to-JD-Vance-to-accompany-MN-report.pdf | ~2026-06 | `LEGISLATIVE_FINDING_OR_ALLEGATION` | Requests White House Task Force review of Minnesota social-services programs; restates staff-report allegations. |
| **HO-WALZ-WT** | Governor Tim Walz written testimony | https://oversight.house.gov/wp-content/uploads/2026/03/Walz-Written-Testimony.pdf | 2026-03-04 | `LEGISLATIVE_FINDING_OR_ALLEGATION` (hearing submission; oath status of oral testimony not confirmed from GPO transcript) | Walz: “the buck ultimately stops with me”; “if you defraud public programs… we will throw you in jail.” Not a confession of D/E. |
| **HO-ELLISON-WT** | Statement of AG Keith Ellison | https://oversight.house.gov/wp-content/uploads/2026/03/Ellison-Written-Testimony.pdf | 2026-03-04 | `LEGISLATIVE_FINDING_OR_ALLEGATION` | Ellison describes MFCU work and disputes federal political targeting; not a charging document. |
| **HO-HONER-TI** | Transcribed interview of Emily Honer | https://oversight.house.gov/wp-content/uploads/2026/06/Emily-Honer-Transcript.pdf | Interview 2026-01-29; posted ~2026-06 | committee interview record | MDE nutrition director; staff-report excerpt: USDA OIG response to Oct/Nov 2020 referral “basically absent”; to her knowledge no investigation started into 2021. |
| **HO-LOUREY-TI** | Transcribed interview of Tony Lourey | https://oversight.house.gov/wp-content/uploads/2026/06/Tony-Lourey-Transcript.pdf | 2026-02-06 | committee interview (URL confirmed; body quoted via staff report this pass) | 2019 communications with Chief of Staff Chris Schmitter on program-integrity tools/authority for CCAP/NEMT/MAT; would not speak to conversations he was not in about briefing Walz. |
| **HO-RICKER-TI** | Mary Cathryn Ricker transcript | https://oversight.house.gov/wp-content/uploads/2026/06/Mary-Cathryn-Ricker-Transcript.pdf | 2026-02-05 | committee interview (URL confirmed) | Former MDE commissioner 2019–2021. |
| **HO-GANDHI-TI** | Shireen Gandhi transcript | https://oversight.house.gov/wp-content/uploads/2026/06/Shireen-Gandhi-Transcript.pdf | 2026-02-17 | committee interview (URL confirmed) | Then-temporary DHS commissioner; EIDBI/HSS high-risk elevation. |
| **HO-HARPSTEAD-TI** | Jodi Harpstead transcript | https://oversight.house.gov/wp-content/uploads/2026/06/Jodi-Harpstead-Transcript.pdf | 2026-02-23 | committee interview (URL confirmed) | Former DHS commissioner 2019–2025. |
| **HO-GRUMDAHL-TI** | Eric Grumdahl transcript | https://oversight.house.gov/wp-content/uploads/2026/06/Eric-Grumdahl-Transcript.pdf | 2026-02-12 | committee interview (URL confirmed) | Former DHS assistant commissioner, homelessness/housing. |
| **HO-SCHMITTER-TI** | Christopher Schmitter transcript | https://oversight.house.gov/wp-content/uploads/2026/06/Chris-Schmitter-Transcript.pdf | 2026-02-27 | committee interview (URL confirmed) | Former Walz chief of staff 2019–2025. |
| **HO-KORTE-TI** | Daron Korte (cited in staff report; PDF filename not separately fetched) | Staff report p. 14 cites interview Feb. 3, 2026 | 2026-02-03 | committee interview (locator via staff report) | MDE had authority to terminate FOF funding without USDA approval. |

Local copies:  
`oversight-law/pdfs/house-oversight-cost-of-doing-nothing-2026-03-04.pdf` (SHA-256 `55decf1f87f12c80caab0bf0b01094f6c256d4bd620b59fa2512a709b18c615a`)  
`oversight-law/pdfs/emily-honer-transcript-2026-01-29.pdf`  
`oversight-law/pdfs/walz-written-testimony-2026-03-04.pdf`  
`oversight-law/pdfs/ellison-written-testimony-2026-03-04.pdf`  
`oversight-law/pdfs/house-oversight-letter-jd-vance-2026-06.pdf`

**A–E warning:** majority staff D-adjacent language is **not** a charging document. Lourey excerpt does **not** close the loop that Walz was briefed. No D/E charging instrument found this pass.

### E. Feeding Our Future — IRS-CI / DOJ OPA re-fetch (bodies confirmed)

These were already numbered S05 / S06 / S12; this pass captured **full readable bodies** (USAO-MN still Akamai-blocked).

| ID | Title | URL | Date | evidence_class | What it proves |
|---|---|---|---|---|---|
| **S05** (re-fetched) | 77th defendant charged in Feeding Our Future fraud scheme | https://www.irs.gov/compliance/criminal-investigation/77th-defendant-charged-in-feeding-our-future-fraud-scheme | 2025-11-20 | `CHARGED_ALLEGED` | **Ousman Camara**, nine-count indictment (wire fraud, federal programs bribery, money laundering); >300,000 meals claimed; >$1 million claimed; >$100,000 wired abroad; ~$87,000 kickbacks; USDA SNAP disqualification of K’s Grocery, Aug. 2015. |
| **S06** (re-fetched) | Feeding Our Future defendant sentenced to 10 years in prison | https://www.irs.gov/compliance/criminal-investigation/feeding-our-future-defendant-sentenced-to-10-years-in-prison | 2025-11-24 | `ADJUDICATED` | **Abdimajid Mohamed Nur**: 120 months + 3 years SR; restitution **$47,920,514**. Empire Cuisine group “stole more than $47 million” “as demonstrated at trial.” Same restitution figure as Farah — **do not add**. |
| **S12** (OPA body captured) | Feeding Our Future Ringleader Sentenced to 500 Months | https://www.justice.gov/opa/pr/feeding-our-future-ringleader-sentenced-500-months (PR 26-549) | 2026-05-22 | `ADJUDICATED` | **Aimee Bock**, 44, **500 months**. “As proven at trial”: >250 sites; ~$3.4M (2019) to nearly $200M (2021); “fraudulently obtained and disbursed more than $240 million”; >$18 million administrative fees. Judge Brasel: “This was a fraud vortex and you were at the epicenter of it.” **Does not state a restitution dollar in this PR.** |

### F. USDA OIG (oig.usda.gov) — national, **not** Minnesota FOF

| ID | Title | URL | Date | evidence_class | What it proves |
|---|---|---|---|---|---|
| **USDA-OIG-50024** | USDA’s Compliance with Improper Payment Requirements for Fiscal Year 2023 (Audit Report 50024-0004-24) | https://www.oig.usda.gov/sites/default/files/reports/2024-11/50024-0004-24FRfinal-distribution.pdf | July 2024 | `AUDIT_FINDING` (national) | USDA not compliant with 4 of 6 PIIA requirements FY2023; FNS should ensure proper reporting/classification of **CACFP**. **Not a Minnesota Feeding Our Future investigation and not a questioned-cost report on MDE.** |

Local: `oversight-law/pdfs/usda-oig-50024-0004-24-improper-payments.pdf`

---

## 2. Still missing (priority)

1. **Official FOF conviction count after 65 (2026-04-09).** Journalism of 68 (Dool, July 2026) / 69 / 80 charged remains **`LEAD_UNVERIFIED`**. No matching DOJ OPA or IRS-CI page retrieved this evening. Fox 9 (2026-08-26) said 66 convicted / >80 charged — also journalism.
2. **78th-defendant USAO-MN PR body** (`justice.gov/usao-mn/pr/78th-defendant-charged-feeding-our-future-fraud-scheme`) — still Akamai/unfetched; no IRS-CI republication found.
3. **Abdiaziz Farah July 2026 120-month juror-bribery sentence** — still no justice.gov / irs.gov / fbi.gov PR. Plea is on .gov (S08); sentence is journalism/reprint (Red Lake Nation News).
4. **Standalone cms.gov PDFs** of Dec. 5, 2025 CAP-request letter and March 19, 2026 CAP-approval letter.
5. **Minnesota-specific USDA OIG** audit, investigation closeout, or press release on Feeding Our Future / MDE CACFP-SFSP. Honer testimony + OLA p. 50 record a referral; OIG work product still absent from oig.usda.gov search.
6. **Official GPO / committee hearing transcript** of March 4, 2026 Part II (Walz/Ellison oral testimony). Written statements captured; floor transcript not.
7. **Daron Korte, Dave Greeman** full transcript PDFs (named in staff report; Korte URL not separately downloaded).
8. **Yussuf / Star Autism plea** USAO PR or PACER (journalism March 2, 2026).
9. **USAO 18 Dec 2025 press-conference transcript/video** (source of $9B arithmetic). Still not in any written DOJ PR.
10. **PACER charging instruments** (forbidden this pass / CourtListener quota).
11. **Proposition D/E:** no primary charging document naming a Minnesota elected official, DHS/MDE commissioner, or CMS official as a criminal defendant.

---

## 3. Claims added

`cases/_inbox/claims-new.json` — **8 stubs**, schema-shaped, not merged into existing `claims.json`:

| claim_id | evidence_class | proposition | One-line |
|---|---|---|---|
| cms-c-001 | AGENCY_POSITION | B | CMS Jan 6 2026 substantial-noncompliance finding (91 FR 1539) |
| cms-c-002 | AGENCY_POSITION | B | $515,154,947.56 quarterly FFP withhold **formula** (not stolen) |
| cms-c-003 | AGENCY_POSITION | B | $3.75B 14-program **program_spend** (CMS analysis) |
| cms-c-004 | AGENCY_POSITION | B | $259,505,491 Q4-FY2025 **deferral** |
| optum-c-001 | AGENCY_POSITION | B | Optum $52.3M **identified_for_recovery** (FFS only) |
| optum-c-002 | AGENCY_POSITION | C | Optum $1.7B potential recoveries ≠ fraud; Connolly disclaimer |
| ho-c-001 | LEGISLATIVE_FINDING_OR_ALLEGATION | B | Majority staff 2019/2020 knowledge allegation; Lourey does not close Walz-briefing loop; **not D/E** |
| fof-c-031 | LEGISLATIVE_FINDING_OR_ALLEGATION | B | Honer: USDA OIG response to Oct/Nov 2020 MDE referral “absent” |

Bock 500-month, Camara 77th, and Nur $47,920,514 already exist in `cases/feeding-our-future/claims.json` (fof-c-009 / fof-c-003 / fof-c-024). Not duplicated.

---

## 4. Money hygiene reminder (this pass)

| Figure | metric_type | Do not treat as |
|---|---|---|
| $515,154,947.56 | program_spend / withhold formula | proven_loss |
| $3.75 billion | program_spend | fraud total |
| $259,505,491 | identified_for_recovery (deferral) | stolen / disallowance |
| $52.3 million | identified_for_recovery | recovered_amount |
| $1.7 billion | unknown_or_disputed (policy-gap opportunity) | fraud_estimate or proven_loss |
| $9 billion | fraud_estimate (Thompson oral; staff report **repeats**) | proven_loss |
| $47,920,514 Nur | restitution_ordered | add to Farah’s same figure |
| >$240 million FOF disbursed | post-trial DOJ characterization | court-certified network net-loss |

---

**last_checked:** 2026-08-26 evening CT  
**next_check:** USAO-MN/IRS-CI for post-65 conviction PRs; cms.gov originals of Dec 5 / Mar 19 letters; USDA OIG FOIA for MN CACFP/SFSP referral file.
