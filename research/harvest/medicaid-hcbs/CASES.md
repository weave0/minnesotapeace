# CASES.md — Prosecution clusters (Medicaid HCBS / related high-risk)
Compiled 2026-08-26. Charges are allegations unless a plea or conviction is noted. Dollar figures keep the source metric.

Status vocabulary: charged | pleaded_guilty (unsentenced) | convicted/sentenced | fugitive | search-warrant-only | unknown

---

## Cluster HSS-W1 — First wave Housing Stabilization Services (Sept. 18, 2025)

- Court: D. Minn. (four cases)
- Charge: wire fraud (federal)
- Status: charged (no USAO sentencing/plea PR located for this cluster as of 2026-08-26)
- Actor: A
- Class: CHARGED_ALLEGED
- URLs: https://www.justice.gov/usao-mn/pr/defendants-charged-first-wave-housing-stabilization-fraud-cases ; https://www.ag.state.mn.us/Office/Communications/2025/09/18_HHS.asp

| Defendant | Entity | Docket | Amount | Metric |
|---|---|---|---|---|
| Moktar Hassan Aden, 30 | Brilliant Minds Services LLC (Griggs-Midway, St. Paul) | 25-cr-349 (MJD/JFD) | about $2.3M claims | amount_billed |
| Mustafa Dayib Ali, 29 | Brilliant Minds | same | $300k-$400k personal (each of four) | alleged_loss (proceeds) |
| Khalid Ahmed Dayib, 26 | Brilliant Minds | same | same | alleged_loss (proceeds) |
| Abdifitah Mohamud Mohamed, 27 | Brilliant Minds; Foundation First Services LLC | same | same | alleged_loss (proceeds) |
| Christopher Adesoji Falade, 62 | Faladcare Inc. | 25-cr-351 (JMB/DJF) | >$2.2M claimed | amount_billed |
| Emmanuel Oluwademilade Falade, 32 | Faladcare | same | same | amount_billed |
| Asad Ahmed Adow, 26 | Leo Human Services LLC | 25-cr-354 (ADM) | about $2.7M received | amount_paid |
| Anwar Ahmed Adow, 25 | Liberty Plus LLC | 25-cr-353 (PAM) | >$1.2M received | amount_paid |

Alleged method (PR): inflated/fake HSS claims; names from addiction-treatment facilities; billing max authorized hours; notes manufactured for a possible audit; AmEx / Kenya real estate / luxury cars as proceeds.

Do not confuse Mustafa Dayib Ali, 29 (this case) with Mustafa Dayib, 22 (Vitality Health, May 2026) — different ages/entities in DOJ materials.

---

## Cluster EIDBI-SMART — Smart Therapy / Asha Farhan Hassan (first EIDBI case)

- Charge date: 2025-09-24 (information, wire fraud)
- Plea: 2025-12-18 guilty, one count wire fraud, sentencing later (Judge David Doty)
- Status: pleaded_guilty (unsentenced)
- Actor: A
- Class: CHARGED_ALLEGED then ADJUDICATED (plea of guilty); loss amount not a restitution_ordered figure in the PR
- URL: https://www.justice.gov/usao-mn/pr/first-defendant-charged-autism-fraud-scheme-0
- Plea URL: https://www.justice.gov/usao-mn/pr/six-additional-defendants-charged-one-defendant-pleads-guilty-ongoing-fraud-schemes

| Item | Amount | Metric |
|---|---|---|
| EIDBI reimbursements obtained (DHS + UCare), Nov. 2019-Dec. 2024 | >$14 million | amount_paid / alleged_loss |
| Feeding Our Future / child nutrition (separate scheme, same defendant) | about $465,000 claimed | amount_billed / alleged_loss |

Alleged method: unqualified techs; parent kickbacks $300-$1,500/month; max-hour billing; forged QSP signatures; concealed co-owners (one DHS-excluded adult-daycare owner); Kenya real estate.

---

## Cluster EIDBI-STAR — Star Autism Center / Abdinajib Hassan Yussuf

- Charge date: 2025-12-18 (information, one count wire fraud)
- Plea: reported 2026-03-02 in multiple news outlets; no USAO PR found
- Status: charged (official); pleaded_guilty SECONDARY_VERIFIED
- Actor: A
- URL: https://www.justice.gov/usao-mn/pr/six-additional-defendants-charged-one-defendant-pleads-guilty-ongoing-fraud-schemes

| Item | Amount | Metric |
|---|---|---|
| EIDBI reimbursements obtained (DHS + UCare), late 2020-Dec. 2024 | >$6 million | amount_paid / alleged_loss |
| Semi-truck | >$100,000 | alleged proceeds |
| Sent to Kenya | >$200,000 | alleged proceeds |

---

## Cluster EIDBI-46M — Shamso Ahmed Hassan and Hanaan Mursal Yusuf (Smart Therapy + Star Autism)

- Charge date: 2026-05-21 indictment (conspiracy to commit health care fraud, health care fraud, false statements, money laundering)
- Status: charged
- Actor: A
- Class: CHARGED_ALLEGED
- URLs: https://www.justice.gov/opa/pr/minnesota-health-care-fraud-takedown-results-charges-against-15-defendants-over-90m-fraud ; https://www.justice.gov/criminal/criminal-fraud/health-care-fraud-unit/2026-minnesota-hcf-case-summaries ; https://www.ag.state.mn.us/Office/Communications/2026/05/21_Medicaid-Fraud.asp

| Item | Amount | Metric |
|---|---|---|
| Scheme through Smart Therapy + Star Autism | $46.6 million | amount_billed |
| Paid | about $21.2 million (OPA said about $21.1-21.2M; case summary $21.2M) | amount_paid |
| EIDBI program claims 2018 to 2025 | >$600,000 to >$400 million | program_spend |

DOJ billed this as "largest Medicaid autism fraud case ever charged." Likely overlaps the $14M and $6M entity figures; do not sum.

MFCU role: AG-FED-0521 says MFCU executed the Dec. 2024 search warrant at Smart Therapy.

---

## Cluster HSS-W2 — December 18, 2025 additional HSS defendants

- URL: https://www.justice.gov/usao-mn/pr/six-additional-defendants-charged-one-defendant-pleads-guilty-ongoing-fraud-schemes
- Class: CHARGED_ALLEGED
- Actor: A (includes out-of-state "fraud tourism")

| Defendant | Entity | Instrument | Amount | Metric | Notes |
|---|---|---|---|---|---|
| Anthony Waddell Jefferson, 37 (Philadelphia) | MN LLCs; marketed as "The Housing Guys" | information, wire fraud | about $3.5M claims / about 230 beneficiaries (with Brown) | amount_billed | Fake notes; invented employees |
| Lester Brown, 53 (Philadelphia) | same | information, wire fraud | same | amount_billed | |
| Hassan Ahmed Hussein, 28 | Pristine Health LLC, St. Paul | indictment, wire fraud | about $750,000 claimed / about 100 beneficiaries | amount_billed | Worked with Foundation First (see HSS-W1 Mohamed) |
| Ahmed Abdirashid Mohamed, 27 | Pristine Health | indictment, wire fraud | same | amount_billed | Travel: London, Sydney, Dubai, Istanbul, Saudi Arabia |
| Kaamil Omar Sallah, 26 | SafeLodgings, Inc. | indictment, 4 counts wire fraud | about $1.4M claimed; about $1.3M received (Mar 2023-Aug 2025) | amount_billed / amount_paid | Double billing; about $150k crypto; fugitive after Nov. 2025 grand-jury subpoena; flew MSP to Amsterdam about Nov. 26, 2025 |

HSS program_spend restated: $2.6M predicted; >$21M (2021), $42M, $74M, $104M, $61M H1 2025.

---

## Cluster HSS-W3 — May 21, 2026 takedown (HSS subset)

OPA headline for this subset: eight defendants, approximately $15.7 million (alleged_loss as OPA used it; case summaries break billed vs paid).
URL: DOJ-OPA-0521 + DOJ-SUMM. Class: CHARGED_ALLEGED. Actor: A.

| Defendant | Entity / home | Amount billed | Amount paid | Notes |
|---|---|---|---|---|
| Deborah Hodges, 59, Philadelphia | House of Heroes, Inc. | $5.3M | about $5.2M | Billed in-person services while recipient in inpatient treatment |
| Sharmaine Meadows, 45, Lake Elmo, MN | Cradle of Love, LLC | >$4.3M | nearly $3.7M | Directed employees to bill max hours regardless of delivery |
| Muhammad Abdulqadir Omar, 32, Roseville | North Home Health Care LLC + South Home Health Care LLC | $3.3M (with Abdi) | about $3.2M | Falsified records for insurers |
| Ibrahim Bashir Abdi, 25, Minneapolis | NHHC (co-owner) | same | same | |
| Cynthia Allen, 62, Philadelphia | Cynthia Allen Servicing Company, LLC | about $2,516,025 billed | combined paid about $3,504,307 with Langley | Shared office/employees with Langley; about 350 beneficiaries |
| Candice Langley, 46, Philadelphia | Candice Carene, Inc. | about $988,282 billed | see above | |
| Mustafa Dayib, 22, Minneapolis | Vitality Health Services, LLC | n/s | about $975,000 paid (Jan 2023-Jul 2025) | Information, conspiracy |
| Abdulbasit Ibrahim, 22, Minneapolis | Vitality | n/s | same | |

AG-FED-0521 confirms MFCU assistance on Hodges, Allen, Langley.

---

## Cluster ICS-1 — Ultimate Home Health / Ahmed Kadar (first ICS prosecution)

- Investigation public: 2025-12-18 search warrant unsealed (Ultimate Home Health Services LLC)
- Charge: 2026-05-21 indictment — 3 counts health care fraud, 2 counts money laundering
- Defendant: Ahmed Kadar / Ahmed Othman Kadar, 22, Rosemount, MN
- Status: charged
- Actor: A
- Class: CHARGED_ALLEGED
- URLs: DOJ-DEC18; DOJ-OPA-0521; DOJ-SUMM

| Item | Amount | Metric |
|---|---|---|
| Dec. 2025 warrant narrative (Jun 2024-Aug 2025, 13 clients) | >$1.1 million claims | amount_billed |
| May 2026 indictment | about $1.4 million billed and paid | amount_billed / amount_paid |
| $400,000 transferred | money-laundering allegation | alleged proceeds |
| ICS program since 2021 | >$400M (Dec PR) / >$460M (May PR) | program_spend |

Alleged method: billing 12-24 hour ICS not provided; power shut off / no heat; billed the day before a 24-hour-care recipient was found deceased.

ICS program design (B): providers can bill up to 24 hours/day; explosive growth 2021-2025.

---

## Cluster IHS-1 — Healey Homes (first IHS criminal prosecution)

- Charge: 2026-05-21 indictment — conspiracy to commit health care fraud and money laundering
- Defendants: Charles Wayne Healey, 61, Blue Earth, MN; Katherin Suzan Larsen-Guthmiller, 66, Blue Earth, MN
- Entity: Healey Homes / Charles Healy Foster Home, LLC (AG spelling "Healy")
- Status: charged
- Actor: A
- Class: CHARGED_ALLEGED
- URLs: DOJ-OPA-0521; DOJ-SUMM; AG-FED-0521

| Item | Amount | Metric |
|---|---|---|
| Medicaid reimbursements 2021 until DHS closed Healey Homes in 2025 | $22.7 million | amount_paid / alleged_loss |
| IHS program 2018 to 2025 | >$100M to >$700M | program_spend |

Alleged method: IHS is for recipients in their own homes and is disallowed in provider-controlled settings; defendants owned/controlled the residences, concealed ownership from Medicaid, below-market rent in exchange for billing identity; proceeds to more real estate, luxury autos, jewelry. OPA: "over 20 separate residences."

---

## Cluster IHS/HCBS-STATE — Guardian Home Health / Mohamed Abdirashid Omarxeyd (MN MFCU)

- Charge date: 2026-01-14
- Charges: 8 counts felony theft by false representation (state)
- Status: charged
- Actor: A
- Class: CHARGED_ALLEGED
- URLs: https://www.ag.state.mn.us/Office/Communications/2026/01/14_MedicaidFraud.asp ; complaint https://www.ag.state.mn.us/Office/Communications/2026/docs/Omarxeyd_Complaint.pdf

| Item | Amount | Metric |
|---|---|---|
| PR: "over $3 million" | >$3,000,000 | alleged_loss / amount_paid |
| Complaint: unlawfully received | $3,213,658.47 | amount_paid (alleged) |
| Omarxeyd, wife, and his other companies received from Guardian accounts | >$2 million | alleged proceeds |
| Period | Jan 2020-Jan 2024 | |

Services billed (several now high-risk): PCA, companion care, homemaking, respite, individualized home supports, comprehensive community support. Kickbacks to recipients/responsible parties alleged. Referred by DHS Medicaid Provider Audits and Investigations.

---

## Cluster ARMHS-1 — Reva Health / Salman Ahmed Elmi (MN MFCU)

- Charge date: announced 2026-08-17 (complaint about Aug. 13 per local press)
- Charges: 8 felony theft counts (AG PR)
- Status: charged (Ramsey County)
- Actor: A
- Class: CHARGED_ALLEGED
- URLs: https://www.ag.state.mn.us/Office/Communications/2026/08/17_Medicaid-Fraud.asp ; https://www.ag.state.mn.us/Office/Communications/2026/docs/5749_Elmi_Complaint.pdf

| Item | Amount | Metric |
|---|---|---|
| AG PR: Reva billed for services not provided / ineligible | over $1,000,000 | alleged_loss |
| Combined with Rashid case | over $1.5 million | alleged_loss |
| Sample count in complaint (one warrant window) | >$60,000 paid Jul 9, 2025-Jan 8, 2026 | amount_paid (subset) |

Alleged method: falsified ARMHS documentation; kickbacks for use of recipient identities; ineligible providers; little/no required supervision. Co-conspirators at Reva "remain under investigation"; AG notes separate Hennepin County charges against some co-conspirators (sex-trafficking case is outside this corpus's fraud totals; do not import those counts as Medicaid loss).

Journalism (Star Tribune) says ARMHS grew from 234 providers / $63M (2018) to 531 providers / almost $190M "last year" — LEAD_UNVERIFIED as program_spend until a DHS table is captured.

---

## Cluster PCA-STATE — Liberty Home Health Care / Mohamed Haji Rashid (MN MFCU)

- Announced: 2026-08-17 with Elmi, "separate and independent"
- Charges: 9 felony theft
- Period: at least Aug 2020-Feb 2025
- Amount: over $300,000 alleged_loss
- URL: AG-ARMHS-0817
- Notes: PCA / HCBS; billed PCA not provided on >3,300 occasions. Adjacent to high-risk HCBS, not ARMHS.

---

## Cluster EIDBI-SW — April 28, 2026 MFCU/FBI/HHS-OIG search warrants

- URL: https://www.ag.state.mn.us/Office/Communications/2026/04/28_MFCU.asp
- Class: AGENCY_POSITION (warrants). No defendants named in the PR.
- Scope: five sites, four businesses claiming to provide EIDBI.
- Status: search-warrant-only as of that PR.

---

## Out of HCBS scope (listed so they are not mixed into Medicaid HCBS totals)

From the May 21, 2026 OPA "$90 million intended_loss" headline:

| Defendant | Program | Amount | Why out of scope |
|---|---|---|---|
| Jillaine Ann Mertens, 42 | Great Start Compensation Support Payment Program (state child care) | about $425,000 paid | Not Medicaid HCBS |
| Fahima Mahamud, 50 | Feeding Our Future + CCAP | $854k nutrition + $4.6M CCAP, about $5.48M | Child nutrition / CCAP |

Do not add these into HSS/EIDBI/ICS/IHS/ARMHS loss tables. The $90M is an intended_loss umbrella for the whole takedown.

---

## Running tally hygiene (DERIVED_INFERENCE — use only as a map, not a loss total)

Charged HCBS-related amounts as the government stated them, not summed (overlaps, billed vs paid, intended vs paid):

- HSS W1 entity figures: about $2.3 billed + $2.2 billed + $2.7 paid + $1.2 paid
- HSS W2: $3.5 billed + $0.75 billed + $1.4 billed / $1.3 paid
- HSS W3 OPA: about $15.7M alleged (breaks out in summaries)
- EIDBI Asha: $14M obtained
- EIDBI Yussuf: $6M obtained
- EIDBI Shamso/Hanaan: $46.6M billed / $21.2M paid (overlaps Smart + Star)
- ICS Kadar: $1.4M
- IHS Healey: $22.7M paid
- State Omarxeyd: $3.21M paid alleged
- State Elmi ARMHS: >$1M
- State Rashid PCA: >$0.3M

No proven_loss column is populated from these PRs. Restitution/forfeiture orders were not located in this pass.
