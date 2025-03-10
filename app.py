import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import json
import matplotlib.pyplot as plt
import numpy as np
import time
from modules.suggestions.get_brewing_suggestions import get_brewing_suggestions
from modules.extraction_chart.add_extraction_chart import add_extraction_chart
import csv


# CSV file to store sheet IDs
SHEET_REGISTRY_FILE = "coffee_tracker_sheets.csv"

# Function to load existing sheet registrations
def load_sheet_registry():
    if not os.path.exists(SHEET_REGISTRY_FILE):
        # Create the file with headers if it doesn't exist
        with open(SHEET_REGISTRY_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["email", "sheet_id", "created_date"])
        return pd.DataFrame(columns=["email", "sheet_id", "created_date"])

    return pd.read_csv(SHEET_REGISTRY_FILE)


# Function to save a new sheet registration
def save_sheet_registry(email, sheet_id):
    registry_df = load_sheet_registry()

    # Check if this email already exists
    if email in registry_df["email"].values:
        # Update existing record
        registry_df.loc[registry_df["email"] == email, "sheet_id"] = sheet_id
        registry_df.loc[
            registry_df["email"] == email, "created_date"
        ] = datetime.now().strftime("%Y-%m-%d %H:%M")
    else:
        # Add new record
        new_row = pd.DataFrame(
            {
                "email": [email],
                "sheet_id": [sheet_id],
                "created_date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
            }
        )
        registry_df = pd.concat([registry_df, new_row], ignore_index=True)

    # Save back to CSV
    registry_df.to_csv(SHEET_REGISTRY_FILE, index=False)


# Define the scope and credentials needed for Google Sheets API
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
        credentials_path = "creds.json"
        if os.path.exists(credentials_path):
            with open(credentials_path, "r") as f:
                credentials_dict = json.load(f)

            credentials = Credentials.from_service_account_info(
                credentials_dict, scopes=scope
            )
            gc = gspread.authorize(credentials)
            st.session_state["credentials"] = credentials
            return gc

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


# Reduced API calls - Cache data in session state
def load_data(gc, worksheet_name):
    """Load data from a specific worksheet with caching"""
    cache_key = f"{worksheet_name}_data"

    # Return cached data if available and not forcing refresh
    if cache_key in st.session_state and not st.session_state.get(
        "force_refresh", False
    ):
        return st.session_state[cache_key]

    try:
        sheet = gc.open_by_key(st.session_state["sheet_id"])
        worksheet = sheet.worksheet(worksheet_name)

        # Get all values directly and convert to DataFrame manually
        values = worksheet.get_all_values()
        if values:
            headers = values[0]
            data = pd.DataFrame(values[1:], columns=headers)
            data = data.dropna(how="all")  # Remove empty rows

            # Cache the data
            st.session_state[cache_key] = data
            return data
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading {worksheet_name}: {e}")
        return pd.DataFrame()

# Add this function to update the extraction calculator page
def add_brewing_suggestions_to_extraction_calculator(gc):
    """
    Add brewing suggestions to the extraction calculator page.
    """
    # Load coffee beans data
    beans_df = load_data(gc, "Beans Inventory")

    # Check if there's a selected coffee
    if (
        "selected_coffee_option" in st.session_state
        and st.session_state.selected_coffee_option
    ):
        coffee_name = st.session_state.selected_coffee_option.split(" (")[0]
        if not beans_df.empty and coffee_name in beans_df["name"].values:
            # Get varietal and process
            coffee_data = beans_df[beans_df["name"] == coffee_name].iloc[0]
            varietal = coffee_data.get("varietal", "")
            process = coffee_data.get("process", "")

            # Get brewing suggestions
            if varietal or process:
                suggestions = get_brewing_suggestions(varietal, process)

                # Display suggestions
                with st.expander("☕ AI Brewing Suggestions", expanded=True):
                    st.markdown(f"### Suggested Brewing Parameters for {coffee_name}")
                    st.markdown(f"**Based on:** {varietal} varietal, {process} process")
                    st.markdown(f"**Description:** {suggestions['description']}")
                    # st.write(suggestions)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Brew Ratio:** {suggestions['brew_ratio']}")
                        st.markdown(f"**Grind Size:** {suggestions['grind_size']}")
                        st.markdown(
                            f"**Water Temperature:** {suggestions['water_temp']}"
                        )
                    with col2:
                        st.markdown(
                            f"**Water Quality:** {suggestions['water_quality']}"
                        )
                        st.markdown(f"**Target Brew Time:** {suggestions['brew_time']}")
                        st.markdown(f"**Technique:** {suggestions['technique']}")

                    # Add a button to apply these suggestions
                    if st.button("Apply These Settings"):
                        # Parse brew ratio to calculate coffee and water amounts
                        brew_ratio = suggestions["brew_ratio"]
                        # Extract the ratio as a number, handling different formats
                        try:
                            if ":" in brew_ratio:
                                ratio_parts = brew_ratio.split(":")
                                # Handle format like "1:15.5 to 1"
                                ratio_text = ratio_parts[1].strip()
                                # Extract just the number part
                                ratio = float(ratio_text.split()[0])
                            elif "to" in brew_ratio.lower():
                                # Handle format like "1 to 15.5"
                                ratio_parts = brew_ratio.lower().split("to")
                                ratio = float(ratio_parts[1].strip())
                            else:
                                # Default case, just try to convert the whole string
                                ratio = float(brew_ratio)

                            # Set a default coffee amount and calculate water
                            coffee_amount = 15.0  # Convert to float (was 15)
                            water_amount = coffee_amount * ratio

                            # Update session state to apply these values - ensure consistent types
                            st.session_state.suggested_coffee_dose = float(
                                coffee_amount
                            )
                            st.session_state.suggested_water_amount = float(
                                water_amount
                            )

                            # For grind size, make sure it's properly handled
                            grind_text = suggestions["grind_size"]
                            if " " in grind_text:
                                grind_part = grind_text.split(" ")[0]
                            else:
                                grind_part = grind_text
                            st.session_state.suggested_grind_size = grind_part

                            st.rerun()
                        except (ValueError, IndexError) as e:
                            st.error(
                                f"Could not parse brew ratio: {brew_ratio}. Error: {str(e)}"
                            )


def save_data(gc, data_dict):
    """Save all data at once to reduce API calls"""
    try:
        sheet = gc.open_by_key(st.session_state["sheet_id"])

        # Save each dataset
        for worksheet_name, df in data_dict.items():
            worksheet = sheet.worksheet(worksheet_name)
            worksheet.clear()
            set_with_dataframe(worksheet, df)

            # Update cache
            st.session_state[f"{worksheet_name}_data"] = df

        # Reset force refresh flag
        st.session_state["force_refresh"] = False
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False


def update_coffee_inventory(beans_df, coffee_id, used_grams):
    """Update the coffee inventory by subtracting used grams"""
    if coffee_id in beans_df["id"].values:
        idx = beans_df[beans_df["id"] == coffee_id].index[0]
        beans_df.at[idx, "grams_remaining"] = (
            float(beans_df.at[idx, "grams_remaining"]) - used_grams
        )
        return True, beans_df.at[idx, "grams_remaining"], beans_df
    return False, 0, beans_df


def initialize_stopwatch():
    """Initialize stopwatch in session state if not present"""
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0
    if "elapsed_time" not in st.session_state:
        st.session_state.elapsed_time = 0
    if "running" not in st.session_state:
        st.session_state.running = False


def format_time(seconds):
    """Format time in mm:ss format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def main():
    st.set_page_config(
        page_title="Coffee Extraction & Inventory Manager",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Setup Google Sheets connection
    gc = setup_google_sheets()
    if not gc:
        st.error(
            "Google Sheets connection failed. Please ensure credentials are available."
        )
        return

    # Initialize stopwatch
    initialize_stopwatch()

    # Check if we've already set up the sheet
    if "sheet_id" not in st.session_state:
        st.title("Coffee Tracker Setup")

        # Load existing sheet registry
        registry_df = load_sheet_registry()

        # If we have saved sheets, show them for selection
        if not registry_df.empty:
            st.markdown("### Your Coffee Tracker Sheets")
            st.dataframe(registry_df[["email", "created_date"]])

            selected_email = st.selectbox(
                "Select your email to load your sheet",
                [""] + registry_df["email"].tolist(),
            )

            if selected_email and st.button("Load Existing Sheet"):
                sheet_id = registry_df[registry_df["email"] == selected_email][
                    "sheet_id"
                ].iloc[0]
                try:
                    # Test if we can open the sheet
                    gc.open_by_key(sheet_id)
                    st.session_state["sheet_id"] = sheet_id
                    st.session_state["user_email"] = selected_email
                    st.success(f"Loaded sheet for {selected_email}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not open sheet: {e}")

        # Option to create a new sheet
        st.markdown("---")
        st.markdown("### Create New Coffee Tracker")
        email = st.text_input("Enter your email to share the Coffee Tracker sheet")
        if email and st.button("Create Coffee Tracker"):
            sheet_id = create_coffee_tracker_sheet(gc, email)
            if sheet_id:
                st.session_state["sheet_id"] = sheet_id
                st.session_state["user_email"] = email
                st.success(f"Coffee Tracker sheet created and shared with {email}")
                st.rerun()

        # Option to use existing sheet ID directly
        st.markdown("---")
        st.markdown("### Or use an existing sheet")
        col1, col2 = st.columns(2)
        with col1:
            sheet_id = st.text_input("Enter your existing Google Sheet ID")
        with col2:
            sheet_email = st.text_input("Your email (for future reference)")

        if sheet_id and sheet_email and st.button("Connect to Existing Sheet"):
            try:
                # Test if we can open the sheet
                gc.open_by_key(sheet_id)
                st.session_state["sheet_id"] = sheet_id
                st.session_state["user_email"] = sheet_email

                # Save to registry for future use
                save_sheet_registry(sheet_email, sheet_id)

                st.success("Connected to existing Google Sheet")
                st.rerun()
            except Exception as e:
                st.error(f"Could not open sheet: {e}")

        return

    # Sidebar navigation (simplified)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", ["Extraction Calculator", "Beans Inventory", "Brew Log"]
    )

    # Add "sheet info" display in sidebar
    if "sheet_id" in st.session_state and "user_email" in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Your Sheet Info")
        st.sidebar.text_input(
            "Sheet ID", value=st.session_state["sheet_id"], disabled=True
        )
        st.sidebar.text_input(
            "Email", value=st.session_state["user_email"], disabled=True
        )

        if st.sidebar.button("Disconnect Sheet"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if page == "Extraction Calculator":
        extraction_calculator_page(gc)
    elif page == "Beans Inventory":
        beans_inventory_page(gc)
    elif page == "Brew Log":
        brew_log_page(gc)


def extraction_calculator_page(gc):
    st.title("Coffee Extraction Calculator")
    st.markdown(
        "This calculator helps you determine your coffee's TDS and extraction yield using a scale."
    )

    st.markdown(
        "You can access the full Google Sheet here: [Coffee Tracker Sheet](https://docs.google.com/spreadsheets/d/"
        + st.session_state["sheet_id"]
        + "/edit)"
    )
    # Load coffee beans and brewers (with caching)
    beans_df = load_data(gc, "Beans Inventory")
    brewers_df = load_data(gc, "Brewers")

    # Select coffee from inventory
    coffee_options = []
    if not beans_df.empty and "name" in beans_df.columns and "id" in beans_df.columns:
        for _, row in beans_df.iterrows():
            if pd.notna(row["name"]) and pd.notna(row["grams_remaining"]):
                remaining = float(row["grams_remaining"])
                coffee_options.append(f"{row['name']} ({remaining:.1f}g)")

    selected_coffee = None
    selected_coffee_id = None

    if coffee_options:
        selected_coffee_option = st.selectbox(
            "Select Coffee",
            [""] + coffee_options,
            key="selected_coffee_option",
            on_change=lambda: st.session_state.pop("suggested_coffee_dose", None),
        )
        if selected_coffee_option:
            coffee_name = selected_coffee_option.split(" (")[0]
            selected_coffee = coffee_name
            selected_coffee_id = beans_df[beans_df["name"] == coffee_name]["id"].values[
                0
            ]

            # Check if coffee is low on supply
            remaining = float(
                beans_df[beans_df["name"] == coffee_name]["grams_remaining"].values[0]
            )
            if remaining < 50:
                st.warning(
                    f"⚠️ Low coffee supply: Only {remaining:.1f}g remaining of {coffee_name}"
                )

            # Display brewing suggestions after coffee selection
            add_brewing_suggestions_to_extraction_calculator(gc)
    else:
        st.info(
            "No coffee beans in inventory. Please add some in the Beans Inventory page."
        )

    # Create two columns for input fields
    col1, col2 = st.columns(2)

    with col1:
        # Use suggested values if available
        default_coffee_dose = st.session_state.get("suggested_coffee_dose", 0.0)
        coffee_dose = st.number_input(
            "Coffee Dose (g)",
            min_value=0.0,
            step=0.1,
            format="%.1f",
            value=default_coffee_dose,
            help="Weight of your ground coffee",
        )

        dry_weight = st.number_input(
            "Dry Weight (g)",
            min_value=0.0,
            step=0.1,
            format="%.1f",
            help="Weight of dripper + wet filter + dry coffee",
        )

        # Use suggested values if available
        default_water = st.session_state.get("suggested_water_amount", 0.0)
        total_water = st.number_input(
            "Total Water (g)",
            min_value=0.0,
            step=0.1,
            format="%.1f",
            value=default_water,
            help="Total amount of water used for brewing",
        )

        # Use timer value or manual entry
        brew_time = ""
        brew_time = st.text_input(
            "Brew Time(mm : ss)", help="Total brewing time in minutes : seconds format"
        )

    with col2:
        beverage_weight = st.number_input(
            "Beverage Weight (g)",
            min_value=0.0,
            step=0.1,
            format="%.1f",
            help="Weight of your final brewed coffee",
        )

        wet_weight = st.number_input(
            "Wet Weight (g)",
            min_value=0.0,
            step=0.1,
            format="%.1f",
            help="Weight of dripper + wet filter + used coffee after brewing",
        )

        # Use suggested values if available
        default_grind = st.session_state.get("suggested_grind_size", "")
        grind_size = st.text_input(
            "Grind Size", value=default_grind, help="Your grinder setting"
        )

        notes = st.text_area(
            "Tasting Notes", help="Record your impressions of this brew"
        )

    # Information box
    with st.expander("How to use this calculator"):
        st.markdown(
            """
        1. Rinse your filter and place it in the dripper
        2. Add your ground coffee to the wet filter
        3. Weigh and record the dripper + wet filter + dry coffee (Dry Weight)
        4. Brew your coffee, measuring the exact amount of water used (Total Water)
        5. Weigh your brewed coffee (Beverage Weight)
        6. Weigh the dripper + wet filter + used coffee after brewing (Wet Weight)
        7. Enter your coffee dose amount separately
        """
        )

    # Calculate results only if all required inputs are provided
    # Calculate results only if all required inputs are provided
    if coffee_dose and dry_weight and total_water and beverage_weight and wet_weight:
        error = None

        # Validate inputs
        if wet_weight < dry_weight:
            error = "Wet weight must be greater than dry weight"
        elif beverage_weight > total_water:
            error = "Beverage weight cannot exceed total water used"

        if error:
            st.error(error)
        else:
            # Calculate all values using the provided formulas
            retention = wet_weight - dry_weight
            coffee_water = total_water - retention
            solids = abs(coffee_water - beverage_weight)
            tds_percent = (solids / coffee_water) * 100
            extraction_yield = (tds_percent * beverage_weight) / (
                coffee_dose - (0.035 * coffee_dose)
            )

            # Calculate brew ratio
            brew_ratio = total_water / coffee_dose

            # Display results
            st.markdown("### Results")

            # Create metrics in rows instead of columns to avoid space issues
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Water Retention", f"{retention:.1f} g")
                st.metric("Brew Ratio", f"1:{brew_ratio:.1f}")

            with col2:
                st.metric("Dissolved Solids", f"{solids:.1f} g")
                st.metric("TDS", f"{tds_percent:.2f}%")

            # Handle extraction yield separately without using delta_color
            st.markdown("#### Extraction Yield")

            # Create a colored box for the extraction yield value
            if extraction_yield < 17:
                extraction_status = "Under-extracted"
                box_color = "rgba(66, 133, 244, 0.2)"  # Light blue
                text_color = "rgb(66, 133, 244)"
            elif extraction_yield > 22:
                extraction_status = "Over-extracted"
                box_color = "rgba(234, 67, 53, 0.2)"  # Light red
                text_color = "rgb(234, 67, 53)"
            else:
                extraction_status = "Ideal range"
                box_color = "rgba(52, 168, 83, 0.2)"  # Light green
                text_color = "rgb(52, 168, 83)"

            # Custom HTML/CSS for the colored result
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-top: 0.5rem;">
                    <div style="
                        background-color: {box_color}; 
                        color: {text_color}; 
                        font-weight: bold; 
                        padding: 0.5rem 1rem; 
                        border-radius: 0.3rem;
                        font-size: 1.2rem;
                    ">
                        {extraction_yield:.2f}% - {extraction_status}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Add the extraction chart visualization
            add_extraction_chart(tds_percent, extraction_yield)

            # Display formula explanation
            with st.expander("View calculation details"):
                st.markdown(
                    """
                ### Coffee Extraction Formulas:
                - **Water Retention** = Wet Weight - Dry Weight
                - **Coffee Water** = Total Water - Water Retention
                - **Dissolved Solids** = |Coffee Water - Beverage Weight|
                - **TDS%** = (Dissolved Solids / Coffee Water) × 100
                - **Extraction Yield%** = (TDS% × Beverage Weight) / (Coffee Dose - (0.035 × Coffee Dose))
                - **Brew Ratio** = Total Water / Coffee Dose
                
                ### Interpretation:
                - **Under-extracted** (<17%): Coffee may taste sour, weak, or lacking sweetness
                - **Ideal range** (17-22%): Balanced extraction with optimal flavor
                - **Over-extracted** (>22%): Coffee may taste bitter, harsh, or astringent
                """
                )

            # Save this brew to the log - single save button that updates both datasets at once
            if st.button("Save Brew to Log"):
                if selected_coffee_id:
                    # Prepare data for bulk save
                    brew_log_df = load_data(gc, "Brew Log")
                    new_brew = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "coffee_id": selected_coffee_id,
                        "coffee_name": selected_coffee,
                        "dose": coffee_dose,
                        "total_water": total_water,
                        "brew_time": brew_time,
                        "grind_size": grind_size,
                        "tds_percent": tds_percent,
                        "extraction_yield": extraction_yield,
                        "notes": notes,
                    }

                    # Add the new brew as a new row
                    brew_log_df = pd.concat(
                        [brew_log_df, pd.DataFrame([new_brew])], ignore_index=True
                    )

                    # Update coffee inventory
                    success, remaining, updated_beans_df = update_coffee_inventory(
                        beans_df, selected_coffee_id, coffee_dose
                    )

                    if success:
                        # Save both datasets at once
                        if save_data(
                            gc,
                            {
                                "Brew Log": brew_log_df,
                                "Beans Inventory": updated_beans_df,
                            },
                        ):
                            st.success(
                                f"Brew saved! Updated {selected_coffee} inventory: {remaining:.1f}g remaining"
                            )
                            # Reset the timer after saving
                            st.session_state.elapsed_time = 0
                            st.session_state.running = False
                            # Force refresh data on next load
                            st.session_state["force_refresh"] = True
                            st.rerun()
                        else:
                            st.error("Failed to save data")
                    else:
                        st.error("Failed to update coffee inventory")
                else:
                    st.error("Please select a coffee")
    else:
        st.info("Fill in all required fields to calculate extraction yield")


def beans_inventory_page(gc):
    st.title("Coffee Beans Inventory")

    # Load existing inventory
    beans_df = load_data(gc, "Beans Inventory")

    # Form for adding new coffee
    with st.form("add_coffee_form"):
        st.markdown("### Add New Coffee")

        # Generate a unique ID for new coffee
        new_id = datetime.now().strftime("%Y%m%d%H%M%S")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Coffee Name")
            varietal = st.text_input("Varietal")
            process = st.text_input("Process")

        with col2:
            origin = st.text_input("Origin")
            roast_date = st.date_input("Roast Date")
            grams = st.number_input("Grams", min_value=0.0, step=10.0)

        notes = st.text_area("Notes")

        submit_button = st.form_submit_button("Add Coffee")

        if submit_button:
            # Create new coffee entry
            new_coffee = {
                "id": new_id,
                "name": name,
                "varietal": varietal,
                "process": process,
                "origin": origin,
                "roast_date": roast_date.strftime("%Y-%m-%d"),
                "grams_remaining": grams,
                "notes": notes,
            }

            # Add to dataframe
            beans_df = pd.concat(
                [beans_df, pd.DataFrame([new_coffee])], ignore_index=True
            )

            # Save to Google Sheets
            if save_data(gc, {"Beans Inventory": beans_df}):
                st.success(f"Added {name} to inventory!")
                st.session_state["force_refresh"] = True
                st.rerun()
            else:
                st.error("Failed to save to inventory")

    # Display current inventory
    st.markdown("### Current Inventory")

    if not beans_df.empty:
        # Sort by newest first
        if "roast_date" in beans_df.columns:
            beans_df["roast_date"] = pd.to_datetime(beans_df["roast_date"])
            beans_df = beans_df.sort_values("roast_date", ascending=False)

        # Convert to numeric if not already
        if "grams_remaining" in beans_df.columns:
            beans_df["grams_remaining"] = pd.to_numeric(
                beans_df["grams_remaining"], errors="coerce"
            )

        # Display table with highlighting for low inventory
        if "grams_remaining" in beans_df.columns:
            st.dataframe(
                beans_df.style.apply(
                    lambda x: [
                        "background-color: rgba(234, 67, 53, 0.2)"
                        if x.name == "grams_remaining" and v < 50
                        else ""
                        for i, v in enumerate(x)
                    ],
                    axis=1,
                )
            )
        else:
            st.dataframe(beans_df)

        # Add option to update coffee inventory
        st.markdown("### Update Coffee Inventory")

        # Create options list with name and ID
        options = []
        for _, row in beans_df.iterrows():
            if pd.notna(row["name"]) and pd.notna(row["id"]):
                options.append(f"{row['name']} (ID: {row['id']})")

        if options:
            selected_option = st.selectbox("Select Coffee to Update", [""] + options)

            if selected_option:
                coffee_id = selected_option.split("(ID: ")[1].split(")")[0]
                coffee_row = beans_df[beans_df["id"] == coffee_id].iloc[0]

                update_type = st.radio("Update Type", ["Add More", "Adjust Amount"])

                if update_type == "Add More":
                    add_amount = st.number_input(
                        "Grams to Add", min_value=0.0, step=10.0
                    )
                    if st.button("Save Changes"):
                        idx = beans_df[beans_df["id"] == coffee_id].index[0]
                        current = float(beans_df.at[idx, "grams_remaining"])
                        beans_df.at[idx, "grams_remaining"] = current + add_amount
                        if save_data(gc, {"Beans Inventory": beans_df}):
                            st.success(
                                f"Added {add_amount}g to {coffee_row['name']}. New total: {current + add_amount}g"
                            )
                            st.session_state["force_refresh"] = True
                            st.rerun()

                else:
                    new_amount = st.number_input(
                        "New Amount (g)",
                        min_value=0.0,
                        step=10.0,
                        value=float(coffee_row["grams_remaining"]),
                    )
                    if st.button("Save Changes"):
                        idx = beans_df[beans_df["id"] == coffee_id].index[0]
                        beans_df.at[idx, "grams_remaining"] = new_amount
                        if save_data(gc, {"Beans Inventory": beans_df}):
                            st.success(f"Updated {coffee_row['name']} to {new_amount}g")
                            st.session_state["force_refresh"] = True
                            st.rerun()
    else:
        st.info("No coffee beans in inventory. Add some using the form above.")


def brew_log_page(gc):
    st.title("Coffee Brew Log")

    # Load brew log
    brew_log_df = load_data(gc, "Brew Log")

    if not brew_log_df.empty:
        # Sort by newest first
        if "date" in brew_log_df.columns:
            brew_log_df["date"] = pd.to_datetime(brew_log_df["date"])
            brew_log_df = brew_log_df.sort_values("date", ascending=False)

        # Display the log
        st.dataframe(brew_log_df)

        # Show statistics if we have enough data
        if len(brew_log_df) > 1:
            st.markdown("### Brewing Statistics")

            # Calculate statistics
            stats_col1, stats_col2 = st.columns(2)

            with stats_col1:
                # Convert columns to numeric
                brew_log_df["extraction_yield"] = pd.to_numeric(
                    brew_log_df["extraction_yield"], errors="coerce"
                )
                brew_log_df["tds_percent"] = pd.to_numeric(
                    brew_log_df["tds_percent"], errors="coerce"
                )

                avg_extraction = brew_log_df["extraction_yield"].mean()
                avg_tds = brew_log_df["tds_percent"].mean()

                st.metric("Average Extraction Yield", f"{avg_extraction:.2f}%")
                st.metric("Average TDS", f"{avg_tds:.2f}%")

            with stats_col2:
                # Most used coffee and brewer
                if "coffee_name" in brew_log_df.columns:
                    most_used_coffee = (
                        brew_log_df["coffee_name"].value_counts().idxmax()
                    )
                    most_used_count = brew_log_df["coffee_name"].value_counts().max()
                    st.metric(
                        "Most Used Coffee",
                        f"{most_used_coffee} ({most_used_count} brews)",
                    )

                if "brewer" in brew_log_df.columns:
                    most_used_brewer = brew_log_df["brewer"].value_counts().idxmax()
                    most_used_brewer_count = brew_log_df["brewer"].value_counts().max()
                    st.metric(
                        "Most Used Brewer",
                        f"{most_used_brewer} ({most_used_brewer_count} brews)",
                    )

                # Total brews
                st.metric("Total Brews Logged", len(brew_log_df))
    else:
        st.info("No brews logged yet. Use the Extraction Calculator to record brews.")


if __name__ == "__main__":
    main()
