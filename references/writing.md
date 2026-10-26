# Writing rules

## The page

- **Opening**: two or three sentences that say what the page covers and for whom. No
  "in this article", no "welcome".
- **Sections**: each has a heading that a reader would type or ask (a question or a
  plain noun phrase). Order follows the reader's path: what it is, the rules, the work,
  how to start, money, risks, how the site helps, questions.
- **Country or region parts**: one subsection per jurisdiction with a real difference.
  Do not repeat the same paragraph for each country; when the rule is the same, say it
  once and list the countries.
- **The site block**: written once for the series in SERIES.md, adapted to the item in
  one or two sentences, never more than one section.
- **FAQ**: real questions, short answers that stand alone (answer engines quote them
  without the page around them). Each answer that states a rule cites its source.

## Citations

- Marker `[s:id]` right after the claim it supports, before the full stop.
- One claim, at least one marker. A paragraph of three rules may need three markers.
- A `null` value is written as the site's "not verified yet" wording, never as a guess,
  and the item goes into `unverified` with what is missing.
- Dates of laws and figures appear in the text ("decree of 12 March 2014"), not only in
  the source list.

## Style

- Average sentence about 12 to 18 words, with real variation. Short sentences are fine.
- Concrete nouns, active verbs. Name the office, the document, the fee.
- **Banned in published text**: the em dash (use a colon, a comma or parentheses); filler
  such as "in essence", "it is worth noting", "the key is", "concrètement",
  "il est important de noter", "voici pourquoi", "en somme", "non négociable"; claims
  nobody can check ("the best", "the reference", "100 %", "leading").
- The en dash is allowed only as a range sign (2 500 to 3 000 is better still).
- No invented examples presented as real people, no testimonials, no wages or prices
  that the site itself would be committing to unless SERIES.md says it publishes them.
- Each language is written natively: French with French typography (space before « : ; ! ? »
  is the site's choice, keep it consistent), English in one spelling (British or American,
  as SERIES.md says).

## Metadata

- `seo_title`: under the limit in SERIES.md once the site suffix is added (often 55).
- `meta_description`: 130 to 160 characters, a full sentence that says what the reader
  will learn, measured as published.
- `excerpt`: one or two sentences for listing cards.

## Overrides

When the user corrects a page, write the rule here under `## Project overrides` in the
project copy of this file (or in SERIES.md), so every later page follows it.
