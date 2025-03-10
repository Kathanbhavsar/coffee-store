import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()


def setup_google_sheets():
    # Create a connection to Google Sheets
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    # Check if credentials are already in session state
    if "credentials" in st.session_state:
        credentials = st.session_state["credentials"]
        try:
            return gspread.authorize(credentials)
        except Exception as e:
            st.error(f"Error connecting to Google Sheets: {e}")
            return None

    # Try to load credentials from different sources
    try:
        # First try local file
        credentials = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        # if os.path.exists(credentials_path):
        #     with open(credentials_path, "r") as f:
        #         credentials_dict = json.load(f)

        #     credentials = Credentials.from_service_account_info(
        #         credentials_dict, scopes=scope
        #     )
        #     gc = gspread.authorize(credentials)
        #     st.session_state["credentials"] = credentials
        #     return gc

        # Fall back to secrets if available
        credentials_dict = st.secrets["gcp_service_account"]
        credentials = Credentials.from_service_account_info(
            credentials_dict, scopes=scope
        )
        gc = gspread.authorize(credentials)
        st.session_state["credentials"] = credentials
        return gc
    except Exception as e:
        st.error(f"Error loading credentials: {e}")
        return None


def create_coffee_tracker_sheet(gc, email):
    """Create and initialize the Coffee Tracker Google Sheet"""
    try:
        # Create a new Google Sheet
        sheet = gc.create("Coffee Tracker")
        sheet.share(email, perm_type="user", role="writer")

        # Create worksheets for beans, brew logs, and brewers
        beans_worksheet = sheet.add_worksheet(
            title="Beans Inventory", rows=1000, cols=20
        )
        brew_log_worksheet = sheet.add_worksheet(title="Brew Log", rows=1000, cols=20)
        brewers_worksheet = sheet.add_worksheet(title="Brewers", rows=1000, cols=10)

        # Initialize beans inventory headers
        beans_data = pd.DataFrame(
            {
                "id": [],
                "name": [],
                "varietal": [],
                "process": [],
                "origin": [],
                "roast_date": [],
                "grams_remaining": [],
                "notes": [],
            }
        )
        set_with_dataframe(beans_worksheet, beans_data)

        # Initialize brew log headers
        brew_log_data = pd.DataFrame(
            {
                "date": [],
                "coffee_id": [],
                "coffee_name": [],
                "dose": [],
                "total_water": [],
                "grind_size": [],
                "tds_percent": [],
                "extraction_yield": [],
                "notes": [],
            }
        )
        set_with_dataframe(brew_log_worksheet, brew_log_data)

        # Initialize brewers
        brewers_data = pd.DataFrame(
            {"id": [], "name": [], "type": [], "capacity": [], "notes": []}
        )
        set_with_dataframe(brewers_worksheet, brewers_data)

        # Delete default Sheet1
        default_worksheet = sheet.get_worksheet(0)
        sheet.del_worksheet(default_worksheet)

        # Save to registry
        save_sheet_registry(email, sheet.id)

        return sheet.id
    except Exception as e:
        st.error(f"Error creating Google Sheet: {e}")
        return None