# Eindopdracht IDS – Casus 7: Nabijheid van voorzieningen

**Vraag:** gaat een supermarkt binnen 1 km samen met een hogere woningwaarde (WOZ),
en verschilt dat tussen stad en platteland?

**Data:** twee CBS-tabellen, opgehaald via de open API van het CBS (peiljaar 2023):
- `85830NED` Nabijheid voorzieningen; afstand locatie, wijk- en buurtcijfers 2023
- `85618NED` Kerncijfers wijken en buurten 2023

Plus één punt per buurt van PDOK (CBS gebiedsindelingen 2023) voor de kaart.
Zie `data_verantwoording.md` voor de details.

## Mappen

| Map / bestand | Wat staat erin |
|---|---|
| `ophalen.py` | haalt de data op via de API's en maakt het schone bestand (één keer draaien) |
| `Home.py` | startpagina van het dashboard: hoofdvraag en conclusie |
| `pages/` | de andere pagina's: kaart, analyse, data |
| `src/laden.py` | leest het schone bestand in |
| `src/schoon.py` | van lang formaat naar één rij per buurt, koppelen, lege rijen weg |
| `src/analyse.py` | afgeleide kolommen en de regressie |
| `src/grafieken.py` | alle grafieken, met vaste kleuren |
| `data/raw/` | de ruwe data zoals hij van de API komt, plus de codeboeken |
| `data/processed/` | `buurten.csv`: het schone bestand dat het dashboard leest |
| `notebooks/` | eerste verkenning van de data |
| `data_verantwoording.md` | bronnen, versies, aantallen rijen en wat er misging |

## Starten

```bash
pip install -r requirements.txt
python ophalen.py        # alleen nodig als data/ leeg is
streamlit run Home.py
```
