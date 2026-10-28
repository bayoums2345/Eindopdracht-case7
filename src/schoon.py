import pandas as pd

KOLOMMEN_NABIJHEID = {
    "D000025": "afstand_supermarkt",
    "D000028": "afstand_huisarts",
    "D000029": "afstand_kinderdagverblijf",
    "D000052": "afstand_treinstation",
}

KOLOMMEN_KERNCIJFERS = {
    "M001642": "woz",
    "M000224": "inkomen",
    "M000100": "dichtheid",
    "1014800_1": "koopwoningen",
    "ZW25807": "nieuwbouw",
    "ZW10290": "eengezinswoningen",
    "ST0001": "stedelijkheid",
    "T001036": "inwoners",
}


def lang_naar_breed(df_lang, kolomnamen):
    df_lang = df_lang.copy()
    df_lang["WijkenEnBuurten"] = df_lang["WijkenEnBuurten"].str.strip()
    df_lang["Measure"] = df_lang["Measure"].str.strip()

    breed = df_lang.pivot(index="WijkenEnBuurten", columns="Measure", values="Value")
    breed = breed.rename(columns=kolomnamen)
    breed = breed.reset_index()
    breed = breed.rename(columns={"WijkenEnBuurten": "buurtcode"})
    breed.columns.name = None
    return breed


def voeg_namen_toe(df, codeboek_regios):
    namen = dict(zip(codeboek_regios["Identifier"].str.strip(),
                     codeboek_regios["Title"].str.strip()))
    df = df.copy()
    df["buurtnaam"] = df["buurtcode"].map(namen)
    df["gemeentecode"] = "GM" + df["buurtcode"].str[2:6]
    df["gemeente"] = df["gemeentecode"].map(namen)
    return df


def koppel(nabijheid, kerncijfers, punten):
    df = nabijheid.merge(kerncijfers, on="buurtcode", how="inner",
                         validate="one_to_one")
    df = df.merge(punten, on="buurtcode", how="left", validate="one_to_one")
    return df


def verwijder_lege_rijen(df):
    return df.dropna(subset=["woz", "afstand_supermarkt", "stedelijkheid"])


def maak_schoon(nabijheid_lang, kerncijfers_lang, codeboek_regios, punten):
    nabijheid = lang_naar_breed(nabijheid_lang, KOLOMMEN_NABIJHEID)
    kerncijfers = lang_naar_breed(kerncijfers_lang, KOLOMMEN_KERNCIJFERS)
    df = koppel(nabijheid, kerncijfers, punten)
    df = voeg_namen_toe(df, codeboek_regios)
    df = verwijder_lege_rijen(df)
    return df
