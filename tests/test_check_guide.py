import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_guide as cg  # noqa: E402

EXAMPLE = json.loads((ROOT / "assets" / "guide.example.json").read_text(encoding="utf-8"))
LOOSE = dict(cg.DEFAULT_FLOOR, languages=["en"], min_words=20, min_sections=2,
             min_sources=2, min_faq=1)


def check(page, floor=LOOSE):
    return cg.check_page("x.json", page, floor)


class CheckPage(unittest.TestCase):
    def test_example_passes_loose_floor(self):
        self.assertEqual(check(EXAMPLE), [])

    def test_example_fails_default_floor(self):
        self.assertTrue(check(EXAMPLE, cg.DEFAULT_FLOOR))

    def test_unknown_citation(self):
        p = copy.deepcopy(EXAMPLE)
        p["languages"]["en"]["sections"][0]["body"] += " [s:nope]"
        self.assertTrue(any("s:nope" in e for e in check(p)))

    def test_uncited_source(self):
        p = copy.deepcopy(EXAMPLE)
        p["sources"].append(dict(p["sources"][0], id="extra"))
        self.assertTrue(any("never cited" in e for e in check(p)))

    def test_secondary_kind_rejected(self):
        p = copy.deepcopy(EXAMPLE)
        p["sources"][0]["kind"] = "blog"
        self.assertTrue(any("primary" in e for e in check(p)))

    def test_em_dash_rejected(self):
        p = copy.deepcopy(EXAMPLE)
        p["languages"]["en"]["intro"] += " A — B."
        self.assertTrue(any("banned" in e for e in check(p)))

    def test_null_fact_must_be_flagged(self):
        p = copy.deepcopy(EXAMPLE)
        p["unverified"] = []
        self.assertTrue(any("null" in e for e in check(p)))

    def test_meta_length(self):
        p = copy.deepcopy(EXAMPLE)
        p["languages"]["en"]["meta_description"] = "Too short."
        self.assertTrue(any("meta_description" in e for e in check(p)))

    def test_missing_language(self):
        self.assertTrue(any("language fr missing" in e
                            for e in check(EXAMPLE, dict(LOOSE, languages=["en", "fr"]))))


class Shared(unittest.TestCase):
    def test_copied_text_between_pages_fails(self):
        a = copy.deepcopy(EXAMPLE)
        body = " ".join(f"Sentence number {i} is long enough to be counted by the rule." for i in range(5))
        a["languages"]["en"]["sections"][0]["body"] = body
        b = copy.deepcopy(a)
        probs = cg.shared_sentences([("a.json", a), ("b.json", b)], LOOSE)
        self.assertIn("a.json", probs)

    def test_shared_section_is_ignored(self):
        a = copy.deepcopy(EXAMPLE)
        a["languages"]["en"]["sections"][1]["body"] = " ".join(
            f"Shared sign up sentence {i} that every page repeats on purpose." for i in range(6))
        b = copy.deepcopy(a)
        b["languages"]["en"]["intro"] = "Different intro for the second page."
        b["languages"]["en"]["faq"][0]["a"] = "Another answer."
        b["languages"]["en"]["sections"][0]["body"] = "Other body."
        self.assertEqual(cg.shared_sentences([("a.json", a), ("b.json", b)], LOOSE), {})


if __name__ == "__main__":
    unittest.main()
