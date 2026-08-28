# GAPS.md — What was searched and not confirmed as a primary source

**Compiled:** 26 August 2026.  
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

## 2. CMS documents not retrieved from cms.gov HTML

| Missing item | Lead | Status |
|---|---|---|
| Administrator Oz **6 January 2026** letter to Gov. Walz (cms.gov / HHS original PDF) | Reproduced inside a CMS “notice of opportunity for hearing” circulating as CMS-FILE_6607 | Text used from that reproduction and from the State’s 30 Jan CAP, which answers the letter. **Need Federal Register citation** for the § 1904 hearing notice. |
| CMS letter **approving** the revised CAP (state says **19 March 2026**) | https://mn.gov/dhs/program-integrity/factcheck/ | State claim only; CMS original not fetched |
| 31 December 2025 first CAP PDF | Referenced as deficient | Not fetched |
| CMS 5 December 2025 correspondence recommending moratoria | Cited in 30 Jan CAP | Not fetched |
| Focused CMS-64 review workpapers for the 14 high-risk services | Described in 6 Jan letter | Not public |
| Full 25 February 2026 deferral letter on cms.gov | DocumentCloud https://s3.documentcloud.org/documents/27420090/cms-medicaid-deferral-letter-q4-2025.pdf plus CMS press release | Letter appears genuine CMS stationery; still a third-party host |

---

## 3. USDA OIG — Minnesota-specific CACFP/SFSP / Feeding Our Future

**Searched:** oig.usda.gov, usda.gov OIG/GAO-IG reports, FNS research library, general web.

**Not found:** A USDA OIG audit titled Feeding Our Future, Minnesota CACFP sponsor, or MDE administration of CACFP/SFSP.

National FNS improper-payment / meal-claim feasibility studies exist and are not Minnesota-primary.

**Implication:** FOF dollar allegations in this corpus rest on **DOJ charging** and **OLA 2024**, not on a USDA OIG questioned-cost report.

---

## 4. GAO — Minnesota-specific

**Not found:** A GAO audit of Minnesota Medicaid, CCAP, or Feeding Our Future.

National improper-payment products (GAO-26-108694, GAO-25-107770, GAO-25-108172) are indexed in `AUDITS.md` as context only.

---

## 5. OLA — Great Start Compensation Support Payment Program; recent CCAP

| Topic | Result |
|---|---|
| OLA audit of Great Start Compensation Support Payment Program (Minn. Stat. § 142D.21 / former 119B.27) | **Not found** (2023–2026 OLA report lists / search). DCYF annual legislative reports exist (agency self-reports). |
| OLA CCAP audit 2024–2026 | **Not found.** 2019 special reviews are the last OLA CCAP products located. April 2025 OLA evaluation-topic paper declined a new CCAP evaluation because of DHS→DCYF transfer. |
| OLA Medicaid waiver / HSS / ICS / EIDBI performance audit | **Not found** as of this pass. High-risk Medicaid work in 2025–26 is CMS CAP / USAO / DHS OIG, not OLA. |
| Full BHA 2026 PDF close-read of dollar overpayments | PDF downloaded (`pdfs/ola-fad2601-bha-grants.pdf`); HTML findings list used. Exact overpayment dollars for Finding 5 not extracted into this markdown. |

---

## 6. Statutes — 2026 MAP Act newly coded section numbers

2026 Minn. Laws ch. 127 repeals § 609.466 and “proposes coding for new law in … 609.” The Revisor display on 26 August 2026 still showed 2025 Statutes text plus repeal banners.

**Gap:** pin-cite of the **new** Medical Assistance fraud offense subdivisions (false enrollment, record destruction, $100k / $1M tiers) as they will appear in the 2026 Minnesota Statutes pamphlet. Use ch. 127 article text until Revisor recodifies.

256B.064 and 256B.04 were **amended by 2026 ch. 121** (not fully merged on the Revisor page). New subds. 2a–2g, 6, 8 of 256B.064 need session-law text for post-effective-date citation.

---

## 7. Precedent — bound U.S. Reports page for *Kousisis*; *Cairns* CA8 PDF stability

| Item | Status |
|---|---|
| *Kousisis* bound-volume citation | Slip opinion and 605 U.S. page-proof PDF confirmed. Some commercial reporters give **605 U.S. 114 (2025)**; this corpus cites **605 U.S. ___ (2025) (No. 23-909)** until the bound volume is final. |
| *Escobar* / *Sabri* / *Fischer* (2000) PDFs | Official supremecourt.gov URLs indexed; *Escobar* PDF returned 429 to one fetch tool; URL is the standard 15-7 slip path. |
| *Cairns* 8th Cir. PDF at ecf.ca8.uscourts.gov | WebFetch succeeded; subsequent curl 404. Cite CA8 URL + Justia PDF mirror. |
| *SuperValu* 21-1326 PDF | Official URL https://www.supremecourt.gov/opinions/22pdf/21-1326_6jfl.pdf indexed; curl of that exact filename was not re-tried after an earlier 404 in a chained download. 598 U.S. page-proof PDF https://www.supremecourt.gov/opinions/22pdf/598us2r30_g2bh.pdf was fetched via search. |

---

## 8. Hearings — transcripts and oath status

| Hearing | Gap |
|---|---|
| U.S. House Oversight Part II, **4 March 2026** (Walz, Ellison) | Hearing page and majority wrap-up exist. **Official GPO/committee transcript not retrieved.** Sworn status assumed from House practice, not confirmed from the record. Minority witness testimony (Rev. Mariah Tollgaard) not read. |
| U.S. House Oversight Part I, **7 January 2026** | Announced in later Comer release; transcript not retrieved. |
| Minnesota House Fraud Prevention & Agency Oversight Committee (2025–26, ~24 hearings) | Final report PDFs located; **individual hearing transcripts / oath logs not inventoried.** |
| LAC 6 January 2026 BHA grants | Minutes retrieved; full video/transcript not retrieved. |

Without transcripts, do not quote Walz/Ellison “admissions” from majority press releases as if they were the hearing record.

---

## 9. MFCU charging documents vs. press releases

AG and USAO **press releases** are indexed. Underlying **indictments, complaints, plea agreements, and judgments** (PACER / Minnesota state district court) were **not** bulk-downloaded.

For any dollar figure used as proven loss, the next research step is the judgment/plea — not the PR.

HHS OIG MFCU annual statistical reports after FY 2022 were not individually pulled beyond the AG’s own FY2025-window slides.

---

## 10. Proposition D (official criminality)

**No primary-source indictment, information, or conviction of a Minnesota statewide elected official or DHS/MDE commissioner for stealing program funds was found in this pass.**

House Oversight majority staff report (4 Mar 2026) **alleges** knowledge, delay, and whistleblower retaliation. That is `LEGISLATIVE_FINDING_OR_ALLEGATION`, not **D**.

OLA LAC minutes allege BHA staff **backdated or created documents after the audit began**. That is an auditor integrity concern; it is not a criminal disposition.

---

## 11. Items searched and confirmed *not* to be treated as primary

- Wikipedia, Justia case *summaries* (opinions themselves are primary; headnotes are not)
- Law-firm client alerts on *Kousisis*
- Georgetown CCF blog on PERM / CMS “weaponizing fraud” (useful critique; not a primary CMS document)
- KARE 11 $20.83 billion spending table (journalism + data-practices; useful denominator update, not a fraud total)

---

## 12. Suggested next retrievals (priority)

1. USAO 18 Dec 2025 news-conference video/transcript (C-SPAN, local TV pool, FOIA).
2. Federal Register notice of CMS § 1904 hearing; cms.gov PDF of 6 Jan 2026 Oz letter and 19 Mar 2026 CAP-approval letter.
3. 2026 Minn. Laws ch. 127 and ch. 121 full article text for recodified 609 and 256B.064 cites.
4. PACER docket sheet for lead EIDBI / HSS / ICS / FOF cases (charged loss vs. restitution).
5. USDA OIG FOIA or report search under MDE / Feeding Our Future / CACFP Minnesota.
6. House Oversight official transcript 4 Mar 2026.
7. OLA work plan 2026 for any forthcoming Medicaid-waiver audit.

---

*End of GAPS.md. Gaps are retrieval failures or true absences as of 26 August 2026, not invitations to invent citations.*
