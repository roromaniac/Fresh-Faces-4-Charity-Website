import os
import json
import pandas as pd

from collections import OrderedDict

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

SHEET_ID = os.getenv("PUBLIC_QUALIFIER_SHEET_ID")
RANGE_NAME = "Simplified Responses!A2:G"
NUM_QUALIFIERS = 24

def qualifier_population(qualifier_dataframe: pd.DataFrame):
    """
    Creates an Excel file with NUM_QUALIFIERS sheets showing MAIN and WAITLIST.
    Choices 1, 2, and 3 have equal rank. The first 24 unique Twitch names to
    select a qualifier in any choice go to MAIN, ordered by signup timestamp.
    Explicit waitlist signups and overflow choice signups share one WAITLIST,
    ordered together by timestamp, excluding anyone already in MAIN.
    Each Twitch name appears once per qualifier, using its earliest eligible
    signup. Equal timestamps retain the input row order.
    """
    OUTDIR = "data"
    OUTPATH = os.path.join(OUTDIR, "qualifiers.xlsx")

    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    # Sort once so both MAIN and WAITLIST follow timestamp order.
    df = qualifier_dataframe.copy()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values("Timestamp", kind="stable")

    with pd.ExcelWriter(OUTPATH, engine="xlsxwriter") as writer:
        for qualifier_num in range(1, NUM_QUALIFIERS + 1):
            qstr = str(qualifier_num)

            # All three choices have equal rank.
            mask_choices = (
                (df["Choice 1"] == qstr) | (df["Choice 2"] == qstr) | (df["Choice 3"] == qstr)
            )
            mask_waitlist = (df["Waitlist"] == qstr)

            # Duplicate registrations must not consume extra MAIN slots.
            choice_signups = df[mask_choices].drop_duplicates(subset=["Twitch"], keep="first")
            main_df = choice_signups.iloc[:24]
            main_names = list(main_df["Twitch"])

            # After excluding MAIN, matching choice signups are overflow.
            # Select both waitlist sources together to preserve chronological order.
            waitlist_df = df[
                (mask_waitlist | mask_choices) & ~df["Twitch"].isin(main_names)
            ]
            waitlist_df = waitlist_df.drop_duplicates(subset=["Twitch"], keep="first")
            waitlist_names = list(waitlist_df["Twitch"])

            # Create DataFrame with two columns: "MAIN" and "WAITLIST"
            sheet_dict = OrderedDict()
            max_rows = max(len(main_names), len(waitlist_names))
            sheet_dict["MAIN"] = main_names + [""] * (max_rows - len(main_names))
            sheet_dict["WAITLIST"] = waitlist_names + [""] * (max_rows - len(waitlist_names))
            sheet_df = pd.DataFrame(sheet_dict)

            sheet_name = f"Qualifier {qualifier_num}"
            sheet_df.to_excel(writer, index=False, sheet_name=sheet_name)
    
def main():
    # Load credentials info as a dict from env variable exactly as in visit_state.py
    raw_creds = os.getenv("SERVICE_ACCOUNT_JSON")
    if not raw_creds:
        raise RuntimeError("Missing SERVICE_ACCOUNT_JSON")
    creds_info = json.loads(raw_creds)

    try:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=SCOPES,
        )

        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        result = (
            sheet.values()
            .get(spreadsheetId=SHEET_ID, range=RANGE_NAME)
            .execute()
        )
        columns = [
            "Timestamp",
            "Twitch",
            "Discord",
            "Choice 1",
            "Choice 2",
            "Choice 3",
            "Waitlist",
        ]
        values = result.get("values", [])
        qual_df = pd.DataFrame(values, columns=columns)
        qualifier_population(qual_df)
        print(qual_df.head())
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()