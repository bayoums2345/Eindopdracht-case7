import streamlit as st

from src.laden import laad_buurten
from src.analyse import voeg_dichtbij_toe, premie_per_gebied, gemiddelde_woz, euro
from src.grafieken import grafiek_gemiddelde_woz

st.set_page_config(page_title="Supermarkt op loopafstand", layout="wide")

GRENS_KM = 1.0

buurten = laad_buurten()
buurten = voeg_dichtbij_toe(buurten, "afstand_supermarkt", GRENS_KM)
resultaten = premie_per_gebied(buurten)
stad = resultaten["stad"]
platteland = resultaten["platteland"]

st.title("Wat is een supermarkt op loopafstand waard?")
st.caption(f"CBS 2023 | {len(buurten)} buurten in de data | "
           f"{buurten['inkomen'].isna().sum()} zonder inkomenscijfer | "
           f"{stad['buurten'] + platteland['buurten']} buurten in de berekening")

st.markdown(
    "**Hoofdvraag:** gaat een supermarkt binnen 1 km samen met een hogere "
    "woningwaarde in de buurt, en verschilt dat tussen stad en platteland?"
)

kolom1, kolom2, kolom3 = st.columns(3)
kolom1.metric("Stad: verschil in WOZ-waarde",
              f"{euro(stad['premie'])} ± {euro(stad['marge'])}",
              f"{stad['premie_procent']:.1f}% t.o.v. buurten verder weg",
              delta_color="off")
kolom2.metric("Platteland: verschil in WOZ-waarde",
              f"{euro(platteland['premie'])} ± {euro(platteland['marge'])}",
              f"{platteland['premie_procent']:.1f}% t.o.v. buurten verder weg",
              delta_color="off")
kolom3.metric("Buurten in de analyse", stad["buurten"] + platteland["buurten"],
              "met WOZ, afstand én inkomen", delta_color="off")

st.subheader("Conclusie: een supermarkt naast de deur levert geen hogere woningwaarde op")
st.markdown(
    f"""
In buurten met een supermarkt binnen 1 km is de WOZ-waarde **niet hoger maar lager**.
Een deel daarvan komt doordat die buurten vaker appartementen en lagere inkomens hebben.
Houden we inkomen, koopwoningen, bouwjaar en woningtype constant, dan blijft er over:

- **Stad:** {euro(stad['premie'])} per woning, met een marge van {euro(stad['marge'])}
  ({stad['premie_procent']:.1f}%). Klein, en dicht bij nul.
- **Platteland:** {euro(platteland['premie'])} per woning, met een marge van {euro(platteland['marge'])}
  ({platteland['premie_procent']:.1f}%). Dat is een duidelijk verschil.

Op het platteland is de supermarkt een teken dat je in de dorpskern woont. De duurste woningen
staan juist verder weg, in het buitengebied, met meer grond. Ruimte is daar meer waard dan nabijheid.
"""
)

st.plotly_chart(grafiek_gemiddelde_woz(gemiddelde_woz(buurten)))
st.caption("Gemiddelde WOZ-waarde van buurten mét (ja) en zonder (nee) een supermarkt binnen 1 km. "
           "Dit is het verschil vóór correctie; de bedragen bovenaan zijn na correctie.")

st.info(
    "**Advies:** reken bij een woningproject niet op een hogere woningwaarde door een supermarkt "
    f"op loopafstand. In de stad is het effect ongeveer {-stad['premie_procent']:.0f}% en op het "
    f"platteland gaat nabijheid samen met een {-platteland['premie_procent']:.0f}% lagere WOZ-waarde. "
    "Een supermarkt is een voorziening voor bewoners, geen prijsverhoger."
)
