# Minnesota Public-Program Fraud Research Corpus

This directory is the evidence layer for The Record on MinnesotaPeace.com.

## Mission

Build a source-verifiable, legally careful, continuously updatable record of fraud, alleged fraud, oversight failures, program vulnerabilities, enforcement actions, court outcomes, recoveries, disputed claims, and unresolved questions involving Minnesota-administered public programs and related federal funds.

This corpus must not assume that "the State of Minnesota committed fraud" as a blanket proposition. It distinguishes fraud committed against public programs from documented administrative failures, civil liability, criminal conduct by identified actors, political allegations, and unproven claims.

## Evidence classes

Every substantive statement must be classified before publication:

1. **ADJUDICATED** — conviction, guilty plea, final judgment, sentence, or other final adjudication.
2. **CHARGED_ALLEGED** — indictment, information, criminal complaint, search-warrant allegation, or prosecutor allegation not yet adjudicated.
3. **CIVIL_ALLEGED_OR_RESOLVED** — False Claims Act complaint, settlement, consent order, corporate integrity agreement, or other civil disposition; settlement language must preserve any express denial/no-determination caveat.
4. **AUDIT_FINDING** — finding of OLA, HHS OIG, USDA OIG, CMS, GAO, or another identified audit authority.
5. **AGENCY_POSITION** — factual or legal position advanced by MDE, DHS, DCYF, Attorney General, Governor, CMS, USDA, etc.; not treated as independent proof merely because an agency states it.
6. **SWORN_TESTIMONY** — testimony under oath, deposition, transcribed interview, or legislative hearing testimony.
7. **LEGISLATIVE_FINDING_OR_ALLEGATION** — committee report, member statement, hearing summary, or legislative investigative claim. Record party/committee provenance and distinguish majority/minority material.
8. **SECONDARY_VERIFIED** — high-quality reporting that is independently corroborated or that documents facts not available in a primary source.
9. **LEAD_UNVERIFIED** — social media, anonymous tip, partisan assertion, or other lead awaiting verification. Never publish as established fact.
10. **DERIVED_INFERENCE** — an analytical conclusion produced from cited evidence. Must identify its supporting records and must never masquerade as a source fact.

## Money taxonomy

Amounts must never be collapsed into one headline number. Each amount receives a `metric_type`:

- `program_spend`
- `amount_billed`
- `amount_paid`
- `alleged_loss`
- `intended_loss`
- `proven_loss`
- `restitution_ordered`
- `forfeiture_ordered`
- `recovered_amount`
- `identified_for_recovery`
- `civil_settlement`
- `improper_payment_estimate`
- `error_rate`
- `fraud_estimate`
- `unknown_or_disputed`

Example: the widely repeated "$9 billion" Minnesota Medicaid figure is an estimate/investigative hypothesis derived from spending in high-risk services, not a presently adjudicated loss figure. It must be displayed separately from charged, proven, recovered, or audited amounts.

## Core entities

The corpus should normalize and connect:

- people
- organizations and DBAs
- nonprofits
- provider entities and NPI/provider identifiers
- meal sites / child-care centers / treatment sites
- state agencies and divisions
- federal agencies
- public programs and benefits
- cases, dockets, filings, pleas, trials, judgments, sentences
- audits and audit findings
- grants and contracts
- real property and other identified assets
- transactions and transfers when supported by public records
- laws, rules, regulations, waivers, state-plan amendments, executive orders
- legislative hearings and testimony
- locations
- complaints, referrals, sanctions, payment holds, disenrollments
- source documents
- factual claims and contradictions

## Required claim fields

At minimum each claim must preserve:

`claim_id`, `subject_ids`, `claim_text`, `evidence_class`, `status`, `event_date`, `source_id`, `source_date`, `source_locator`, `jurisdiction`, `case_number`, `program_ids`, `amount`, `metric_type`, `corroborating_source_ids`, `contradicting_claim_ids`, `confidence`, `is_allegation`, `is_inference`, `reviewed_at`, `review_notes`.

## Contradiction ledger

The project explicitly records conflicts between public claims. A source being official does not eliminate contradictions.

Seed example: the Minnesota Judicial Branch stated on September 23, 2022 that Judge John Guthmann never ordered MDE to resume Feeding Our Future reimbursement payments; MDE resumed payments voluntarily. Any contrary public assertion is linked to that judicial correction rather than silently overwritten.

## Source priority

Prefer, in order:

1. Court filings, judgments, plea agreements, trial verdicts, sentencing orders, official dockets.
2. Statutes, regulations, session laws, federal/state plan documents and waivers.
3. DOJ / USAO / FBI / IRS-CI / HHS-OIG / USDA-OIG / CMS / state MFCU primary materials.
4. Minnesota Office of the Legislative Auditor and other formal audit reports.
5. Minnesota Judicial Branch, Revisor, Legislature, agency records and licensing/enforcement records.
6. Sworn congressional/state legislative testimony and investigative materials, clearly labeled by provenance.
7. Corporate, charity, property, campaign-finance, tax-exempt organization, licensing, UCC and other public records when relevant.
8. Credible news reporting for context, chronology, interviews, or leads.
9. Social media and anonymous material only as leads to independently verify.

## Current investigation families

Initial research confirms the corpus must cover at least:

- Feeding Our Future / federal child nutrition programs
- Housing Stabilization Services (HSS)
- Early Intensive Developmental and Behavioral Intervention (EIDBI) / autism services
- Integrated Community Supports (ICS)
- Individualized Home Supports (IHS) and related HCBS services
- Adult Rehabilitative Mental Health Services (ARMHS)
- substance-use treatment / Medicaid kickback and double-billing matters
- Child Care Assistance Program (CCAP)
- Great Start Compensation Support Payment Program
- personal-care, companion-care, homemaking, respite and related Medicaid cases
- Behavioral Health Administration grants and internal-control failures
- the broader set of DHS-designated high-risk Medicaid services
- obstruction, witness tampering and juror bribery connected with fraud prosecutions
- enforcement, recovery, payment-withhold, provider-screening and revalidation actions
- federal and state legislative oversight of Minnesota program integrity

## Research rule

No fact is promoted to the public site because it is politically convenient, widely repeated, viral, or asserted by an official. It is promoted because its provenance and evidentiary status are explicit and reproducible.
