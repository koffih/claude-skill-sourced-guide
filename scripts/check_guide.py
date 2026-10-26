#!/usr/bin/env python3
"""Floor check for sourced guide pages.

    check_guide.py guides/*.json --floor guides/floor.json [--json]

Reads files only (no network), so the answer is the same on every run.
Exit code 0 when every page passes, 1 when any check fails, 2 on bad usage.
"""
import argparse
import itertools
import json
import re
import sys
from pathlib import Path

DEFAULT_FLOOR = {
    "languages": ["en"],
    "min_words": 2500,
    "min_sections": 8,
    "min_sources": 15,
    "min_faq": 6,
    "meta_min": 130,
    "meta_max": 160,
    "title_max": 55,
    "allowed_kinds": ["law", "regulator", "government", "statistics",
                      "profession", "standard", "organisation"],
    "banned": ["—"],
    "max_shared_sentences": 3,
    "shared_sentence_min_words": 8,
}

MARKER = re.compile(r"\[s:([a-z0-9][a-z0-9._-]*)\]")
WORD = re.compile(r"[^\W\d_](?:[^\W_]|['’-])*", re.UNICODE)


def words(text):
    return len(WORD.findall(MARKER.sub(" ", text or "")))


def sentences(text):
    text = MARKER.sub("", text or "")
    text = re.sub(r"[*_#>`\[\]()]", " ", text)
    for s in re.split(r"(?<=[.!?])\s+|\n+", text):
        s = re.sub(r"\s+", " ", s).strip().lower()
        if s:
            yield s


def lang_texts(lang):
    yield lang.get("intro", "")
    for sec in lang.get("sections", []):
        yield sec.get("heading", "")
        yield sec.get("body", "")
    for qa in lang.get("faq", []):
        yield qa.get("q", "")
        yield qa.get("a", "")


def check_page(path, page, floor):
    errors = []
    err = errors.append
    sources = page.get("sources", [])
    ids = [s.get("id") for s in sources]
    if len(set(ids)) != len(ids):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        err(f"duplicate source ids: {', '.join(map(str, dup))}")
    if len(sources) < floor["min_sources"]:
        err(f"{len(sources)} sources, floor is {floor['min_sources']}")
    for s in sources:
        sid = s.get("id", "?")
        if s.get("kind") not in floor["allowed_kinds"]:
            err(f"source {sid}: kind {s.get('kind')!r} is not a primary kind")
        if not str(s.get("url", "")).startswith(("https://", "http://")):
            err(f"source {sid}: missing or bad url")
        for key in ("title", "publisher", "read"):
            if not s.get(key):
                err(f"source {sid}: missing {key}")

    cited = set()
    langs = page.get("languages", {})
    for code in floor["languages"]:
        lang = langs.get(code)
        if not lang:
            err(f"language {code} missing")
            continue
        for key in ("title", "seo_title", "meta_description", "excerpt", "intro"):
            if not str(lang.get(key, "")).strip():
                err(f"[{code}] {key} empty")
        meta = len(lang.get("meta_description", ""))
        if not floor["meta_min"] <= meta <= floor["meta_max"]:
            err(f"[{code}] meta_description is {meta} chars, want {floor['meta_min']} to {floor['meta_max']}")
        title = len(lang.get("seo_title", ""))
        if title > floor["title_max"]:
            err(f"[{code}] seo_title is {title} chars, limit {floor['title_max']}")
        secs = lang.get("sections", [])
        if len(secs) < floor["min_sections"]:
            err(f"[{code}] {len(secs)} sections, floor is {floor['min_sections']}")
        faq = lang.get("faq", [])
        if len(faq) < floor["min_faq"]:
            err(f"[{code}] {len(faq)} questions, floor is {floor['min_faq']}")
        texts = list(lang_texts(lang)) + [lang.get(k, "") for k in ("title", "seo_title", "meta_description", "excerpt")]
        n = sum(words(t) for t in lang_texts(lang))
        if n < floor["min_words"]:
            err(f"[{code}] {n} words, floor is {floor['min_words']}")
        blob = "\n".join(texts)
        low = blob.lower()
        for b in floor["banned"]:
            hit = blob.count(b) if not b.isalpha() and len(b) == 1 else low.count(b.lower())
            if hit:
                err(f"[{code}] banned {b!r} found {hit} time(s)")
        if MARKER.search(lang.get("meta_description", "") + lang.get("seo_title", "") + lang.get("excerpt", "")):
            err(f"[{code}] citation marker in title, meta or excerpt")
        for m in MARKER.findall(blob):
            cited.add(m)
            if m not in ids:
                err(f"[{code}] cites [s:{m}] which is not in sources")

    unused = [i for i in ids if i not in cited]
    if unused:
        err(f"sources listed but never cited: {', '.join(unused)}")

    facts = page.get("facts", {}) or {}
    flagged = {u.get("fact") for u in page.get("unverified", []) or []}
    for k, v in facts.items():
        if v is None and k not in flagged:
            err(f"fact {k} is null but not in unverified")
    for k in flagged:
        if k not in facts:
            err(f"unverified lists {k}, absent from facts")
    return errors


def shared_sentences(pages, floor):
    """Sentences repeated between two pages, outside sections marked shared."""
    sets = {}
    for path, page in pages:
        bag = set()
        for lang in page.get("languages", {}).values():
            parts = [lang.get("intro", "")] + [s.get("body", "") for s in lang.get("sections", []) if not s.get("shared")]
            parts += [qa.get("a", "") for qa in lang.get("faq", [])]
            for t in parts:
                for s in sentences(t):
                    if len(s.split()) >= floor["shared_sentence_min_words"]:
                        bag.add(s)
        sets[path] = bag
    problems = {}
    for a, b in itertools.combinations(sets, 2):
        common = sets[a] & sets[b]
        if len(common) > floor["max_shared_sentences"]:
            sample = next(iter(common))
            msg = f"{len(common)} sentences shared with {{other}}, e.g. \"{sample[:90]}\""
            problems.setdefault(a, []).append(msg.format(other=Path(b).name))
            problems.setdefault(b, []).append(msg.format(other=Path(a).name))
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--floor", help="floor.json (defaults built in)")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    args = ap.parse_args(argv)

    floor = dict(DEFAULT_FLOOR)
    if args.floor:
        floor.update(json.loads(Path(args.floor).read_text(encoding="utf-8")))

    pages, report = [], {}
    for f in args.files:
        p = Path(f)
        if p.name.startswith("_") or p.name == "floor.json":
            continue
        try:
            page = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            report[str(p)] = [f"unreadable: {e}"]
            continue
        pages.append((str(p), page))
        report[str(p)] = check_page(p, page, floor)
    for path, msgs in shared_sentences(pages, floor).items():
        report[path].extend(msgs)

    if not report:
        print("no guide files given", file=sys.stderr)
        return 2
    failed = {k: v for k, v in report.items() if v}
    if args.json:
        print(json.dumps({"pages": len(report), "failed": failed}, ensure_ascii=False, indent=2))
    else:
        for path, msgs in report.items():
            print(("FAIL " if msgs else "ok   ") + path)
            for m in msgs:
                print("     - " + m)
        print(f"\n{len(report) - len(failed)} of {len(report)} pages pass the floor")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
