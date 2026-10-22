# Minnesota Peace — October 22, 2026 evidence desk

**Research-only staging note; not a publication manifest or live-page update.** Checked against public source pages October 22, 2026. Legal status is sourced as of the individual action date. Do not use this memo to change generated `STATUS-SNAPSHOT` marker blocks; follow the canonical claims/source/build process.

## 1. Housing Stabilization Services — Sharmaine Meadows jury conviction

- **Official source:** U.S. Attorney's Office, District of Minnesota, release dated October 8, 2026: https://www.justice.gov/usao-mn/pr/minnesota-woman-convicted-36m-scheme-defraud-medicaid-housing-services-program
- **Evidence class:** ADJUDICATED (jury verdict as reported by DOJ); judgment and sentencing order still to acquire.
- **Disposition date:** October 7, 2026 (DOJ reports verdict the prior day). **Release date:** October 8.
- **What is established by the official report:** A federal jury convicted Meadows on **three counts of health-care fraud** in the Minnesota HSS matter. DOJ says the program paid more than **$3.6 million** to her company's accounts between 2020 and 2025. Reported trial evidence includes improper billing for beneficiaries in hospital, employees outside Minnesota / the country, and implausible working hours.
- **Money semantics:** `amount_paid` per DOJ's verdict announcement, **not** court-ordered restitution, a collected recovery, or a fresh amount to sum into Feeding Our Future losses. Verify whether later judgments change legal characterization.
- **Unresolved:** federal case number, verdict form, final judgment, restitution/forfeiture order, sentencing date and sentence; do not assert any of these from the press release.
- **Ready-to-use wording:** "A federal jury convicted Sharmaine Meadows of three health-care-fraud counts on October 7 in a Housing Stabilization Services case. DOJ said more than $3.6 million was paid to the company over 2020–2025. Sentencing remains a separate proceeding."
- **Publication targets after provenance ingestion:** `status/index.html` HSS section; homepage 'Latest verified'; separate HSS case-event record. **No invented program-wide convicted count.**

## 2. Refocus Recovery / Kyros — charity governance civil complaint

- **Official source:** Minnesota AG, October 1, 2026: https://www.ag.state.mn.us/Office/Communications/2026/10/01_Refocus-Recovery.asp
- **Evidence class:** CIVIL_ALLEGED_OR_RESOLVED, specifically **civil complaint/allegations**, not an adjudicated finding or criminal charge.
- **What the complaint alleges:** Refocus Recovery, a nonprofit, and founder Daniel Larson improperly used the nonprofit as a Medicaid-fund pass-through benefiting related for-profit Kyros entities (Kyros PBC, Kyros Services, LLC, Kyros Staffing, LLC), with governance and conflict-of-interest violations. The AG says the suit was filed in Ramsey County and explicitly states its Charities Division's authority is civil.
- **Relationship hygiene:** Nonprofit, founder and the three named for-profit corporations should be distinct entities. The alleged transfers/outsourcing are *alleged complaint relationships*, not independently proven bank transfers merely because the parties share a person.
- **Unresolved:** obtain the filed complaint, exhibits, case number, signed contracts and any transaction detail before producing a definitive dollar-flow chart; seek answer / denial and subsequent docket activity.
- **Ready-to-use wording:** "Minnesota's Attorney General filed a civil suit October 1 alleging that Refocus Recovery and its former founder used the nonprofit to route Medicaid-funded operations and revenue to related Kyros businesses. The allegations have not been established by a judgment."
- **Editorial lane:** nonprofit governance / Medicaid provider relationships, separate from HSS and Feeding Our Future.

## 3. Partners in Nutrition — civil settlement obligation, not proof of collection

- **Official source:** Minnesota AG, September 24, 2026: https://www.ag.state.mn.us/Office/Communications/2026/09/24_Partners-In-Nutrition.asp
- **Evidence class:** CIVIL_ALLEGED_OR_RESOLVED (consent judgment), not a federal criminal conviction.
- **Instrument:** AG says lawsuit and consent judgment require Partners in Nutrition / Partners in Quality Care to pay **$18,517,909.27** (all funds in its possession), produce additional records, and voluntarily dissolve.
- **Money semantics:** `civil_settlement` / **payment ordered or agreed**, pending independent bank/court documentation of transfer. Do **not** recode as `recovered_amount` or `collected` purely because the agency's release headline uses "recovers." The release says these funds **will** be returned to MDE and ultimately USDA.
- **Additional condition:** a **stayed $1 million civil penalty** is conditional and is neither currently collected nor additive to the settlement payment. Investigations of individuals, site operators and vendors remain ongoing; the consent resolution does not resolve their liability.
- **Unresolved:** consent-judgment PDF/court case number; satisfaction or receipt of funds; dates of dissolution and transfer; any overlap with existing meal-program records or previously identified funds.
- **Ready-to-use wording:** "A September 24 civil consent judgment requires Partners in Nutrition to pay $18,517,909.27 and dissolve. Minnesota's Attorney General says the funds are to be returned through the state education agency to USDA. Payment completion has not been independently verified here."

## 4. Feeding Our Future — newly indicted defendant / conflicting ordinal sources

- **Reporting, not independently reconciled primary ordinal:** Minnesota Public Radio (October 5, 2026), https://www.mprnews.org/story/2026/10/05/shaakir-mohamud-ibrahim-indicted-feeding-our-future-fraud-money-laundering ; Minnesota Star Tribune (October 2, 2026), https://www.startribune.com/man-accused-of-defrauding-food-program-of-1-million-in-feeding-our-future-scheme/601896701
- **Reported filing date:** indictment September 29; unsealed October 1. Reporters identify Shaakir Mohamud Ibrahim as the **81st** person charged, while our official DOJ milestone remains **78th**, dated November 24, 2025.
- **Evidence class for presently acquired references:** SECONDARY_VERIFIED as a reporting lead for a **CHARGED_ALLEGED** filing, not a court-verified ordinal in our corpus.
- **Alleged amounts as reported:** approximately $1.2 million in reimbursement requests, about $1.1 million paid to the entities; do not convert those allegations into a verified fraud loss or add them to separate existing defendant amounts.
- **Required to promote:** acquire indictment and docket, verify identity and alleged program/site relationships, reconcile 79–81 on the individual-defendant roster, and determine whether DOJ issued a newer official count. Do not silently overwrite the generated 78 card or assert 81 as a DOJ ordinal.
- **Permissible interim description:** "An October 2026 indictment is reported against Shaakir Mohamud Ibrahim in the Feeding Our Future investigation; the project's last explicitly verified DOJ ordinal count predates this filing."

## 5. Additional state Medicaid prosecution lead

- **Official source:** Minnesota AG, September 29, 2026: https://www.ag.state.mn.us/Office/Communications/2026/09/29_Medicaid-Fraud.asp
- **Evidence class:** CHARGED_ALLEGED, state prosecutions. AG announced nine individuals charged in several cases and alleged more than $3 million across them. Do not collapse individual accusations into verdicts or any HSS/FOF program total.
- **Follow-up:** fetch Ramsey/Hennepin county complaints and docket statuses; build cases individually, with amounts identified by allegation and provider rather than one indistinct total.

## 6. Audience and publication findings

- **Observed October 22:** https://minnesotapeace.com/ leads with October 1 movement and says "Updated Oct. 6, 2026." The generated https://minnesotapeace.com/status/ also indicates October 6.
- **Actual repo:** `status/index.html` embeds generated markers for the three official ordinal cards and the "Status checked" dates. Never hand-edit these blocks: `scripts/build-status-snapshot.py` derives them from canonical claim records.
- **Homepage copy gap:** its "Latest verified" module omits the October 7 Meadows verdict. The FOF figure 78 is legitimately labeled as a **November 2025 DOJ count**, not a purported October 2026 full roster.
- **Active research dependency:** PR #67 remains open and unmerged as of this check (judgments, forfeiture evidence, and evidence-basis gates). Do not overwrite that work or turn court-ordered sums into collected totals.
- **Zero-cost guardrail:** existing repository workflows run on pull requests and on pushes to `main`, including Cloudflare deployment. Because the project owner directed **no paid GitHub Actions/workflows**, stage on a separate branch without opening a PR or pushing to main. Do not run `workflow_dispatch`. Publishing needs a separately authorized zero-cost mechanism or confirmation that these CI triggers are disabled.
- **Publication sequence:** (1) ingest primary-source records, (2) validate legal/money classification and ownership links, (3) reconcile generated snapshots without manual HTML edits, (4) update HSS and distinct civil-enforcement surfaces, (5) run local validations, (6) only then publish via a confirmed no-cost route. No automated publication from a social-media allegation.

## 7. Cross-state viral posts as investigative leads

The October 22 viral post about Virginia Sen. Louise Lucas is outside the Minnesota public-program case roster. It is a reminder to separate corporate registrations, Medicaid participation, property ownership, campaign transfers, accusations, indictments, and findings of guilt. It should **not** become an MN Peace finding or a fraud-network relationship without separate primary documentary support.
