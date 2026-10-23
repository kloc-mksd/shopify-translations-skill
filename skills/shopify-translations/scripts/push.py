"""Register translations on Shopify (translationsRegister).

  python push.py --dry-run          # show what would be written
  python push.py                    # write validated translations from out/*.json
  python push.py --resync [--skip-rids rids.txt]
      # outdated rows only: re-register the CURRENT translation against the new
      # source digest, for when the English was re-saved but the translation is
      # still right. Review the --dry-run table first.

Safety: right before writing, every resource is re-read. A field is skipped if
its English changed since the audit or someone translated it in the meantime.
Every write is appended to translations-work/pushed.jsonl with the previous
value, and already-pushed rows are skipped on re-run.
"""
import argparse, collections, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shop

PER_REQUEST = 20          # resources per mutation (aliased)
MAX_TRANSLATIONS = 250    # Shopify cap per request


def fresh_state(rids, locales):
    """rid -> {key: (source, digest, {locale: (value, outdated)})}"""
    aliases = " ".join(f'{l.replace("-", "_")}: translations(locale:"{l}"){{key value outdated}}' for l in locales)
    q = f"query($ids:[ID!]!){{ translatableResourcesByIds(first:50, resourceIds:$ids){{ nodes{{ resourceId translatableContent{{key value digest}} {aliases} }} }} }}"
    out = {}
    for i in range(0, len(rids), 50):
        for n in shop.gql(q, {"ids": rids[i:i + 50]})["translatableResourcesByIds"]["nodes"]:
            trs = {l: {t["key"]: (t["value"], t["outdated"]) for t in n[l.replace("-", "_")]} for l in locales}
            out[n["resourceId"]] = {c["key"]: (c["value"], c["digest"], {l: trs[l].get(c["key"]) for l in locales})
                                    for c in n["translatableContent"]}
    return out


def register(chunk):
    """chunk: [(rid, [TranslationInput])] -> (ok rids, [(rid, error)])"""
    defs, parts, v = [], [], {}
    for i, (rid, trs) in enumerate(chunk):
        defs.append(f"$id{i}: ID!, $t{i}: [TranslationInput!]!")
        parts.append(f"r{i}: translationsRegister(resourceId: $id{i}, translations: $t{i}) {{ userErrors {{ message }} }}")
        v[f"id{i}"], v[f"t{i}"] = rid, trs
    d = shop.gql(f"mutation({', '.join(defs)}) {{ {' '.join(parts)} }}", v)
    errs = [(rid, e["message"]) for i, (rid, _) in enumerate(chunk) for e in d[f"r{i}"]["userErrors"]]
    bad = {r for r, _ in errs}
    return [rid for rid, _ in chunk if rid not in bad], errs


def planned(a, W):
    """-> [(rid, key, locale, value, expected_source)]"""
    if a.resync:
        skip = set(open(a.skip_rids).read().split()) if a.skip_rids else set()
        return [(g["rid"], g["key"], g["locale"], g["current"], g["source"])
                for g in shop.read_jsonl(os.path.join(W, "gaps.jsonl"))
                if g["issue"] == "outdated" and g["rid"] not in skip]
    got = {}
    for p in glob.glob(os.path.join(W, "out", "*.json")):
        got.update(json.load(open(p, encoding="utf-8"))["items"])
    vpath = os.path.join(W, "validation.json")
    if not os.path.exists(vpath):
        sys.exit("run validate.py first")
    blocked = {(b["uid"], b["loc"]) for b in json.load(open(vpath, encoding="utf-8"))["blocked"]}
    rows = []
    for u in shop.read_jsonl(os.path.join(W, "units.jsonl")):
        for o in u["occ"]:
            val = (got.get(u["uid"]) or {}).get(o["locale"])
            if val and (u["uid"], o["locale"]) not in blocked:
                rows.append((o["rid"], o["key"], o["locale"], val, u["text"]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--resync", action="store_true")
    ap.add_argument("--skip-rids", help="file of resource ids to leave alone (resync)")
    a = ap.parse_args()
    W = shop.WORK
    log_path = os.path.join(W, "pushed.jsonl")
    done = {(r["rid"], r["key"], r["locale"]) for r in shop.read_jsonl(log_path)} if os.path.exists(log_path) else set()

    rows = [r for r in planned(a, W) if r[:3] not in done]
    locales = sorted({r[2] for r in rows})
    state = fresh_state(sorted({r[0] for r in rows}), locales) if rows else {}
    by_rid, stats, log = collections.defaultdict(list), collections.Counter(), {}
    for rid, key, loc, val, src in rows:
        cur = state.get(rid, {}).get(key)
        if not cur or cur[0] != src:
            stats["skipped: source changed since audit"] += 1
            continue
        old = cur[2].get(loc)
        if old and old[0] and not old[1] and not a.resync:
            stats["skipped: translated meanwhile"] += 1
            continue
        by_rid[rid].append({"key": key, "locale": loc, "value": val, "translatableContentDigest": cur[1]})
        log[(rid, key, loc)] = old[0] if old else None
    n = sum(len(v) for v in by_rid.values())
    print(f"to write: {n} translations on {len(by_rid)} resources | {dict(stats)} | already pushed: {len(done)}")

    if a.dry_run:
        for rid, trs in list(by_rid.items())[:25]:
            for t in trs[:8]:
                src = state[rid][t["key"]][0]
                print(f"  {rid.rsplit('/', 1)[1][:30]:30s} {t['key'][:18]:18s} {t['locale']}  {src[:40]!r} -> {t['value'][:60]!r}")
        return

    chunk, count, ok, errors = [], 0, 0, []
    with open(log_path, "a", encoding="utf-8") as logf:
        def flush():
            nonlocal ok
            good, errs = register(chunk)
            errors.extend(errs)
            for rid, trs in chunk:
                if rid in good:
                    ok += len(trs)
                    for t in trs:
                        logf.write(json.dumps({"rid": rid, "key": t["key"], "locale": t["locale"], "value": t["value"],
                                               "previous": log[(rid, t["key"], t["locale"])]}, ensure_ascii=False) + "\n")
            logf.flush()
        for rid, trs in by_rid.items():
            for i in range(0, len(trs), 100):          # max 100 translations per resource per call
                part = trs[i:i + 100]
                if chunk and (count + len(part) > MAX_TRANSLATIONS or len(chunk) >= PER_REQUEST):
                    flush()
                    chunk, count = [], 0
                chunk.append((rid, part))
                count += len(part)
        if chunk:
            flush()
    print(f"written {ok} | errors {len(errors)}")
    for rid, msg in errors[:20]:
        print(f"  {rid}: {msg}")


if __name__ == "__main__":
    main()
