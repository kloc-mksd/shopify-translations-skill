"""Turn translations-work/gaps.jsonl into translation batches.

Identical source strings are translated once. Strings whose translation already
exists elsewhere in the store (tm.json) are filled from it and never reach a
translator. For titles shaped "Name - Variant" the store's existing rendering of
the variant (e.g. a colourway) is attached as a hint, so new titles follow the
catalogue convention.

  python batch.py [--max-chars 6000] [--max-items 40]

Writes translations-work/units.jsonl, batches/b####.json, out/tm.json.
"""
import argparse, collections, glob, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shop

KEY_CTX = {"title": "title", "body_html": "rich-text description (HTML)", "summary_html": "short summary (HTML)",
           "product_type": "category name", "meta_title": "SEO page title",
           "meta_description": "SEO meta description", "label": "UI label", "name": "name / option label",
           "alt": "image alt text", "body": "rich-text body (HTML)", "value": "field value"}


def ctx_for(t, key):
    leaf = key.split(":")[0].split(".")[-1]
    if t.startswith("ONLINE_STORE_THEME"):
        return "storefront UI string (theme)"
    if t in ("MENU", "LINK"):
        return "navigation label"
    if t == "FILTER":
        return "storefront filter label"
    if t == "PRODUCT_OPTION":
        return "product option name (e.g. Size)"
    if t == "PRODUCT_OPTION_VALUE":
        return "product option value (e.g. a size or colour)"
    return t.lower().replace("_", " ") + " " + KEY_CTX.get(leaf, leaf)


def suffix_hints(tm):
    """'Blue Floral' -> {locale: most common rendering} learned from live title translations"""
    votes = collections.defaultdict(collections.Counter)
    for k, tr in tm.items():
        key, src = k.split("||", 1)
        if key != "title" or " - " not in src:
            continue
        suf = src.rsplit(" - ", 1)[1].strip()
        for l, v in tr.items():
            if " - " in v:
                votes[(suf, l)][v.rsplit(" - ", 1)[1].strip()] += 1
    hints = collections.defaultdict(dict)
    for (suf, l), c in votes.items():
        hints[suf][l] = c.most_common(1)[0][0]
    return hints


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-chars", type=int, default=6000)
    ap.add_argument("--max-items", type=int, default=40)
    a = ap.parse_args()
    W = shop.WORK
    for d in ("batches", "out"):
        os.makedirs(os.path.join(W, d), exist_ok=True)
        for p in glob.glob(os.path.join(W, d, "*.json")):
            os.remove(p)   # a fresh plan; stale batches would mismatch the new uids

    tm = json.load(open(os.path.join(W, "tm.json"), encoding="utf-8"))
    hints = suffix_hints(tm)
    units = {}
    for g in shop.read_jsonl(os.path.join(W, "gaps.jsonl")):
        ctx = ctx_for(g["type"], g["key"])
        uid = hashlib.md5(f"{ctx}||{g['source']}".encode()).hexdigest()[:16]
        u = units.setdefault(uid, {"uid": uid, "ctx": ctx, "key": g["key"], "text": g["source"], "locales": [], "occ": []})
        if g["locale"] not in u["locales"]:
            u["locales"].append(g["locale"])
        u["occ"].append({"rid": g["rid"], "key": g["key"], "locale": g["locale"]})

    tm_out, todo = {}, []
    for u in units.values():
        hit = tm.get(f"{u['key']}||{u['text']}", {})
        if all(hit.get(l) for l in u["locales"]):
            tm_out[u["uid"]] = {l: hit[l] for l in u["locales"]}
        else:
            todo.append(u)
    shop.write_jsonl(os.path.join(W, "units.jsonl"), list(units.values()))
    with open(os.path.join(W, "out", "tm.json"), "w", encoding="utf-8") as f:
        json.dump({"batch_id": "tm", "items": tm_out}, f, ensure_ascii=False)

    todo.sort(key=lambda u: (u["ctx"], -len(u["text"])))
    batches, cur, chars = [], [], 0
    for u in todo:
        if cur and (chars + len(u["text"]) > a.max_chars or len(cur) >= a.max_items or u["ctx"] != cur[-1]["ctx"]):
            batches.append(cur)
            cur, chars = [], 0
        cur.append(u)
        chars += len(u["text"])
    if cur:
        batches.append(cur)
    for i, b in enumerate(batches, 1):
        items = []
        for u in b:
            it = {"uid": u["uid"], "ctx": u["ctx"], "locales": sorted(u["locales"]), "text": u["text"]}
            suf = u["text"].rsplit(" - ", 1)[1].strip() if u["key"] == "title" and " - " in u["text"] else None
            if suf in hints:
                it["hint"] = {suf: hints[suf]}
            items.append(it)
        with open(os.path.join(W, "batches", f"b{i:04d}.json"), "w", encoding="utf-8") as f:
            json.dump({"batch_id": f"b{i:04d}", "items": items}, f, ensure_ascii=False, indent=1)

    print(f"units {len(units)} | filled from store memory {len(tm_out)} | to translate {len(todo)} "
          f"({sum(len(u['text']) for u in todo):,} chars) in {len(batches)} batches")


if __name__ == "__main__":
    main()
