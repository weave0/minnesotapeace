# Minnesota Fraud Corpus — JSON Schema (draft-2020-12)

These schemas are the contract for the research corpus. They are **JSON Schema draft-2020-12**. Validate instances with any 2020-12 validator; this directory is also parse-checked with `python3 -c "import json, pathlib; [json.loads(p.read_text()) for p in pathlib.Path('.').glob('*.json')]"`.

`$schema` on every file: `https://json-schema.org/draft/2020-12/schema`.

`additionalProperties` is `false` on objects unless a notes-shaped object needs extra keys.

## Files

| File | Record |
|---|---|
| `claim.schema.json` | Atomic, testable claim |
| `source.schema.json` | Durable source / document |
| `money.schema.json` | First-class dollar figure |
| `entity.schema.json` | Person, org, program, place, etc. |
| `relationship.schema.json` | Directed evidence-backed edge |
| `event.schema.json` | Chronology event |
| `case.schema.json` | Criminal / civil / administrative case |
| `legal.schema.json` | Statute or precedent (`kind`) |
| `contradiction.schema.json` | Source or claim disagreement |
| `warning.schema.json` | Who-knew-what-when |
| `investigation-family.schema.json` | Program / investigation family |

## Compatibility

- **Existing GitHub `claim.schema.json` required fields remain.** Required on every claim: `claim_id`, `claim_text`, `evidence_class`, `status`, `source_ids`, `confidence`, `is_allegation`, `is_inference`, `reviewed_at`. Original *optional* fields still present: `subject_ids`, `event_date`, `source_locator`, `jurisdiction`, `case_number`, `program_ids`, `amounts` (field name still `value`), `corroborating_source_ids`, `contradicting_claim_ids`, `review_notes`. Mandate extensions (`normalized_claim`, `claim_type`, `supporting_passages`, entity arrays, `date_start`/`date_end`, `qualifiers`, `editorial_notes`, timestamps, `valid_from`/`valid_until`/`superseded_by`, `assertion_ladder`, `proposition_class`) are optional, so previously written claim files remain valid instances.
- **Old lowercase `status` values remain valid.** The original enum (`confirmed`, `adjudicated`, `charged`, `alleged`, `disputed`, `superseded`, `withdrawn`, `unresolved`) is still accepted. Uppercase extensions (`ALLEGED`, `CHARGED`, `ADMITTED`, `STIPULATED`, `PROVEN_AT_TRIAL`, `JUDICIAL_FINDING`, `AUDIT_FINDING`, `AGENCY_FINDING`, `ADMINISTRATIVE_FINDING`, `DISPUTED`, `PARTIALLY_CORROBORATED`, `CORROBORATED`, `RETRACTED`, `OVERTURNED`, `UNRESOLVED`, `ANALYTICAL_INFERENCE`) are additive. `confidence` remains a number in `[0, 1]` **or** a qualitative enum (`VERY_HIGH` … `UNVERIFIED`).
- **Shared address ≠ conspiracy.** `SHARES_ADDRESS_WITH` is a shared address. Do not display it as a “connected fraud network.” Common attorney, accountant, employee, neighborhood, bank, program, or vendor is not automatically evidence of conspiracy. See `relationship.schema.json`.
- **Never sum overlapping dollars.** `amount_billed` ≠ `amount_paid` ≠ `alleged_loss` ≠ `proven_loss` ≠ `restitution_ordered` ≠ `recovered_amount` ≠ `program_spend`. Record overlaps on `money.overlaps` (`INCLUDED_IN`, `OVERLAPS_WITH`, `SUPERSEDES`, `PARTIAL_COMPONENT_OF`, `MAY_OVERLAP`, `NON_OVERLAPPING`) and on claim `amounts[].overlap_group_id`. A program-wide estimate may already contain charged-case amounts; those cases cannot be added to the program estimate. Never put a TOTAL FRAUD number on a homepage.
- **Journalism is a lead.** Reputable journalism is `source_status: REPUTABLE_JOURNALISM` / typically `source_tier` 8 and `evidence_class: LEAD_UNVERIFIED` unless independently verified against a primary record. Social media and anonymous material are `UNVERIFIED_LEAD` and are never published as established fact.
- **A–E propositions are not interchangeable.** `proposition_class` is optional but, when used, must not collapse:
  - **A** `A_FRAUD_AGAINST_STATE` — private actors intentionally defrauded government-funded programs.
  - **B** `B_OVERSIGHT_FAILURE` — agency failed to prevent, identify, stop, investigate, or respond.
  - **C** `C_NEGLIGENCE_MISADMINISTRATION` — negligence, incompetence, misadministration, or policy failure.
  - **D** `D_OFFICIAL_MISCONDUCT` — a specified official knowingly violated a legal/ethical/administrative duty.
  - **E** `E_GOVERNMENT_CRIMINAL_PARTICIPATION` — a public official knowingly participated in criminal conduct.
  Evidence of B does not establish C; C does not establish D; D does not establish E. Use `assertion_ladder` for high-stakes wording.
- **$9B is `fraud_estimate`.** The circulating “$9 billion” Minnesota Medicaid figure is a `fraud_estimate` (investigative hypothesis / oral estimate), **not** `proven_loss`. Do not headline it as money stolen.

## Claim `evidence_class`

`ADJUDICATED` · `CHARGED_ALLEGED` · `CIVIL_ALLEGED_OR_RESOLVED` · `AUDIT_FINDING` · `AGENCY_POSITION` · `SWORN_TESTIMONY` · `LEGISLATIVE_FINDING_OR_ALLEGATION` · `SECONDARY_VERIFIED` · `LEAD_UNVERIFIED` · `DERIVED_INFERENCE`

An indictment is `CHARGED_ALLEGED` (what prosecutors alleged), not `ADJUDICATED`. An official source is not independently proven merely because it is official.

## Metric types

Shared by `claim.amounts[].metric_type` and `money.metric_type`:

`program_authorization`, `program_spend`, `amount_requested`, `amount_billed`, `amount_claimed`, `amount_approved`, `amount_paid`, `alleged_loss`, `actual_loss`, `intended_loss`, `proven_loss`, `improper_payment`, `improper_payment_estimate`, `error_rate`, `fraud_estimate`, `restitution_requested`, `restitution_ordered`, `forfeiture_sought`, `forfeiture_ordered`, `assets_seized`, `assets_recovered`, `recovered_amount`, `identified_for_recovery`, `civil_settlement`, `administrative_recoupment`, `unknown_or_disputed`.


## Assertion ladder

For major or controversial claims, populate `assertion_ladder`:

| Field | Role |
| --- | --- |
| `claim` | The high-stakes formulation being tested |
| `evidence_available[]` | What the record actually shows |
| `missing_evidence[]` | What would be required for a stronger formulation and is not yet in the corpus |
| `current_assessment` | Qualified assessment that preserves A–E boundaries |

Example: the formulation “officials knowingly facilitated fraud” may have evidence that complaints existed, the agency received them, some investigations were inadequate, and payments continued, while missing evidence that a specified official knowingly joined the scheme. Current assessment: strong evidence of oversight failure (B); insufficient evidence for criminal participation by specified officials (E).
