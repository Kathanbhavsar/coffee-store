from get_brewing_suggestions import get_brewing_suggestions
import streamlit as st
import pandas as pd
from app.py import load_data, save_data, update_coffee_inventory

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
