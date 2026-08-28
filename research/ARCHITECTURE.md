# Minnesota Fraud Corpus — Architecture

This tree (`minnesota-fraud-corpus/`) is the **research substrate** for MinnesotaPeace coverage of public-program fraud, oversight failure, and related prosecutions. It is not a website. It is not a homepage. Records here must be able to survive link rot, later revisions, and adversarial reading.

**Research before website.** Do not publish a fraud dashboard, TOTAL FRAUD number, or “connected network” graphic until the corpus behind it passes the quality gates below. Journalism, press releases, and charging documents are inputs, not ceilings.

**Do not gut `main`.** The live MinnesotaPeace site (MN Peace public face + The Record on `main`) must not be stripped, redirected, or replaced by unfinished research. Land research on `research/minnesota-fraud-corpus` (or the working branch named for this work). Keep `main` intact.

## research/ layout

Canonical directories (this working copy uses these names at repo root of the research tree):

```
research/                          # this corpus
  sources/                         # source.schema.json instances + preserved bytes
  claims/                          # claim.schema.json instances
  entities/                        # entity.schema.json instances
  cases/                           # case.schema.json instances
  events/                          # event.schema.json instances
  money/                           # money.schema.json instances
  law/                             # legal.schema.json instances (statute | precedent)
  contradictions/                  # contradiction.schema.json instances
  analyses/                        # memos, assertion ladders, reconciliation notes
  datasets/                        # derived tables, extracts, join keys (not articles)
  schema/                          # draft-2020-12 JSON Schema files (this contract)
  pipelines/                       # ingest, validate, export jobs
  exports/                         # versioned dumps for review (never a homepage)
```

Investigation-family working shelves (narrative + primary PDFs while JSON is still being normalized):

```
  feeding-our-future/
  medicaid-hcbs/
  oversight-law/
  discovery/                       # acquisition queue
  reports/                         # research-state snapshots
```

Each family also exists (or will exist) as an `investigation-family.schema.json` record with `coverage_state`, `last_checked`, `next_check`, `source_depth`, `legal_maturity`, `prosecution_maturity`, and `missing_records`.

IDs are durable. Display names are not keys. Entity merges require `merge_evidence`.

## Record graph

```
source ──supports──► claim ──about──► entity
                      │                  │
                      │                  └──relationship──► entity
                      ├──amounts──► money (overlaps recorded; never summed blindly)
                      ├──events──► event
                      ├──cases──► case (defendants, charges, dispositions)
                      └──law──► legal (kind: statute | precedent)
warning (who-knew-what-when) ──► agency / program / subject_entity
contradiction ──links──► claim_a × claim_b (do not silently overwrite)
```

## Quality gates (1–9)

Before a claim can appear as a high-confidence **public factual statement**, it must pass these gates. Pipelines fail closed. A politically convenient, widely repeated, viral, or official sentence is not enough.

1. **Source.** Does a valid source exist? (`source_ids` / `source.schema.json`, preserved copy, `source_tier` 1–8, `source_status`)
2. **Passage.** Can we identify exactly where the source supports it? (`supporting_passages[]` with `source_id`, page, and/or quote. Do not cite a PDF you have not opened.)
3. **Interpretation.** Does the source actually say what the claim says? Primary-document-first: if a secondary sentence says “the audit found officials ignored dozens of warnings,” extract the audit’s own language, pages, period, and whether “ignored” is the audit’s term or the journalist’s.
4. **Status.** Is it allegation, finding, admission, verdict, estimate, etc.? Public wording must match `status` / `evidence_class`. An indictment is `CHARGED_ALLEGED`, not `ADJUDICATED`. Do not write “X stole $14 million” when the evidence only supports “prosecutors alleged….”
5. **Corroboration.** Is another source available or required? (`corroborating_source_ids`) Journalism is a lead, not the evidentiary ceiling.
6. **Contradiction.** Does contradictory evidence exist? If yes, record it in `contradictions/`; do not silently drop it or pick a favorite source. Official ≠ independently proven.
7. **Context.** Would omission of surrounding context materially mislead? Qualifiers (settlement no-determination language, as-of dates, joint-and-several restitution) travel with the claim.
8. **Currency.** Has later litigation or evidence changed the status? Preserve history with `valid_from` / `valid_until` / `superseded_by` rather than overwriting.
9. **Publication.** Is public wording appropriately qualified? A–E proposition class is not collapsed. Shared address is not conspiracy. Overlapping dollars are not summed. No homepage TOTAL FRAUD number. Research system before website; do not gut `main` until this corpus can replace it.

Also encoded in the schemas (not substitutes for gates 1–9): money hygiene (`metric_type`, `overlaps`); assertion ladder for high-stakes wording; entity `merge_evidence`; relationship_status `OBSERVED` / `ALLEGED` / `ANALYTICAL_INFERENCE` / `ADJUDICATED`. Instance JSON must validate against the matching draft-2020-12 file (`additionalProperties: false`).

## Non-goals

- A homepage “fraud total.”
- Treating `$9 billion` as stolen.
- Collapsing B/C oversight findings into D/E criminality.
- Treating shared addresses or community as a conspiracy graph.
- Replacing the live site on `main` with an unfinished research dump.

## Pipelines (intent)

`pipelines/` should, as they are built:

- ingest sources (hash, archive, extract text)
- emit/validate JSON against `schema/`
- refuse export of claims that fail gates 1–5
- refuse money rollups that ignore `overlaps`
- write versioned artifacts to `exports/` for review, not for the homepage
