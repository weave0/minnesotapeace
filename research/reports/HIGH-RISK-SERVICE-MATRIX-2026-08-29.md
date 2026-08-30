# Minnesota Medicaid high-risk service matrix — 29 August 2026

**Scope:** the 14 service/program areas evaluated in the Optum Phase 1 payment-integrity work and designated high risk by Minnesota DHS.  
**Purpose:** separate program purpose, control status, criminal-case coverage and money status before these services are presented publicly.

Machine-readable companion: `research/cases/medicaid-hcbs/high-risk-services-matrix.json`

## What "high risk" means here

The label is an administrative/program-integrity designation. It does **not** mean every provider is suspected, charged or fraudulent. The state/Optum work uses claims analytics, enrollment screening, policy review and pre-payment controls to identify vulnerabilities or anomalous claims. Criminal guilt requires a separate case record.

Optum Phase 1 analyzed **46 months of fee-for-service paid claims** across the 14 areas; managed-care claims were outside scope. The report says it executed **192 targeted analytics**. Its executive summary identifies >$52.3M in funds described as direct recoveries/recoupment opportunities, >$1.7B in potential recovery opportunities and >$165M in cost avoidance. Those are not interchangeable and none is a statewide proven-fraud total.

Primary source record: `research/sources/src-mn-optum-2026-01-30-phase1-payment-integrity.json`.

## Service-by-service state

| Service | What the service is for | Criminal-case coverage currently in corpus | Current control / operational status |
|---|---|---|---|
| Adult Companion Services | Non-medical care, supervision and socialization tied to therapeutic/community-integration goals | **Mixed-service charged:** Guardian complaint; Tremayne Jackson case includes companion care with PCA/homemaker | High-risk screening, revalidation, pre-pay review, enrollment moratorium framework |
| Adult Day Services | Daytime care, supervision, activities and training based on assessed needs | **No dedicated Medicaid-billing prosecution located this pass.** 2019 Meisa case is tax misconduct involving adult-day owners, not proof of false Medicaid claims | High-risk controls; licensing/enrollment controls |
| ARMHS | Rehabilitative mental-health services supporting psychiatric stability and independent/community living | **Dedicated + mixed charged:** Reva Health >$1M alleged; Jessica Wavra mixed ARMHS/targeted case management >$29k | High-risk controls; current provider/supervision requirements |
| ACT | Intensive 24/7 team-based nonresidential mental-health treatment | **No dedicated ACT fraud case located** | High-risk controls; 2026 HMA rate/payment-methodology review includes program-integrity objective |
| CFSS | Home/community assistance replacing PCA/CSG | **No dedicated CFSS case located.** Legacy PCA cases must not be relabeled CFSS | Transition still active; DHS says extended PCA ends Sept. 30, 2026 |
| EIDBI | Medically necessary autism/related-condition services for people under 21 | **Multiple dedicated federal cases:** Smart Therapy, Star Autism, Smart+Star indictment family | Separate enrollment moratorium; revalidation, site visits, updated medical necessity/authorization review; Aug. 25 authorization backlog |
| HSS | Housing-support state-plan HCBS for seniors/people with disabilities | **Multiple dedicated federal waves; several guilty pleas** | Program ended Oct. 31, 2025; no post-end-date HSS reimbursement |
| IHS | Support/training for people living in own/family home | **Dedicated + mixed charged:** Healey Homes; Guardian | High-risk controls; own-home rule is central to charged Healey theory |
| ICS | Support/training for adults in provider-controlled integrated settings | **Dedicated federal case:** Ultimate Home Health/Ahmed Kadar | High-risk controls; provider-controlled setting enrollment/capacity rules |
| IRTS | Community-based medically monitored residential mental-health treatment | **No dedicated IRTS fraud case located** | High-risk controls; 2026 HMA rate/payment-methodology review |
| Night Supervision | Assessed overnight assistance/supervision in a person's own home | **Mixed-service charged:** Guardian complaint includes overnight/night-supervision-related billing allegations | High-risk controls; awake/asleep rate frameworks separated in 2026 |
| NEMT | Transportation to covered nonemergency health appointments | **Dedicated state case:** Driving Miss Daisy >$1.4M alleged | Seven-county metro enrollment moratorium through Jan. 27, 2027; DHS announced Aug. 24 claims-compliance reviews |
| Recovery Peer Support | Peer-delivered substance-use recovery support/planning | **No dedicated service-fraud criminal case located** | High-risk controls; statutory billing/supervision restrictions and monetary-recovery authority |
| Recuperative Care | Short-term care for people experiencing homelessness who can leave hospital but cannot safely recover unhoused | **No dedicated case located** | Pre-enrollment risk assessment/habitability checks; prior authorization for all services since Aug. 1, 2026 |

## Case-coverage taxonomy

The public site should not use a binary `fraud / no fraud` marker. Use:

- **Dedicated case** — charging instrument is principally about that service.
- **Mixed-service case** — the service appears directly in charged allegations but the amount spans multiple services.
- **Adjacent enforcement** — misconduct involves an organization/provider in the field but not false claims for that service (e.g. a tax case).
- **No dedicated case located** — no dedicated criminal case was found in the current corpus/search pass; this is not proof no misconduct exists.
- **Adjudicated** — plea/verdict/judgment captured for an offense; financial metrics still require their own source/status.

## Fresh operational updates that matter for the eventual website

### EIDBI — Aug. 25, 2026

DHS says Acentra Health is taking longer than required to process EIDBI service authorizations because review volume increased. DHS/Acentra say they are increasing review capacity and prioritizing initial CMDE/ITP cases and renewals at risk of gaps. This is a real service-access consequence and should be presented as an agency operational update, **not** as proof that fraud controls caused all delays.

Source: `research/sources/src-mn-dhs-2026-08-25-eidbi-authorization-backlog.json`.

### NEMT — Aug. 24, 2026

DHS says Myers & Stauffer will review NEMT provider claims for state/federal compliance throughout 2026. Selection for review is not an accusation of fraud.

Source: `research/sources/src-mn-dhs-2026-08-24-nemt-program-reviews.json`.

### CFSS / PCA — Aug. 28, 2026

DHS says extended PCA services end Sept. 30, 2026 as the PCA/CSG-to-CFSS transition continues; regular PCA can continue until an individual completes the transition. The source page has an apparent footer typo under the item (`8/28/27`), while the item is headed Aug. 28, 2026 and appears in the 2026 chronology. The source record preserves that anomaly.

Source: `research/sources/src-mn-dhs-2026-08-28-cfss-transition.json`.

### Recuperative Care — Aug. 1, 2026 control change

DHS now requires prior authorization for all recuperative-care services.

Source: `research/sources/src-mn-dhs-2026-07-24-recuperative-prior-auth.json`.

### Enrollment moratoria

DHS says CMS approved extending the moratorium for 12 of the 14 high-risk services through Jan. 27, 2027; EIDBI has a separate moratorium through Oct. 31, 2026; HSS ended in 2025. NEMT has a specific seven-county metro enrollment moratorium through Jan. 27, 2027.

Source: `research/sources/src-mn-dhs-2026-07-high-risk-moratoria-extension.json`.

## Money discipline

Do not create a "14 high-risk programs = $X fraud" graphic.

The known numbers belong to different classes:

- program spending;
- claims billed;
- claims paid;
- charged alleged loss;
- post-plea government characterization;
- identified recoupment opportunity;
- potential recovery opportunity;
- cost avoidance;
- restitution ordered;
- cash recovered.

Companion ledger: `research/money/recovery-ledger-2026-08-29.json`.

## Next acquisition priorities

1. **Annual spend + provider counts:** derive all 14 services from one primary state/CMS data method and consistent dates.
2. **Court normalization:** every dedicated/mixed case through complaint/indictment → plea/verdict → judgment → restitution/forfeiture → appeal.
3. **No-case categories:** search historical MFCU civil/criminal archives, FCA settlements and state district court records before presenting absence as anything stronger than `not located`.
4. **Administrative actions:** preserve monthly revalidation, payment-hold, sanction and termination snapshots instead of replacing old totals.
5. **Control outcomes:** track whether moratoria, pre-pay review, prior authorization and revalidation reduce improper claims without calling every denial fraud.

## Public-build implication

Each program page can eventually answer five questions in this order:

1. **What was this money/service for?**
2. **Why did DHS call it high risk?**
3. **What actual cases exist?**
4. **What has been proven versus alleged?**
5. **What changed, and did the change work?**

That structure is more useful than an undifferentiated fraud count and protects the site from treating administrative risk as criminal guilt.
