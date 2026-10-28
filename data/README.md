# Data

- `raw/` – precies wat de API teruggeeft, niet aanpassen.
  - `nabijheid_lang.csv` – CBS 85830NED, lang formaat (buurt × meetwaarde)
  - `kerncijfers_lang.csv` – CBS 85618NED, lang formaat (buurt × meetwaarde)
  - `codeboek_maten.csv` – welke code (bv. `M001642`) welke meetwaarde is
  - `codeboek_regios.csv` – welke code (bv. `BU0363AA01`) welke buurt of gemeente is
  - `buurtpunten.csv` – één punt (lengte- en breedtegraad) per buurt, van PDOK
- `processed/buurten.csv` – één rij per buurt, gekoppeld en opgeschoond. Dit leest het dashboard.

Alles wordt gemaakt door `python ophalen.py` in de hoofdmap.
