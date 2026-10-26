# sourced-guide

A [Claude Code](https://claude.com/claude-code) skill that writes a **series of long
reference pages** (one per trade, city, country, procedure...) where every legal, health,
money or number claim points to a primary source, and that keeps the series from turning
into the same text with the name changed.

Part of the [koffih skills catalog](https://github.com/koffih/claude-skills).

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/koffih/claude-skill-sourced-guide/main/install.sh | bash
```

Run it again to update. `--project` installs into `./.claude/skills`, `--uninstall`
removes it. Requirements: git and Python 3.8+ for the checker.

## Use

Ask in plain words ("write a guide page for each trade on the site, with sources") or run
`/sourced-guide <series>`. The skill:

1. frames the series with you in `guides/SERIES.md`: the item list from the project's own
   data, the reader, what the site must never claim, jurisdictions, the floor, allowed
   structured data;
2. researches each item in three parts (the rules, the practice, the reader's path) from
   primary sources only, saving every quote to disk as it goes;
3. writes each page by hand, per language, with `[s:id]` citation markers;
4. stores each page as `guides/<slug>.json` and checks it;
5. writes one example, waits for your verdict, then scales to the rest, optionally in up
   to three parallel lanes with [`autonomous-relaunch`](https://github.com/koffih/claude-skill-autonomous-relaunch).

## The floor checker

```bash
python3 ~/.claude/skills/sourced-guide/scripts/check_guide.py guides/*.json --floor guides/floor.json
```

Files only, no network, same answer every time, so it can be a project's test. It fails a
page on:

| Check | Default |
|---|---|
| words per language | 2 500 |
| sections, FAQ questions | 8, 6 |
| sources, all of a primary kind (law, regulator, government, statistics, profession, standard, organisation) | 15 |
| a citation that resolves to no source, a source never cited | any |
| meta description length, title length | 130 to 160, 55 |
| banned typography and filler (em dash, "in essence", ...) | any |
| a `null` fact not listed as unverified | any |
| sentences shared with another page of the series, outside a section marked `shared` | more than 3 |

## Files

| Path | What |
|---|---|
| `SKILL.md` | the method |
| `references/research.md` | what counts as primary, the three parts, the notes format |
| `references/writing.md` | text rules, citations, metadata |
| `references/data-model.md` | page JSON, jurisdictions file, floor file |
| `references/lanes.md` | one example first, then parallel lanes, publishing |
| `references/pitfalls.md` | traps already paid for |
| `assets/` | `SERIES.md`, `floor.json`, `plan.lane.md`, `guide.example.json` |
| `scripts/check_guide.py` | the checker |
| `tests/` | `python3 -m unittest discover -s tests` |

## License

MIT
