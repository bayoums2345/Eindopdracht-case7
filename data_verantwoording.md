### Data-verantwoording

**Bronnen.** (1) CBS-tabel **85830NED**, *Nabijheid voorzieningen; afstand locatie, wijk- en buurtcijfers 2023* (versie 28-03-2025): gemiddelde afstand over de weg tot de dichtstbijzijnde voorziening. (2) CBS-tabel **85618NED**, *Kerncijfers wijken en buurten 2023* (versie 31-03-2026): gemiddelde WOZ-waarde (waardepeildatum 1 januari 2022), inkomen, woningvoorraad en stedelijkheid. (3) Voor de kaart: PDOK *CBS gebiedsindelingen 2023*, laag `buurt_labelpoint` (één punt per buurt). Opgehaald op 27 oktober 2026.

**Ophalen.** `ophalen.py` gebruikt `requests` op de OData-API van het CBS (`datasets.cbs.nl/odata/v1`). Ik vraag alleen de benodigde codes op en alleen buurten (`BU…`). Het CBS geeft maximaal 10.000 rijen per keer, dus het script volgt de `nextLink`. PDOK geeft 1.000 punten per keer, dus daar loopt het script met `startIndex` door. De ruwe bestanden staan in `data/raw/`, het schone bestand in `data/processed/buurten.csv`.

**Bewerken en koppelen.** Beide CBS-tabellen komen in lang formaat met codes (één rij per buurt per meetwaarde). Die heb ik gepivoteerd naar één rij per buurt en via het codeboek (`MeasureCodes`) vertaald naar kolomnamen. Buurt- en gemeentenamen komen uit het codeboek van de regio's. De koppeling loopt op buurtcode, met `validate="one_to_one"` zodat dubbele buurten een foutmelding geven.

| Stap | Rijen |
|---|---|
| Nabijheid: 54.672 rijen lang → buurten | 13.668 |
| Kerncijfers: 105.249 rijen lang → buurten | 14.421 |
| Na koppelen (inner join op buurtcode) | 13.668 |
| Na weglaten van buurten zonder WOZ-waarde | **12.622** |
| In de regressie (met inkomenscijfer) | 11.727 |

**Wat er onderweg misging of opviel.** De 753 buurten die alleen in de kerncijfers staan, hebben geen afstandscijfer: 98% daarvan heeft minder dan 50 inwoners (bedrijventerreinen, natuur). 1.046 buurten hebben geen WOZ-waarde, omdat het CBS die niet publiceert bij minder dan 20 woningen of te weinig bekende WOZ-waarden. Die vallen weg: zonder WOZ is er niets te vergelijken. 895 buurten hebben geen inkomenscijfer; het zijn kleine buurten (mediaan 75 inwoners) waar het CBS het inkomen geheimhoudt. Die blijven op de kaart staan maar doen niet mee in de regressie. Ik vul ze niet met een gemiddelde, omdat het juist kleine, landelijke buurten zijn en een ingevuld gemiddelde het platteland zou vertekenen. In 2024 was inkomen maar voor 1.950 buurten ingevuld; daarom gebruik ik 2023. De WOZ-waarde is per woning, niet per m², en het woningtype is maar ruw bekend.
