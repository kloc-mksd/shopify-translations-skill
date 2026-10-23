"""QA translator output before anything is pushed.

  python validate.py --protect "I was a Sari" "B Corp"

Fatal per (uid, locale), blocked from push: missing output, HTML tag sequence
changed, Liquid/placeholders changed, protected term lost, digits that don't
match the source (a sign the output belongs to a different item), SEO field
trimmed to under 70% of the source. Writes translations-work/validation.json.
Exit code 1 while anything is blocked.
"""
import argparse, collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shop

TAG_RE = re.compile(r"<\s*(/?)\s*([a-zA-Z][a-zA-Z0-9-]*)")
PH_RE = re.compile(r"(\{\{.*?\}\}|\{%.*?%\}|\{[a-zA-Z_][a-zA-Z0-9_]*\}|%\{[^}]+\}|%[sd])")


def tags(s):
    return [(m.group(1), m.group(2).lower()) for m in TAG_RE.finditer(s)]


def digits_off(src, out):
    """True when the digit runs differ by more than a small slack (1.8 vs 1,8 count as equal)."""
    strip = lambda s: collections.Counter(re.findall(r"\d+", re.sub(r"<[^>]+>", " ", s)))
    ds, do = strip(src), strip(out)
    gone = ds - do
    if "3/4" in src:                                  # "3/4 sleeves" may be written out
        k = min(gone["3"], gone["4"]); gone["3"] -= k; gone["4"] -= k
    for y in [y for y in gone if re.fullmatch(r"(19|20)\d0", y)]:   # "1950s" -> "anni Cinquanta"
        del gone[y]
    lost, extra = sum(v for v in gone.values() if v > 0), sum((do - ds).values())
    return lost + extra > max(2, 0.15 * sum(ds.values()))


def check(it, out, protect):
    """-> {locale: [reasons]} for one item"""
    s, bad = it["text"], collections.defaultdict(list)
    for l in it["locales"]:
        v = (out or {}).get(l)
        if not v or not str(v).strip():
            bad[l].append("missing output")
            continue
        if tags(v) != tags(s):
            bad[l].append("html tags differ")
        if sorted(PH_RE.findall(v)) != sorted(PH_RE.findall(s)):
            bad[l].append("placeholders differ")
        bad[l] += [f"lost '{t}'" for t in protect if t in s and t not in v]   # case-sensitive on purpose
        if digits_off(s, v):
            bad[l].append("digits differ from source")
        if "SEO" in it["ctx"] and len(s) > 120 and len(v) < len(s) * 0.7:
            bad[l].append("SEO field trimmed")
    return {l: r for l, r in bad.items() if r}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--protect", nargs="*", default=[], help="terms that must survive verbatim")
    a = ap.parse_args()
    W = shop.WORK
    items = {}
    for p in glob.glob(os.path.join(W, "batches", "*.json")):
        for it in json.load(open(p, encoding="utf-8"))["items"]:
            items[it["uid"]] = it | {"batch": os.path.basename(p)[:-5]}
    got = {}
    for p in glob.glob(os.path.join(W, "out", "*.json")):
        try:
            got.update(json.load(open(p, encoding="utf-8"))["items"])
        except (ValueError, KeyError) as e:
            print(f"unreadable {os.path.basename(p)}: {e}")

    blocked, counts = [], collections.Counter()
    for uid, it in items.items():
        for l, why in check(it, got.get(uid), a.protect).items():
            blocked.append({"uid": uid, "loc": l, "batch": it["batch"], "why": why, "src": it["text"][:100]})
            counts.update(why)
    with open(os.path.join(W, "validation.json"), "w", encoding="utf-8") as f:
        json.dump({"blocked": blocked}, f, ensure_ascii=False, indent=1)
    print(f"items {len(items)} | blocked (uid,locale) {len(blocked)} | {dict(counts)}")
    for b in blocked[:15]:
        print(f"  {b['batch']} {b['uid']} {b['loc']}: {'; '.join(b['why'])} | {b['src']!r}")
    bad = sorted({b["batch"] for b in blocked})
    print("batches to redo:", ", ".join(bad) or "none")
    return 1 if blocked else 0


if __name__ == "__main__":
    it = {"text": "<p>Pink Floral, <em>1.8 cm</em>, I was a Sari</p>", "ctx": "product title", "locales": ["de"]}
    assert check(it, {"de": "<p>Floral rosa, <em>1,8 cm</em>, I was a Sari</p>"}, ["I was a Sari"]) == {}
    assert check(it, {"de": "<p>Floral rosa, 45 cm, I was a sari</p>"}, ["I was a Sari"])["de"] == [
        "html tags differ", "lost 'I was a Sari'", "digits differ from source"]
    sys.exit(main())
