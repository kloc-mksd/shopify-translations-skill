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
