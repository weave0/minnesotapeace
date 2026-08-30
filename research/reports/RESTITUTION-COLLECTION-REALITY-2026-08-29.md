# Restitution Collection Reality — 2026-08-29

## What this closes

`research/money/recovery-ledger-2026-08-29.json` listed several `known_missing_components`, including "actual cash collections by case and year," "outstanding restitution balances," and a "breakdown of the AG's $90M mixed judgments/recoveries figure." This pass produces the first hard, sourced numbers against those gaps.

## Headline finding

The Attorney General's oft-repeated "$90 million in judgments and recoveries since 2019" is, per a 2026-08-03 KSTP 5 INVESTIGATES review of state court records:

- **~$32M** criminal restitution *ordered* in MFCU-prosecuted cases (2019–2026)
- of which only **~$3M (~9%)** had actually been *collected* as of May 2026
- plus **~$61M** in civil judgments the AG's office says it separately tracks — but this component is **AG-stated only**; DHS confirmation was requested by KSTP and was still pending at publication
- note: $32M + $61M = $93M, not $90M — a ~$3M discrepancy against the AG's own headline that is not explained in the source and is preserved, not smoothed over

The Attorney General's chief of staff told KSTP the AG's office "plays no role in collecting restitution" — that's the probation system's and the courts' job — and that Minnesota law does not let the state seize assets the way federal prosecutors could in Feeding Our Future (reported $60–70M in cash/assets seized federally). That legal-authority claim is recorded as `AGENCY_POSITION` only; it has **not** been checked against the statutory-authority crosswalk from PR #27 and should be before it's used to explain the collection gap on the public site.

There is also an on-camera moment worth preserving for what it illustrates about the ordered-vs-collected distinction this whole corpus is built around: during the same interview cycle, AG Ellison initially disputed the low collection figures using his own MFCU's cumulative recovery paper, until MFCU Director Nicolas Wanka corrected him on camera — those were "restitution orders and judgments," not money actually recovered. Sourced primarily through a partisan outlet's account of the broadcast (americanexperiment.org, HTTP 403 to our fetcher on verification), corroborated by the fact that the dollar figures in the exchange match KSTP's own independently-reported numbers.

## A second, incompatible dataset

FOX 9 published its own restitution analysis on 2026-05-17 — three months before KSTP's — covering a specific 48-case sample since 2020: $13.3M ordered, $2.355M (17.7%) collected. That is a **different population and a different collection rate** from KSTP's MFCU-wide $32M/9% figures, not a corroborating measurement. Recorded as an open, unresolved contradiction (`contradiction-restitution-collection-scope-kstp-vs-fox9`) rather than merged, averaged, or silently preferred one over the other.

## New corpus records

- `research/sources/src-kstp-2026-08-03-restitution-collection-analysis.json`
- `research/sources/src-fox9-2026-05-17-restitution-collection-analysis.json`
- `research/sources/src-americanexperiment-2026-08-04-ellison-restitution-exchange.json`
- `research/claims/claim-mfcu-restitution-ordered-vs-collected-2019-2026.json`
- `research/claims/claim-fox9-48case-restitution-ordered-collected-2026-05.json`
- `research/claims/claim-ag-civil-judgments-61m-unverified.json`
- `research/claims/claim-warsame-hu-individual-restitution-2026-05.json`
- `research/claims/claim-mn-no-state-asset-seizure-authority.json`
- `research/claims/claim-ellison-wanka-restitution-confusion-2026-08.json`
- `research/contradictions/contradiction-restitution-collection-scope-kstp-vs-fox9.json`
- `research/money/recovery-ledger-addendum-2-2026-08-29.json`

## Still open (unchanged or newly surfaced gaps)

- DHS has not confirmed the ~$61M civil-judgments component, and the ~$3M arithmetic gap against the $90M headline is unexplained.
- No case-by-case reconciliation exists between the KSTP and FOX 9 datasets.
- DHS's own >$56M "identified for recovery" figure still has no public assessed-vs-collected breakdown — the DHS Office of Inspector General public pages repeat the >$56M headline and a "$2.29 return per dollar invested" framing but do not publish a collection ledger.
- Forfeiture-ordered-vs-realized and administrative-recoupment-assessed-vs-collected remain entirely undocumented in any public source found this pass.
- The AG's "Minnesota law doesn't allow asset seizure" claim needs statutory verification (Minn. Stat. ch. 609.5311 et seq. or successor provisions) before it's treated as settled fact, not just an agency's explanation for a bad number.
- No entity records yet exist for Keith Ellison, Nicolas Wanka, the MFCU as an organization, or DHS as an organization; several new claims above reference provisional slug IDs (`person-keith-ellison`, `org-mn-attorney-general-mfcu`, etc.) that should be backed by real `research/entities/` records before these claims are promoted to the public `/money/` or `/authority/` pages.

## Not yet promoted to the public site

None of this has been pushed into `/money/index.html` yet. Per the corpus's own publication rule, it should only be promoted once the DHS-confirmation gap on the $61M figure and the statutory check on the asset-seizure claim are resolved, or once it's promoted with those specific caveats intact rather than smoothed into a single number.
