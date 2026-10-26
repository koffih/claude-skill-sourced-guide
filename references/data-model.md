# Data model

One file per item: `guides/<slug>.json`. The shape is the contract between the writer,
the checker and whatever publishes the page. Full example: `assets/guide.example.json`.

```json
{
  "slug": "real-estate-agent",
  "series": "trades",
  "updated": "2026-10-26",
  "slugs": { "fr": "agent-immobilier", "en": "real-estate-agent" },
  "languages": {
    "fr": {
      "title": "...",
      "seo_title": "...",
      "meta_description": "...",
      "excerpt": "...",
      "intro": "...",
      "sections": [ { "id": "regles", "heading": "...", "body": "markdown with [s:id] markers" } ],
      "faq": [ { "q": "...", "a": "..." } ]
    },
    "en": { "...": "same keys" }
  },
  "facts": { "tg_licence_required": true, "sn_guarantee_amount": null },
  "unverified": [ { "fact": "sn_guarantee_amount", "why": "decree text not found on the official portal" } ],
  "sources": [
    {
      "id": "sn-decree-2014-agents",
      "kind": "law",
      "jurisdiction": "SN",
      "title": "...",
      "publisher": "...",
      "url": "https://...",
      "read": "2026-10-26",
      "note": ""
    }
  ]
}
```

## Rules

- `sources` is shared by all languages of the page: the same law is cited in French and
  English with the same id.
- `kind` is one of: `law`, `regulator`, `government`, `statistics`, `profession`,
  `standard`, `organisation`. Anything else fails the check (secondary sources do not
  belong here).
- `facts` holds the values that matter and could change (amounts, delays, yes or no
  rules). `null` means not verified; the text must then say so. Keeping them as data lets
  a later pass re-check them without rereading prose.
- Section `body` is Markdown. The publisher converts it to the site's format (HTML,
  rich text) and turns `[s:id]` into a numbered link to the source list at the bottom.
  Never publish the raw markers.
- Rules that are the same for every item of the series in one jurisdiction (labour law,
  company registration, tax) live once in `guides/_jurisdictions.json`, keyed by country
  code, with their own sources. A page cites them by the same ids.

## Floor file

`guides/floor.json` (template `assets/floor.json`):

```json
{
  "languages": ["fr", "en"],
  "min_words": 2500,
  "min_sections": 8,
  "min_sources": 15,
  "min_faq": 6,
  "meta_min": 130, "meta_max": 160,
  "title_max": 55,
  "allowed_kinds": ["law", "regulator", "government", "statistics", "profession", "standard", "organisation"],
  "banned": ["—", "in essence", "it is worth noting", "concrètement", "il est important de noter", "voici pourquoi", "non négociable"],
  "max_shared_sentences": 3
}
```

`max_shared_sentences` is checked across all files given together: more than that many
identical sentences (outside the site block, marked `"shared": true` on its section)
between two pages fails both. It is the machine form of "never the same text with the
name changed".
