# Minnesota Peace: October 2026 evidence release — reviewed November 1

## Publication principles

This is the internal review ledger for the November 1 public status and tracker update, not a replacement for primary documents. The public release uses source-backed **events** and does not upgrade Feeding Our Future's three dated aggregate milestones (78 charged, 68 convicted, 31 sentenced) because the latest releases do not supply a newer complete DOJ ordinal in each category.

**Do not publish an overall fraud total.** DOJ's nearly $83 million is a mixed alleged/proven intended-loss description across multiple legal stages. The $29.1 million newly charged figure is not an additional amount to stack on top. Payments to businesses, billed amounts, lawsuit allegations, criminal proceeds, restitution, seizure, forfeiture sought and recoveries can overlap. No amount in this release qualifies as independently verified new cash collected.

## Official source ledger and substantive changes

| Date of underlying event | Source date | Program | Subject / proceeding | Stage and evidence category | What changes |
|---|---|---|---|---|---|
| Sep. 29 | Oct. 30 | Federal child nutrition / Feeding Our Future | Shaakir Mohamud Ibrahim | Indicted / CHARGED_ALLEGED | Alleged $1.1M scheme; do not infer charged-defendant ordinal |
| Oct. 7 | Oct. 8 | HSS | Sharmaine Meadows | Jury verdict / ADJUDICATED | Three healthcare-fraud convictions; DOJ says company received more than $3.6M in Medicaid payments; no sentencing in source |
| Oct. 19 | Oct. 30 | Feeding Our Future | Three Minneapolis properties | Civil forfeiture complaint / FORFEITURE_SOUGHT | Approx. $519K valuation, lis pendens; no forfeiture judgment or collected proceeds |
| Oct. 21 | Oct. 30 | Child nutrition / Feeding Our Future and PIN | Muna Wais Fidhin | Jury verdict / ADJUDICATED | Nine counts; trial evidence involves both sponsors |
| Oct. 21 | Oct. 30 | SNAP | Ahmed Abdul Razaq Al Obaidi and Muhammad Abdullah Kahn | Criminal complaints / CHARGED_ALLEGED | Separate SNAP benefit-trafficking allegations; do not add to FOF |
| Oct. 22 | Oct. 30 | EIDBI | Emily Marice Ravits | Indictment / CHARGED_ALLEGED | $7.7M scheme alleged; supervisory certification issues |
| Oct. 22 | Oct. 30 | EIDBI | Feisal Mohamed Elmi | Indictment / CHARGED_ALLEGED | $8.2M scheme alleged; purported services not delivered |
| Oct. 26 | Oct. 26 | Child nutrition / PIN | Nasib Bakery, Abshir Hossen | Civil False Claims Act complaint / CIVIL_ALLEGED | Alleged false claims and payments; civil case, not FOF criminal conviction |
| Oct. 26 | Oct. 26 | Child nutrition / PIN, EAHN | East African Healthcare Network and related parties | Civil False Claims Act complaint / CIVIL_ALLEGED | More than $10M reimbursement claims alleged; do not combine parties' overlapping claims |
| Oct. 28 | Oct. 30 | Feeding Our Future | Salim Ahmed Said | Sentenced / ADJUDICATED | 360-month prison sentence. DOJ describes over $44M in proceeds facilitated, not an adjudicated collection figure |
| Oct. 28 | Oct. 30 | Medicaid / estates | Nicole and Shaun Slegers | Pleaded guilty / ADJUDICATED | Deceased recipients' estates, vehicles; distinct from service-claim reimbursement schemes |
| Oct. 28 | Oct. 30 | Other Medicaid programs | Faiza Osman Ahmed | Indictment / CHARGED_ALLEGED | Alleged ~$10M, separate programs |
| Oct. 28 | Oct. 30 | Integrated Community Supports | Jama Yusuf Mohamod | Indictment / CHARGED_ALLEGED | Alleged $3.2M |
| Oct. 29 | Oct. 30 | EIDBI | Habiba Mohamed | Charged by information / CHARGED_ALLEGED | Alleged $19.1M involving previously charged co-conspirators; overlap warning |
| Oct. 30 | Oct. 30 | Juror bribery | Said Farah | Sentenced / ADJUDICATED | 78 months and $40K fine for distinct juror-bribery offense; not a new FOF food-fraud conviction |

### Core primary source URLs

- USAO-MN October 30: https://www.justice.gov/usao-mn/pr/dojs-fraud-division-and-united-states-attorneys-office-district-minnesota-uncover-nearly
- USAO-MN October 8: https://www.justice.gov/usao-mn/pr/minnesota-woman-convicted-36m-scheme-defraud-medicaid-housing-services-program
- Minnesota AG October 26 civil claims: https://www.ag.state.mn.us/Office/Communications/2026/10/26_Nutrition-Fraud.asp
- Minnesota AG September 24 PIN settlement announcement: https://www.ag.state.mn.us/Office/Communications/2026/09/24_Partners-In-Nutrition.asp

## Open primary-document and accounting gaps

1. **Individual filings:** Acquire the actual October 2026 indictments, information, complaints, verdict forms and signed judgments; release summaries establish announcements and statuses, not every underlying legal detail.
2. **Salim Ahmed Said:** Acquire signed October 28 sentencing judgment and orders for precise restitution, forfeiture, joint-and-several responsibility and payment statuses.
3. **October 19 forfeiture:** Acquire civil complaint, property identifiers, valuations, orders, disposition, receipts and allocation; do not mark $519K collected.
4. **Partners in Nutrition:** Court hearing announced for December 15, 2026. **Proposed settlement** $18,517,909.27, judicial approval and payment realization not verified; $1M stayed penalty is contingent.
5. **Count reconciliation:** News reporting mentions 81 charged and 32 sentenced after Said, but the canonical official ordinal fields require explicit current official milestone or reconciled primary docket data under revised methodology. Keep historical milestones dated.
6. **Civil vs criminal:** AG lawsuits against PIN-associated entities are *state civil* matters, not members of Feeding Our Future's criminal defendant roster.
7. **Further backlog:** October 26 *State v. Yusuf* appellate reversal, October 29 Iska/Bright Horizon EIDBI searches (investigations, no established guilt), September 24 OLA Optum oversight review and October DHS provider-enforcement statistics require dedicated primary-document ingestion before a broader program-integrity feature.
8. **Existing PR #67:** Court-backed restitution/forfeiture evidence remains open and should be reconciled separately, without overwriting existing recovery entries.

## Publication change boundary

New official source records and 12 individual event rows are selected for the generated Public Money Tracker and Accountability Brief. The homepage and current-status page show October court and enforcement developments with direct official citations. PIN civil suits are described on the human-readable status page and research memo but are *not* misclassified as Feeding Our Future criminal cases in the tracker. Recovery ledger remains unchanged. Generated milestone cards remain untouched.

## QA

Review source citations and legal stages, run `scripts/check-research-integrity.py`, `scripts/build-tracker.py`, `scripts/test-tracker-boundary.py`, `scripts/build-accountability-brief.py`, `scripts/test-accountability-brief.py`, `scripts/check-public-provenance.py`, `scripts/check-status-snapshot-fresh.py`, `scripts/test-status-snapshot-boundary.py` and production smoke tests before calling release published. Do not imply tests or deployment succeeded until CI/runtime verifies them.
