# Feeding Our Future — structured case family

Normalized 2026-08-26 (America/Chicago) from local markdown and primary files under `feeding-our-future/`. Journalism is a lead only. Do not invent numbers. Do not sum overlapping dollars. Do not treat `$250 million` as `proven_loss`. Do not upgrade defendant status from news. The circulating `$9 billion` figure is **not** a record in this family.

Source markdown: `feeding-our-future/SOURCES.md`, `CLAIMS.md`, `DEFENDANTS.md`, `GAPS.md`.

## Files

| File | Contents |
|---|---|
| `family.json` | Investigation-family record (`family_id`: `feeding-our-future`) |
| `sources.json` | S01–S31 primary/official + L01–L05 news leads; SHA-256 of local `primary/` bytes |
| `claims.json` | `fof-c-001` … atomic claims with required fields |
| `defendants.json` | Named defendants from `DEFENDANTS.md` (status from primaries only) |
| `money.json` | Typed amounts; Nur/Farah `$47,920,514` is `MAY_OVERLAP` |
| `contradictions.json` | Guthmann, conviction-count, OLA vs MDE, scheme-size, juror-bribery term |
| `events.json` | Chronology events citing sources |

Collection files wrap schema-shaped records in `{ family_id, generated_at, …, <records> }`. `family.json` is a single investigation-family object.

## Local primary hashes (sha256sum)

| Path | sha256 |
|---|---|
| `feeding-our-future/primary/ola-2024-mdefof.pdf` | `dc5b7d9db66dff4b4febc7d50664ffd11a4617d47233b3d28e9da68393d50ef6` (120 pp.) |
| `feeding-our-future/primary/ola-2024-mdefof-sum.pdf` | `c1350704297e181027365fb626e3824134edf8d7d93adc6f2cfa9d1bd67f41d4` (2 pp.) |
| `feeding-our-future/primary/bock-said-order-acquittal-2025-08-22.pdf` | `353114cc4a7d71befa9330c44eb7440cefefe083517f828bff15aa7c4b484dcf` (31 pp.) |
| `feeding-our-future/primary/mncourts-guthmann-2022-09-23.html` | `3632472c01ebf9c1fd01afd6984e02b2357c06e709c2f230f0ab0df09c6f8da2` |
| `feeding-our-future/primary/ola-2024-mdefof.txt` | `7e200e2c892a357fc98b6c8c83d8e12b30647fd94d6e58adf9fff52004c2eeb2` (extracted text of the full OLA report) |

## Operating rules encoded here

- **A ≠ B ≠ C ≠ D.** Private fraud (A) is extensively charged/adjudicated. OLA supports oversight failure (B) and unprepared/inadequate investigations (C). No charging document in this corpus names MDE officials as criminal defendants (D).
- **Indictment ≠ conviction.** Rows marked `charged` stay allegations until a captured primary says otherwise.
- **68 convictions = `LEAD_UNVERIFIED`.** Last verified official count is **65 on 2026-04-09** (S11).
- **Guthmann.** Judicial Branch 2022-09-23: Judge Guthmann never ordered MDE to resume payments; MDE resumed voluntarily. Contrary Walz/Star Tribune/commissioner statements are preserved as a contradiction, not overwritten.
- **Money.** `$47,920,514` appears for both Abdimajid Mohamed Nur and Abdiaziz Shafii Farah — `MAY_OVERLAP`, likely joint-and-several; **do not add**. `$250 million` is `alleged_loss` / charging headline, not `proven_loss`. **No `$9 billion` in this family.**

## OLA passage binding

OLA claims (`fof-c-010`, `fof-c-018`–`fof-c-022`) bind supporting passages to printed pages **S-1, 37, 49–51, 53, 55, 57** of `ola-2024-mdefof.pdf` (and the two-page summary).
