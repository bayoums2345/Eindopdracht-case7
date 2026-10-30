import streamlit as st

from src.laden import laad_buurten
from src.analyse import VOORZIENINGEN, voeg_dichtbij_toe, premie_per_gebied, gemiddelde_woz, woz_per_afstand, euro
from src.grafieken import grafiek_gemiddelde_woz, grafiek_woz_per_afstand

st.set_page_config(page_title="Analyse", layout="wide")

buurten = laad_buurten()

st.sidebar.header("Instellingen")
voorziening = st.sidebar.selectbox("Voorziening", list(VOORZIENINGEN.keys()))
grens_km = st.sidebar.slider("Loopafstand: binnen hoeveel km?", 0.25, 3.0, 1.0, step=0.25)

afstandkolom = VOORZIENINGEN[voorziening]
buurten = voeg_dichtbij_toe(buurten, afstandkolom, grens_km)
resultaten = premie_per_gebied(buurten)
stad = resultaten["stad"]
platteland = resultaten["platteland"]

st.title(f"Wat is een {voorziening.lower()} binnen {grens_km} km waard?")
st.markdown(
    "We vergelijken buurten mét de voorziening binnen de gekozen afstand met buurten zonder. "
    "Een eerlijke vergelijking houdt de andere verschillen tussen buurten gelijk: "
    "**inkomen, % koopwoningen, % nieuwbouw en % eengezinswoningen.**"
)

kolom_stad, kolom_platteland = st.columns(2)

kolom_stad.subheader("Stad")
if stad is None:
    kolom_stad.warning("Te weinig buurten om te vergelijken (minder dan 30 in een groep). Kies een andere afstand.")
else:
    kolom_stad.metric("Verschil in WOZ-waarde na correctie",
                      f"{euro(stad['premie'])} ± {euro(stad['marge'])}",
                      f"{stad['premie_procent']:.1f}% t.o.v. buurten verder weg",
                      delta_color="off")
    kolom_stad.caption(f"{stad['buurten']} buurten | ruw verschil {euro(stad['ruw_verschil'])}")

kolom_platteland.subheader("Platteland")
if platteland is None:
    kolom_platteland.warning("Te weinig buurten om te vergelijken (minder dan 30 in een groep). Kies een andere afstand.")
else:
    kolom_platteland.metric("Verschil in WOZ-waarde na correctie",
                            f"{euro(platteland['premie'])} ± {euro(platteland['marge'])}",
                            f"{platteland['premie_procent']:.1f}% t.o.v. buurten verder weg",
                            delta_color="off")
    kolom_platteland.caption(f"{platteland['buurten']} buurten | ruw verschil {euro(platteland['ruw_verschil'])}")

st.subheader("Gemiddelde WOZ-waarde: dichtbij tegenover verder weg")
st.plotly_chart(grafiek_gemiddelde_woz(gemiddelde_woz(buurten)))
st.caption(f"Ja = {voorziening.lower()} binnen {grens_km} km. Dit is het verschil vóór correctie; "
           "de bedragen hierboven zijn na correctie.")

st.subheader("WOZ-waarde per afstand")
st.plotly_chart(grafiek_woz_per_afstand(woz_per_afstand(buurten), voorziening))

st.markdown(
    """
**Hoe het berekend is.** Voor de stad en het platteland apart reken ik uit hoeveel een voorziening
dichtbij scheelt in de woningwaarde. Ik vergelijk daarbij alleen buurten die op elkaar lijken: met
hetzelfde inkomen en hetzelfde percentage koopwoningen, nieuwbouw en eengezinswoningen. Zo is het
enige verschil de voorziening. Dit heet een regressie:
`woz_euro ~ dichtbij + inkomen + koopwoningen + nieuwbouw + eengezinswoningen`.

De marge (±) laat zien hoe zeker het getal is: het echte verschil ligt met 95% zekerheid binnen die
marge. Buurten zonder inkomenscijfer doen niet mee.

**Wat de data níet kan zeggen.** We weten niet hoe groot de huizen precies zijn: een boerderij is
groter dan een appartement, en dat zit maar deels in de cijfers. En we zien alleen wat samengaat,
niet wat er zou gebeuren als er morgen een nieuwe supermarkt wordt gebouwd.
"""
)
