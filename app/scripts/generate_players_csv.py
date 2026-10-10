import pandas as pd
import os

from datetime import datetime

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

responses = pd.read_csv("data/FF4_Responses.csv")
responses.columns = ["timestamp", "discord_name", "twitch_name", "display_name", "division", "country", "pronouns", "a1", "a2", "a3", "code"]

display_csv = pd.DataFrame(columns=["display_name", "ttv_name | pronouns", "country"])

COMMON_COUNTRYENTRIES = {
    "america": "US",
    "North America": "US",
    "America": "US",
    "USA": "US",
    "United States": "US",
    "United States of America": "US",
    "United Kingdom": "UK",
    "United Kingdome": "UK",
    "England": "EN",
    "Canada": "CA",
    "Australia": "AU",
    "New Zealand": "NZ",
    "South Africa": "ZA",
    "India": "IN",
    "China": "CN",
    "Japan": "JP",
    "Korea": "KR",
    "Russia": "RU",
    "Germany": "DE",
    "France": "FR",
    "Italy": "IT",
    "Spain": "ES",
    "Netherlands": "NL",
    "Belgium": "BE",
    "Belgium ": "BE",
    "Switzerland": "CH",
    "Austria": "AT",
    "Sweden": "SE",
    "Norway": "NO",
    "Mexico": "MX",
    "Brazil": "BR",
    "Brasil": "BR",
    "Argentina": "AR",
    "CL (chile)": "CL",
    "Chile": "CL",
    "Colombia": "CO",
    "Colombia ": "CO",
    "Peru": "PE",
    "Venezuela": "VE",
    "Ecuador": "EC",
    "Bolivia": "BO",
    "Paraguay": "PY",
    "Uruguay": "UY",
    "Denmark": "DK",
    "Bosnia and Herzegovina": "BA",
    "Bosnia": "BA",
    "Kosovo": "XK",
    "Ireland": "IE",
    "Republic of Ireland": "IE",
    "can you put the lgbt flag, i think that would be funny. if not then N/A": "PRIDE",
    "Can you put a trans flag? otherwise N/A": "PRIDE",
    "Peru": "PE",
    "Bretagne (or France if you don't find the Bretagne flag)": "FR",
    "USA, unless you can put the Trans flag instead.": "PRIDE",
    "Scotland": "SL",
    "ENGLAND BRUV": "EN",
    "USA or N/A Whatever looks better": "US",
    "Portugal": "PT",
    "French": "FR",
    "Malaysia": "MY",
    "USA/Panama": "US",
    "Zamunda": "ZX",
    "Panama": "PA"
}

def get_pronouns(pronouns_string):
    slash_split = pronouns_string.split("/")[:2]
    if len(slash_split) == 2:
        return "/".join(slash_split)
    else:
        return ""

for idx, player in responses.iterrows():
    pronouns = get_pronouns(player["pronouns"])
    display_csv.loc[idx, "display_name"] = player["display_name"]
    display_csv.loc[idx, "ttv_name | pronouns"] = "ttv/" + player["twitch_name"] + ((" | " + pronouns) if pronouns != "" else "")
    display_csv.loc[idx, "country"] = COMMON_COUNTRYENTRIES.get(player["country"], None)

safe_now = NOW.replace(":", "-")
os.makedirs(f"data/{safe_now}", exist_ok=True)
display_csv.to_csv(f"data/{safe_now}/players.csv", index=False)