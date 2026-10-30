### Data-verantwoording

**Bronnen:** CBS 85830NED, Nabijheid voorzieningen 2023 (versie 28-03-2025), en CBS 85618NED, Kerncijfers wijken en buurten 2023 (versie 31-03-2026, WOZ-peildatum 1 januari 2022). Voor de kaart: PDOK, buurtindeling 2023.

**Ophalen:** ophalen.py haalt de data met requests op via de API's van het CBS en PDOK, in delen tot alles binnen is.

**Koppelen:** Het CBS levert per buurt een rij per cijfer, met codes. Ik heb er één rij per buurt van gemaakt, de codes met het codeboek vertaald en de tabellen op buurtcode samengevoegd.

| Stap | Buurten |
|---|---|
| Afstanden (54.672 rijen) | 13.668 |
| Buurtcijfers (105.249 rijen) | 14.421 |
| Samengevoegd | 13.668 |
| Zonder WOZ-waarde eruit (dashboard) | **12.622** |
| Zonder inkomen eruit (berekening) | 11.727 |

**Wat er misging:** 753 buurten, vooral bedrijventerreinen, hebben geen afstand. 1.046 buurten hebben te weinig woningen voor een WOZ-waarde en vallen weg. Bij 895 kleine buurten is het inkomen geheim: die staan wel op de kaart, maar niet in de berekening. 2024 viel af, omdat daar het inkomen meestal ontbrak.
