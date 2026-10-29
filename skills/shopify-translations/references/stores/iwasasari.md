# Store profile: I was a Sari (shopiwasasari.myshopify.com)

Locales: de, es, fr, it (primary en). India store (shopiwasasari-india) is English only.

## Brand and voice
Mumbai-based social enterprise: discarded silk saris upcycled into clothing, accessories and
homeware by women artisans from underserved communities. Warm, editorial, craft-led, quietly
premium. Never salesy or corporate. Sustainability claims are factual, not breathless.

## Validate with
`python validate.py --protect "I was a Sari" "The Story Edit" "B Corp"`

## Never translate
`I was a Sari` (capital S, the brand), `IWAS`, `The Story Edit`, `The Journal`, `Sari`/`Saris`,
`B Corp`, `2nd Innings Handicrafts Pvt Ltd`, `Rivo`, `Klaviyo`, `Impact Points` (programme name,
e.g. "Earns 36 Impact Points"), people, cities, artisan names, collection code names
(`The Riviera Edit`), quoted press headlines.

Exception: the lowercase tagline `I was a sari, now I am` is wordplay and IS translated.

## Product titles: colourways ARE translated
About 80% of live titles translate the colourway after " - ", e.g. "Cesto portaoggetti trapuntato -
Paisley rosso", "Floreale blu". Use the batch `hint` when present. Without a hint, translate the
colourway with colour-noun agreement (ES `Floral rosa`, FR `Motif floral rose`, IT `Floreale rosa`).
The old SLICE_TASK rule "keep colourways English" is wrong for titles.

## Product SEO and Google Shopping title: fixed format, owned by Vincenzo

Vincenzo Cannata (feeds/SEO) set the rules on 18 Oct 2026 and checks every active product each
Monday. Anything not in his format gets rewritten, so never write these fields freehand:

| Field | Where | Max |
|---|---|---|
| Google Shopping title | product metafield `gmc.title` (all 7 Multifeeds feeds; IT/DE/FR feeds read its translation) | 150 |
| Meta title | product SEO "Page title" (translation key `meta_title`) | 60 |
| Meta description | product SEO "Meta description" (translation key `meta_description`) | 155 |

All three, in EN, IT, FR, DE and ES, come from `build(title, colour, pattern)` in
`iwas_title_rules.py` (next to this file; Vincenzo's module from his `iwas-product-text-check`
skill). Example from Vincenzo's live output, `Clutch bag - Yellow Floral`:

- gmc.title `Clutch Bag – Yellow Floral, Metal Frame, Chain Strap, Upcycled Sari, Handcrafted`
- meta title `Clutch Bag – Yellow Floral | Upcycled Sari | I was a Sari`
- meta description `Clutch Bag – Yellow Floral. Handmade in India by women artisans from upcycled saris. A bag with a sari's story, for every day.`

**Translation audits always skip them**, or the normal flow overwrites them with free translations:
`python audit.py ... --skip-fields PRODUCT.meta_title PRODUCT.meta_description --skip-metafields gmc.title`

Filling them for new products:
- Scope is the new products only (created since the last Monday check, or the ones the user
  names). For anything wider, or rewriting fields that are already filled on older products,
  stop: the user must tell Vincenzo first so the two runs don't overwrite each other. Never email
  the client; draft only if asked.
- Inputs: `title` = Shopify product title (never changed by this). `colour` = display name of
  `custom.product_color_3`, `pattern` = display name of `custom.product_pattern_2` (both metaobject
  references: query the metaobjects to map ids to names, don't hardcode ids).
- Empty `custom.product_color_3`: don't write anything and don't guess from photos or title. List
  the product for the IWAS team to set the colour.
- `build()` returns `None` for a family missing from the module (184 of the 343 products created
  18–28 Oct were missing from the 20 Oct copy, e.g. Clutch bag, Furoshiki wrap, "/ Do Good"
  variants). Don't improvise a title: report the families and ask for Vincenzo's current module.
  Replace this file with it; never edit the module yourself.
- Duplicated products arrive with the source product's three fields and translations. Always
  regenerate them, even when filled.
- Also set `gmc.color` and `gmc.color_it` from `gmc_colour(colour)`.
- Writes: `metafieldsSet` (gmc.title, gmc.color, gmc.color_it, max 25 per call), `productUpdate`
  `seo{title description}`, then `translationsRegister` for it/fr/de/es with
  `translatableContentDigest = digest(<current EN value>)`: keys `meta_title`/`meta_description`
  on the product, key `value` on the gmc.title Metafield gid (read the ids after metafieldsSet).
  Show a dry-run sample and get an explicit yes first, then re-read to verify.
- Other product fields (title, body_html, product_type, options, FAQs, alt texts) still go
  through the normal audit, batch, translate, push flow.

## Glossary
| EN | DE | ES | FR | IT |
|---|---|---|---|---|
| Sari | Sari | Sari | Sari | Sari |
| Kaftan | Kaftan | Caftán | Caftan | Caftano |
| Shorts | Shorts | Pantalones cortos | Short | Pantaloncini |
| Jogger Pants | Jogginghose | Pantalones jogger | Pantalon de jogging | Pantaloni jogger |
| Scrunchie | Scrunchie | Coletero | Chouchou | Scrunchie |
| Scarf | Schal | Pañuelo | Foulard | Foulard |
| Kimono | Kimono | Kimono | Kimono | Kimono |
| Tote bag | Tote Bag | Bolso tote | Tote bag | Borsa tote |
| Pouch | Etui | Estuche | Pochette | Pochette |
| Cushion cover | Kissenbezug | Funda de cojín | Housse de coussin | Federa per cuscino |
| Bandana | Bandana | Bandana | Bandana | Bandana |
| Robe | Robe | Bata | Peignoir | Vestaglia |
| Top | Top | Top | Top | Top |
| Dress | Kleid | Vestido | Robe | Vestito |
| Jacket | Jacke | Chaqueta | Veste | Giacca |
| Upcycled | Upcycelt | Reciclado creativo (upcycling) | Upcyclé | Riciclato creativo (upcycling) |
| Handmade | Handgefertigt | Hecho a mano | Fait main | Fatto a mano |
| One of a kind | Unikat | Pieza única | Pièce unique | Pezzo unico |
| Limited edition | Limitierte Auflage | Edición limitada | Édition limitée | Edizione limitata |
| Sold out | Ausverkauft | Agotado | Épuisé | Esaurito |
| Add to bag | In den Warenkorb | Añadir a la bolsa | Ajouter au panier | Aggiungi al carrello |
| Shop now | Jetzt shoppen | Comprar ahora | Acheter | Acquista ora |
| Filter & Sort | Filtern & Sortieren | Filtrar y ordenar | Filtrer et trier | Filtra e ordina |
| Share | Teilen | Compartir | Partager | Condividi |
| Print | Print | Estampado | Imprimé | Fantasia |
| Mood | Stimmung | Estilo | Ambiance | Mood |

## Scope notes
- "Feed products" for Google Shopping (Vincenzo) = ACTIVE + some UNLISTED products that are only on
  the Online Store channel. Default audit scope is `status:active`; ask before widening to UNLISTED.
- ~42 main-nav category collections are invisible to `collections()` but are returned by
  `translatableResources`, so the audit covers them.
- Theme setting `size_filter_label` is string-compared in Liquid and must stay English (textfilter
  already skips it).
- Some English descriptions contain leftover placeholder text (e.g. "All material details from the
  original, preserved verbatim."). Flag those to the user instead of translating them.
- Outdated main-nav collection titles (Clothing, Bags, Jewelry…) were still correct on 2026-10-23:
  the English was re-saved, not changed. Use `push.py --resync` after reviewing.
