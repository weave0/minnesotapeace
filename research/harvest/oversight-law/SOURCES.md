# Minnesota Public-Program Fraud Corpus — Oversight & Law Sources

**Corpus path:** `/workspace/minnesota-fraud-corpus/oversight-law/`  
**Compiled:** 26 August 2026 (America/Chicago).  
**Ceiling:** primary sources only. Journalism is treated as a lead, not as proof.  
**Do not treat $9 billion as stolen.** See `NINE-BILLION.md`.

## How this corpus classifies propositions

| Code | Proposition type | What it means in this corpus |
|---|---|---|
| **A** | Private fraud | A private person or entity is alleged or proven to have obtained public funds by deceit, kickback, false claim, or similar crime. |
| **B** | Oversight failure | A government agency failed to prevent, detect, or stop fraud that a reasonably designed control environment should have addressed. Not the same as the agency committing the fraud. |
| **C** | Negligence / inadequate administration | Weak controls, unpaid findings, unpaid training, late reconciliations, or other administrative failure short of proven criminal intent by officials. |
| **D** | Official criminality | A public official personally committed a crime (bribery, theft, obstruction, false statements). **This corpus does not contain a primary-source conviction or charging document establishing D for Minnesota executive officers.** House Oversight staff reports allege knowledge and delay; those are labeled `LEGISLATIVE_FINDING_OR_ALLEGATION`, not proven D. |

**Evidence classes used throughout:** `STATUTE` · `JUDICIAL_HOLDING` · `AUDIT_FINDING` · `ENFORCEMENT_CHARGING_OR_OFFICIAL_PR` · `AGENCY_DETERMINATION` · `SWORN_TESTIMONY` · `LEGISLATIVE_FINDING_OR_ALLEGATION` · `fraud_estimate` · `JOURNALISM_LEAD` (locator only).

Companion files in this directory:

- `STATUTES.md` — federal and Minnesota statutes with official URLs
- `PRECEDENT.md` — Supreme Court and 8th Circuit holdings
- `NINE-BILLION.md` — provenance of the $9 billion figure
- `AUDITS.md` — OLA, HHS OIG, USDA OIG, GAO, CMS PERM/CAP
- `GAPS.md` — what was searched and not found as a primary source
- `pdfs/` — downloaded official PDFs where retrieval succeeded

---

## A. Office of the Legislative Auditor (Minnesota)

### A1. Minnesota Department of Education: Oversight of Feeding Our Future (Special Review)

- **Title:** Minnesota Department of Education: Oversight of Feeding Our Future
- **Publisher:** Office of the Legislative Auditor, Special Reviews Division
- **Date:** 13 June 2024 (minor edits 3 July 2024 on pp. 8, 9, 15)
- **Official HTML:** https://www.auditor.leg.state.mn.us/sreview/2024/mdefof.htm
- **Official PDF:** https://www.auditor.leg.state.mn.us/sreview/pdf/2024-mdefof.pdf (local: `pdfs/ola-2024-mdefof.pdf`)
- **Summary PDF:** https://www.auditor.leg.state.mn.us/sreview/pdf/2024-mdefof-sum.pdf
- **Evidence class:** `AUDIT_FINDING`
- **Supports:** **B** (oversight failure) and **C** (inadequate administration). OLA found MDE’s inadequate oversight “created opportunities for fraud.” OLA did **not** find that MDE officials stole the funds. Commissioner Willie L. Jett II’s 7 June 2024 response disputes the characterization and attributes the crime to indicted/convicted private actors (**A**).
- **What it does not support:** **D**. The report is an oversight review, not a criminal charging document against officials.

### A2. DHS Behavioral Health Administration Grants (Performance Audit, 2026)

- **Title:** Department of Human Services: Behavioral Health Administration Grants — Performance Audit
- **Publisher:** OLA Financial Audit Division
- **Date:** Released 6 January 2026. Scope: 1 July 2022 – 31 December 2024.
- **Official HTML:** https://www.auditor.leg.state.mn.us/fad/2026/fad26-01.htm
- **Official PDF:** https://www.auditor.leg.state.mn.us/fad/pdf/fad2601.pdf (local: `pdfs/ola-fad2601-bha-grants.pdf`)
- **LAC presentation:** https://www.auditor.leg.state.mn.us/meeting/mm/mm_Auditor_LAC-20260106-DHSBHAG-Pres.pdf
- **LAC minutes:** https://www.auditor.leg.state.mn.us/meeting/m/m_Auditor_LAC-20260106.htm
- **Evidence class:** `AUDIT_FINDING` (report); LAC minutes also record Legislative Auditor Judy Randall’s statement that some BHA staff created or backdated documents after the audit began (`SWORN_TESTIMONY` / official auditor statement to a legislative commission — treat minutes as official meeting record, not a criminal finding).
- **Supports:** **C** (inadequate internal controls; 13 findings, 4 repeats; payments for work before agreements executed; overpayments; unsupported costs; missing reconciliations). Finding 12 is a **legislative design gap**, not private fraud. Document backdating, if proven, is an integrity issue that could later support obstruction inquiry; it is **not** a completed **D** finding in this audit.
- **What it does not support:** that BHA grant dollars were stolen at a proven amount, or that named officials committed crimes.

### A3. DHS Behavioral Health Grants Management (prior audit)

- **Title:** Department of Human Services: Behavioral Health Grants Management
- **Publisher:** OLA Financial Audit Division
- **Date:** Report fad21-03 (period July 2017 – March 2020)
- **Official PDF:** https://www.auditor.leg.state.mn.us/fad/pdf/fad21-03.pdf (local: `pdfs/ola-fad21-03-bha.pdf`)
- **Evidence class:** `AUDIT_FINDING`
- **Supports:** **C** — internal controls “not adequate”; noncompliance with grant-oversight legal requirements and Office of Grants Management policy. Establishes that 2026 repeat findings have a documented prior-audit pedigree.

### A4. Child Care Assistance Program — Assessment of Internal Controls (2019)

- **Title:** Child Care Assistance Program: Assessment of Internal Controls
- **Publisher:** OLA Special Reviews
- **Official PDF:** https://www.auditor.leg.state.mn.us/sreview/ccapic.pdf (local: `pdfs/ola-ccap-internal-controls-2019.pdf`)
- **Evidence class:** `AUDIT_FINDING`
- **Supports:** **B/C**. “DHS’s program integrity controls are insufficient to effectively prevent, detect, and investigate fraud in Minnesota’s Child Care Assistance Program.” Limited-scope FY 2018 review.

### A5. Child Care Assistance Program — Assessment of Fraud Allegations (2019)

- **Title:** Child Care Assistance Program: Assessment of Fraud Allegations
- **Publisher:** OLA Special Reviews (released ~13 March 2019 per report body)
- **Official PDF:** https://www.auditor.leg.state.mn.us/sreview/ccap.pdf (local: `pdfs/ola-ccap-fraud-allegations-2019.pdf`)
- **Evidence class:** `AUDIT_FINDING` (and an early `fraud_estimate` discussion)
- **Supports:** OLA did **not** substantiate a $100 million annual CCAP fraud allegation. OLA believed fraud exceeded the $5–6 million prosecutors had then proved, but “cannot offer a reliable estimate.” Template for how this corpus treats unproven dollar estimates.

### A6. OLA did not issue a 2024–2026 Great Start Compensation Support Payment Program audit

See `GAPS.md`. The Department of Children, Youth, and Families issued a statutory legislative report, which is an agency self-report, not an independent audit:

- **Title:** Great Start Compensation Support Payment Program: Fiscal Year 2025 Annual Report to the Legislature
- **Publisher:** Minnesota Department of Children, Youth, and Families
- **Date:** January 2026 (submitted 27 January 2026)
- **URL:** https://dcyf.mn.gov/sites/default/files/2026-02/GSCSPP%20FY2026%20Legislative%20Report_Final%20submitted%201.27.26.pdf
- **Evidence class:** `AGENCY_DETERMINATION` (self-report). Not an OLA finding.

---

## B. HHS Office of Inspector General

### B1. Minnesota CCAP attendance / CCDF payments (A-05-24-00001)

- **Title:** Minnesota Could Better Ensure That Childcare Assistance Providers Comply With Attendance Requirements
- **Publisher:** U.S. Department of Health and Human Services, Office of Inspector General
- **Report no.:** A-05-24-00001
- **Date:** completed 21 May 2025 (work-plan page)
- **Official PDF:** https://oig.hhs.gov/documents/audit/10320/A-05-24-00001.pdf (local: `pdfs/hhs-oig-A-05-24-00001-ccap.pdf`)
- **Work-plan page:** https://oig.hhs.gov/reports/work-plan/browse-work-plan-projects/srs-a-25-007/
- **Evidence class:** `AUDIT_FINDING`
- **Supports:** **B/C**. Estimated 11 percent of 2023 payments to 1,155 licensed childcare centers had one or more attendance-record errors. Recommends collecting overpayments, routine attendance-record reviews, and a real-time electronic attendance system (OLA’s earlier recommendation). **Improper-payment / documentation error is not proven theft.**

### B2. Minnesota MFCU 2022 Inspection

- **Title:** Minnesota Medicaid Fraud Control Unit: 2022 Inspection
- **Publisher:** HHS OIG Evaluation and Inspections
- **Report no.:** OEI-06-22-00430
- **Date:** September 2023 (issued 5 September 2023)
- **Official HTML:** https://oig.hhs.gov/reports/all/2023/minnesota-medicaid-fraud-control-unit-2022-inspection/
- **Official PDF:** https://oig.hhs.gov/documents/evaluation/3015/OEI-06-22-00430-Complete%20Report.pdf (local: `pdfs/hhs-oig-mfcu-2022-inspection.pdf`)
- **Evidence class:** `AUDIT_FINDING` (inspection)
- **Supports:** Mixed. Unit “operated in accordance with applicable laws” and reported strong case outcomes FYs 2020–2022 (**A** enforcement capacity). Findings concern staffing/supervision, few abuse/neglect referrals, no efficient case-management system, inconsistent supervisory file reviews (**C** as to Unit operations, not as to DHS program design).

### B3. Minnesota MFCU 2026 Recertification Letter

- **Title:** Minnesota Medicaid Fraud Control Unit — 2026 Recertification Letter
- **Publisher:** HHS OIG
- **Official PDF:** https://oig.hhs.gov/documents/medicaid-fraud-control-units/11768/Minnesota_Medicaid_Fraud_Control_Unit_-_2026_Recertification_Letter.pdf
- **Evidence class:** `AGENCY_DETERMINATION`
- **Supports:** Conditional recertification; unimplemented 2022 recommendation to implement a comprehensive case-management system remains open. Notes a large 2025–2026 increase in PIU referrals and quality problems with some referrals.

---

## C. USDA OIG / FNS

No Minnesota-specific USDA OIG audit of Feeding Our Future / CACFP sponsor Feeding Our Future was located on oig.usda.gov as of 26 August 2026. National FNS improper-payment / CACFP meal-claiming studies exist but are not Minnesota-primary. See `GAPS.md`.

Criminal CACFP/SFSP facts in this corpus come from DOJ charging documents and the OLA MDE special review, not from a USDA OIG audit report.

---

## D. GAO (national, not Minnesota-specific)

### D1. Payment Integrity FY 2025

- **Title:** Payment Integrity: Agencies’ Estimated Improper Payments Increased to $186 Billion in Fiscal Year 2025
- **Publisher:** U.S. Government Accountability Office
- **Report:** GAO-26-108694
- **Official product page:** https://www.gao.gov/products/gao-26-108694
- **Official PDF:** https://www.gao.gov/assets/gao-26-108694.pdf
- **Evidence class:** `AUDIT_FINDING` (national)
- **Supports:** National Medicaid improper-payment estimate ~$37 billion FY 2025. **Improper payments ≠ proven fraud.** HHS attributed part of the Medicaid increase to eligibility-redetermination and provider-screening errors as COVID flexibilities unwound.

### D2. Medicaid managed-care improper-payment estimate methodology

- **Title:** Medicaid Managed Care: Improper Payment Estimate
- **Publisher:** GAO
- **Report:** GAO-25-107770
- **URL:** https://www.gao.gov/products/gao-25-107770
- **Evidence class:** `AUDIT_FINDING` (methodological)
- **Supports:** CMS’s managed-care PERM component reviews state-to-plan capitation, not plan-to-provider claims. That gap is relevant to Minnesota, where much high-risk waiver billing is FFS or encounter-based; do not treat a low managed-care PERM rate as proof of low provider-level fraud.

---

## E. CMS — PERM, CAP, substantial-noncompliance, deferral

### E1. CMS PERM CAP process (national rules)

- **Title:** Corrective Action Plan (CAP) Process
- **Publisher:** CMS
- **URL:** https://www.cms.gov/data-research/monitoring-programs/improper-payment-measurement-programs/payment-error-rate-measurement-perm/corrective-action-plan-cap-process
- **PERM CAP manual excerpt:** https://www.cms.gov/research-statistics-data-and-systems/monitoring-programs/medicaid-and-chip-compliance/perm/downloads/permmanualcapexcerpt.pdf
- **Evidence class:** `STATUTE`/`AGENCY_DETERMINATION` (implementing PIIA / PERM)
- **Supports:** After each PERM cycle, measured states must submit Medicaid and CHIP CAPs within 90 days of error-rate notification. Minnesota is Cycle 1 (next measurement RY 2028).

### E2. Minnesota RY 2025 PERM error-rate notification

- **Title:** Notification of RY 2025 Medicaid Improper Payment Rates — State: Minnesota
- **Publisher:** CMS (letter dated 20 January 2026, posted by MN DHS)
- **Official PDF (state host of CMS letter):** https://mn.gov/dhs/assets/2025-medicaid-error-notification_tcm1053-720555.pdf (local: `pdfs/mn-perm-ry2025-notification.pdf`)
- **Evidence class:** `AGENCY_DETERMINATION`
- **Key figures (from the letter):** Overall Medicaid improper-payment rate **2.16%** (95% CI 0.76–3.56%); FFS 1.32%; managed care 0.00%; eligibility 1.52%. Sample: 900. Review period: payments 1 July 2023 – 30 June 2024.
- **Supports:** Minnesota’s measured PERM rate is **below** the national rolling average CMS has published. The letter itself warns: “improper payments do not necessarily represent expenses that should not have occurred” (missing documentation / technically improper payments). **PERM is not a fraud rate and is not the $9 billion figure.**

### E3. CMS Administrator letter — substantial noncompliance (6 January 2026)

- **Title:** Letter from CMS Administrator to Governor Tim Walz finding substantial noncompliance with Medicaid program-integrity requirements
- **Publisher:** CMS / HHS
- **Date:** 6 January 2026
- **Locator used:** the letter is reproduced inside CMS’s subsequent notice of opportunity for hearing (circulated as CMS-FILE_6607). Direct cms.gov HTML of the 6 Jan letter was not independently retrieved in this pass; the hearing-notice reproduction and the state’s 30 January CAP reply both treat 6 January 2026 as the date of Administrator Oz’s letter.
- **Hearing-notice URL (secondary host of official text):** https://kstp.com/wp-content/uploads/2026/01/CMS-FILE_6607.pdf.pdf — **use as a lead to the Federal Register / CMS original; prefer the Federal Register notice when located** (see `GAPS.md`).
- **Evidence class:** `AGENCY_DETERMINATION`
- **Supports:** **B** as CMS’s administrative finding (not a court judgment, not a criminal charge). CMS concluded Minnesota was operating in substantial noncompliance with SSA § 1902(a)(64) and 42 C.F.R. Part 455 Subpart A. Threatened quarterly FFP withholding tied to 14 high-risk services (CMS letter estimated ~$515 million federal share per quarter as a withholding formula, distinct from the later $259.5 million Q4-2025 **deferral**). First CAP (31 Dec 2025) deemed deficient; revised CAP due 30 Jan 2026.

### E4. Minnesota revised CAP (30 January 2026)

- **Title:** Corrective Action Plan for Program Integrity Update (letter from John Connolly, Deputy Commissioner and Minnesota Medicaid Director, to CMS)
- **Publisher:** Minnesota Department of Human Services
- **Date:** 30 January 2026
- **Official PDF:** https://mn.gov/dhs/assets/2026-01-30_cap-response_final_redacted_tcm1053-728931.pdf (local: `pdfs/mn-cap-response-2026-01-30.pdf`)
- **Evidence class:** `AGENCY_DETERMINATION` (state submission). Self-description of controls; not independent verification that the controls work.
- **Supports:** Documents the 14/13 high-risk service list, HSS termination (CMS-approved, end of October 2025), ~6,000 inactive-provider disenrollments, 500+ payment withholds in 2025, off-cycle revalidation of ~5,640 high-risk providers, Optum prepayment review, enrollment moratoria. Distinguishes DHS’s payment-stop authority from MFCU/USAO charging authority.

### E5. CMS deferral of $259,505,491 FFP (25 February 2026)

- **Title:** Notice of four deferrals totaling $259,505,491 federal financial participation
- **Publisher:** CMS Financial Management Group
- **Date:** 25 February 2026
- **DocumentCloud host of CMS letter:** https://s3.documentcloud.org/documents/27420090/cms-medicaid-deferral-letter-q4-2025.pdf
- **CMS press release describing the same action:** https://www.cms.gov/newsroom/press-releases/trump-administration-prioritizes-affordability-announcing-major-crackdown-health-care-fraud
- **Evidence class:** `AGENCY_DETERMINATION`
- **Supports:** Administrative **deferral** (42 C.F.R. § 430.40) of QE 30 September 2025 CMS-64 claims, **not** a completed disallowance and **not** a finding that $259.5 million was stolen. Mixes (per CMS PR) “unsupported or potentially fraudulent” claims and immigration-status documentation issues. Distinct from the $9 billion estimate.

### E6. DHS program-integrity fact page (state narrative)

- **URL:** https://mn.gov/dhs/program-integrity/factcheck/
- **Evidence class:** `AGENCY_DETERMINATION` (advocacy/fact-check page)
- **Use:** locator for CAP approval date claimed by the state (CMS approved revised CAP 19 March 2026, per this page). Confirm against a CMS letter when available (`GAPS.md`).

---

## F. U.S. Department of Justice / USAO District of Minnesota (private-fraud charging — Proposition A)

### F1. 18 December 2025 USAO press release (the contemporaneous official charging announcement)

- **Title:** Six Additional Defendants Charged, One Defendant Pleads Guilty in Ongoing Fraud Schemes
- **Publisher:** U.S. Attorney’s Office, District of Minnesota
- **Date:** 18 December 2025
- **Official URL:** https://www.justice.gov/usao-mn/pr/six-additional-defendants-charged-one-defendant-pleads-guilty-ongoing-fraud-schemes
- **Evidence class:** `ENFORCEMENT_CHARGING_OR_OFFICIAL_PR`
- **Supports:** **A** (alleged private fraud) in EIDBI/autism, Housing Stabilization Services, and the opening of an Integrated Community Supports investigation. Specific alleged loss figures in **this** release are case-level (e.g., Star Autism >$6 million obtained; HSS claims of ~$3.5 million, ~$750,000, ~$1.4 million claimed; ICS Ultimate Home Health >$1.1 million billed). HSS program-level spending cited: ~$2.6 million predicted annually vs. $21M (2021), $42M (2022), $74M (2023), $104M (2024), $61M in first six months of 2025. ICS: $4.6M (2021) to >$170M (2024); >$400M since 2021.
- **Does not contain the $9 billion figure.** See `NINE-BILLION.md`. Informations/indictments are allegations.

### F2. 2026 Minnesota Health Care Fraud Takedown

- **Title:** Minnesota Health Care Fraud Takedown Results in Charges Against 15 Defendants for Over $90M in Fraud
- **Publisher:** DOJ Office of Public Affairs
- **URL:** https://www.justice.gov/opa/pr/minnesota-health-care-fraud-takedown-results-charges-against-15-defendants-over-90m-fraud
- **AAG speech:** https://www.justice.gov/opa/speech/assistant-attorney-general-colin-m-mcdonald-announces-minnesota-medicaid-fraud-takedown
- **Case summaries hub:** https://www.justice.gov/criminal/criminal-fraud/health-care-fraud-unit/2026-minnesota-hcf-case-summaries
- **Evidence class:** `ENFORCEMENT_CHARGING_OR_OFFICIAL_PR`
- **Supports:** **A**. Intended-loss figure in this takedown is **over $90 million**, not $9 billion. AAG McDonald states HSS was shut down after costs rose from an estimated ~$2.5 million/year to over $104 million by 2024 “due to fraud” — that causal attribution is a prosecutor’s statement, not an adjudicated statewide loss.

---

## G. Minnesota Attorney General / MFCU (Proposition A enforcement; MAP Act)

### G1. MFCU statistical presentation (FY 2025 window)

- **Title:** Medicaid Fraud Control Unit (MFCU) presentation
- **Publisher:** Minnesota Department of Human Services host of AG/MFCU slides
- **URL:** https://mn.gov/dhs/assets/sfs-mfcu-presentation_tcm1053-627492.pdf
- **Evidence class:** `AGENCY_DETERMINATION`
- **Supports:** For 1 Oct 2024 – 30 Sep 2025: 50 cases charged, 38 criminal convictions, $3.347 million criminal restitution ordered, $18.578 million civil recoveries; 187 open fraud cases as of 30 Sep 2025. Describes MAP Act tools effective 1 August 2026.

### G2. MAP Act passage and implementation (AG releases)

- 17 May 2026: https://www.ag.state.mn.us/Office/Communications/2026/05/17_MAP-Act.asp
- 23 June 2026 National Health Care Fraud Takedown Day (seven charged, >$700,000 alleged): https://www.ag.state.mn.us/Office/Communications/2026/06/23_Medicaid-Fraud.asp
- 3 August 2026 sentencing-guidelines upgrade: https://www.ag.state.mn.us/Office/Communications/2026/08/03_Medicaid-Fraud.asp
- Session law: Minnesota Laws 2026, Chapter 127 — https://www.revisor.mn.gov/laws/2026/0/Session+Law/Chapter/127/
- **Evidence class:** `ENFORCEMENT_CHARGING_OR_OFFICIAL_PR` / `STATUTE`
- **Supports:** **A** (charging and conviction statistics as claimed by the AG). MAP Act expands MFCU from 32 to 50 staff, creates higher penalty tiers, subpoena authority, and repeals Minn. Stat. § 609.466 (replaced by broader Medical Assistance fraud provisions in ch. 609). Does **not** quantify $9 billion in proven loss.

---

## H. Legislative oversight hearings

Label carefully. Committee majority reports are **not** trial findings.

### H1. Minnesota House Fraud Prevention and State Agency Oversight Committee — Final Report

- **Title:** Fraud Prevention and Agency Oversight Committee Final Report (executive summary circulating as House committee document)
- **Publisher:** Minnesota House of Representatives, Fraud Prevention & State Agency Oversight Committee (created January 2025)
- **PDF locators:** https://www.house.mn.gov/comm/docs/PBkehwf-FEOo19Pitj0Z8A.pdf and https://www.house.mn.gov/comm/docs/gR_JcjoZB0u_WimLNADCRg.pdf
- **Evidence class:** `LEGISLATIVE_FINDING_OR_ALLEGATION`
- **Supports:** Committee **allegations** of multi-agency oversight failure after “two dozen hearings.” Use as a map of hearing record, not as adjudicated fact. Where the report restates OLA or DOJ, cite the underlying primary source instead.

### H2. Minnesota House — OLA Feeding Our Future presentations to the Fraud Committee

- 11 February 2025 presentation: https://www.house.mn.gov/comm/docs/ewvm2k-SrUa7fQ6q6xSuyA.pdf
- 21 April 2026 presentation: https://www.house.mn.gov/comm/docs/0NSdqTLBsEe6SbzLqpaUGA.pdf
- **Evidence class:** `SWORN_TESTIMONY` if given under oath at a noticed hearing; otherwise official auditor presentation to a legislative committee. Confirm oath status from the hearing record (`GAPS.md`).
- **Supports:** **B/C** as restated OLA findings.

### H3. U.S. House Oversight and Government Reform — Minnesota hearings, 2026

- Part I hearing page (7 January 2026, state lawmakers): referenced from Comer 4 March announcement.
- Part II, 4 March 2026, “Oversight of Fraud and Misuse of Federal Funds in Minnesota: Part II”
  - Hearing page: https://oversight.house.gov/hearing/oversight-of-fraud-and-misuse-of-federal-funds-in-minnesota-part-ii/
  - Witnesses: Gov. Tim Walz; AG Keith Ellison; Rev. Mariah Tollgaard (minority)
  - Wrap-up (majority): https://oversight.house.gov/release/hearing-wrap-up-minnesota-governor-walz-and-attorney-general-ellison-lied-about-knowledge-of-fraud-and-silenced-whistleblowers/
- **Interim majority staff report:** *The Cost of Doing Nothing: How Tim Walz and Keith Ellison Fueled Minnesota’s Fraud Explosion* (4 March 2026)
  - URL: https://oversight.house.gov/wp-content/uploads/2026/03/The-Cost-of-Doing-Nothing_How-Tim-Walz-and-Keith-Ellison-Fueled-Minnesotas-Fraud-Explosion_3.4.26_FINAL.pdf
- **Evidence class:** hearing appearances by Walz and Ellison = `SWORN_TESTIMONY` if under oath (standard for House witnesses). Majority staff report = `LEGISLATIVE_FINDING_OR_ALLEGATION`.
- **Supports:** The staff report **alleges** senior-official knowledge as early as 2019 (DHS) and April 2020 (MDE), payment-stop authority unused, and retaliation. Those are **D-adjacent allegations**, not convictions. The report’s use of “potentially $9 billion in Medicaid-related funds” **repeats the prosecutor estimate**; it does not independently measure loss. See `NINE-BILLION.md`.
- **Transcript gap:** official GPO / committee transcript of the 4 March 2026 hearing was not retrieved in this pass (`GAPS.md`).

### H4. Minnesota Legislative Audit Commission — BHA Grants hearing, 6 January 2026

- Minutes: https://www.auditor.leg.state.mn.us/meeting/m/m_Auditor_LAC-20260106.htm
- **Evidence class:** official commission minutes (Legislative Auditor statement).
- **Supports:** **C**, plus an auditor integrity concern (backdated/created documents). Not a criminal charge.

---

## I. Statutes and precedent (indexes)

Full tables live in `STATUTES.md` and `PRECEDENT.md`. All statute URLs below were opened on official revisor.mn.gov, uscode.house.gov, or govinfo.gov on 26 August 2026.

---

## J. Local PDF inventory (this box)

Downloaded into `pdfs/` on 26 August 2026:

| File | Source |
|---|---|
| `ola-2024-mdefof.pdf` | OLA MDE Feeding Our Future special review |
| `ola-fad2601-bha-grants.pdf` | OLA BHA grants 2026 |
| `ola-fad21-03-bha.pdf` | OLA BHA grants ~2021 |
| `ola-ccap-internal-controls-2019.pdf` | OLA CCAP controls |
| `ola-ccap-fraud-allegations-2019.pdf` | OLA CCAP fraud-allegation review |
| `hhs-oig-A-05-24-00001-ccap.pdf` | HHS OIG CCAP attendance |
| `hhs-oig-mfcu-2022-inspection.pdf` | HHS OIG MFCU 2022 inspection |
| `mn-perm-ry2025-notification.pdf` | CMS RY 2025 PERM letter (MN host) |
| `mn-cap-response-2026-01-30.pdf` | MN revised CAP |
| `kousisis-23-909.pdf` | SCOTUS slip opinion |
| `ciminelli-21-1170.pdf` | SCOTUS opinion |

8th Circuit *Cairns* PDF at `https://ecf.ca8.uscourts.gov/opndir/22/07/202445P.pdf` returned 404 to curl from this environment after WebFetch succeeded; cite the PACER/CA8 URL and the Justia PDF mirror `https://cases.justia.com/federal/appellate-courts/ca8/20-2445/20-2445-2022-07-26.pdf` as a secondary official-text host.

---

*End of SOURCES.md. Compiled 26 August 2026. No citation in this file was invented; items that could not be confirmed are in `GAPS.md`.*
