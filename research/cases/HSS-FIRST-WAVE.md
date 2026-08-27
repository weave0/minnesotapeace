# Housing Stabilization Services — First Federal Charge Wave

**Primary source:** U.S. Attorney's Office, District of Minnesota, “Defendants Charged in First Wave of Housing Stabilization Fraud Cases,” Sept. 18, 2025.

**Evidence class:** `CHARGED_ALLEGED` for defendant conduct; `AGENCY_POSITION` for broader prosecutorial descriptions of program vulnerability and investigative scope.

**Publication rule:** Every defendant is presumed innocent unless and until convicted. Amounts below are alleged billing/payment figures reported by DOJ from charging documents, not adjudicated loss unless separately established by judgment or plea.

## Program context stated by DOJ

DOJ described Minnesota HSS as a Medicaid benefit intended to help eligible people with disabilities, seniors, and people with mental illness or substance-use disorders obtain or maintain housing. DOJ said the program had low barriers to entry and minimal reimbursement-document requirements, which prosecutors described as making it susceptible to fraud.

DOJ reported program payouts of approximately:

- $21 million in 2021
- $42 million in 2022
- $74 million in 2023
- $104 million in 2024
- $61 million in the first six months of 2025

These figures are **program payments**, not fraud-loss figures.

## 25-cr-349 — United States v. Moktar Aden et al.

Provider: **Brilliant Minds Services LLC**

Named defendants in DOJ release:

- Moktar Hassan Aden
- Mustafa Dayib Ali
- Khalid Ahmed Dayib
- Abdifitah Mohamud Mohamed

DOJ alleged Brilliant Minds submitted approximately **$2.3 million** in HSS reimbursement claims between roughly September 2022 and April 2025. Prosecutors alleged the defendants caused fake and inflated billing and personally received substantial company funds. DOJ also identified Foundation First Services LLC, operated by Abdifitah Mohamed, as a related HSS provider/consultation entity.

Metric handling:

- `$2.3M` → `amount_billed` / `CHARGED_ALLEGED`
- personal distributions described by DOJ → alleged proceeds, not proven loss

## 25-cr-351 — United States v. Christopher Falade et al.

Provider: **Faladcare Inc.**

Named defendants:

- Christopher Adesoji Falade
- Emmanuel Oluwademilade Falade

DOJ alleged Faladcare claimed services for about 100 beneficiaries and sought more than **$2.2 million**, with reimbursement claims that prosecutors characterized as inflated and fraudulent.

Metric handling:

- `>$2.2M` → `amount_billed` / `CHARGED_ALLEGED`

## 25-cr-354 — United States v. Asad Ahmed Adow

Provider: **Leo Human Services LLC**

Named defendant:

- Asad Ahmed Adow

DOJ alleged employees were encouraged to maximize hours and manufacture service notes, and that Leo Human Services ultimately received approximately **$2.7 million** in HSS funds for claimed services to about 250 beneficiaries.

Metric handling:

- `$2.7M` → `amount_paid` / `CHARGED_ALLEGED`

## 25-cr-353 — United States v. Anwar Ahmed Adow

Provider: **Liberty Plus LLC**

Named defendant:

- Anwar Ahmed Adow

DOJ alleged Liberty Plus received more than **$1.2 million** in Medicaid funds for claimed services to approximately 200 beneficiaries and that employees were encouraged to inflate billable hours.

Metric handling:

- `>$1.2M` → `amount_paid` / `CHARGED_ALLEGED`

## Case-family relationships to preserve

- Asad Ahmed Adow and Anwar Ahmed Adow are brothers according to DOJ.
- DOJ alleged transfers/proceeds moved among providers, principals, employees, and related persons; those relationships should be modeled as separately sourced edges rather than collapsed into a single conspiracy unless a charging instrument expressly alleges one.
- `25-cr-349`, `25-cr-351`, `25-cr-353`, and `25-cr-354` were announced together as the first federal HSS charge wave but are separate criminal matters.

## Open acquisition gaps

The charging instruments for all four matters still need to be locally acquired, hashed, and count-mapped. This file is therefore a DOJ-release case-family map, not a substitute for indictment-level extraction.

## Source

https://www.justice.gov/usao-mn/pr/defendants-charged-first-wave-housing-stabilization-fraud-cases


## Local charging instruments (2026-08-26 RECAP)

- **25-cr-349** ECF 1 indictment archived (`0_25-cr-00349_ecf1_aden-hss.pdf`). Counts 1–6 are 18 U.S.C. § 1343. Caption defendants match the DOJ release. OCR of p.7 alleges each defendant personally pocketed about $300,000–$400,000 from Brilliant Minds — still CHARGED_ALLEGED; do not add those four figures into a loss total.
- **25-cr-351** ECF 1 indictment archived (`0_25-cr-00351_ecf1_falade-hss.pdf`). Counts 1–4 are 18 U.S.C. § 1343.
- **25-cr-353** ECF 1 is a **felony information**, not an indictment (`0_25-cr-00353_ecf1_anwar-adow-hss.pdf`). Counts 1–4 are 18 U.S.C. § 1343. The information states Liberty Plus **received more than $1.2 million** (`amount_paid` / CHARGED_ALLEGED) for purported services to about 200 beneficiaries, and that Anwar diverted proceeds to employees and to his brother Asad Adow. Docket: waiver of indictment and change of plea 2025-10-23 — plea is a docket fact; wait for judgment before ADJUDICATED.
- **25-cr-354** Asad Adow felony information is **not** on RECAP (`is_available=false`). Still a local-document gap.

Do not sum the $2.3M / >$2.2M / $2.7M / >$1.2M figures. They are overlapping program-family billing/payment allegations across four matters.


## Guilty-plea docket facts (not yet judgments)

These come from CourtListener docket minutes, not from archived plea-agreement PDFs. Sentence/restitution are **not** entered on these dockets as of the May 2026 related-case notices.

- **Anwar Ahmed Adow, 25-cr-353, ECF 7 (2025-10-23):** Judge Magnuson; “Plea entered … Guilty as to Count 1 of the Information.” Waiver of indictment ECF 8. Plea agreement ECF 9 exists and is **not** on RECAP. PSR is pending; objection deadline continued 2026-01-05. Treat Count 1 guilt as a court-minute fact; do not invent a sentence or restitution number.
- **Asad Ahmed Adow, 25-cr-354, ECF 12 (2025-11-17):** Judge Blackwell; guilty as to Count 1. Waiver ECF 13. Plea agreement ECF 14 **not** on RECAP. The felony information itself is still not on RECAP.
- Related-case leads from Asad reassignment orders: **25-cr-479** and **25-cr-482**. Not yet pulled.
