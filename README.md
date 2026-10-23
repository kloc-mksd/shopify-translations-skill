# shopify-translations (Claude Code skill)

Finds every untranslated or outdated field in a Shopify store's native translations, filters by
resource type (products, collections, theme, pages…), translates in validated batches and pushes
with `translationsRegister`.

## Install

In Claude Code:

```
/plugin marketplace add kloc-mksd/shopify-translations-skill
/plugin install shopify-translations@kloc-shopify
```

Then, inside the store's project folder (needs a `.env` with `SHOPIFY_STORE` and
`SHOPIFY_ACCESS_TOKEN`, and `pip install requests python-dotenv`), ask e.g.
"what's untranslated on the store?" or "translate the products created this week".

Store-specific rules live in `skills/shopify-translations/references/stores/`.
