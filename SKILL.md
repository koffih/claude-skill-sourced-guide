---
name: sourced-guide
description: "Write a series of long reference pages (one per trade, city, country, procedure, product type...) where every legal, health, money or number claim points to a primary source, in one or several languages, each page written by hand and never filled from a template, held by a floor check a machine can decide (words, sections, sources cited and listed, FAQ, meta lengths, banned typography). Covers the three-part research, the writing rules, a reusable data model, the floor checker, and running the series in parallel lanes. Use when asked for guide pages, trade or job pages, pages per city or country, a reference page that must cite its sources, or to scale one approved example page to all the others. French triggers (pages metiers, une page par metier, guides de reference, pages par ville ou par pays, guide sourcé, fiche metier, generaliser la page exemple a tous les metiers, pages de recrutement par metier, contenu de reference avec sources)."
argument-hint: "[series to write, e.g. 'trade pages for site X' | check <guide.json> | status]"
---

# Sourced guide: a series of reference pages that hold up

A reference page earns its place when a reader, a search engine or an answer engine can
trust each sentence that matters. This skill writes such pages **in series** (all the
trades, all the cities, all the procedures of a site) without the series turning into the
same text with the name changed.

**Request:** $ARGUMENTS

The method has five parts. Read the reference file of a part before doing that part.

| Part | What | Reference |
|---|---|---|
| 1. Frame | what one page is, who reads it, what it must never claim | this file |
| 2. Research | three parts, primary sources only, notes saved as you go | `references/research.md` |
| 3. Write | rules for the text, per language | `references/writing.md` |
| 4. Store and check | data model, floor checker | `references/data-model.md`, `scripts/check_guide.py` |
| 5. Scale | one approved example, then the rest in parallel lanes | `references/lanes.md` |

Paid-for traps are in `references/pitfalls.md`. Read it before part 5.

## 1. Frame the series before writing anything

Write `guides/SERIES.md` in the project (template: `assets/SERIES.md`) and get it right
with the user. It fixes, once for the whole series:

- **The item list**: every page of the series, with its slug per language. Take it from
  the project's own data (a taxonomy, a table, a config file), never from memory.
- **The reader and the action**: who lands on the page and what they should be able to do
  after reading it. One page, one main action.
- **What the site must never claim**: invented numbers, testimonials, partners, wages,
  approvals, a job that does not exist. If the site has a "we only publish what can be
  checked" promise, the guides are where it is most tested.
- **The jurisdictions**: countries or regions the pages cover. A rule that differs by
  country lives once per country, outside the pages (see the data model), not copied
  into each page.
- **The floor**: the numbers the checker enforces (`assets/floor.json`). Default: 2 500
  words per language, 8 sections, 15 sources, 6 questions, every language present. Raise
  it for health or legal topics, lower it only with a reason written in SERIES.md.
- **Structured data**: which schema.org types the page may carry. Never `JobPosting` on
  anything that is not a real open position, never `Review` or `AggregateRating` without
  real reviews. `FAQPage` and `Article` are safe.
- **Where the text goes**: files in the repository, rows written through an API, or both.

If the user gave one example page to imitate, read it fully and list what made it good:
that list becomes part of SERIES.md.

## 2. Research (summary, details in references/research.md)

Three parts for each item, done before a single sentence of the page:

1. **The rules**: law, decree, regulator, licence, card, registration, tax status. Read
   the official gazette, the regulator's site, the ministry. Never a law firm's blog.
2. **The practice**: what the work or the place really is, from professional bodies,
   official statistics, standards bodies, public training curricula.
3. **The reader's path**: the actual steps, forms, fees and delays, from the official
   service that runs them.

Every fact goes into `guides/research/<slug>.md` **as soon as it is found**, with its URL,
the exact quote, and the date read. A session can be cut at any time; research kept only
in context is lost with it.

A value that is contradictory between two primary sources, or that you could only read
second hand, is stored as `null` and shown as "not verified yet". It is never averaged,
rounded or guessed.

## 3. Write (summary, details in references/writing.md)

- Written for this item, by hand. If two pages of the series share a paragraph beyond the
  sign-up block, one of them is wrong.
- Every legal, health, money, delay or number claim carries a citation marker `[s:id]`
  that resolves to an entry of the page's source list. A source listed but never cited
  fails the check too: it is padding.
- No em dash, no filler phrases, no unverifiable superlatives. Each language written
  natively, not translated sentence by sentence.
- Meta description 130 to 160 characters, title under the site's limit, both measured
  after any template is filled.

## 4. Store and check

Each page is one file per item, `guides/<slug>.json`, in the shape of
`assets/guide.example.json`. Run the checker after every page and before any publish:

```bash
python3 ~/.claude/skills/sourced-guide/scripts/check_guide.py guides/*.json --floor guides/floor.json
```

It exits non-zero on any failure and prints each one. It needs no network and gives the
same answer every time, so it can be the project's test (see pitfalls). If the project
already has a test runner, wrap it there too.

## 5. Scale

1. Write **one** page end to end, publish it where the user can see it, and wait for the
   user's verdict. Fold every remark into SERIES.md and `writing.md` overrides before the
   second page.
2. Then the rest, one item per session, in up to three parallel lanes, each on its own
   clone, as described in `references/lanes.md`.
3. Publish between runs, never during one.

## Status and reporting

`/sourced-guide status` lists items done, in progress and left, from `guides/*.json` and
the checker's result. When reporting to the user: pages published (with links), pages
that failed the floor and why, every value left `null`, and every decision that waits
for them.
