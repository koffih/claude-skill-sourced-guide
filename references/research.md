# Research: three parts, primary sources only

## What counts as a primary source

A primary source is the body that **makes, runs or measures** the thing:

| Kind | Examples |
|---|---|
| law | official gazette, national legal portal, the text of a law or decree, a court ruling |
| regulator | the authority that issues the licence, the card, the registration |
| government | ministry page, official procedure portal, tax administration |
| statistics | national statistics office, central bank, an international body's dataset (ILO, World Bank, WHO, UN-Habitat, ISO) |
| profession | the professional order, chamber or federation that the law names |
| standard | the standards body itself (ISO, national standards office) |
| organisation | the official site of the company, school or body being described, for facts about itself |

Not primary: blogs, law firm articles, news summaries, directories, Wikipedia, forums,
another site's guide, an AI answer. They can help you **find** the primary source; the
page cites the primary source, never them. If the only trace of a fact is secondary, the
value is `null`.

A PDF of a law hosted by a third party is acceptable when the official portal does not
publish it, if the text is the official text (gazette number and date visible). Cite it
with `kind: "law"` and say in `note` where it is hosted.

## Part 1: the rules

For each jurisdiction of the series:

- Is the activity regulated? By which text (number, date, article)?
- Who issues the right to practise (licence, card, registration, order membership)?
  Conditions: diploma, experience, guarantee, insurance, criminal record, nationality.
- Obligations while practising: mandate in writing, escrow account, register, fees
  display, anti money laundering duties, data protection.
- Penalties for practising without the right.
- Tax and social status options for an independent.

When nothing regulates the activity in a country, say so only if a primary source says
so or the official list of regulated professions omits it; otherwise `null`.

## Part 2: the practice

- What the work consists of, day to day, from the professional body or a public
  curriculum (national qualification framework, public training reference).
- Where the work is: market size, number of practitioners, prices or fee scales only
  from an official or professional-body source, with the year.
- Skills and tools that the official curricula name.

## Part 3: the reader's path

- The real steps to start, in order, with the office that handles each, the documents,
  the official fee and delay when published.
- The link to the official form or portal.
- Then, and only then, how the site helps (the sign-up block, written once per series).

## Working method

1. Search in the language of the jurisdiction first (French for most of West and Central
   Africa, Portuguese for Lusophone countries, Arabic or French in the Maghreb). Official
   portals are often in one language only.
2. Open the source itself. Never cite a page you did not open in this session.
3. Copy the **exact sentence** that carries the fact into the notes file, with the URL,
   the title, the publisher and today's date. A fact without its quote is not usable.
4. Write notes to `guides/research/<slug>.md` after each source, not at the end.
5. When two primary sources disagree, write both with their dates, keep the value `null`
   in the guide, and add it to the page's `unverified` list.
6. Stop the research when every planned section has its facts, not when the source count
   is reached. The floor is a minimum, not a goal.

## Notes file format

```markdown
# <slug>, research notes

## s:tg-law-2018  (law, Togo)
URL: https://...
Title: Loi n° ... relative à ...
Publisher: Journal officiel de la République togolaise
Read: 2026-10-26
Quote: « ... exact sentence ... »
Used for: licence conditions (section "Exercer au Togo")
```

The `## s:<id>` heading is the id the page will cite. Keep ids stable: short, lowercase,
jurisdiction first (`sn-decree-2014-agents`, `ilo-isco-3334`).
