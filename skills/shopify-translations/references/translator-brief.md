# Translator brief (any store)

Read this plus the store profile (`references/stores/<store>.md`) before translating a batch.
The store profile wins where they disagree.

## Input / output

Input `translations-work/batches/b0001.json`:

```json
{"batch_id": "b0001", "items": [{"uid": "…", "ctx": "product title", "locales": ["de","fr"],
  "text": "Swing dress with belt - Blue Tropical", "hint": {"Blue Tropical": {"de": "Blau Tropisch"}}}]}
```

Output `translations-work/out/b0001.json`, written once the whole batch is done:

```json
{"batch_id": "b0001", "items": {"<uid>": {"de": "…", "fr": "…"}}}
```

- Every uid, exactly the locales listed on that item. No extras.
- Valid UTF-8 JSON. No markdown fences, no commentary in the file.
- If `out/<batch_id>.json` already exists, the batch is done: skip it.
- Only write your own batch files. Parallel translators share nothing but `out/`.
- `hint` holds how the store already renders the part after " - " in titles (usually a
  colourway). Use it verbatim so new titles match the live catalogue.
- `ctx` says what the string is. Let it set register and length.

## HTML and placeholders (the most common failure)

- Keep every tag, attribute, `class`, `href`, `src`, `style` and entity (`&amp;`, `&nbsp;`)
  exactly, in order. Translate only visible text and human-readable attributes (`alt`,
  `title`, `placeholder`, `aria-label`).
- Inline tags (`<em>`, `<strong>`, `<b>`, `<i>`, `<span>`, `<a>`, `<br>`) appear the same number
  of times in the same order as the source. If the emphasis reads oddly, move it, keep the tag.
- Never touch anything inside `<script>` or `<style>`, JSON-LD included.
- Keep `{{ … }}`, `{% … %}`, `{ count }`, `%s`, `%{name}`, `[[…]]`, emoji and markdown markers verbatim.
- Keep leading/trailing whitespace and line breaks exactly.
- Rich-text JSON blobs: translate only `"value"` / `"text"` leaves and link `"title"`; keep every
  structural key and the original key order and escaping.
- Check tag sequences programmatically before writing; `validate.py` will block any mismatch.

## Numbers and codes

Values never change. Prices, size codes (XS/S/M/L/XL/XXL/OS), SKUs and dimensions stay verbatim.
Decimal separators in running prose localise for comma locales (DE/ES/FR/IT/PT/NL…):
`1.8 cm` → `1,8 cm`, `1.6 million` → `1,6 Millionen`.

## Length

- UI strings (buttons, labels, filters, navigation, option names) stay at or near source length.
- SEO fields match the source's length. Never summarise, never cut to a textbook limit; do not
  exceed the source by more than ~25%.

## Register defaults (override in the store profile)

- DE: Sie-form. ES: European Spanish, impersonal. FR: vous. IT: impersonal.
- No em-dashes or en-dashes in generated prose; use commas or colons.
- If a string is genuinely untranslatable (a code, a filename), return the source unchanged.
