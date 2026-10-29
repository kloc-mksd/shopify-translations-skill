import re,hashlib

def F(names,extra=None,base=True): return dict(n=names.split('|'),x=extra.split('|') if extra else None,b=base)
L=('en','it','fr','de','es')
BASE=dict(en='Upcycled Sari, Handcrafted',it='sari riciclato, artigianale',fr='sari recyclé, fait main',de='aus recyceltem Sari, handgefertigt',es='sari reciclado, artesanal')
COL={'Red':('Red','rosso','rouge','Rot','rojo'),'Yellow':('Yellow','giallo','jaune','Gelb','amarillo'),'Blue':('Blue','blu','bleu','Blau','azul'),
'Pink':('Pink','rosa','rose','Rosa','rosa'),'Beige':('Beige','beige','beige','Beige','beige'),'Green':('Green','verde','vert','Grün','verde'),
'Grey':('Grey','grigio','gris','Grau','gris'),'White':('White','bianco','blanc','Weiß','blanco'),'Brown':('Brown','marrone','marron','Braun','marrón'),
'Orange':('Orange','arancione','orange','Orange','naranja'),'Black':('Black','nero','noir','Schwarz','negro'),'Purple':('Purple','viola','violet','Lila','morado'),
'Multicolor':('Multicolor','multicolore','multicolore','Mehrfarbig','multicolor')}
PAT={'Tropical':('Tropical','Tropicale','Tropical','Tropisch','Tropical'),'Paisley':('Paisley',)*5,
'Floral':('Floral','Floreale','Floral','Blumenmuster','Floral'),'Abstract':('Abstract','Astratto','Abstrait','Abstrakt','Abstracto'),
'Micro Design':('Micro Design','Micro disegno','Micro-motif','Mikrodesign','Microdiseño'),'Leaves':('Leaves','Foglie','Feuilles','Blätter','Hojas'),'Organic':('Organic','Organico','Organique','Organisch','Orgánico'),'Ikat':('Ikat',)*5,'Eclectic':('Eclectic','Eclettico','Éclectique','Eklektisch','Ecléctico'),'Heritage':('Heritage',)*5,
'Geometric':('Geometric','Geometrico','Géométrique','Geometrisch','Geométrico'),'Indian Ethnic':('Indian Ethnic','Etnico indiano','Ethnique indien','Indisch-ethnisch','Étnico indio')}
FAM={
'a line skirt with slit':F('A-Line Skirt with Slit|Gonna svasata con spacco|Jupe trapèze fendue|A-Linien-Rock mit Schlitz|Falda acampanada con abertura'),
'a6 hard cover notebook':F('A6 Hard Cover Notebook|Taccuino A6 con copertina rigida|Carnet A6 à couverture rigide|A6-Notizbuch mit Hardcover|Cuaderno A6 de tapa dura','Pre-Loved Sari Cover, 100% Recycled Paper, Handcrafted|copertina in sari usato, carta 100% riciclata, artigianale|couverture en sari de seconde main, papier 100 % recyclé, fait main|Einband aus Second-Hand-Sari, 100 % Recyclingpapier, handgefertigt|tapa de sari de segunda mano, papel 100% reciclado, artesanal',False),
'angel christmas ornament':F('Angel Christmas Ornament|Decorazione natalizia angelo|Ornement de Noël ange|Weihnachtsanhänger Engel|Adorno navideño de ángel'),
'beach bag':F('Beach Bag|Borsa mare|Sac de plage|Strandtasche|Bolso de playa'),
'bomber jacket':F('Bomber Jacket|Giacca bomber|Blouson bomber|Bomberjacke|Chaqueta bomber','Cropped Fit|taglio corto|coupe courte|kurz geschnitten|corte cropped'),
'bow earrings':F('Bow Earrings|Orecchini a fiocco|Boucles d\'oreilles nœud|Schleifen-Ohrringe|Pendientes de lazo','Lead-Free, Nickel Safe|senza piombo, senza nichel|sans plomb, sans nickel|bleifrei, nickelfrei|sin plomo, sin níquel',False),
'bronze be kind bomber jacket':F('Bronze Be Kind Bomber Jacket|Giacca bomber Be Kind bronzo|Blouson bomber Be Kind bronze|Bomberjacke Be Kind Bronze|Chaqueta bomber Be Kind bronce'),
'gold be kind bomber jacket':F('Gold Be Kind Bomber Jacket|Giacca bomber Be Kind oro|Blouson bomber Be Kind doré|Bomberjacke Be Kind Gold|Chaqueta bomber Be Kind dorada'),
'gold heart bomber jacket':F('Gold Heart Bomber Jacket|Giacca bomber Cuore oro|Blouson bomber Cœur doré|Bomberjacke Herz Gold|Chaqueta bomber Corazón dorado'),
'gold love bomber jacket':F('Gold Love Bomber Jacket|Giacca bomber Love oro|Blouson bomber Love doré|Bomberjacke Love Gold|Chaqueta bomber Love dorado'),
'pink heart bomber jacket':F('Pink Heart Bomber Jacket|Giacca bomber Cuore rosa|Blouson bomber Cœur rose|Bomberjacke Herz Rosa|Chaqueta bomber Corazón rosa'),
'pink love bomber jacket':F('Pink Love Bomber Jacket|Giacca bomber Love rosa|Blouson bomber Love rose|Bomberjacke Love Rosa|Chaqueta bomber Love rosa'),
'red heart bomber jacket':F('Red Heart Bomber Jacket|Giacca bomber Cuore rosso|Blouson bomber Cœur rouge|Bomberjacke Herz Rot|Chaqueta bomber Corazón rojo'),
'red love bomber jacket':F('Red Love Bomber Jacket|Giacca bomber Love rosso|Blouson bomber Love rouge|Bomberjacke Love Rot|Chaqueta bomber Love rojo'),
'cheer ornament gift box set':F('Cheer Ornament Gift Box Set|Set regalo di decorazioni Cheer|Coffret cadeau d\'ornements Cheer|Geschenkbox-Set Anhänger Cheer|Set de regalo de adornos Cheer'),
'sparkling ornament gift box set':F('Sparkling Ornament Gift Box Set|Set regalo di decorazioni Sparkling|Coffret cadeau d\'ornements Sparkling|Geschenkbox-Set Anhänger Sparkling|Set de regalo de adornos Sparkling'),
'timeless ornament gift box set':F('Timeless Ornament Gift Box Set|Set regalo di decorazioni Timeless|Coffret cadeau d\'ornements Timeless|Geschenkbox-Set Anhänger Timeless|Set de regalo de adornos Timeless'),
'cord bracelet with charm sun medallion':F('Cord Bracelet with Sun Medallion Charm|Bracciale in corda con ciondolo medaglione sole|Bracelet cordon avec breloque médaillon soleil|Kordelarmband mit Sonnenmedaillon-Anhänger|Pulsera de cordón con colgante medallón de sol','18K Gold Plated, Adjustable|placcato oro 18K, regolabile|plaqué or 18 carats, réglable|18 Karat vergoldet, verstellbar|chapado en oro de 18 K, ajustable',False),
'foulard':F('Foulard|Foulard|Foulard|Foulard-Tuch|Fular','Lightweight Square Scarf, 100 cm x 100 cm|foulard quadrato leggero, 100 cm x 100 cm|carré léger, 100 cm x 100 cm|leichtes quadratisches Tuch, 100 cm x 100 cm|pañuelo cuadrado ligero, 100 cm x 100 cm'),
'foulard keyring':F('Foulard Keyring|Portachiavi con foulard|Porte-clés foulard|Schlüsselanhänger mit Tuch|Llavero con pañuelo'),
'high low shirt':F('High-Low Shirt|Camicia asimmetrica high-low|Chemise asymétrique|High-Low-Hemd|Camisa asimétrica'),
'long shirt dress':F('Long Shirt Dress|Abito chemisier lungo|Robe chemise longue|Langes Hemdblusenkleid|Vestido camisero largo'),
'loop scarf':F('Loop Scarf|Sciarpa ad anello|Écharpe snood|Loop-Schal|Bufanda circular'),
'maxi romantic dress':F('Maxi Romantic Dress|Abito lungo romantico|Robe longue romantique|Romantisches Maxikleid|Vestido largo romántico'),
'maxi tiered dress':F('Maxi Tiered Dress|Abito lungo a balze|Robe longue à volants|Stufen-Maxikleid|Vestido largo de volantes','Adjustable Halter Neck|scollo all\'americana regolabile|col licou réglable|verstellbarer Neckholder|cuello halter ajustable'),
'midi tiered skirt':F('Midi Tiered Skirt|Gonna midi a balze|Jupe midi à volants|Stufen-Midirock|Falda midi de volantes'),
'neck scarf':F('Neck Scarf|Foulard da collo|Foulard de cou|Halstuch|Pañuelo de cuello'),
'night dress':F('Night Dress|Camicia da notte|Chemise de nuit|Nachthemd|Camisón','Lace Trim|bordo in pizzo|bordure en dentelle|mit Spitzenbesatz|ribete de encaje'),
'panta pareo':F('Panta Pareo Trousers|Pantaloni Pareo|Pantalon paréo|Pareo-Hose|Pantalón pareo'),
'pareo':F('Pareo|Pareo|Paréo|Pareo|Pareo','Lightweight Rectangular Wrap|copricostume rettangolare leggero|étole rectangulaire légère|leichtes rechteckiges Wickeltuch|pareo rectangular ligero'),
'pj set long':F('Long PJ Set|Set pigiama lungo|Pyjama long|Pyjama-Set lang|Pijama largo'),
'pj set long with long sleeves':F('Long Sleeve PJ Set|Set pigiama lungo a maniche lunghe|Pyjama long à manches longues|Langarm-Pyjama-Set|Pijama largo de manga larga','Two-Piece with Contrast Piping|due pezzi con profilo a contrasto|deux pièces avec passepoil contrasté|zweiteilig mit Kontrastpaspel|dos piezas con vivo en contraste'),
'pj set short':F('Short PJ Set|Set pigiama corto|Pyjashort|Kurz-Pyjama-Set|Pijama corto','Eyelash Lace Trim|bordo in pizzo a ciglia|bordure en dentelle cils|mit Wimpernspitze|ribete de encaje de pestañas'),
'plant pot cover set 2 pieces s, m':F('Plant Pot Cover Set of 2, S & M|Set di 2 copri-vaso, taglie S e M|Lot de 2 cache-pots, tailles S et M|Übertopf-Hüllen 2er-Set, Größen S und M|Set de 2 cubremacetas, tallas S y M','Waterproof Lining|fodera impermeabile|doublure imperméable|wasserdichtes Futter|forro impermeable'),
'playsuit with long sleeve':F('Long Sleeve Playsuit|Tutina a maniche lunghe|Combishort à manches longues|Langarm-Playsuit|Mono corto de manga larga'),
'quilted barrel bag':F('Quilted Barrel Bag|Borsa a bauletto trapuntata|Sac polochon matelassé|Gesteppte Barrel Bag|Bolso barril acolchado','Spacious Everyday Bag|borsa capiente da tutti i giorni|sac spacieux du quotidien|geräumige Alltagstasche|bolso amplio para el día a día'),
'quilted beach bag':F('Quilted Beach Bag|Borsa mare trapuntata|Sac de plage matelassé|Gesteppte Strandtasche|Bolso de playa acolchado','Lightweight & Spacious Tote|tote leggera e capiente|cabas léger et spacieux|leichte, geräumige Tote|tote ligero y amplio'),
'quilted bowling bag':F('Quilted Bowling Bag|Borsa bowling trapuntata|Sac bowling matelassé|Gesteppte Bowling-Tasche|Bolso bowling acolchado','Soft Quilted Finish|finitura trapuntata morbida|finition matelassée douce|weiche Steppung|acabado acolchado suave'),
'quilted carry-all bag':F('Quilted Carry-All Bag|Borsa capiente trapuntata|Sac fourre-tout matelassé|Gesteppte Allzwecktasche|Bolso multiusos acolchado'),
'quilted duffle bag':F('Quilted Duffle Bag|Borsone trapuntato|Sac de voyage matelassé|Gesteppte Reisetasche|Bolsa de viaje acolchada','Structured and Spacious|strutturato e capiente|structuré et spacieux|formstabil und geräumig|estructurada y amplia'),
'quilted large shoulder bag':F('Quilted Large Shoulder Bag|Borsa a spalla grande trapuntata|Grand sac porté épaule matelassé|Große gesteppte Schultertasche|Bolso de hombro grande acolchado'),
'quilted sling bag':F('Quilted Sling Bag|Borsa a tracolla trapuntata|Sac bandoulière matelassé|Gesteppte Sling Bag|Bolso bandolera acolchado'),
'quilted slippers':F('Quilted Slippers|Pantofole trapuntate|Chaussons matelassés|Gesteppte Hausschuhe|Zapatillas de casa acolchadas','Soft Fabric, Cushioned Sole|tessuto morbido, suola imbottita|tissu doux, semelle rembourrée|weicher Stoff, gepolsterte Sohle|tejido suave, suela acolchada'),
'quilted storage basket':F('Quilted Storage Basket|Cesto portaoggetti trapuntato|Panier de rangement matelassé|Gesteppter Aufbewahrungskorb|Cesta de almacenaje acolchada'),
'quilted sunglasses case':F('Quilted Sunglasses Case|Custodia per occhiali da sole trapuntata|Étui à lunettes de soleil matelassé|Gestepptes Sonnenbrillenetui|Funda acolchada para gafas de sol','Soft Padded Protection|protezione imbottita morbida|protection rembourrée douce|weich gepolstert|protección acolchada suave'),
'quilted utility pouch':F('Quilted Utility Pouch|Pochette utility trapuntata|Pochette utilitaire matelassée|Gesteppte Utility-Tasche|Neceser acolchado','Lightly Padded|leggermente imbottita|légèrement rembourrée|leicht gepolstert|ligeramente acolchado'),
'quilted work tote bag':F('Quilted Work Tote Bag|Borsa tote da lavoro trapuntata|Cabas de travail matelassé|Gesteppte Arbeits-Tote|Bolso tote de trabajo acolchado'),
'swing dress with detachable belt':F('Swing Dress with Detachable Belt|Abito swing con cintura removibile|Robe trapèze avec ceinture amovible|Swing-Kleid mit abnehmbarem Gürtel|Vestido swing con cinturón extraíble','Lightweight A-Line|linea ad A leggera|coupe trapèze légère|leichte A-Linie|línea A ligera'),
'swing dress':F('Swing Dress|Abito swing|Robe trapèze|Swing-Kleid|Vestido swing','Mini-Length A-Line|mini a trapezio|mini coupe trapèze|Mini in A-Linie|mini de línea A'),
'reusable bag':F('Reusable Bag|Borsa riutilizzabile|Sac réutilisable|Wiederverwendbare Tasche|Bolsa reutilizable','Lightweight Foldable Shopper|shopper leggera e pieghevole|cabas léger et pliable|leichter, faltbarer Shopper|shopper ligero y plegable'),
'shirt':F('Shirt|Camicia|Chemise|Hemd|Camisa'),
'short kimono robe':F('Short Kimono Robe|Vestaglia kimono corta|Kimono court|Kurzer Kimono-Morgenmantel|Bata kimono corta','Lightweight Wrap|leggera, a portafoglio|léger, croisé|leicht, zum Wickeln|ligera, cruzada'),
'short shirt dress':F('Short Shirt Dress|Abito chemisier corto|Robe chemise courte|Kurzes Hemdblusenkleid|Vestido camisero corto'),
'short tiered skirt':F('Short Tiered Skirt|Gonna corta a balze|Jupe courte à volants|Kurzer Stufenrock|Falda corta de volantes'),
'sleeveless blouse':F('Sleeveless Blouse|Blusa smanicata|Blouse sans manches|Ärmellose Bluse|Blusa sin mangas'),
'slip top':F('Slip Top|Top a sottoveste|Top caraco|Slip-Top|Top lencero'),
'stole':F('Stole|Stola|Étole|Stola|Estola','Rectangular Wrap|foulard rettangolare|foulard rectangulaire|rechteckiges Tuch|pañuelo rectangular'),
'sunset coat':F('Sunset Coat|Cappotto Sunset|Manteau Sunset|Sunset-Mantel|Abrigo Sunset','Below-Knee Wrap, Adjustable Fit|a portafoglio sotto il ginocchio, regolabile|portefeuille sous le genou, ajustable|Wickelschnitt, wadenlang, verstellbar|cruzado por debajo de la rodilla, ajustable'),
'thin hairband':F('Thin Hairband|Cerchietto sottile|Serre-tête fin|Schmaler Haarreif|Diadema fina'),
'timeless heart ornament':F('Timeless Heart Ornament|Decorazione a cuore Timeless|Ornement cœur Timeless|Herz-Anhänger Timeless|Adorno de corazón Timeless'),
'timeless star ornament':F('Timeless Star Ornament|Decorazione a stella Timeless|Ornement étoile Timeless|Stern-Anhänger Timeless|Adorno de estrella Timeless'),
'tunic set':F('Tunic Set|Completo tunica|Ensemble tunique|Tunika-Set|Conjunto de túnica','Wrap Top & Wide-Leg Pants|top a portafoglio e pantaloni a gamba larga|haut portefeuille et pantalon large|Wickeltop und weite Hose|top cruzado y pantalón ancho'),
'waistcoat':F('Waistcoat|Gilet|Gilet|Weste|Chaleco'),
'waistcoat set':F('Waistcoat Set|Completo con gilet|Ensemble gilet|Westen-Set|Conjunto con chaleco'),
'wide leg palazzo trousers':F('Wide-Leg Palazzo Trousers|Pantaloni palazzo a gamba larga|Pantalon palazzo large|Weite Palazzohose|Pantalón palazzo ancho'),
'wide leg pleated trouser':F('Wide-Leg Pleated Trousers|Pantaloni a gamba larga con pieghe|Pantalon large à pinces|Weite Bundfaltenhose|Pantalón ancho con pinzas'),
'work tote bag':F('Work Tote Bag|Borsa tote da lavoro|Cabas de travail|Arbeits-Tote|Bolso tote de trabajo','Reinforced Base|base rinforzata|base renforcée|verstärkter Boden|base reforzada'),
'wrap dress':F('Wrap Dress|Abito a portafoglio|Robe portefeuille|Wickelkleid|Vestido cruzado'),
}
ALIAS={'short shirt dres':'short shirt dress','i was a sari midi tiered upcycled skirt':'midi tiered skirt','i was a sari swing dress with detachable belt':'swing dress with detachable belt',
'red floral swing dress with detachable belt':'swing dress with detachable belt','swing dress with belt':'swing dress with detachable belt','swing dress with detachable tie belt':'swing dress with detachable belt'}
FAM2={
'a5 hard cover notebook':F('A5 Hard Cover Notebook|Taccuino A5 con copertina rigida|Carnet A5 à couverture rigide|A5-Notizbuch mit Hardcover|Cuaderno A5 de tapa dura','Upcycled Sari Cover, Handcrafted|copertina in sari riciclato, artigianale|couverture en sari recyclé, fait main|Einband aus recyceltem Sari, handgefertigt|tapa de sari reciclado, artesanal',False),
'angel christmas ornament set of 3':F('Angel Christmas Ornament Set of 3|Set di 3 decorazioni natalizie angelo|Lot de 3 ornements de Noël ange|Weihnachtsanhänger Engel, 3er-Set|Set de 3 adornos navideños de ángel'),
'assorted cheer ornaments set of 3':F('Cheer Ornament Set of 3, Assorted|Set di 3 decorazioni Cheer, assortite|Lot de 3 ornements Cheer, assortis|Anhänger Cheer, 3er-Set, sortiert|Set de 3 adornos Cheer, surtidos'),
'assorted crescent moon ornament set of 2':F('Crescent Moon Ornament Set of 2, Assorted|Set di 2 decorazioni a mezzaluna, assortite|Lot de 2 ornements croissant de lune, assortis|Halbmond-Anhänger, 2er-Set, sortiert|Set de 2 adornos de luna creciente, surtidos','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'assorted ornaments set of 2':F('Ornament Set of 2, Crescent Moon & Snowflake|Set di 2 decorazioni, mezzaluna e fiocco di neve|Lot de 2 ornements, croissant de lune et flocon|Anhänger-Set, Halbmond und Schneeflocke, 2 Stück|Set de 2 adornos, luna creciente y copo de nieve','Hand-Embroidered|ricamate a mano|brodés main|handbestickt|bordados a mano'),
'assorted timeless ornaments set of 2':F('Timeless Ornament Set of 2, Assorted|Set di 2 decorazioni Timeless, assortite|Lot de 2 ornements Timeless, assortis|Anhänger Timeless, 2er-Set, sortiert|Set de 2 adornos Timeless, surtidos'),
'assorted timeless ornaments set of 3':F('Timeless Ornament Set of 3, Assorted|Set di 3 decorazioni Timeless, assortite|Lot de 3 ornements Timeless, assortis|Anhänger Timeless, 3er-Set, sortiert|Set de 3 adornos Timeless, surtidos','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'bandana necklace with charm':F('Bandana Necklace with Charm|Collana bandana con ciondolo|Collier bandana avec breloque|Bandana-Halskette mit Anhänger|Collar bandana con colgante'),
'be kind tote bag':F('Be Kind Tote Bag|Borsa tote Be Kind|Cabas Be Kind|Tote Bag Be Kind|Bolso tote Be Kind'),
'beach robe':F('Beach Robe|Vestaglia da spiaggia|Robe de plage|Strandkleid zum Binden|Bata de playa','Full-Length with Tie Belt|lunga con cintura da annodare|longue avec ceinture à nouer|lang mit Bindegürtel|larga con cinturón anudado'),
'beaded drop earrings':F('Beaded Drop Earrings|Orecchini pendenti con perline|Boucles d\'oreilles pendantes perlées|Perlen-Hängeohrringe|Pendientes colgantes de cuentas','Recycled Cotton Rope, Nickel Safe|corda di cotone riciclato, senza nichel|corde en coton recyclé, sans nickel|recyceltes Baumwollseil, nickelfrei|cuerda de algodón reciclado, sin níquel'),
'bell sleeve coat':F('Bell Sleeve Coat|Cappotto con maniche a campana|Manteau à manches évasées|Mantel mit Glockenärmeln|Abrigo con mangas de campana','Lightweight|leggero|léger|leicht|ligero'),
'belt top':F('Belt Top|Top con cintura|Top à ceinture|Top mit Gürtel|Top con cinturón','Adjustable Tie Waist|vita regolabile con laccio|taille ajustable à nouer|verstellbare Bindetaille|cintura ajustable con lazo'),
'bookmark set of 3':F('Bookmark Set of 3|Set di 3 segnalibri|Lot de 3 marque-pages|Lesezeichen, 3er-Set|Set de 3 marcapáginas','Canvas Tassel|nappina in tela|pompon en toile|Quaste aus Canvas|borla de lona'),
'bowtie shirt':F('Bowtie Shirt|Camicia con fiocco|Chemise à nœud|Hemdbluse mit Schleife|Camisa con lazo','Long Sleeve, Relaxed Fit|manica lunga, vestibilità comoda|manches longues, coupe ample|langarm, lockere Passform|manga larga, corte holgado'),
'canvas placemat set of 4':F('Canvas Placemat Set of 4|Set di 4 tovagliette in tela|Lot de 4 sets de table en toile|Canvas-Tischsets, 4er-Set|Set de 4 manteles individuales de lona','Reversible, Washable|reversibili, lavabili|réversibles, lavables|wendbar, waschbar|reversibles, lavables'),
'cheer bell ornament':F('Cheer Bell Ornament|Decorazione a campana Cheer|Ornement cloche Cheer|Glocken-Anhänger Cheer|Adorno de campana Cheer','Aari Embroidery|ricamo Aari|broderie Aari|Aari-Stickerei|bordado Aari'),
'cheer crescent moon ornament':F('Cheer Crescent Moon Ornament|Decorazione a mezzaluna Cheer|Ornement croissant de lune Cheer|Halbmond-Anhänger Cheer|Adorno de luna creciente Cheer','Aari Embroidery|ricamo Aari|broderie Aari|Aari-Stickerei|bordado Aari'),
'cheer gift ornament':F('Cheer Gift Ornament|Decorazione a pacchetto regalo Cheer|Ornement paquet cadeau Cheer|Geschenk-Anhänger Cheer|Adorno de regalo Cheer','Aari Embroidery|ricamo Aari|broderie Aari|Aari-Stickerei|bordado Aari'),
'cheer heart ornament':F('Cheer Heart Ornament|Decorazione a cuore Cheer|Ornement cœur Cheer|Herz-Anhänger Cheer|Adorno de corazón Cheer','Aari Embroidery|ricamo Aari|broderie Aari|Aari-Stickerei|bordado Aari'),
'cheer mitten ornament':F('Cheer Mitten Ornament|Decorazione a muffola Cheer|Ornement moufle Cheer|Fäustling-Anhänger Cheer|Adorno de manopla Cheer','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'cheer snowflake ornament':F('Cheer Snowflake Ornament|Decorazione a fiocco di neve Cheer|Ornement flocon de neige Cheer|Schneeflocken-Anhänger Cheer|Adorno de copo de nieve Cheer','Aari Embroidery|ricamo Aari|broderie Aari|Aari-Stickerei|bordado Aari'),
'cheer star ornament':F('Cheer Star Ornament|Decorazione a stella Cheer|Ornement étoile Cheer|Stern-Anhänger Cheer|Adorno de estrella Cheer','Aari Embroidery|ricamo Aari|broderie Aari|Aari-Stickerei|bordado Aari'),
'cheer tree ornament':F('Cheer Tree Ornament|Decorazione ad albero Cheer|Ornement sapin Cheer|Tannenbaum-Anhänger Cheer|Adorno de árbol Cheer','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'cord bracelet with charm heart':F('Cord Bracelet with Heart Charm|Bracciale in corda con ciondolo a cuore|Bracelet cordon avec breloque cœur|Kordelarmband mit Herz-Anhänger|Pulsera de cordón con colgante de corazón','18K Gold Plated, Adjustable|placcato oro 18K, regolabile|plaqué or 18 carats, réglable|18 Karat vergoldet, verstellbar|chapado en oro de 18 K, ajustable',False),
'cord bracelet with charm shell':F('Cord Bracelet with Shell Charm|Bracciale in corda con ciondolo a conchiglia|Bracelet cordon avec breloque coquillage|Kordelarmband mit Muschel-Anhänger|Pulsera de cordón con colgante de concha','18K Gold Plated, Adjustable|placcato oro 18K, regolabile|plaqué or 18 carats, réglable|18 Karat vergoldet, verstellbar|chapado en oro de 18 K, ajustable',False),
'cord bracelet with charm star fish':F('Cord Bracelet with Starfish Charm|Bracciale in corda con ciondolo a stella marina|Bracelet cordon avec breloque étoile de mer|Kordelarmband mit Seestern-Anhänger|Pulsera de cordón con colgante de estrella de mar','18K Gold Plated, Adjustable|placcato oro 18K, regolabile|plaqué or 18 carats, réglable|18 Karat vergoldet, verstellbar|chapado en oro de 18 K, ajustable',False),
'cotton sofa throw with broad sari edging':F('Cotton Sofa Throw with Broad Sari Edging|Plaid in cotone con ampio bordo in sari|Plaid en coton à large bordure en sari|Baumwoll-Sofadecke mit breiter Sari-Kante|Manta de algodón con ancho ribete de sari','Handcrafted|artigianale|fait main|handgefertigt|artesanal',False),
'cushion cover with piping edge set of 2 (30x30 cm)':F('Cushion Cover Set of 2 with Piping Edge, 30 x 30 cm|Set di 2 federe per cuscino con profilo, 30 x 30 cm|Lot de 2 housses de coussin passepoilées, 30 x 30 cm|Kissenbezüge mit Paspel, 2er-Set, 30 x 30 cm|Set de 2 fundas de cojín con vivo, 30 x 30 cm'),
'cushion cover with piping edge set of 2 (40x40 cm)':F('Cushion Cover Set of 2 with Piping Edge, 40 x 40 cm|Set di 2 federe per cuscino con profilo, 40 x 40 cm|Lot de 2 housses de coussin passepoilées, 40 x 40 cm|Kissenbezüge mit Paspel, 2er-Set, 40 x 40 cm|Set de 2 fundas de cojín con vivo, 40 x 40 cm'),
'day blouse':F('Day Blouse|Blusa Day|Blouse Day|Bluse Day|Blusa Day','Long Sleeve, Band Collar|manica lunga, collo alla coreana|manches longues, col officier|langarm, Stehkragen|manga larga, cuello mao'),
'day waistcoat':F('Day Waistcoat|Gilet Day|Gilet Day|Weste Day|Chaleco Day','Sleeveless V-Neck|scollo a V senza maniche|col V sans manches|ärmellos mit V-Ausschnitt|sin mangas con cuello en V'),
'do good bomber':F('Do Good Bomber Jacket|Giacca bomber Do Good|Blouson bomber Do Good|Bomberjacke Do Good|Chaqueta bomber Do Good'),
'do good potli':F('Do Good Potli Bag|Borsa potli Do Good|Sac potli Do Good|Potli-Beutel Do Good|Bolso potli Do Good'),
'do good tote bag':F('Do Good Tote Bag|Borsa tote Do Good|Cabas Do Good|Tote Bag Do Good|Bolso tote Do Good'),
'do good work tote bag':F('Do Good Work Tote Bag|Borsa tote da lavoro Do Good|Cabas de travail Do Good|Arbeits-Tote Do Good|Bolso tote de trabajo Do Good'),
'double frill cushion cover set of 2':F('Double Frill Cushion Cover Set of 2, 40 cm|Set di 2 federe per cuscino con doppia balza, 40 cm|Lot de 2 housses de coussin à double volant, 40 cm|Kissenbezüge mit Doppelrüsche, 2er-Set, 40 cm|Set de 2 fundas de cojín con doble volante, 40 cm','Reversible|reversibili|réversibles|wendbar|reversibles'),
'floret dangler earring':F('Floret Dangler Earrings|Orecchini pendenti Floret|Boucles d\'oreilles pendantes Floret|Hängeohrringe Floret|Pendientes colgantes Floret','Nickel Safe, 5.5 cm|senza nichel, 5,5 cm|sans nickel, 5,5 cm|nickelfrei, 5,5 cm|sin níquel, 5,5 cm'),
'flower christmas stocking':F('Flower Christmas Stocking, 29 x 39 cm|Calza di Natale Flower, 29 x 39 cm|Chaussette de Noël Flower, 29 x 39 cm|Weihnachtsstrumpf Flower, 29 x 39 cm|Calcetín de Navidad Flower, 29 x 39 cm','Beaded Embellishments|decorazioni con perline|ornements perlés|Perlenverzierung|adornos de cuentas'),
'folded celebration card set of 6':F('Folded Celebration Card Set of 6|Set di 6 biglietti augurali pieghevoli|Lot de 6 cartes de célébration pliées|Klappkarten-Set, 6 Stück|Set de 6 tarjetas de celebración plegables','100% Recycled Paper, Sari Fabric Motifs|carta 100% riciclata, decori in tessuto di sari|papier 100 % recyclé, motifs en tissu de sari|100 % Recyclingpapier, Sari-Stoff-Motive|papel 100% reciclado, motivos de tela de sari',False),
'love folded celebration card set of 6':F('Love Folded Celebration Card Set of 6|Set di 6 biglietti augurali pieghevoli Love|Lot de 6 cartes de célébration pliées Love|Klappkarten-Set Love, 6 Stück|Set de 6 tarjetas de celebración plegables Love','100% Recycled Paper, Sari Fabric Motifs|carta 100% riciclata, decori in tessuto di sari|papier 100 % recyclé, motifs en tissu de sari|100 % Recyclingpapier, Sari-Stoff-Motive|papel 100% reciclado, motivos de tela de sari',False),
'folded postcard set (10 pieces)':F('Folded Postcard Set of 10 with Envelopes|Set di 10 cartoline pieghevoli con buste|Lot de 10 cartes pliées avec enveloppes|Klappkarten-Set mit Umschlägen, 10 Stück|Set de 10 postales plegables con sobres','100% Recycled Paper, Sari Fabric|carta 100% riciclata, tessuto di sari|papier 100 % recyclé, tissu de sari|100 % Recyclingpapier, Sari-Stoff|papel 100% reciclado, tela de sari',False),
'frill hoop earrings':F('Frill Hoop Earrings|Orecchini a cerchio con balza|Créoles à volant|Creolen mit Rüsche|Aros con volante','Lead-Free, Nickel Safe, 4 cm|senza piombo, senza nichel, 4 cm|sans plomb, sans nickel, 4 cm|bleifrei, nickelfrei, 4 cm|sin plomo, sin níquel, 4 cm'),
'frill skirt set':F('Frill Skirt Set|Completo con gonna a balze|Ensemble jupe à volants|Rock-Set mit Rüschen|Conjunto de falda con volantes','Two-Piece Co-ord|coordinato due pezzi|ensemble deux pièces|zweiteiliges Set|conjunto de dos piezas'),
'fringe shopper bag':F('Fringe Shopper Bag|Borsa shopper con frange|Cabas à franges|Shopper mit Fransen|Bolso shopper con flecos','Cotton Canvas with Sari Lining|tela di cotone con fodera in sari|toile de coton doublée de sari|Baumwoll-Canvas mit Sari-Futter|lona de algodón con forro de sari',False),
'gold colored ball ornament':F('Gold Colored Ball Ornament, 8 cm|Pallina decorativa color oro, 8 cm|Boule décorative dorée, 8 cm|Goldfarbene Kugel, 8 cm|Bola decorativa dorada, 8 cm','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'gold colored crescent moon ornament':F('Gold Colored Crescent Moon Ornament|Decorazione a mezzaluna color oro|Ornement croissant de lune doré|Goldfarbener Halbmond-Anhänger|Adorno de luna creciente dorado','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'gold colored crescent moon ornament set of 2':F('Gold Colored Crescent Moon Ornament Set of 2|Set di 2 decorazioni a mezzaluna color oro|Lot de 2 ornements croissant de lune dorés|Goldfarbene Halbmond-Anhänger, 2er-Set|Set de 2 adornos de luna creciente dorados'),
'gold colored star ornament':F('Gold Colored Star Ornament, 15 cm|Decorazione a stella color oro, 15 cm|Ornement étoile doré, 15 cm|Goldfarbener Stern-Anhänger, 15 cm|Adorno de estrella dorado, 15 cm'),
'heart charm rope bracelet with tassels':F('Heart Charm Rope Bracelet with Tassels|Bracciale in corda con ciondolo a cuore e nappine|Bracelet en corde avec breloque cœur et pompons|Seilarmband mit Herz-Anhänger und Quasten|Pulsera de cuerda con colgante de corazón y borlas','Double Wrap, Adjustable|doppio giro, regolabile|double tour, réglable|doppelt gewickelt, verstellbar|doble vuelta, ajustable'),
'heart drop earrings':F('Heart Drop Earrings, 4.5 cm|Orecchini pendenti a cuore, 4,5 cm|Boucles d\'oreilles pendantes cœur, 4,5 cm|Herz-Hängeohrringe, 4,5 cm|Pendientes colgantes de corazón, 4,5 cm','Hand-Embroidered Aari|ricamo Aari a mano|broderie Aari main|Aari-Handstickerei|bordado Aari a mano'),
'imperfect beaded knotted bracelet':F('Beaded Knotted Bracelet, Imperfect|Bracciale annodato con perline, con piccole imperfezioni|Bracelet noué perlé, avec petites imperfections|Geknotetes Perlenarmband mit kleinen Makeln|Pulsera anudada de cuentas, con pequeñas imperfecciones'),
'imperfect clutch handbag':F('Clutch Handbag, Imperfect|Pochette con piccole imperfezioni|Pochette avec petites imperfections|Clutch mit kleinen Makeln|Bolso clutch con pequeñas imperfecciones','Metal Frame|chiusura con montatura in metallo|fermoir en métal|Metallbügel|boquilla de metal'),
'imperfect photo frame a4':F('A4 Photo Frame, Imperfect|Cornice portafoto A4 con piccole imperfezioni|Cadre photo A4 avec petites imperfections|A4-Bilderrahmen mit kleinen Makeln|Marco de fotos A4 con pequeñas imperfecciones','Fabric Covered|rivestita in tessuto|recouvert de tissu|stoffbezogen|forrado de tela'),
'imperfect photo frame a5':F('A5 Photo Frame, Imperfect|Cornice portafoto A5 con piccole imperfezioni|Cadre photo A5 avec petites imperfections|A5-Bilderrahmen mit kleinen Makeln|Marco de fotos A5 con pequeñas imperfecciones','Fabric Covered|rivestita in tessuto|recouvert de tissu|stoffbezogen|forrado de tela'),
'kaftan with lace':F('Kaftan with Lace|Caftano con pizzo|Caftan avec dentelle|Kaftan mit Spitze|Caftán con encaje','Midi Wrap|midi a portafoglio|midi portefeuille|Midi zum Wickeln|midi cruzado'),
'key ring':F('Key Ring, 2 x 12 cm|Portachiavi, 2 x 12 cm|Porte-clés, 2 x 12 cm|Schlüsselanhänger, 2 x 12 cm|Llavero, 2 x 12 cm','Fabric Loop with Metal Ring|passante in tessuto con anello in metallo|boucle en tissu avec anneau métallique|Stoffschlaufe mit Metallring|lazo de tela con anilla metálica'),
'keychain lanyard':F('Keychain Lanyard|Portachiavi a laccetto|Porte-clés tour de cou|Schlüsselband|Llavero con cordón','Tassel Detail|con nappina|avec pompon|mit Quaste|con borla'),
'kimono':F('Kimono|Kimono|Kimono|Kimono|Kimono','Contrast Borders, Fabric Belt|bordi a contrasto, cintura in tessuto|bordures contrastées, ceinture en tissu|Kontrastkanten, Stoffgürtel|bordes en contraste, cinturón de tela'),
'lounge set':F('Lounge Set|Completo loungewear|Ensemble d\'intérieur|Lounge-Set|Conjunto de estar por casa','Relaxed Two-Piece|due pezzi, vestibilità comoda|deux pièces, coupe ample|zweiteilig, lockere Passform|dos piezas, corte holgado'),
'lumbar cotton cushion cover with broad sari edging':F('Lumbar Cotton Cushion Cover with Broad Sari Edging|Federa rettangolare in cotone con ampio bordo in sari|Housse de coussin rectangulaire en coton à large bordure en sari|Rechteckiger Baumwoll-Kissenbezug mit breiter Sari-Kante|Funda de cojín rectangular de algodón con ancho ribete de sari','Handcrafted|artigianale|fait main|handgefertigt|artesanal',False),
'lumbar cotton cushion cover with piping edge (30x50 cm)':F('Lumbar Cotton Cushion Cover with Piping Edge, 30 x 50 cm|Federa rettangolare in cotone con profilo, 30 x 50 cm|Housse de coussin rectangulaire passepoilée, 30 x 50 cm|Rechteckiger Baumwoll-Kissenbezug mit Paspel, 30 x 50 cm|Funda de cojín rectangular de algodón con vivo, 30 x 50 cm','Five-Button Closure|chiusura a cinque bottoni|fermeture à cinq boutons|Fünf-Knopf-Verschluss|cierre de cinco botones'),
'maxi kaftan':F('Maxi Kaftan|Caftano lungo|Caftan long|Maxi-Kaftan|Caftán largo','Cotton Crochet Lace|pizzo all\'uncinetto in cotone|dentelle au crochet en coton|Häkelspitze aus Baumwolle|encaje de ganchillo de algodón'),
'maxi square earrings 145':F('Maxi Square Earrings 145|Orecchini quadrati maxi 145|Boucles d\'oreilles carrées maxi 145|Maxi-Ohrringe eckig 145|Pendientes cuadrados maxi 145','Nickel Safe|senza nichel|sans nickel|nickelfrei|sin níquel'),
'midi wrap dress':F('Midi Wrap Dress|Abito midi a portafoglio|Robe portefeuille midi|Midi-Wickelkleid|Vestido cruzado midi','A-Line with Belt|linea ad A con cintura|coupe trapèze avec ceinture|A-Linie mit Gürtel|línea A con cinturón'),
'mini star bauble':F('Mini Star Bauble|Mini decorazione a stella|Mini ornement étoile|Mini-Stern-Anhänger|Mini adorno de estrella','Hand-Stitched|cucita a mano|cousu main|handgenäht|cosido a mano'),
'napkin ring set of 6':F('Napkin Ring Set of 6|Set di 6 portatovaglioli|Lot de 6 ronds de serviette|Serviettenringe, 6er-Set|Set de 6 servilleteros','Button & Elastic Loop Closure|chiusura con bottone e anello elastico|fermeture bouton et boucle élastique|Knopf- und Gummischlaufen-Verschluss|cierre de botón y lazo elástico'),
'oversized shirt':F('Oversized Shirt|Camicia oversize|Chemise oversize|Oversize-Hemd|Camisa oversize'),
'paperbag high waisted pull on pants':F('Paperbag High Waisted Trousers|Pantaloni paperbag a vita alta|Pantalon paperbag taille haute|Paperbag-Hose mit hoher Taille|Pantalón paperbag de talle alto','Elasticated Waist|vita elastica|taille élastique|elastischer Bund|cintura elástica'),
'patch work christmas stocking':F('Patchwork Christmas Stocking|Calza di Natale patchwork|Chaussette de Noël patchwork|Patchwork-Weihnachtsstrumpf|Calcetín de Navidad patchwork'),
'photo frame a4':F('A4 Photo Frame|Cornice portafoto A4|Cadre photo A4|A4-Bilderrahmen|Marco de fotos A4','Fabric Covered, Tabletop Stand|rivestita in tessuto, da tavolo|recouvert de tissu, à poser|stoffbezogen, zum Aufstellen|forrado de tela, de sobremesa'),
'pj set short with short sleeves':F('Short Sleeve PJ Set|Set pigiama corto a maniche corte|Pyjashort à manches courtes|Kurzarm-Pyjama-Set|Pijama corto de manga corta'),
'plant pot cover set of 2':F('Plant Pot Cover Set of 2, S & M|Set di 2 copri-vaso, taglie S e M|Lot de 2 cache-pots, tailles S et M|Übertopf-Hüllen 2er-Set, Größen S und M|Set de 2 cubremacetas, tallas S y M','Waterproof Lining|fodera impermeabile|doublure imperméable|wasserdichtes Futter|forro impermeable'),
'playsuit with lace':F('Playsuit with Lace|Tutina con pizzo|Combishort avec dentelle|Playsuit mit Spitze|Mono corto con encaje','Adjustable Straps|spalline regolabili|bretelles réglables|verstellbare Träger|tirantes ajustables'),
'pleated earrings 149':F('Pleated Earrings 149|Orecchini plissettati 149|Boucles d\'oreilles plissées 149|Plissee-Ohrringe 149|Pendientes plisados 149','Nickel Safe Hooks|ganci senza nichel|crochets sans nickel|nickelfreie Haken|ganchos sin níquel'),
'pleated earrings 151':F('Pleated Earrings 151|Orecchini plissettati 151|Boucles d\'oreilles plissées 151|Plissee-Ohrringe 151|Pendientes plisados 151','Nickel Safe Hooks|ganci senza nichel|crochets sans nickel|nickelfreie Haken|ganchos sin níquel'),
'pleated earrings 152':F('Pleated Earrings 152|Orecchini plissettati 152|Boucles d\'oreilles plissées 152|Plissee-Ohrringe 152|Pendientes plisados 152','Nickel Safe Hooks|ganci senza nichel|crochets sans nickel|nickelfreie Haken|ganchos sin níquel'),
'pleated earrings 153':F('Pleated Earrings 153|Orecchini plissettati 153|Boucles d\'oreilles plissées 153|Plissee-Ohrringe 153|Pendientes plisados 153','Nickel Safe Hooks|ganci senza nichel|crochets sans nickel|nickelfreie Haken|ganchos sin níquel'),
'pull-on pants':F('Pull-On Trousers|Pantaloni senza chiusura|Pantalon à enfiler|Schlupfhose|Pantalón sin cierre','Elasticated Waist|vita elastica|taille élastique|elastischer Bund|cintura elástica'),
'quilted laptop sleeve 13-14 inch':F('Quilted Laptop Sleeve 13-14 Inch|Custodia trapuntata per laptop 13-14 pollici|Housse matelassée pour ordinateur 13-14 pouces|Gesteppte Laptophülle 13-14 Zoll|Funda acolchada para portátil de 13-14 pulgadas'),
'quilted laptop sleeve 15-16 inch':F('Quilted Laptop Sleeve 15-16 Inch|Custodia trapuntata per laptop 15-16 pollici|Housse matelassée pour ordinateur 15-16 pouces|Gesteppte Laptophülle 15-16 Zoll|Funda acolchada para portátil de 15-16 pulgadas'),
'quilted organizer':F('Quilted Organizer|Organizer trapuntato|Organiseur matelassé|Gesteppter Organizer|Organizador acolchado','Lightly Padded|leggermente imbottito|légèrement rembourré|leicht gepolstert|ligeramente acolchado'),
'quilted pencil pouch':F('Quilted Pencil Pouch|Astuccio trapuntato|Trousse matelassée|Gestepptes Federmäppchen|Estuche acolchado','Padded|imbottito|rembourrée|gepolstert|acolchado'),
'quilted pouch':F('Quilted Pouch|Pochette trapuntata|Pochette matelassée|Gesteppte Tasche|Neceser acolchado','Zip Closure, Medium|chiusura a zip, media|fermeture zippée, taille M|Reißverschluss, mittelgroß|cierre de cremallera, mediano'),
'quilted shopper bag':F('Quilted Shopper Bag|Borsa shopper trapuntata|Cabas matelassé|Gesteppter Shopper|Bolso shopper acolchado'),
'resort shirt':F('Resort Shirt|Camicia resort|Chemise resort|Resort-Hemd|Camisa resort','Long Sleeve, Relaxed Fit|manica lunga, vestibilità comoda|manches longues, coupe ample|langarm, lockere Passform|manga larga, corte holgado'),
'reusable bag set of 3':F('Reusable Bag Set of 3|Set di 3 borse riutilizzabili|Lot de 3 sacs réutilisables|Wiederverwendbare Taschen, 3er-Set|Set de 3 bolsas reutilizables','Foldable Shoppers|shopper pieghevoli|cabas pliables|faltbare Shopper|shoppers plegables'),
'reusable bag set of 5':F('Reusable Bag Set of 5|Set di 5 borse riutilizzabili|Lot de 5 sacs réutilisables|Wiederverwendbare Taschen, 5er-Set|Set de 5 bolsas reutilizables','Foldable Shoppers|shopper pieghevoli|cabas pliables|faltbare Shopper|shoppers plegables'),
'round placemat set of 4':F('Round Placemat Set of 4, 38 cm|Set di 4 tovagliette rotonde, 38 cm|Lot de 4 sets de table ronds, 38 cm|Runde Tischsets, 4er-Set, 38 cm|Set de 4 manteles individuales redondos, 38 cm','Washable Fabric Sleeves|fodere in tessuto lavabili|housses en tissu lavables|waschbare Stoffbezüge|fundas de tela lavables'),
'ruffle earrings 183':F('Ruffle Earrings 183|Orecchini con volant 183|Boucles d\'oreilles à volant 183|Rüschen-Ohrringe 183|Pendientes con volante 183','Nickel Safe Stud, 4 cm|perno senza nichel, 4 cm|tige sans nickel, 4 cm|nickelfreier Stecker, 4 cm|cierre sin níquel, 4 cm'),
'scrunchy set of 2':F('Scrunchy Set of 2|Set di 2 elastici per capelli scrunchie|Lot de 2 chouchous|Scrunchies, 2er-Set|Set de 2 coleteros scrunchie'),
'scrunchy set of 5':F('Scrunchy Set of 5|Set di 5 elastici per capelli scrunchie|Lot de 5 chouchous|Scrunchies, 5er-Set|Set de 5 coleteros scrunchie'),
'tail scrunchy set of 2':F('Tail Scrunchy Set of 2|Set di 2 scrunchie con code|Lot de 2 chouchous à pans|Scrunchies mit Bändern, 2er-Set|Set de 2 scrunchies con cintas'),
'shirt with belt':F('Slim-Fit Shirt with Detachable Belt|Camicia slim fit con cintura removibile|Chemise ajustée avec ceinture amovible|Slim-Fit-Hemd mit abnehmbarem Gürtel|Camisa slim fit con cinturón extraíble','Long Sleeve|manica lunga|manches longues|langarm|manga larga'),
'shopper bag':F('Shopper Bag|Borsa shopper|Cabas|Shopper|Bolso shopper','Cotton Lined|fodera in cotone|doublure en coton|Baumwollfutter|forro de algodón'),
'short kaftan with lace':F('Short Kaftan with Lace|Caftano corto con pizzo|Caftan court avec dentelle|Kurzer Kaftan mit Spitze|Caftán corto con encaje','Relaxed Fit|vestibilità comoda|coupe ample|lockere Passform|corte holgado'),
'shorts':F('Shorts|Shorts|Short|Shorts|Pantalón corto','Adjustable Drawstring Waist|coulisse regolabile in vita|taille à cordon ajustable|verstellbarer Tunnelzug|cintura con cordón ajustable'),
'silver colored ball ornament':F('Silver Colored Ball Ornament, 8 cm|Pallina decorativa color argento, 8 cm|Boule décorative argentée, 8 cm|Silberfarbene Kugel, 8 cm|Bola decorativa plateada, 8 cm','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'silver colored crescent moon ornament':F('Silver Colored Crescent Moon Ornament|Decorazione a mezzaluna color argento|Ornement croissant de lune argenté|Silberfarbener Halbmond-Anhänger|Adorno de luna creciente plateado','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'silver colored crescent moon ornament set of 2':F('Silver Colored Crescent Moon Ornament Set of 2|Set di 2 decorazioni a mezzaluna color argento|Lot de 2 ornements croissant de lune argentés|Silberfarbene Halbmond-Anhänger, 2er-Set|Set de 2 adornos de luna creciente plateados'),
'silver colored snowflake ornament':F('Silver Colored Snowflake Ornament|Decorazione a fiocco di neve color argento|Ornement flocon de neige argenté|Silberfarbener Schneeflocken-Anhänger|Adorno de copo de nieve plateado','Hand-Embroidered|ricamata a mano|brodé main|handbestickt|bordado a mano'),
'silver colored star ornament':F('Silver Colored Star Ornament, 15 cm|Decorazione a stella color argento, 15 cm|Ornement étoile argenté, 15 cm|Silberfarbener Stern-Anhänger, 15 cm|Adorno de estrella plateado, 15 cm','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'single frill cushion cover set of 2':F('Single Frill Cushion Cover Set of 2, 40 cm|Set di 2 federe per cuscino con balza, 40 cm|Lot de 2 housses de coussin à volant, 40 cm|Kissenbezüge mit Rüsche, 2er-Set, 40 cm|Set de 2 fundas de cojín con volante, 40 cm','Reversible|reversibili|réversibles|wendbar|reversibles'),
'strap dress':F('Strap Dress|Abito con spalline|Robe à bretelles|Trägerkleid|Vestido de tirantes','Midi A-Line|midi a trapezio|midi trapèze|Midi in A-Linie|midi de línea A'),
'stripes christmas stocking':F('Stripes Christmas Stocking, 29 x 39 cm|Calza di Natale a righe, 29 x 39 cm|Chaussette de Noël à rayures, 29 x 39 cm|Gestreifter Weihnachtsstrumpf, 29 x 39 cm|Calcetín de Navidad a rayas, 29 x 39 cm','Gold Embellishments|decorazioni dorate|ornements dorés|goldene Verzierungen|adornos dorados'),
'table runner':F('Table Runner, 40 x 160 cm|Runner da tavola, 40 x 160 cm|Chemin de table, 40 x 160 cm|Tischläufer, 40 x 160 cm|Camino de mesa, 40 x 160 cm','Reversible|reversibile|réversible|wendbar|reversible'),
'tear drop earrings':F('Tear Drop Earrings, 2.5 cm|Orecchini a goccia, 2,5 cm|Boucles d\'oreilles goutte, 2,5 cm|Tropfen-Ohrringe, 2,5 cm|Pendientes de gota, 2,5 cm','Embroidered, Lead-Free, Nickel Safe|ricamati, senza piombo, senza nichel|brodées, sans plomb, sans nickel|bestickt, bleifrei, nickelfrei|bordados, sin plomo, sin níquel'),
'tie keychain':F('Tie Keychain|Portachiavi con fiocco|Porte-clés à nouer|Schlüsselanhänger zum Binden|Llavero de lazo'),
'tie up fringe choker':F('Tie-Up Fringe Choker|Choker con frange da annodare|Ras-de-cou à franges à nouer|Choker mit Fransen zum Binden|Gargantilla con flecos para atar','Beaded Details|dettagli con perline|détails perlés|Perlendetails|detalles de cuentas'),
'timeless bell ornament':F('Timeless Bell Ornament|Decorazione a campana Timeless|Ornement cloche Timeless|Glocken-Anhänger Timeless|Adorno de campana Timeless','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'timeless candy cane ornament':F('Timeless Candy Cane Ornament|Decorazione a bastoncino di zucchero Timeless|Ornement sucre d\'orge Timeless|Zuckerstangen-Anhänger Timeless|Adorno de bastón de caramelo Timeless','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'timeless crescent moon ornament':F('Timeless Crescent Moon Ornament|Decorazione a mezzaluna Timeless|Ornement croissant de lune Timeless|Halbmond-Anhänger Timeless|Adorno de luna creciente Timeless'),
'timeless snowflake ornament':F('Timeless Snowflake Ornament|Decorazione a fiocco di neve Timeless|Ornement flocon de neige Timeless|Schneeflocken-Anhänger Timeless|Adorno de copo de nieve Timeless','Organic Cotton Filled|imbottitura in cotone biologico|garnissage en coton bio|Füllung aus Bio-Baumwolle|relleno de algodón orgánico'),
'tree christmas ornament':F('Tree Christmas Ornament|Decorazione natalizia ad albero|Ornement de Noël sapin|Tannenbaum-Weihnachtsanhänger|Adorno navideño de árbol','Layered Fabric, Bead Detail|tessuto a strati, dettaglio con perlina|tissu superposé, détail perlé|Stofflagen, Perlendetail|tela en capas, detalle de cuenta'),
'tree christmas ornament set of 3':F('Tree Christmas Ornament Set of 3|Set di 3 decorazioni natalizie ad albero|Lot de 3 ornements de Noël sapin|Tannenbaum-Weihnachtsanhänger, 3er-Set|Set de 3 adornos navideños de árbol','Layered Fabric|tessuto a strati|tissu superposé|Stofflagen|tela en capas'),
'twin travel bag set (duffle and barrel)':F('Quilted Travel Bag Set, Duffle & Barrel|Set di borse da viaggio trapuntate, borsone e bauletto|Lot de sacs de voyage matelassés, polochon et baril|Gestepptes Reisetaschen-Set, Duffle und Barrel|Set de bolsas de viaje acolchadas, bolsa y barril'),
'vanity pouch set':F('Vanity Pouch Set S & M|Set di 2 beauty case, S e M|Lot de 2 trousses de toilette, S et M|Kosmetiktaschen-Set S und M|Set de 2 neceseres, S y M','Quilted Cotton, Zip Closure|cotone trapuntato, chiusura a zip|coton matelassé, fermeture zippée|gesteppte Baumwolle, Reißverschluss|algodón acolchado, cierre de cremallera'),
'wide leg patch pocket pants':F('Wide-Leg Trousers with Patch Pockets|Pantaloni a gamba larga con tasche applicate|Pantalon large à poches plaquées|Weite Hose mit aufgesetzten Taschen|Pantalón ancho con bolsillos de parche'),
'wine bag':F('Wine Bag|Portabottiglia|Sac à vin|Weinflaschentasche|Bolsa para vino','Fits 750 ml Bottle|per bottiglia da 750 ml|pour bouteille de 75 cl|für 0,75-l-Flasche|para botella de 750 ml'),
'wrap around bracelet with charms':F('Wrap Around Bracelet with Charms|Bracciale avvolgente con ciondoli|Bracelet à enrouler avec breloques|Wickelarmband mit Anhängern|Pulsera envolvente con colgantes','18K Gold Plated Charms, Adjustable|ciondoli placcati oro 18K, regolabile|breloques plaquées or 18 carats, réglable|18 Karat vergoldete Anhänger, verstellbar|colgantes chapados en oro de 18 K, ajustable'),
}
FAM.update(FAM2)
CATKW=[('pj set','clothing'),('playsuit','clothing'),('blouse','clothing'),('coat','clothing'),('trousers','clothing'),('ornament','ornaments'),('bauble','ornaments'),('stocking','home'),('earring','jewellery'),('necklace','jewellery'),('choker','jewellery'),('bracelet','jewellery'),
 ('bag','bags'),('pouch','bags'),('clutch','bags'),('tote','bags'),('organizer','bags'),('laptop sleeve','bags'),('potli','bags'),('shopper','bags'),
 ('placemat','home'),('runner','home'),('napkin','home'),('cushion','home'),('basket','home'),('throw','home'),('frame','home'),('pot cover','home'),
 ('card','accessories'),('postcard','accessories'),('notebook','accessories'),('bookmark','accessories'),
 ('case','accessories'),('scrunch','accessories'),('scarf','accessories'),('stole','accessories'),('foulard','accessories'),('keychain','accessories'),('keyring','accessories'),('key ring','accessories'),('lanyard','accessories'),('slipper','accessories'),('hairband','accessories'),('pareo','accessories')]
def category(en_name):
    t=en_name.lower()
    for k,c in CATKW:
        if k in t: return c
    return 'clothing'
KEY=dict(en='Upcycled Sari',it='Sari riciclato',fr='Sari recyclé',de='Recycelter Sari',es='Sari reciclado')
BRAND='I was a Sari'
BASED={'default':dict(en='Handmade in India by women artisans from upcycled saris.',it='Fatto a mano in India da artigiane, con sari riciclati.',fr="Fait main en Inde par des artisanes, à partir de saris recyclés.",de='Von Kunsthandwerkerinnen in Indien aus recycelten Saris handgefertigt.',es='Hecho a mano en India por artesanas, con saris reciclados.'),
 'ornaments':dict(en='Handmade in India by women artisans from pre-loved saris.',it='Fatto a mano in India da artigiane, con sari già indossati.',fr="Fait main en Inde par des artisanes, à partir de saris déjà portés.",de='Von Kunsthandwerkerinnen in Indien aus getragenen Saris handgefertigt.',es='Hecho a mano en India por artesanas, con saris ya usados.'),
 'jewellery':dict(en='Handmade in India by women artisans with upcycled sari fabric.',it='Fatto a mano in India da artigiane, con tessuto di sari riciclato.',fr="Fait main en Inde par des artisanes, avec du tissu de sari recyclé.",de='Von Kunsthandwerkerinnen in Indien mit recyceltem Sari-Stoff handgefertigt.',es='Hecho a mano en India por artesanas, con tela de sari reciclada.')}
SHORT=dict(en='Handmade from upcycled saris.',it='Fatto a mano con sari riciclati.',fr='Fait main à partir de saris recyclés.',de='Handgefertigt aus recycelten Saris.',es='Hecho a mano con saris reciclados.')
CLOSE={'clothing':dict(en='Every piece carries the story of a sari.',it='Ogni capo porta con sé la storia di un sari.',fr="Chaque pièce porte l'histoire d'un sari.",de='Jedes Stück erzählt die Geschichte eines Saris.',es='Cada prenda lleva la historia de un sari.'),
 'bags':dict(en="A bag with a sari's story, for every day.",it='Una borsa con la storia di un sari, per ogni giorno.',fr="Un sac qui raconte l'histoire d'un sari, au quotidien.",de='Eine Tasche mit der Geschichte eines Saris, für jeden Tag.',es='Un bolso con la historia de un sari, para cada día.'),
 'jewellery':dict(en='A small piece with a big story.',it='Un piccolo gioiello con una grande storia.',fr='Un petit bijou, une grande histoire.',de='Ein kleines Schmuckstück mit großer Geschichte.',es='Una pequeña joya con una gran historia.'),
 'accessories':dict(en='Everyday style with a story behind it.',it='Stile di ogni giorno, con una storia dietro.',fr="Un style du quotidien qui a une histoire.",de='Alltagsstil mit Geschichte.',es='Estilo diario con una historia detrás.'),
 'home':dict(en='The story of a sari, for your home.',it='La storia di un sari, per la tua casa.',fr="L'histoire d'un sari, pour la maison.",de='Die Geschichte eines Saris für das eigene Zuhause.',es='La historia de un sari, para el hogar.'),
 'ornaments':dict(en='A story to hang, year after year.',it='Una storia da appendere, anno dopo anno.',fr='Une histoire à suspendre, année après année.',de='Eine Geschichte zum Aufhängen, Jahr für Jahr.',es='Una historia para colgar, año tras año.')}
TMAX,DMAX,GMAX=60,155,150
def _cp(c,p,i,Lg):
    if not (c or p): return None
    cc=COL[c][i] if c else ''; pp=PAT[p][i] if p else ''
    if Lg=='en': cp=f'{cc} {pp}'.strip()
    elif Lg=='de': cp=(f'{pp} in {cc}' if pp and cc else (pp or cc))
    else: cp=f'{pp} {cc}'.strip() if pp else cc[:1].upper()+cc[1:]
    return cp[:1].upper()+cp[1:]
def _cut(s,n):
    if len(s)<=n: return s
    return s[:n+1].rsplit(' ',1)[0].rstrip(' ,;:-|–')
COLOUR_ALIAS={'Assorted':'Multicolor','Multi Colored':'Multicolor','Multicolour':'Multicolor','Multi Color':'Multicolor'}
IT_COLOUR={'Red':'Rosso','Yellow':'Giallo','Blue':'Blu','Pink':'Rosa','Beige':'Beige','Green':'Verde','Grey':'Grigio','White':'Bianco','Brown':'Marrone','Orange':'Arancione','Black':'Nero','Purple':'Viola','Multicolor':'Multicolore'}
def gmc_colour(colour):
    c=COLOUR_ALIAS.get(colour,colour)
    return (c,IT_COLOUR[c]) if c in IT_COLOUR else (None,None)
def build(title,colour,pattern):
    if 'gift card' in (title or '').lower(): return None
    k=famkey(title)
    if k not in FAM: return None
    f=FAM[k]; colour=COLOUR_ALIAS.get(colour,colour); c=colour if colour in COL else None; p=pattern if pattern in PAT else None
    cat=category(f['n'][0]); out={}
    for i,Lg in enumerate(L):
        cp=_cp(c,p,i,Lg)
        nm=f['n'][i]; sz=None
        mm=re.search(r', (\d[\d.,]*(?: ?x ?\d+)? ?cm)$',nm)
        if mm: nm=nm[:mm.start()]; sz=mm.group(1)
        tail=[t for t in [(f['x'][i] if f['x'] else None),sz,(BASE[Lg] if f['b'] else None)] if t]
        g=nm+(' – '+cp if cp else '')+(', '+', '.join(tail) if tail else '')
        np_=nm+(' – '+cp if cp else '')
        mt=None
        for cand in (f'{np_} | {KEY[Lg]} | {BRAND}',f'{np_} | {BRAND}',np_,f'{nm} | {BRAND}',nm):
            if len(cand)<=TMAX: mt=cand; break
        if mt is None: mt=_cut(np_,TMAX)
        base=BASED.get(cat,BASED['default'])[Lg]; cl=CLOSE[cat][Lg]
        md=None
        for cand in (f'{np_}. {base} {cl}',f'{np_}. {base}',f'{np_}. {SHORT[Lg]} {cl}',f'{np_}. {SHORT[Lg]}',f'{nm}. {SHORT[Lg]}'):
            if len(cand)<=DMAX: md=cand; break
        if md is None: md=_cut(f'{nm}. {SHORT[Lg]}',DMAX)
        out[Lg]=dict(gmc_title=g[:GMAX],meta_title=mt,meta_description=md,category=cat)
    return out
digest=lambda s: hashlib.sha256(s.encode()).hexdigest()

def famkey(t):
    if re.search(r'swing dress with detachable belt',t,re.I): return 'swing dress with detachable belt'
    if t.lower().startswith('timeless star ornament'): return 'timeless star ornament'
    p=re.split(r'\s+[-–]\s+',t)[0].strip().lower().rstrip('.')
    p=re.sub(r'\s+',' ',p); return ALIAS.get(p,p)
