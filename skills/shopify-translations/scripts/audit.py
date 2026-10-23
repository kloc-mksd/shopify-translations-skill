"""Find every untranslated (missing or outdated) field in the store.

  python audit.py                                   # everything, active products only
  python audit.py --types PRODUCT PRODUCT_OPTION PRODUCT_OPTION_VALUE \
      --product-query "status:active created_at:>=2026-10-16" --keys title product_type body_html name
  python audit.py --types COLLECTION --keys title --issue outdated

Writes translations-work/gaps.jsonl (one row per field x locale) and
translations-work/tm.json (current translations, used as translation memory).
"""
import argparse, collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shop
from textfilter import is_translatable

PRODUCT_TYPES = {"PRODUCT", "PRODUCT_OPTION", "PRODUCT_OPTION_VALUE", "MEDIA_IMAGE"}
# ONLINE_STORE_THEME already contains every key of these, auditing both double-counts
THEME_SUBTYPES = {"ONLINE_STORE_THEME_JSON_TEMPLATE", "ONLINE_STORE_THEME_SECTION_GROUP",
                  "ONLINE_STORE_THEME_LOCALE_CONTENT", "ONLINE_STORE_THEME_SETTINGS_CATEGORY",
                  "ONLINE_STORE_THEME_SETTINGS_DATA_SECTIONS"}
PLACEHOLDER_OPTIONS = {"Title", "Default Title"}   # single-variant products, never shown


def product_scope(query):
    """ids of matching products plus their options, option values and media"""
    q = '{ products%s { edges { node { id options { id optionValues { id } } media { edges { node { id } } } } } } }' % (
        '(query:%s)' % json.dumps(query) if query else '')
    ids = set()
    for r in shop.bulk(q):
        ids.add(r["id"])
        for o in r.get("options", []):
            ids.add(o["id"])
            ids.update(v["id"] for v in o["optionValues"])
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--types", nargs="*")
    ap.add_argument("--locales", nargs="*")
    ap.add_argument("--keys", nargs="*", help="only these translatable keys")
    ap.add_argument("--product-query", default="status:active",
                    help='Shopify product search for product-owned types; "" = all products')
    ap.add_argument("--issue", choices=["missing", "outdated", "both"], default="both")
    a = ap.parse_args()

    domain, locales, live = shop.shop_info()
    locales = a.locales or locales
    live_num = live["id"].rsplit("/", 1)[1]
    all_types = [e["name"] for e in shop.gql('{__type(name:"TranslatableResourceType"){enumValues{name}}}')["__type"]["enumValues"]]
    types = a.types or [t for t in all_types if t not in THEME_SUBTYPES]
    print(f"{domain} | locales {locales} | live theme {live['name']}", flush=True)

    scope = product_scope(a.product_query) if PRODUCT_TYPES & set(types) else set()
    if scope:
        print(f"product scope '{a.product_query}': {len(scope)} ids", flush=True)

    aliases = " ".join(f'{l.replace("-", "_")}: translations(locale:"{l}"){{key value outdated}}' for l in locales)
    gaps, tm, summary = [], collections.defaultdict(dict), collections.Counter()
    for t in types:
        q = f"{{ translatableResources(resourceType:{t}) {{ edges {{ node {{ resourceId translatableContent {{ key value digest type }} {aliases} }} }} }} }}"
        for r in shop.bulk(q):
            rid = r["resourceId"]
            if t.startswith("ONLINE_STORE_THEME") and live_num not in rid:
                continue
            # out-of-scope resources still feed translation memory, so new items reuse the catalogue
            in_scope = t not in PRODUCT_TYPES or rid in scope
            for c in r["translatableContent"]:
                src = c["value"] or ""
                if a.keys and c["key"] not in a.keys:
                    continue
                if t.startswith("PRODUCT_OPTION") and src in PLACEHOLDER_OPTIONS:
                    continue
                if not is_translatable(c["key"], src, c.get("type"))[0]:
                    continue
                for l in locales:
                    tr = {x["key"]: x for x in r[l.replace("-", "_")]}.get(c["key"])
                    if tr and tr["value"] and not tr["outdated"]:
                        tm[f"{c['key']}||{src}"][l] = tr["value"]
                        continue
                    if not in_scope:
                        continue
                    issue = "outdated" if tr and tr["value"] else "missing"
                    if a.issue not in ("both", issue):
                        continue
                    gaps.append({"type": t, "rid": rid, "key": c["key"], "locale": l, "issue": issue,
                                 "source": src, "current": tr["value"] if tr else None, "digest": c["digest"]})
                    summary[(t, issue)] += 1
        print(f"  {t}: {sum(v for k, v in summary.items() if k[0] == t)} gaps", flush=True)

    shop.write_jsonl(os.path.join(shop.WORK, "gaps.jsonl"), gaps)
    with open(os.path.join(shop.WORK, "tm.json"), "w", encoding="utf-8") as f:
        json.dump(tm, f, ensure_ascii=False)
    print(f"\n{len(gaps)} gaps on {len({g['rid'] for g in gaps})} resources -> {shop.WORK}")
    for (t, issue), n in sorted(summary.items()):
        print(f"  {t:40s} {issue:9s} {n}")


if __name__ == "__main__":
    main()
