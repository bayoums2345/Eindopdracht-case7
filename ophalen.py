import requests
import pandas as pd

from src.schoon import maak_schoon, KOLOMMEN_NABIJHEID, KOLOMMEN_KERNCIJFERS

CBS_URL = "https://datasets.cbs.nl/odata/v1/CBS"
TABEL_NABIJHEID = "85830NED"
TABEL_KERNCIJFERS = "85618NED"
PDOK_URL = "https://service.pdok.nl/cbs/gebiedsindelingen/2023/wfs/v1_0"

MAP_RUW = "data/raw/"
MAP_SCHOON = "data/processed/"


def haal_cbs_op(url, params=None):
    rijen = []
    while url:
        antwoord = requests.get(url, params=params, timeout=60)
        antwoord.raise_for_status()
        data = antwoord.json()
        rijen = rijen + data["value"]
        url = data.get("@odata.nextLink")
        params = None
    return pd.DataFrame(rijen)


def haal_observaties_op(tabel, codes):
    code_filter = " or ".join(f"Measure eq '{code}'" for code in codes)
    filter_tekst = f"({code_filter}) and startswith(WijkenEnBuurten,'BU')"
    url = f"{CBS_URL}/{tabel}/Observations"
    return haal_cbs_op(url, params={"$filter": filter_tekst})


def haal_buurtpunten_op():
    rijen = []
    start = 0
    while True:
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeNames": "gebiedsindelingen:buurt_labelpoint",
            "outputFormat": "json",
            "srsName": "EPSG:4326",
            "count": 1000,
            "startIndex": start,
        }
        antwoord = requests.get(PDOK_URL, params=params, timeout=60)
        antwoord.raise_for_status()
        punten = antwoord.json()["features"]
        if len(punten) == 0:
            break
        for punt in punten:
            rijen.append({
                "buurtcode": punt["properties"]["statcode"],
                "lon": punt["geometry"]["coordinates"][0],
                "lat": punt["geometry"]["coordinates"][1],
            })
        start = start + 1000
    return pd.DataFrame(rijen)


if __name__ == "__main__":
    print("Nabijheid voorzieningen ophalen...")
    nabijheid = haal_observaties_op(TABEL_NABIJHEID, KOLOMMEN_NABIJHEID.keys())
    nabijheid.to_csv(MAP_RUW + "nabijheid_lang.csv", index=False)
    print(f"  {len(nabijheid)} rijen")

    print("Kerncijfers wijken en buurten ophalen...")
    kerncijfers = haal_observaties_op(TABEL_KERNCIJFERS, KOLOMMEN_KERNCIJFERS.keys())
    kerncijfers.to_csv(MAP_RUW + "kerncijfers_lang.csv", index=False)
    print(f"  {len(kerncijfers)} rijen")

    print("Codeboeken ophalen...")
    codeboek_maten = pd.concat([
        haal_cbs_op(f"{CBS_URL}/{TABEL_NABIJHEID}/MeasureCodes"),
        haal_cbs_op(f"{CBS_URL}/{TABEL_KERNCIJFERS}/MeasureCodes"),
    ])
    codeboek_maten.to_csv(MAP_RUW + "codeboek_maten.csv", index=False)
    codeboek_regios = haal_cbs_op(f"{CBS_URL}/{TABEL_KERNCIJFERS}/WijkenEnBuurtenCodes")
    codeboek_regios.to_csv(MAP_RUW + "codeboek_regios.csv", index=False)

    print("Buurtpunten ophalen bij PDOK...")
    punten = haal_buurtpunten_op()
    punten.to_csv(MAP_RUW + "buurtpunten.csv", index=False)
    print(f"  {len(punten)} punten")

    print("Schoon bestand maken...")
    buurten = maak_schoon(nabijheid, kerncijfers, codeboek_regios, punten)
    buurten.to_csv(MAP_SCHOON + "buurten.csv", index=False)
    print(f"Klaar: {len(buurten)} buurten in {MAP_SCHOON}buurten.csv")
