import pandas as pd
import streamlit as st

from src.laden import laad_buurten
from src.schoon import KOLOMMEN_NABIJHEID, KOLOMMEN_KERNCIJFERS

st.set_page_config(page_title="Data", layout="wide")

buurten = laad_buurten()

st.title("Data en verantwoording")

with open("data_verantwoording.md", encoding="utf-8") as bestand:
    st.markdown(bestand.read())

st.subheader("Codeboek van de gebruikte kolommen")
kolomnamen = KOLOMMEN_NABIJHEID | KOLOMMEN_KERNCIJFERS
codeboek = pd.read_csv("data/raw/codeboek_maten.csv")
codeboek = codeboek[codeboek["Identifier"].isin(kolomnamen.keys())]
codeboek = codeboek.drop_duplicates(subset="Identifier")
codeboek["kolom in dashboard"] = codeboek["Identifier"].map(kolomnamen)
st.dataframe(codeboek[["Identifier", "kolom in dashboard", "Title", "Unit"]], hide_index=True)

st.subheader("De schone tabel")
gemeenten = ["Alle gemeenten"] + sorted(buurten["gemeente"].unique())
gekozen_gemeente = st.selectbox("Gemeente", gemeenten)
selectie = buurten
if gekozen_gemeente != "Alle gemeenten":
    selectie = buurten[buurten["gemeente"] == gekozen_gemeente]

st.caption(f"{len(selectie)} buurten | {selectie['inkomen'].isna().sum()} zonder inkomenscijfer")
st.dataframe(selectie, hide_index=True)
