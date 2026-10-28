import statsmodels.formula.api as smf

VOORZIENINGEN = {
    "Supermarkt": "afstand_supermarkt",
    "Huisartsenpraktijk": "afstand_huisarts",
    "Kinderdagverblijf": "afstand_kinderdagverblijf",
    "Treinstation": "afstand_treinstation",
}

CONTROLES = ["inkomen", "koopwoningen", "nieuwbouw", "eengezinswoningen"]


def voeg_kolommen_toe(df):
    df = df.copy()
    df["woz_euro"] = df["woz"] * 1000
    df["gebied"] = "platteland"
    df.loc[df["stedelijkheid"] <= 3, "gebied"] = "stad"
    return df


def voeg_dichtbij_toe(df, afstandkolom, grens_km):
    df = df.copy()
    df["dichtbij"] = (df[afstandkolom] <= grens_km).astype(int)
    df["op_loopafstand"] = df["dichtbij"].map({1: "ja", 0: "nee"})
    df["afstand_afgerond"] = df[afstandkolom].round()
    return df


def bereken_premie(df):
    df = df.dropna(subset=CONTROLES)

    aantal_dichtbij = (df["dichtbij"] == 1).sum()
    aantal_ver = (df["dichtbij"] == 0).sum()
    if aantal_dichtbij < 30 or aantal_ver < 30:
        return None

    gemiddeld_ver = df[df["dichtbij"] == 0]["woz_euro"].mean()
    gemiddeld_dichtbij = df[df["dichtbij"] == 1]["woz_euro"].mean()

    formule = "woz_euro ~ dichtbij + inkomen + koopwoningen + nieuwbouw + eengezinswoningen"
    model = smf.ols(formule, data=df).fit()

    premie = model.params["dichtbij"]
    marge = 1.96 * model.bse["dichtbij"]

    return {
        "buurten": len(df),
        "ruw_verschil": gemiddeld_dichtbij - gemiddeld_ver,
        "premie": premie,
        "marge": marge,
        "premie_procent": premie / gemiddeld_ver * 100,
    }


def premie_per_gebied(df):
    resultaten = {}
    resultaten["stad"] = bereken_premie(df[df["gebied"] == "stad"])
    resultaten["platteland"] = bereken_premie(df[df["gebied"] == "platteland"])
    return resultaten


def gemiddelde_woz(df):
    df = df.dropna(subset=CONTROLES)
    tabel = df.groupby(["gebied", "op_loopafstand"])["woz_euro"].agg(["mean", "count"])
    tabel = tabel.reset_index()
    tabel = tabel[tabel["count"] >= 30]
    tabel = tabel.rename(columns={"mean": "woz_euro"})
    return tabel


def woz_per_afstand(df):
    df = df[df["afstand_afgerond"] <= 10]
    tabel = df.groupby(["gebied", "afstand_afgerond"])["woz_euro"].agg(["median", "count"])
    tabel = tabel.reset_index()
    tabel = tabel[tabel["count"] >= 30]
    tabel = tabel.rename(columns={"median": "woz_euro"})
    return tabel


def euro(bedrag):
    return f"€ {bedrag:,.0f}".replace(",", ".")
