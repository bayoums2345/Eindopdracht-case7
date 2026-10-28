import pandas as pd
import streamlit as st

from src.analyse import voeg_kolommen_toe

BESTAND = "data/processed/buurten.csv"


@st.cache_data
def laad_buurten():
    df = pd.read_csv(BESTAND)
    df = voeg_kolommen_toe(df)
    return df
