# MinnesotaPeace federal / recovery gap fill — 29 August 2026

**Scope:** primary-source closure after the Aug. 29 high-risk-service/oversight merge.  
**Publication state:** research only.  
**Rule:** administrative approval, settlement, civil judgment, criminal plea, restitution, recovery and identified/potential recovery remain separate evidence and money classes.

## 1. CMS March 19 CAP approval — primary-source gap closed

The prior corpus had Minnesota DHS saying CMS approved the revised Medicaid Corrective Action Plan (CAP) on March 19, 2026, while the standalone federal letter had not been captured.

That authenticity gap is now closed.

CMS's Aug. 4, 2026 approval package for Minnesota's Substance Use Disorder System Reform Program Integrity Plan is hosted on **Medicaid.gov** and includes the complete signed March 19 CMS CAP approval letter as **Attachment A**.

Primary records:

- `src-cms-2026-03-19-mn-medicaid-cap-approval`
- `src-cms-2026-08-04-mn-sud-program-integrity-plan`

The March 19 letter states Minnesota's Jan. 30 revised CAP addressed the deficiencies CMS had identified and expressly concludes that **the CAP is approved**. CMS also required continued implementation and reporting, emphasized high-risk-provider revalidation, and sought a stay of Minnesota's appeal of the potential January withholding while CAP implementation continued.

**Qualification:** approval of the corrective plan is not a finding that every program-integrity deficiency was already cured. It is also separate from the Feb. 25 federal-funds deferral.

## 2. CMS Aug. 4 SUD Program Integrity Plan

CMS approved Minnesota's Program Integrity Plan for the Section 1115 Substance Use Disorder System Reform demonstration on Aug. 4, finding it consistent with the demonstration's program-integrity special term and condition.

The approved plan describes controls broader than SUD alone, including:

- provider screening/enrollment and high-risk revalidation;
- fee-for-service prepayment review;
- post-payment review and managed-care review expansion;
- utilization/prior-authorization controls;
- suspicious-claim analytics and provider risk dashboards;
- law-enforcement referrals;
- program assessments and remediation;
- inactive-provider termination and other CAP work.

The plan says current analytics are **rules-based/descriptive** and do not use automated decision-making or machine-learning models.

A distinct SUD research family is now opened at `research/cases/substance-use-medicaid/README.md`.

## 3. Minnesota MFCU — July 1 conditional federal recertification

HHS-OIG's July 1, 2026 recertification letter is now normalized as:

- `src-hhs-oig-2026-07-01-mn-mfcu-recertification`

OIG **conditionally recertified** Minnesota's Medicaid Fraud Control Unit. OIG says the Unit was generally compliant and effective in Medicaid-fraud investigations/prosecutions, while imposing special corrective conditions.

Important federal-record facts include:

- 32 approved positions / 31 filled in FY2025;
- OIG's size estimate of roughly 41 staff based on Minnesota Medicaid expenditures;
- 18 additional state-authorized positions approved in May 2026;
- 119 PIU/MCO referrals in FY2025 versus nearly 790 from Oct. 1, 2025 through May 14, 2026, with reported quality problems in many referrals;
- 30 open joint investigations with HHS-OIG OI;
- 36 fraud convictions in FY2025;
- 187 fraud investigations and 49 fraud indictments;
- 8 civil settlements/judgments;
- **more than $24 million total monetary recoveries in FY2025**;
- fiscal-control deficiencies and a still-open case-management-system recommendation;
- weaker patient-abuse/neglect output compared with fraud work.

### Recommendation-status correction

A cross-check prevented an interstate misattribution: HHS-OIG recommendation IDs `26-E-07-010` belong to **Oklahoma**, not Minnesota.

Minnesota's current tracker snapshot is normalized separately as:

- `src-hhs-oig-2026-08-14-mn-mfcu-recommendation-status`

For Minnesota's 2022 inspection, three of four recommendations are closed implemented. The remaining open item is the comprehensive case-management system, which the July 1 conditional recertification specifically requires the Unit to implement.

## 4. Substance-use Medicaid enforcement is now a distinct family

### NUWAY Alliance

Primary sources:

- `src-usao-mn-2025-06-26-nuway-medicaid-settlement`
- `src-hhs-oig-2025-05-20-nuway-corporate-integrity-agreement`

NUWAY agreed to a **$18.5 million** civil settlement resolving False Claims Act / Anti-Kickback allegations. Minnesota's Attorney General says more than **$8 million** of the settlement goes to Minnesota.

The actual HHS-OIG Corporate Integrity Agreement is now captured. It imposes a five-year compliance program and independent review. Among other requirements, an Independent Review Organization must review a random sample of 100 Medicaid paid claims per reporting period, test medical necessity/documentation/coding/reimbursement, estimate population overpayments, and require repayment under the CIA methodology.

**Qualification:** DOJ expressly states the resolved claims were allegations and there was no determination of liability/wrongdoing. Claims-review errors/overpayments under the CIA are not automatically criminal fraud.

### Evergreen Recovery

Primary status source:

- `src-mn-ag-2025-10-22-evergreen-recovery-pleas`

Shantel Rene Magadanz and Heather Lynn Heim pleaded guilty to conspiracy to commit wire fraud in the Evergreen Recovery Medicaid matter. The last official release checked said Shawn Ashley Grygo had not pleaded guilty; no later official plea/sentence release was located in the Aug. 29 sweep.

## 5. Recovery ledger — more real numbers, still no fake grand total

New recovery evidence is stored in:

- `research/money/recovery-ledger-addendum-2026-08-29.json`

The important new figures are not additive:

| Record | Figure | Correct type |
|---|---:|---|
| Minnesota MFCU FY2025 | >$24M | mixed total monetary recoveries |
| NUWAY | $18.5M | total civil settlement |
| NUWAY Minnesota share | >$8M | nested state share |
| CVS Minnesota-attributable | >$850K | civil settlement |
| CVS direct Minnesota Medical Assistance amount | >$400K | nested settlement restitution |
| Ibrahim CACFP judgment | $2,481,310.08 + interest | civil judgment entered |
| Ibrahim funds already held | $106,978.10 | funds held pending release |

The MFCU FY2025 aggregate likely includes component recoveries such as settlements occurring in that fiscal year. It must not be added to those components without a published breakdown.

## 6. Emadeldin Ibrahim CACFP judgment — court record captured

Primary court record:

- `src-mn-hennepin-27-cv-22-13107-ibrahim-judgment`

Hennepin County District Court entered a **$2,481,310.08** civil judgment for MDE against Emadeldin Ibrahim, plus prejudgment interest, after a Minnesota False Claims Act jury verdict.

The judgment memorandum identifies:

- $188,350.84 jury-found damages;
- $565,052.52 after trebling;
- $1,695,157.56 civil penalty;
- $220,700 attorneys' fees + $400 court costs;
- $106,978.10 already held by the court, with a later release order to MDE contemplated.

These components are nested inside the total judgment and must not be added again. More importantly, **judgment entered is not judgment collected**. The court-held $106,978.10 is the narrower collection-status fact currently established by the captured order.

This CACFP matter is separate from Feeding Our Future unless a source establishes a direct case relationship.

## 7. Fresh court-status check — latest FOF sentencing financial orders remain pending primary capture

The latest USAO prison terms remain publishable from the official releases, but this pass did not expose new primary RECAP judgments/minutes for:

- Hussein Mohamed Farah / New Vision Foundation;
- Abdihakim Ali Ahmed;
- Ahmed Abdullahi Ghedi;
- Ahmed Sharif Omar-Hashim.

Secondary reporting gives restitution figures for at least Ahmed and Farah, but those financial orders remain pending primary court capture in the corpus.

**Do not upgrade them merely because multiple news stories repeat them.**

## 8. Federal gaps still genuinely open

1. CMS Dec. 5, 2025 initial CAP-request letter on an official federal host.
2. Final public disposition, if any, of CMS's Feb. 25, 2026 **$259,505,491** federal matching-funds deferral.
3. Focused CMS-64 review workpapers/results supporting or resolving that deferral.
4. Primary judgments/sentencing minutes for this week's newest FOF sentencing financial obligations.
5. Any later HHS-OIG action lifting the Minnesota MFCU conditional-recertification special conditions.
6. Component-level annual MFCU recovery data sufficient to reconcile individual cases/settlements with aggregate recovery totals.

A fresh Aug. 29 search did **not** locate a later CMS/Federal Register release resolving the $259.5M deferral. Continue to label it a deferral, not a final disallowance or proven-fraud figure.

## 9. Publication consequence

The research substrate is now strong enough to support separate future public surfaces for:

- program-integrity controls and federal/state chronology;
- the 14 high-risk Medicaid services;
- substance-use Medicaid cases/controls;
- recovery versus judgment versus collection;
- audit findings and implementation status;
- unresolved primary-source gaps.

The website should consume normalized records, not treat this report as visitor copy.
