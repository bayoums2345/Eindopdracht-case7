import plotly.express as px

KLEUR_LOOPAFSTAND = {"ja": "#0f626d", "nee": "#d9822b"}
KLEUR_GEBIED = {"stad": "#4c4f9e", "platteland": "#8aa63a"}


def grafiek_gemiddelde_woz(tabel):
    fig = px.bar(tabel, x="gebied", y="woz_euro", color="op_loopafstand", barmode="group",
                 text_auto=",.0f", color_discrete_map=KLEUR_LOOPAFSTAND,
                 category_orders={"op_loopafstand": ["ja", "nee"], "gebied": ["stad", "platteland"]},
                 labels={"woz_euro": "gemiddelde WOZ-waarde (€)", "gebied": "",
                         "op_loopafstand": "op loopafstand"})
    return fig


def grafiek_woz_per_afstand(tabel, voorziening):
    fig = px.line(tabel, x="afstand_afgerond", y="woz_euro", color="gebied",
                  markers=True, color_discrete_map=KLEUR_GEBIED,
                  category_orders={"gebied": ["stad", "platteland"]},
                  labels={"afstand_afgerond": f"afstand tot {voorziening.lower()} (km, afgerond)",
                          "woz_euro": "mediane WOZ-waarde (€)", "gebied": ""})
    return fig


def kaart(df, kleurkolom, zoom, midden):
    if kleurkolom == "op_loopafstand":
        fig = px.scatter_map(df, lat="lat", lon="lon", color="op_loopafstand",
                             color_discrete_map=KLEUR_LOOPAFSTAND,
                             hover_name="buurtnaam", hover_data=["gemeente", "woz_euro"],
                             zoom=zoom, center=midden, height=620)
    else:
        fig = px.scatter_map(df, lat="lat", lon="lon", color="woz_euro",
                             range_color=[150000, 800000],
                             hover_name="buurtnaam", hover_data=["gemeente", "woz_euro"],
                             zoom=zoom, center=midden, height=620)
    fig.update_traces(marker_size=6)
    return fig
