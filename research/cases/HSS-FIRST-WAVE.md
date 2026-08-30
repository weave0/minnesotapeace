# Housing Stabilization Services — First Federal Charge Wave

**Primary source:** U.S. Attorney's Office, District of Minnesota, “Defendants Charged in First Wave of Housing Stabilization Fraud Cases,” Sept. 18, 2025.

**Evidence class:** `CHARGED_ALLEGED` for unresolved defendant conduct; `ADJUDICATED` for guilty pleas described below; `AGENCY_POSITION` for broader prosecutorial descriptions of program vulnerability and investigative scope.

**Publication rule:** Every defendant is presumed innocent unless and until convicted or a guilty plea is accepted. Amounts below retain their source metric; a guilty plea does not automatically convert every earlier charging allegation into a court-certified loss or restitution figure.

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

- `$2.3M` → `amount_billed` / original `CHARGED_ALLEGED`
- personal distributions described by DOJ → alleged proceeds, not proven loss

### July 2026 guilty-plea update

DOJ Office of Public Affairs reported on **2026-07-24** that all four Brilliant Minds defendants pleaded guilty to **one count of wire fraud each** in separate hearings held between **2026-07-07 and 2026-07-23**:

- Moktar Hassan Aden
- Mustafa Dayib Ali
- Khalid Ahmed Dayib
- Abdifitah Mohamud Mohamed

Primary source: https://www.justice.gov/opa/pr/four-men-plead-guilty-2m-minnesota-medicaid-fraud  
Local source record: `research/sources/src-doj-opa-2026-07-24-hss-brilliant-minds-pleas.json`

DOJ's post-plea account states that the four enrolled approximately **350 people** for HSS, billed for services not provided or materially inflated, and obtained approximately **$2.2 million** from Minnesota Medicaid. DOJ also states that when insurers requested supporting documentation, the defendants fabricated records using **ChatGPT** in an effort to conceal the conduct.

Status handling:

- guilt on the pleaded wire-fraud offense → `ADJUDICATED`;
- approximately `$2.2M` → preserve as DOJ's post-plea scheme amount pending plea-agreement/judgment capture; **not** `restitution_ordered` and **not** `recovered_amount`;
- the `$2.2M` substantially overlaps the earlier approximately `$2.3M amount_billed` figure — **do not add them**;
- DOJ said sentencing dates had not yet been set as of the release.

This supersedes older research text that described the four defendants simply as `charged`.

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

- `$2.7M` → `amount_paid` / `CHARGED_ALLEGED` in charging narrative

## 25-cr-353 — United States v. Anwar Ahmed Adow

Provider: **Liberty Plus LLC**

Named defendant:

- Anwar Ahmed Adow

DOJ alleged Liberty Plus received more than **$1.2 million** in Medicaid funds for claimed services to approximately 200 beneficiaries and that employees were encouraged to inflate billable hours.

Metric handling:

- `>$1.2M` → `amount_paid` / original `CHARGED_ALLEGED`

## Case-family relationships to preserve

- Asad Ahmed Adow and Anwar Ahmed Adow are brothers according to DOJ.
- DOJ alleged transfers/proceeds moved among providers, principals, employees, and related persons; those relationships should be modeled as separately sourced edges rather than collapsed into a single conspiracy unless a charging instrument expressly alleges one.
- `25-cr-349`, `25-cr-351`, `25-cr-353`, and `25-cr-354` were announced together as the first federal HSS charge wave but are separate criminal matters.

## Open acquisition gaps

Asad Adow `25-cr-354` information remains missing from RECAP (re-checked 2026-08-27; no PACER buy). Aden, Falade, Anwar Adow, Hussein 25-cr-479, and Sallah 25-cr-482 charging instruments are count-mapped from the face of ECF 1.

For `25-cr-349`, acquire the four July 2026 plea agreements/minutes and later judgments so the exact admitted factual basis, loss calculation, restitution, forfeiture and sentence can replace press-release-level detail.

## Original first-wave source

https://www.justice.gov/usao-mn/pr/defendants-charged-first-wave-housing-stabilization-fraud-cases


## Local charging instruments (2026-08-26 RECAP)

- **25-cr-349** ECF 1 indictment count-mapped from OCR (`aden-25-cr-349-ecf1.json`). Counts 1–6 are 18 U.S.C. § 1343 (dated wires Sept 2022–Oct 2024). ¶14 Brilliant Minds submitted about **$2.3 million** in reimbursement claims (`amount_billed`; same figure restated ¶21 — do not sum). ¶15 Foundation First submitted about **$222,000** (`amount_billed`, separate provider). ¶23 each defendant personally pocketed about $300,000–$400,000 from Brilliant Minds (proceeds range, **not** 4×, overlaps $2.3M). ¶24 nearly $500,000 Amex charges from company accounts. SOS: Brilliant Minds formed Oct 2020 is consistent with ¶10; Foundation First May 2023 is consistent with ¶15’s operator. Caption OCR initially read § 1348; count-closing line is § 1343.
- **25-cr-351** ECF 1 indictment count-mapped (`falade-25-cr-351-ecf1.json`). Counts 1–4 are 18 U.S.C. § 1343. ¶13 Faladcare submitted **over $2.2 million** in reimbursement claims (`amount_billed`; same figure ¶17 — do not sum). No personal-pocketing dollar on this indictment. SOS Faladcare Inc 2019-10-31 is consistent with ¶10. Caption OCR § 1348 corrected to § 1343 from the closing line.
- **25-cr-353** ECF 1 is a **felony information**, not an indictment (`0_25-cr-00353_ecf1_anwar-adow-hss.pdf`, full text extracted). Counts 1–4 are 18 U.S.C. § 1343 (emails `PlusLibertyLLC@gmail.com`, Mar 2022–Apr 2025). ¶10: owner of Liberty Plus, registered with Minnesota in or about November 2022 (SOS file 1349782500024 original filing 2022-11-17 is consistent). ¶16: Liberty Plus **received more than $1.2 million** (`amount_paid` / CHARGED_ALLEGED) for purported services to about 200 beneficiaries. ¶8 program-wide HSS payouts ($21M/$42M/$74M/$104M/$61M) are `program_spend` background in this charging document — **do not add them to the $1.2M**. ¶1 “millions of dollars” is scheme-purpose language; the specific Liberty Plus figure is ¶16. ¶17 alleges diversion to employees and brother Asad Adow (not itself a charging document against Asad). Docket: guilty as to Count 1 on 2025-10-23 — not a judgment.
- **25-cr-354** Asad Adow felony information is **not** on RECAP (`is_available=false` as of 2026-08-27). Plea agreement ECF 14 and waiver ECF 13 also unavailable. No judgment. Still a local-document gap.
- **25-cr-479** ECF 1 indictment count-mapped (`hussein-25-cr-479-ecf1.json`). Counts 1–5 are 18 U.S.C. § 1343 (emails Apr 2023–Dec 2024). ¶13 / ¶21 Pristine Health submitted about **$750,000** in fraudulent Medicaid claims (`amount_claimed`; same figure, do not sum). Caption OCR § 1348 corrected to § 1343. Foundation First / Brilliant Minds paras 18–19 are recitals, not Aden charges. Not a charge against Asad. Do not add to first-wave totals or FOF.
- **25-cr-482** ECF 1 indictment count-mapped (`sallah-25-cr-482-ecf1.json`). Counts 1–4 are 18 U.S.C. § 1343. ¶13 / ¶23 about **$1.4 million** claimed (`amount_claimed`) and ¶13 **nearly $1.3 million** received (`amount_paid`) — same overlap group, do not add. ¶22 ~$150,000 crypto-exchange diversion overlaps the received figure. ¶21 Employee A previously at Leo Human Services is a recital, not a charge against Asad or Leo. Caption OCR § 1348 corrected to § 1343. Do not add to first-wave totals or FOF.

Do not sum the $2.3M / >$2.2M / $2.7M / >$1.2M figures. They are overlapping program-family billing/payment allegations across four matters.


## Other guilty-plea docket facts (not yet judgments)

These come from CourtListener docket minutes, not from archived plea-agreement PDFs. Sentence/restitution are **not** entered on these dockets as of the May 2026 related-case notices unless superseded by later records.

- **Anwar Ahmed Adow, 25-cr-353, ECF 7 (2025-10-23):** Judge Magnuson; “Plea entered … Guilty as to Count 1 of the Information.” Waiver of indictment ECF 8. Plea agreement ECF 9 exists and is **not** on RECAP. PSR is pending; objection deadline continued 2026-01-05. Treat Count 1 guilt as a court-minute fact; do not invent a sentence or restitution number.
- **Asad Ahmed Adow, 25-cr-354, ECF 12 (2025-11-17):** Judge Blackwell; guilty as to Count 1. Waiver ECF 13. Plea agreement ECF 14 **not** on RECAP. The felony information itself is still not on RECAP.
- Related-case leads from Asad reassignment orders: **25-cr-479** and **25-cr-482** ECF 1 count-mapped 2026-08-27.
