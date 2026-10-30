import streamlit as st

from src.laden import laad_buurten
from src.analyse import VOORZIENINGEN, voeg_dichtbij_toe, euro
from src.grafieken import kaart

st.set_page_config(page_title="Kaart", layout="wide")

buurten = laad_buurten()

st.sidebar.header("Instellingen")
gemeenten = ["Heel Nederland"] + sorted(buurten["gemeente"].unique())
gekozen_gemeente = st.sidebar.selectbox("Gemeente", gemeenten,
                                        index=gemeenten.index("Overbetuwe"))
voorziening = st.sidebar.selectbox("Voorziening", list(VOORZIENINGEN.keys()))
grens_km = st.sidebar.slider("Loopafstand: binnen hoeveel km?", 0.25, 3.0, 1.0, step=0.25)
gebied = st.sidebar.radio("Gebied", ["alles", "stad", "platteland"], horizontal=True)
kleur = st.sidebar.radio("Kleur de buurten op", ["op loopafstand (ja/nee)", "WOZ-waarde"])

afstandkolom = VOORZIENINGEN[voorziening]
selectie = voeg_dichtbij_toe(buurten, afstandkolom, grens_km)
if gekozen_gemeente != "Heel Nederland":
    selectie = selectie[selectie["gemeente"] == gekozen_gemeente]
if gebied != "alles":
    selectie = selectie[selectie["gebied"] == gebied]

st.title(f"Waar ligt een {voorziening.lower()} op loopafstand?")

if len(selectie) == 0:
    st.warning("Geen buurten voor deze keuze. Kies een andere gemeente of gebied.")
    st.stop()

woz_dichtbij = selectie[selectie["dichtbij"] == 1]["woz_euro"].median()
woz_ver = selectie[selectie["dichtbij"] == 0]["woz_euro"].median()

kolom1, kolom2, kolom3, kolom4 = st.columns(4)
kolom1.metric("Buurten", len(selectie))
kolom2.metric(f"Binnen {grens_km} km", f"{selectie['dichtbij'].mean() * 100:.0f}%")
kolom3.metric("Mediane WOZ, dichtbij", euro(woz_dichtbij))
kolom4.metric("Mediane WOZ, verder weg", euro(woz_ver))

if gekozen_gemeente == "Heel Nederland":
    zoom = 6.3
    midden = {"lat": 52.2, "lon": 5.3}
else:
    zoom = 10.5
    midden = {"lat": selectie["lat"].mean(), "lon": selectie["lon"].mean()}

if kleur == "WOZ-waarde":
    kleurkolom = "woz_euro"
else:
    kleurkolom = "op_loopafstand"

st.plotly_chart(kaart(selectie, kleurkolom, zoom, midden))

st.markdown(
    """
**Conclusie:** op het platteland liggen de buurten met een supermarkt op loopafstand in de
dorpskernen, en de duurste buurten liggen eromheen in het buitengebied. Een supermarkt dichtbij
gaat daar dus samen met een lagere woningwaarde. Dat komt niet door de supermarkt, maar doordat
de dure woningen buiten de dorpskern staan. In de stad liggen bijna alle buurten dicht bij een
supermarkt, dus daar zie je op de kaart geen duidelijk patroon.
"""
)
