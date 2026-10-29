---
name: shopify-translations
description: Find and fix untranslated content in a Shopify store's native translations (the ones Translate & Adapt shows). Audits every translatable resource type (products, options, collections, theme, pages, articles, menus, metaobjects, image alts, policies…) for missing or outdated translations per locale, filters by resource type, product status or creation date, then translates in validated batches and registers them via translationsRegister. Use when someone asks what is not translated, wants translation gaps or a translation audit, wants new products/collections/theme strings translated into store languages, sees "outdated" translations in Translate & Adapt, or reports a foreign-language storefront or Google Shopping feed showing English.
---

# Shopify translations: audit, translate, push

Scripts live in this skill's `scripts/` folder. Run them from the store's project folder: they
read `.env` there (`SHOPIFY_STORE`, `SHOPIFY_ACCESS_TOKEN` with read/write_translations,
read_products, read_themes, read_content, read_online_store_navigation, read_metaobjects) and
write everything to `./translations-work/`. Needs `pip install requests python-dotenv`.

## 1. Load the store profile

Read `references/translator-brief.md` and `references/stores/<store>.md` (match on the
myshopify domain). No profile for this store? Copy the iwasasari one's headings into a new file,
fill in what the user tells you (brand name, terms never to translate, register, glossary) and
keep the store-specific facts out of the generic brief.

Some fields have a fixed format owned by someone else (iwasasari: product SEO title/description
and the `gmc.title` Google feed title). Follow the profile's rules for them and pass its
`--skip-fields` / `--skip-metafields` to every audit so they are never translated freehand.

## 2. Audit

```bash
python scripts/audit.py                                   # all types, ACTIVE products only
python scripts/audit.py --types PRODUCT PRODUCT_OPTION PRODUCT_OPTION_VALUE \
  --product-query "status:active created_at:>=2026-10-16" --keys title product_type body_html name
python scripts/audit.py --types COLLECTION --keys title --issue outdated
```

`--product-query` takes Shopify product search syntax and scopes PRODUCT, PRODUCT_OPTION(_VALUE)
and MEDIA_IMAGE; `""` means all products. Defaults that keep the numbers honest: active products
only, live theme only, theme sub-types skipped (ONLINE_STORE_THEME already holds their keys),
handles, URLs, colours, numbers and "Default Title" options skipped.

Report the gaps as a table by resource type, issue and locale. **Missing** = no translation.
**Outdated** = the English was saved after the translation. Often the translation is still right
(step 6). Agree the scope with the user before translating anything.

## 3. Batch

```bash
python scripts/batch.py
```

Dedupes identical strings, fills from translations that already exist in the store, and adds
`hint`s so titles follow the catalogue's existing colourway rendering.

## 4. Translate

Translate every `translations-work/batches/b*.json` into `translations-work/out/<batch_id>.json`
following the translator brief and store profile. Up to ~10 batches: do them yourself. More:
split the batch ids into slices and give each slice to a parallel subagent, passing it the path
of both reference files and its own batch ids only. Agents must not share scratch folders.

## 5. Validate, then push

```bash
python scripts/validate.py --protect <terms from the store profile>
```

Anything blocked: delete that batch's out file, retranslate, re-run until 0 blocked. Then:

```bash
python scripts/push.py --dry-run
```

Show the user the counts and a sample. **This writes to the live store; get an explicit yes**,
then run `python scripts/push.py`. It re-reads each resource first and skips fields whose
English changed or that someone translated in the meantime; it resumes safely if re-run.

## 6. Outdated but still correct

When the English was only re-saved (e.g. collection titles), re-register the existing
translation against the new digest instead of retranslating:

```bash
python scripts/audit.py --types COLLECTION --issue outdated
python scripts/push.py --resync --dry-run
```

Check each English/translation pair yourself. Put resource ids whose translation no longer
matches the English into a file and pass `--skip-rids that_file.txt`. Retranslate those with
steps 3 to 5. After the user says yes, run `python scripts/push.py --resync`.

## 7. Verify

Re-run the same audit command. The scope should come back with 0 gaps (or only the ones you
deliberately skipped). Report what was written per resource type and locale.

`translations-work/pushed.jsonl` records every write with its previous value. To roll back, re-register
`previous`, or remove the translation where `previous` is null.
