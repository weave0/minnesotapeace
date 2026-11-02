# November 1, 2026 — Cross-judgment financial obligations and shared-property reconciliation

## Scope and independence

This is a second November research tranche built on merged PR #72. It does **not** modify the public tracker recovery totals, historical DOJ aggregate milestones, or the canonical recovery inventory's 27 entries.

**Newly located record**: the October 19, 2026 federal in-rem civil forfeiture proceeding concerning three Minneapolis properties was identified by **docket number 0:26-cv-04533**, `United States v. 2900 Pillsbury Avenue, Minneapolis, Minnesota et al.`, D. Minn. Justia's court-docket mirror describes **ECF 1**, the complaint for forfeiture in rem; the actual complaint's contents have **not** been read. The DOJ October 30, 2026 release provides a separate agency-sourced approximate group value of $519,000. This case identification is new confirmation of an existing DOJ news item, not a court finding of ownership, wrongdoing, or forfeiture.

## Source acquisition and limitations

| Record | Docket | Located at | What is established | What is missing |
| --- | --- | --- | --- | --- |
| Three-property federal action | `0:26-cv-04533`, ECF 1 | [Justia docket extract](https://dockets.justia.com/docket/minnesota/mndce/0:2026cv04533/236900), showing Oct. 19 filing | U.S. filed civil forfeiture complaint concerning 2900/2906 Pillsbury Avenue and 211 W. 29th Street, Minneapolis, under 18 U.S.C. 981 | Actual signed complaint, exhibits, updated docket, any judicial orders or disposition |
| Ahmed Sharif Omar-Hashim restitution | `0:22-cr-223`, ECF 1036 | [Third-party court judgment text and PDF link](https://pandemicdarlings.com/source-documents/sentencing-judgment-united-states-v-bock-et-al-feeding-our-future-dkt-b2dc59da87/) | Filed Sep. 1; 36-month imprisonment; $3,314,276 restitution with named joint-and-several co-defendants Bock, Said and Abdulkadir Salah | PDF binary/hash independently verified, satisfaction and payment ledger, comparison to each co-defendant's own judgment |
| Omar-Hashim property share | `0:22-cr-223`, ECF 874 | [Third-party reproduced order](https://pandemicdarlings.com/source-documents/order-granting-868-motion-for-preliminary-order-of-united-states-v-boc-a27c44454d/) | May 18 second preliminary forfeiture order lists 2722/2742 Park Avenue South and confirms Omar-Hashim's **20% interest** for credit against his money judgment | Final third-party resolution and disposition; verified sales ledger and net proceeds |
| Government property explanation | `0:22-cr-223`, ECF 868 | [Third-party reproduced motion](https://pandemicdarlings.com/source-documents/second-motion-for-preliminary-order-of-forfeiture-united-states-v-bock-a398c7653f/) | Government says the Park Ave property belonged to Cosmopolitan Business Properties LLC, owned among Said, Salah and Omar-Hashim, and was already included in Said ECF 805; purchase price alleged $2,780,000 | Independent property/ownership proof and disposition values, check exact order-to-order overlap |
| Said preliminary forfeiture | `0:22-cr-223`, ECF 805 | [Source record from tranche 1](../sources/src-court-mnd-22-cr-223-ecf805-said-preliminary-forfeiture.json) | Preliminary $7,837,656.60 forfeiture money judgment, with net forfeited asset credits | Signed October 28 sentencing judgment and final judgment terms |

Original PDF URLs supplied by the archive were **not fetchable by the current tooling** (web retrieval cache misses; runtime outbound DNS unavailable). Reproduced text was inspected and the archive supplies SHA-256 values, but our team did **not independently compute or verify** those SHA-256 values; do not claim originals acquired/hashed. CourtListener search results did not expose the three-property civil complaint for free in this session. No paid PACER access used.

## Analytical finding A — shared obligation, not additive dollars

ECF 1036 is a court-judgment record of **$3,314,276 restitution ordered** from Omar-Hashim; its joint-and-several schedule explicitly references Bock, Said and Abdulkadir Salah. Individual named rows in this schedule do not become separate new money pools. The existing corpus has Bock ECF 907's **$242,807,755 restitution**. Its own judgment reportedly has a blank co-defendant schedule; that asymmetry is not enough to allege legal contradiction. Reconcile the exact obligation/victim schedule using the other defendants' filed judgments. A secondary report says Said received over $44 million in restitution ordered October 28; signed judgment not acquired, and no exact amount should be entered.

## Analytical finding B — same physical asset across multiple orders

The Park Avenue real property occurs in Said's preliminary forfeiture proceeding (ECF 805) and Omar-Hashim's separately signed second preliminary forfeiture order (ECF 874), with government motion ECF 868 linking the ownership. **Omar-Hashim's 20% interest** is specifically reflected in ECF 874. An asset's name repeated in multiple defendant filings cannot be treated as multiple independently realized properties. A historic purchase price does not establish realizable sale price; neither does a forfeiture order prove collection or a final disposition.

## Analytical finding C — civil forfeiture filing vs recovered property

In `0:26-cv-04533`, the three property addresses are case-defendant names in a **civil in-rem complaint**, not names of criminally convicted people. The government announced approximate value of $519,000 and lis pendens. The actions establish a claim and property-title notice, not cash realized, transfer of final title, auction proceeds or court-approved forfeiture. **The Pillsbury and Park Avenue properties are different groups**; there is no evidentiary basis to conflate them.

## Canonical work performed

- Four research-only source records under `research/sources/`.
- Non-additive asset/obligation map `research/money/fof-court-asset-overlap-2026-11-01.json`, including evidence classes, legal stages, shared ownership and missing collection data.
- Public `/money/` page addition explaining why multiple orders and a filing do not translate to government cash returned.
- No new `recovered_amount` rows and no changes to `research/money/tracker-recovery-v1.json` or its generated published projection.

## Next zero-cost acquisitions (ranked)

1. **D. Minn. 0:26-cv-04533 ECF 1** complaint and any exhibits. Obtain via free RECAP upload, district court government-host publication or reporter copy; do not pay PACER. Then inspect property-specific allegations, valuation, liens, claimants and any subsequent order.
2. **D. Minn. 0:22-cr-223, Said judgment entered after 2026-10-28**. Retrieve actual signed judgment and restitution schedule; compare it to ECF 805, Omar-Hashim ECF 1036 and Bock ECF 907.
3. **D. Minn. 0:22-cr-223 ECF 653, 805, 868, 874 and 1036** original PDF copies plus any final forfeiture orders; hash exact bytes and inspect page images; trace Park Avenue property share and disposition.
4. **Omar-Hashim and co-defendant collections**: obtain clerk Financial Litigation Unit accounting, final forfeiture disposition/USMS real property sale records and any satisfaction entries. Do not use a defendant's ability-to-pay schedule as evidence paid.
5. **Empire-family ECF gaps in 0:22-cr-124**: Farah 851/858; Ismail 690; Nur 939; Hayat Nur 869; forfeiture 665/902; determine joint-and-several overlap with verified judgment and collection records.
6. **State EAHN/Nasib**: obtain assigned docket numbers, responses, verified disbursement records; proposed Partners in Nutrition settlement hearing December 15 remains future as of Nov. 1.
7. Review additional `0:22-cr-223` sentencing judgments ECF 1032, 1048 and 1014 for individual restitution and cross-defendant schedules (preliminary leads only here, not published totals).

## Integrity rules

- Only primary evidence or clearly attributed document extracts; court documents available through third-party transcription carry a visible verification limitation.
- Allegations remain allegations; motions reflect party positions; judgments and orders reflect what the court ordered.
- *No grand totals* from restitution plus forfeiture plus asset seizures; the same property/obligation may be represented repeatedly.
- Exact 78/68/31 DOJ historical ordinal counts remain dated.
- Never claim recovery from an order alone.
