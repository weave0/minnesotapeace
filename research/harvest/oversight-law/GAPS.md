# GAPS.md — What was searched and not confirmed as a primary source

**Compiled:** 26 August 2026; **last reconciled:** 31 August 2026.  
A gap is not proof that a document does not exist. It means this pass did not retrieve an official full text or did not find the document on the official host.

---

## 1. The $9 billion figure — missing primary transcript

| Missing item | Why it matters | What was used instead |
|---|---|---|
| Official transcript or video of the **18 December 2025 USAO news conference** | The $9B / “half or more of $18B” statement is **not** in the justice.gov press release | AP, CBS, KSTP, Minnesota Reformer, Fox contemporaneous quotes of AUSA Joseph Thompson (`JOURNALISM_LEAD`) |
| CMS data pull / spreadsheet of the **$18 billion** 14-program claims extract | Thompson attributed the denominator to a CMS pull; the extract itself was not posted | Oral description + later KARE 11 data-practices reporting of $20.83B (`JOURNALISM_LEAD`) |
| Written DHS IG / Medicaid Director statements of 18–19 Dec 2025 | Pushback is currently news-quoted | Forum / CBS / Reformer quotes |
| Any OLA, GAO, or HHS OIG report that **measures** $9 billion in Medicaid fraud | Would be needed to treat the figure as an audit finding | **None found.** Figure remains `fraud_estimate` |

**Do not close this gap by treating House Oversight’s reuse of “estimated $9 billion” as independent measurement.**

---

## 2. CMS correspondence and review records

**2026-08-30 pass:** Both Minnesota CAP letters retrieved directly from mn.gov/dhs: `src-mn-dhs-2025-12-31-cap-original` and `src-mn-dhs-2026-01-30-cap-revised`.

**2026-08-31 pass:** Federal Register document **2026-00512** was located on the official Federal Register host. It is the CMS section 1904 notice of opportunity for hearing and reproduces the **January 6, 2026 Administrator Oz letter to Governor Walz**. This closes two formerly separate gaps: the official hearing-notice citation and primary-host full text of the January 6 letter. Indexed as `src-cms-federal-register-2026-00512-mn-1904-hearing`.

| Missing item | Lead | Status |
|---|---|---|
| Administrator Oz **6 January 2026** letter to Gov. Walz | Federal Register document 2026-00512 | **RESOLVED (2026-08-31).** Official Federal Register notice reproduces the letter. |
| Federal Register citation for the § 1904 hearing notice | Federal Register document 2026-00512 | **RESOLVED (2026-08-31).** |
| CMS letter **approving** the revised CAP (state says **19 March 2026**) | https://mn.gov/dhs/program-integrity/factcheck/ | State claim only; CMS original still not fetched from a primary host. |
| 31 December 2025 first CAP PDF | DHS program-integrity page | **RESOLVED (2026-08-30).** |
| CMS 5 December 2025 correspondence recommending/demanding corrective action | January 6 letter and both CAPs reference it | Existence and function now multiply primary-corroborated; the December 5 document itself is still not fetched. |
| Focused CMS-64 review workpapers for the 14 high-risk services | Described by CMS | Not public. |
| Full 25 February 2026 deferral letter on cms.gov | DocumentCloud copy + CMS press release | Still not fetched from a primary host. |
| **December 17, 2025 DHS-to-CMS reply** | December 31 CAP says “as we stated in our December 17 reply to your letter” | Not fetched; existence/date confirmed by DHS. |
| **January 21-22, 2026 in-person CMS-DHS meetings** | January 30 revised CAP | No minutes, agenda, or readout captured. |

---

## 3. USDA OIG — Minnesota-specific CACFP/SFSP / Feeding Our Future

No Minnesota-specific USDA OIG audit of Feeding Our Future, MDE CACFP/SFSP administration, or a Minnesota sponsor was located. National FNS improper-payment material is context only. FOF dollar allegations therefore remain grounded in DOJ charging/dispositions and OLA 2024, not a USDA OIG questioned-cost audit.

---

## 4. GAO — Minnesota-specific

No GAO audit of Minnesota Medicaid, CCAP, or Feeding Our Future was located. National improper-payment products remain context only.

---

## 5. OLA — Great Start, CCAP, Medicaid-waiver work

| Topic | Result |
|---|---|
| OLA audit of Great Start Compensation Support Payment Program | **Not found.** DCYF annual legislative reports are agency self-reports. |
| OLA CCAP audit 2024–2026 | **Not found.** 2019 special reviews remain the last OLA CCAP products located. |
| OLA Medicaid waiver / HSS / ICS / EIDBI performance audit | **Not found** in this pass. |
| Full BHA 2026 PDF close-read of dollar overpayments | PDF already downloaded; exact Finding 5 overpayment dollars still need structured extraction. |

---

## 6. Statutes — 2026 enacted session-law text

**2026-08-31 update:** The official Revisor session-law sources have now been pinned in the corpus:

- `src-mn-laws-2026-ch127-medical-assistance-fraud` — 2026 Minn. Laws ch. 127, controlling enacted text for the new Medical Assistance fraud framework while permanent-statutes recodification is incomplete.
- `src-mn-laws-2026-ch121-medicaid-program-integrity` — 2026 Minn. Laws ch. 121, primary enacted source for the identified amendments affecting § 256B.064.

This **closes the primary-source retrieval gap**. A narrower editorial task remains: map each provision to its exact article/section/effective-date pin cite and, once published, reconcile against the final 2026 Minnesota Statutes numbering. Do not invent permanent section numbers before that reconciliation.

---

## 7. Precedent

| Item | Status |
|---|---|
| *Kousisis* bound-volume citation | Slip opinion and 605 U.S. page-proof confirmed; final bound-volume reconciliation remains. |
| *Escobar* / *Sabri* / *Fischer* (2000) PDFs | Official Supreme Court URLs indexed; one fetch path was rate-limited. |
| *Cairns* 8th Cir. PDF | CA8 URL has shown instability; preserve official URL plus mirror provenance. |
| *SuperValu* | Official Supreme Court source identified; retain primary-source citation. |

---

## 8. Hearings — transcripts and oath status

| Hearing | Gap |
|---|---|
| U.S. House Oversight Part II, **4 March 2026** (Walz, Ellison) | Hearing page and majority materials exist. **Official GPO/committee transcript still not retrieved.** Do not convert press-release characterizations into transcript quotes. |
| U.S. House Oversight Part I, **7 January 2026** | Transcript not retrieved. |
| Minnesota House Fraud Prevention & Agency Oversight Committee | Individual hearing transcripts/oath logs not inventoried. |
| LAC 6 January 2026 BHA grants | Minutes retrieved; full video/transcript not retrieved. |

---

## 9. MFCU / criminal case primary dispositions

AG and USAO press releases are indexed, but underlying indictments, complaints, plea agreements, sentencing judgments, restitution orders, and state-court records are not yet comprehensively normalized across the Medicaid case families. For any dollar figure presented as proven loss or restitution, the disposition document should outrank the press release.

The **August 27, 2026 USAO Feeding Our Future sentencing release** is also a freshness signal: sentencing/disposition data are still changing and the public/canonical case-state layer needs a recurring reconciliation against new DOJ releases and underlying judgments.

---

## 10. Proposition D (official criminality)

No primary-source indictment, information, or conviction of a Minnesota statewide elected official or DHS/MDE commissioner for stealing program funds was found in this pass. Legislative allegations, audit integrity concerns, administrative findings, charged conduct, convictions, and proven restitution must remain separate evidence classes.

---

## 11. Items not to treat as primary

Wikipedia; commercial case summaries/headnotes; law-firm alerts; advocacy/blog commentary; journalism-derived spending denominators; DocumentCloud copies where an issuing-agency original has not been retrieved. These can be leads or corroboration, not substitutes for the best available primary record.

---

## 12. Current priority retrieval queue — 31 August 2026

1. **Disposition freshness:** ingest the August 27, 2026 FOF sentencing update and reconcile every current FOF defendant against judgment/restitution/sentencing status.
2. **CMS chain:** retrieve the March 19, 2026 CAP-approval letter, December 5, 2025 CMS correspondence, December 17 DHS reply, and February 25 deferral letter from issuing-government hosts where possible.
3. **$9B provenance:** obtain the December 18, 2025 USAO news-conference video/transcript and, if obtainable, the underlying CMS 14-service claims extract/methodology.
4. **Medicaid criminal dispositions:** normalize PACER/state-court charging instruments, plea agreements, judgments, restitution, and forfeiture for lead EIDBI/HSS/ICS/MFCU cases.
5. **Hearings:** retrieve official March 4 and January 7 House Oversight transcripts and inventory Minnesota legislative hearing records.
6. **2026 law pin cites:** extract exact article/section/effective-date cites from chapters 127 and 121 and later reconcile to final 2026 Statutes numbering.
7. **Audit horizon:** check OLA, HHS OIG, USDA OIG, and GAO for newly released Minnesota-specific work; absence must remain explicitly recorded rather than inferred away.

---

*End of GAPS.md. Gaps are retrieval failures or true absences as of the stated reconciliation date, not invitations to invent citations.*
