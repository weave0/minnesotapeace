# Congressional testimony on Minnesota fraud — primary transcript harvest

**As of:** 2026-08-29  
**Scope:** official GPO transcripts for U.S. House Oversight Part I (Jan. 7, 2026) and Part II (Mar. 4, 2026).  
**Publication state:** research only.

## 1. The prior transcript/oath gap is closed

Official Government Publishing Office records are now available for both 2026 House Oversight hearings:

- **Part I**, Jan. 7, 2026, Serial No. 119-54 — `src-gpo-2026-01-07-mn-fraud-hearing-part-i`
- **Part II**, Mar. 4, 2026, Serial No. 119-59 — `src-gpo-2026-03-04-mn-fraud-hearing-part-ii`

Both transcripts affirmatively establish that the witnesses were sworn under Committee Rule 9(g).

Part I witnesses: Kristin Robbins, Walter Hudson, Marion Rarick, Brendan Ballou.  
Part II witnesses: Gov. Tim Walz, Attorney General Keith Ellison, Rev. Mariah Furness Tollgaard.

This means statements can now be classified as `SWORN_TESTIMONY` where appropriate rather than relying on committee press releases or assuming oath status.

**But sworn does not mean independently proven.** A transcript proves what the witness said under oath. It does not convert every factual premise, opinion, accusation, estimate, or inference into an audit finding or adjudicated fact.

## 2. What Walz actually testified about knowledge

### Personal awareness

Asked for the date he first became aware of Feeding Our Future fraud, Walz said he could not give a specific date. He testified that **by late 2020** the administration began seeing irregularities being flagged.

Corpus treatment: `SWORN_TESTIMONY`, partially corroborated at the agency level by OLA's independent record that MDE had longstanding complaints and that MDE officials said concerns were shared with USDA OIG in October or November 2020.

That does **not** independently establish the date Walz personally learned a particular allegation.

### May 2020 agency awareness

Asked whether his administration was aware of Feeding Our Future fraud concerns by May 2020, Walz said he believed that was correct **with the agency, the Department of Education, and USDA**.

He then distinguished agency handling from personal notice, saying he personally was not necessarily notified of every allegation.

This is a materially stronger source than saying merely that the Committee alleged early awareness. It is also narrower than saying Walz admitted personal knowledge in May 2020.

### Chief of staff

A member stated that the Committee had sworn testimony that Walz's former chief of staff was notified directly by commissioners. Walz responded that this **could be correct**, but said he did not recall whether the chief of staff notified him at that time.

Current status: unresolved. The member's premise and Walz's qualified response are not enough to establish a precise notice chain. The relevant transcribed interview and contemporaneous communications should be acquired before publishing a definitive `commissioner -> chief of staff -> governor` timeline.

## 3. What Walz testified about early controls

When asked about 2019 action on child-care fraud, Walz said his administration lowered the proof standard for **administrative fraud disqualification** because he believed the prior evidentiary standard was too difficult to satisfy.

This exchange is especially vulnerable to misleading clipping. It should **not** be rendered as “Walz lowered fraud standards” without the explanation that he said the change lowered the proof threshold needed to impose an administrative fraud disqualification.

Next legal step: bind this testimony to the relevant 2019 statute/rule/agency-policy change before publishing it as a legal-history fact.

## 4. Ellison's authority and enforcement claims

Ellison testified that his office **does not have authority to order a stop-payment** and that it prosecutes Medicaid-fraud matters presented by the responsible agency.

Treat this as sworn legal-position testimony pending a statutory crosswalk of:

- Attorney General criminal jurisdiction;
- MFCU authority;
- DHS payment-withhold/suspension authority;
- county-attorney referral requirements.

Ellison also testified that his office had obtained **300 Medicaid-fraud convictions** and recovered **more than $80 million**.

Do not add those figures to current MFCU statistics. HHS-OIG's July 2026 recertification letter quotes different, dated windows: 36 FY2025 fraud convictions, 115 over three years, and >$24M FY2025 monetary recoveries. Different periods and definitions make these reconciliation questions, not automatic contradictions.

## 5. Part I: strong allegations remain allegations

Part I contains much stronger interpretations of motive and knowledge.

### Robbins

Robbins testified that in her view Walz knew about fraud from the beginning of his administration because prosecutions, OLA work, and fraud coverage already existed when he took office.

That is a sworn inference about knowledge. Existing public warnings can corroborate the **context** but do not by themselves prove personal knowledge of a specific scheme.

### Hudson

Hudson agreed with a committee member's characterization that political incentives created a motive to overlook or cover up fraud.

That is expressly opinion/inference. The official transcript proves Hudson gave the opinion under oath; it does not establish a criminal or political cover-up as fact.

### Rarick

Rarick testified that whistleblowers described retaliation, blacklisting, threats, surveillance-related concerns, and intimidation, and later stated that the administration retaliated against and dismissed whistleblowers.

These are serious sworn allegations. Current corpus treatment: `SWORN_TESTIMONY_ALLEGATION`, unresolved unless personnel records, investigative findings, judicial records, or other independent evidence substantiate the specific acts and responsible actors.

Walz later denied that whistleblowers should be retaliated against, said Minnesota has whistleblower protections, and said he could not speak to the specific allegations raised in Part II. The hearings therefore contain competing sworn accounts, not a resolved factual finding.

## 6. The $9 billion number did not become stronger because Congress repeated it

Part I repeatedly discussed approximately $9 billion as Minnesota Medicaid fraud. Robbins attributed the estimate to the U.S. Attorney's view that roughly half of high-risk Medicaid spending could be fraudulent.

The GPO transcript is a primary source for **the fact that witnesses and legislators repeated the estimate**. It is not a new measurement.

Nothing in the hearing changes the corpus classification:

- `$9B` remains `fraud_estimate` / investigative hypothesis;
- it is not an audit finding;
- it is not a restitution total;
- it is not a court-certified loss;
- House repetition is not independent corroboration.

## 7. A cleaner “who knew what, when” ladder

The combined primary record currently supports these distinctions:

1. **Public/program warning context:** fraud/control problems in Minnesota programs predated the Walz administration.
2. **MDE/agency-level FOF concerns:** OLA documents complaints beginning in 2018 and a reported USDA-OIG escalation in late 2020.
3. **Walz sworn testimony:** by late 2020 irregularities were being flagged; he could not give a specific personal-awareness date.
4. **Walz sworn testimony on agency awareness:** he said MDE/agency awareness by May 2020 was, in his words, believed correct.
5. **Chief-of-staff notice:** Walz said committee testimony that the chief of staff was notified “could be correct,” but he did not recall whether that notice reached him personally.
6. **Personal criminal participation:** no primary charging instrument currently in the corpus alleges Walz or Ellison joined a public-program fraud conspiracy.

These are six different propositions. The future site should not collapse them into either “officials knew nothing” or “officials were part of the fraud.”

## 8. Structured output

The detailed statement-by-statement treatment is stored at:

`research/oversight/congressional-testimony-matrix-2026.json`

Each item records:

- speaker and role;
- oath status;
- statement category;
- summary and locator;
- evidence class;
- corroboration status;
- corroborating source IDs where applicable;
- unresolved qualification.

## 9. Next acquisitions

1. Christopher Schmitter transcribed interview and any contemporaneous communications needed to resolve chief-of-staff notice.
2. Tony Lourey transcribed interview for 2019 DHS program-integrity discussions.
3. Emily Honer interview for MDE/USDA-OIG referral chronology.
4. Any personnel/investigative records independently substantiating or rejecting specific whistleblower-retaliation allegations.
5. Minnesota statutory/rule history behind the 2019 administrative-fraud-disqualification proof-standard change.
6. MFCU/AG statutory authority crosswalk for Ellison's stop-payment/jurisdiction testimony.

## Publication rule

A future “What officials said” page should present **statement + source + corroboration status**, not isolated clips. Questions asked by legislators, statements by witnesses, audit findings, court records, and derived conclusions must retain their separate evidence classes.
