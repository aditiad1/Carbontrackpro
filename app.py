import streamlit as st

# Get query params for embedded mode
# Need to do this before st.set_page_config
import re
from urllib.parse import parse_qs

# Get URL query parameters for embedding functionality
query_params = st.query_params

# Check if we're in embedded mode
embedded = False
if 'embed' in query_params:
    embed_value = query_params.get('embed')
    if isinstance(embed_value, list) and len(embed_value) > 0:
        embedded = embed_value[0].lower() == 'true'
    else:
        embedded = str(embed_value).lower() == 'true'

# Get theme preference
theme = 'light'
if 'theme' in query_params:
    theme_value = query_params.get('theme')
    if isinstance(theme_value, list) and len(theme_value) > 0:
        theme = theme_value[0]
    else:
        theme = str(theme_value)

# Check if branding should be shown
show_branding = True
if 'showBranding' in query_params:
    branding_value = query_params.get('showBranding')
    if isinstance(branding_value, list) and len(branding_value) > 0:
        show_branding = branding_value[0].lower() == 'true'
    else:
        show_branding = str(branding_value).lower() == 'true'

# Check for parent website for customization
parent_site = None
if 'parentSite' in query_params:
    parent_value = query_params.get('parentSite')
    if isinstance(parent_value, list) and len(parent_value) > 0:
        parent_site = parent_value[0].lower()
    else:
        parent_site = str(parent_value).lower()

# Special handling for Earth Carbon Foundation
is_earth_carbon = parent_site == 'earthcarbonfoundation.org'

# Page configuration - must be called first
st.set_page_config(
    page_title="Carbon Footprint Calculator",
    page_icon="🌍",
    layout="centered" if embedded else "wide",
    initial_sidebar_state="collapsed" if embedded else "expanded"
)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import os
import json

# Import custom modules
import ghg_protocol as ghg
import emission_factors as ef
import visualizations as viz
import recommendations as rec
import database as db
import history
import carbon_offsets as co
import report_generator as report
import eco_challenge as eco

# We already have the query parameters defined at the top

# Original page config already set at top
# No need to update layout dynamically - the embedded CSS will take care of appearance

# Custom CSS for embedded mode
if embedded:
    # Define CSS based on theme
    if theme == 'dark':
        background_color = "#121212"
        text_color = "#f1f1f1"
        card_bg_color = "#1e1e1e"
        border_color = "#333333"
    else:  # light theme
        background_color = "#ffffff"
        text_color = "#333333"
        card_bg_color = "#f9f9f9"
        border_color = "#e0e0e0"
    
    # Earth Carbon Foundation custom theme
    if is_earth_carbon:
        button_color = "#336633"  # Earth green
        button_hover_color = "#254D25"  # Darker green
    else:
        button_color = "#4CAF50"  # Default green
        button_hover_color = "#45a049"  # Default hover
    
    # Apply CSS
    st.markdown(f"""
    <style>
        .embedded-calculator {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: {text_color};
            background-color: {background_color};
        }}
        .stApp {{
            background-color: {background_color};
        }}
        /* Make input fields wider to accommodate 10 digits */
        input[type="number"] {{
            width: 100% !important;
            min-width: 180px !important;
        }}
        div.stNumberInput > div {{
            width: 100% !important;
        }}
        /* Custom button styling */
        div.stButton > button {{
            background-color: {button_color};
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }}
        div.stButton > button:hover {{
            background-color: {button_hover_color};
        }}
        /* Card styling */
        .metric-card {{
            background-color: {card_bg_color};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 15px;
            margin: 5px 0;
        }}
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            border-radius: 5px 5px 0 0;
            padding: 10px 20px;
            background-color: {card_bg_color};
        }}
        /* Download button styling */
        .download-button {{
            display: inline-block;
            background-color: {button_color};
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 10px;
            cursor: pointer;
        }}
        .download-button:hover {{
            background-color: {button_hover_color};
        }}
    </style>
    <div class="embedded-calculator"></div>
    """, unsafe_allow_html=True)

# Main title
st.title("Carbon Footprint Calculator")

# More compact sidebar with essential information
with st.sidebar:
    st.header("GHG Protocol Scopes")
    st.markdown("""
    **Scope 1**: Direct emissions (owned sources) \n
    **Scope 2**: Indirect emissions (purchased energy) \n
    **Scope 3**: Value chain emissions
    """)
    
    # If in embedded mode and showing branding is enabled
    if embedded and show_branding:
        st.markdown("---")
        
        # Special branding for Earth Carbon Foundation
        if is_earth_carbon:
            st.markdown("<div style='text-align: center; opacity: 0.8;'>Provided by<br/>Earth Carbon Foundation</div>", 
                        unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; opacity: 0.7;'>Powered by<br/>Carbon Footprint App</div>", 
                        unsafe_allow_html=True)
                        
        # Get current URL and remove query parameters for the full app URL
        from urllib.parse import urlparse
        import os
        
        # Try to get the app URL from environment or fallback to a request-based approach
        try:
            base_url = os.environ.get('REPLIT_URL', '')
            if not base_url:
                # Try alternative ways to get the URL
                from streamlit.web.server.server import Server
                base_url = Server.get_current().get_base_url()
                
            # If still no URL, use a basic fallback
            if not base_url:
                base_url = './'
        except:
            base_url = './'
        
        # Custom link text for different sites    
        link_text = "Open calculator in new window"
        if is_earth_carbon:
            link_text = "View full Earth Carbon Calculator"
            
        st.markdown(f"<div style='text-align: center; font-size: 0.8em;'><a href='{base_url}' target='_blank'>{link_text}</a></div>", 
                    unsafe_allow_html=True)

# Initialize session state for storing results
if 'total_emissions' not in st.session_state:
    st.session_state.total_emissions = 0
if 'emissions_by_scope' not in st.session_state:
    st.session_state.emissions_by_scope = {"Scope 1": 0, "Scope 2": 0, "Scope 3": 0}
if 'emissions_by_category' not in st.session_state:
    st.session_state.emissions_by_category = {}
if 'input_complete' not in st.session_state:
    st.session_state.input_complete = False

# Add Eco-Challenge CSS
eco.add_eco_challenge_css()

# Main content - Hide history tab in embedded mode
if embedded:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Input Data", "Results Dashboard", "Recommendations", "Carbon Offsets", "Eco-Challenge"])
else:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Input Data", "Results Dashboard", "Recommendations", "Carbon Offsets", "Eco-Challenge", "History"])

# Input Data Tab
with tab1:
    st.header("Enter Your Emissions Data")
    
    # Organization information
    st.subheader("Organization Information")
    col1, col2 = st.columns(2)
    with col1:
        organization_name = st.text_input("Organization Name")
        industry = st.selectbox("Industry", 
                              ["Manufacturing", "Technology", "Retail", "Healthcare", 
                               "Education", "Financial Services", "Food & Beverage", "Other"])
    with col2:
        reporting_year = st.selectbox("Reporting Year", list(range(2023, 2015, -1)))
        num_employees = st.number_input("Number of Employees", min_value=1, step=1)
    
    # Scope 1 Emissions (Direct)
    st.subheader("Scope 1: Direct Emissions")
    
    st.markdown("##### Stationary Combustion")
    col1, col2 = st.columns(2)
    with col1:
        natural_gas = st.number_input("Natural Gas (m³)", min_value=0.0, step=100.0)
        diesel = st.number_input("Diesel (liters)", min_value=0.0, step=100.0)
    with col2:
        propane = st.number_input("Propane (liters)", min_value=0.0, step=100.0)
        fuel_oil = st.number_input("Fuel Oil (liters)", min_value=0.0, step=100.0)
    
    st.markdown("##### Mobile Combustion (Company Vehicles)")
    col1, col2 = st.columns(2)
    with col1:
        gasoline = st.number_input("Gasoline (liters)", min_value=0.0, step=100.0)
        diesel_vehicles = st.number_input("Diesel for Vehicles (liters)", min_value=0.0, step=100.0)
    with col2:
        jet_fuel = st.number_input("Jet Fuel (liters)", min_value=0.0, step=100.0)
        
    st.markdown("##### Refrigerants & Process Emissions")
    col1, col2 = st.columns(2)
    with col1:
        refrigerant_options = ["R-134a", "R-410A", "R-404A", "R-22", "None"]
        refrigerant_type = st.selectbox("Refrigerant Type", refrigerant_options)
        if refrigerant_type != "None":
            refrigerant_amount = st.number_input(f"{refrigerant_type} Leakage (kg)", min_value=0.0, step=0.1)
        else:
            refrigerant_amount = 0.0
    
    # Scope 2 Emissions (Indirect - Electricity)
    st.subheader("Scope 2: Indirect Emissions from Purchased Energy")
    
    electricity_source = st.radio(
        "Electricity Source",
        ["Grid Electricity", "Renewable Energy", "Mixed Sources"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        electricity = st.number_input("Electricity Consumption (kWh)", min_value=0.0, step=1000.0)
    with col2:
        grid_region = st.selectbox("Grid Region", 
                                ["Northeast US", "Midwest US", "South US", "West US", 
                                 "Western Europe", "Eastern Europe", "Asia", "Other"])
    
    # Scope 3 Emissions (Other Indirect)
    st.subheader("Scope 3: Other Indirect Emissions")
    
    st.markdown("##### Business Travel")
    col1, col2 = st.columns(2)
    with col1:
        air_travel_short = st.number_input("Short-haul Flights (<500 miles) - Passenger Miles", min_value=0.0, step=1000.0)
        air_travel_medium = st.number_input("Medium-haul Flights (500-1500 miles) - Passenger Miles", min_value=0.0, step=1000.0)
        air_travel_long = st.number_input("Long-haul Flights (>1500 miles) - Passenger Miles", min_value=0.0, step=1000.0)
    with col2:
        car_rental = st.number_input("Car Rental - Miles", min_value=0.0, step=100.0)
        hotel_stays = st.number_input("Hotel Stays - Room Nights", min_value=0, step=10)
    
    st.markdown("##### Employee Commuting")
    col1, col2 = st.columns(2)
    with col1:
        avg_commute_distance = st.number_input("Average Daily Commute Distance (miles)", min_value=0.0, step=1.0)
    with col2:
        commute_days_per_year = st.number_input("Work Days Per Year", min_value=0, max_value=365, value=230)
        
    commute_mode = st.selectbox(
        "Primary Commute Mode",
        ["Car (Single Occupancy)", "Carpool", "Public Transit", "Walking/Biking", "Work from Home", "Mixed"]
    )
    
    # Initialize variables with default values (these will be overwritten if Mixed mode is selected)
    car_percent = 0
    carpool_percent = 0
    public_transit_percent = 0
    walking_biking_percent = 0
    wfh_percent = 0
    
    if commute_mode == "Mixed":
        st.markdown("##### Commute Mode Breakdown")
        col1, col2 = st.columns(2)
        with col1:
            car_percent = st.slider("Car (Single Occupancy) %", 0, 100, 30)
            carpool_percent = st.slider("Carpool %", 0, 100, 20)
            public_transit_percent = st.slider("Public Transit %", 0, 100, 30)
        with col2:
            walking_biking_percent = st.slider("Walking/Biking %", 0, 100, 10)
            wfh_percent = st.slider("Work from Home %", 0, 100, 10)
            
            # Ensure total is 100%
            total_percent = car_percent + carpool_percent + public_transit_percent + walking_biking_percent + wfh_percent
            if total_percent != 100:
                st.warning(f"Percentages should total 100%. Current total: {total_percent}%")
    
    st.markdown("##### Waste Generation")
    col1, col2 = st.columns(2)
    with col1:
        landfill_waste = st.number_input("Landfill Waste (tons)", min_value=0.0, step=1.0)
        recycled_waste = st.number_input("Recycled Waste (tons)", min_value=0.0, step=1.0)
    with col2:
        composted_waste = st.number_input("Composted Waste (tons)", min_value=0.0, step=1.0)
        incinerated_waste = st.number_input("Incinerated Waste (tons)", min_value=0.0, step=1.0)
    
    st.markdown("##### Purchased Goods and Services")
    purchased_goods = st.number_input("Annual Procurement Spend ($)", min_value=0, step=10000)
    
    # Calculate Button
    calculate_button = st.button("Calculate Carbon Footprint")
    
    if calculate_button:
        with st.spinner("Calculating your carbon footprint..."):
            # Calculate Scope 1 emissions
            scope1_stationary = ghg.calculate_stationary_combustion(
                natural_gas=natural_gas,
                diesel=diesel,
                propane=propane,
                fuel_oil=fuel_oil
            )
            
            scope1_mobile = ghg.calculate_mobile_combustion(
                gasoline=gasoline,
                diesel=diesel_vehicles,
                jet_fuel=jet_fuel
            )
            
            scope1_refrigerants = ghg.calculate_refrigerant_emissions(
                refrigerant_type=refrigerant_type,
                amount=refrigerant_amount
            )
            
            # Calculate Scope 2 emissions
            scope2_electricity = ghg.calculate_electricity_emissions(
                electricity=electricity,
                grid_region=grid_region,
                electricity_source=electricity_source
            )
            
            # Calculate Scope 3 emissions
            scope3_business_travel = ghg.calculate_business_travel_emissions(
                air_travel_short=air_travel_short,
                air_travel_medium=air_travel_medium,
                air_travel_long=air_travel_long,
                car_rental=car_rental,
                hotel_stays=hotel_stays
            )
            
            scope3_employee_commuting = ghg.calculate_employee_commuting_emissions(
                avg_commute_distance=avg_commute_distance,
                num_employees=num_employees,
                commute_days_per_year=commute_days_per_year,
                commute_mode=commute_mode,
                mode_breakdown={
                    "car": car_percent/100 if commute_mode == "Mixed" else (1 if commute_mode == "Car (Single Occupancy)" else 0),
                    "carpool": carpool_percent/100 if commute_mode == "Mixed" else (1 if commute_mode == "Carpool" else 0),
                    "public_transit": public_transit_percent/100 if commute_mode == "Mixed" else (1 if commute_mode == "Public Transit" else 0),
                    "walking_biking": walking_biking_percent/100 if commute_mode == "Mixed" else (1 if commute_mode == "Walking/Biking" else 0),
                    "wfh": wfh_percent/100 if commute_mode == "Mixed" else (1 if commute_mode == "Work from Home" else 0)
                }
            )
            
            scope3_waste = ghg.calculate_waste_emissions(
                landfill_waste=landfill_waste,
                recycled_waste=recycled_waste,
                composted_waste=composted_waste,
                incinerated_waste=incinerated_waste
            )
            
            scope3_purchased_goods = ghg.calculate_purchased_goods_emissions(
                purchased_goods=purchased_goods,
                industry=industry
            )
            
            # Aggregate results
            scope1_total = scope1_stationary + scope1_mobile + scope1_refrigerants
            scope2_total = scope2_electricity
            scope3_total = scope3_business_travel + scope3_employee_commuting + scope3_waste + scope3_purchased_goods
            
            total_emissions = scope1_total + scope2_total + scope3_total
            
            # Store results in session state
            st.session_state.total_emissions = total_emissions
            st.session_state.emissions_by_scope = {
                "Scope 1": scope1_total,
                "Scope 2": scope2_total,
                "Scope 3": scope3_total
            }
            
            st.session_state.emissions_by_category = {
                "Stationary Combustion": scope1_stationary,
                "Mobile Combustion": scope1_mobile,
                "Refrigerants": scope1_refrigerants,
                "Purchased Electricity": scope2_electricity,
                "Business Travel": scope3_business_travel,
                "Employee Commuting": scope3_employee_commuting,
                "Waste Generation": scope3_waste,
                "Purchased Goods & Services": scope3_purchased_goods
            }
            
            # Generate recommendations
            st.session_state.recommendations = rec.generate_recommendations(
                st.session_state.emissions_by_category,
                industry=industry
            )
            
            st.session_state.input_complete = True
            
            # Save results to database only if not in embedded mode
            if not embedded and organization_name:
                try:
                    # Prepare input data to save
                    input_data = {
                        "organization_info": {
                            "organization_name": organization_name,
                            "industry": industry,
                            "reporting_year": reporting_year,
                            "num_employees": num_employees
                        },
                        "scope1": {
                            "natural_gas": natural_gas,
                            "diesel": diesel,
                            "propane": propane,
                            "fuel_oil": fuel_oil,
                            "gasoline": gasoline,
                            "diesel_vehicles": diesel_vehicles,
                            "jet_fuel": jet_fuel,
                            "refrigerant_type": refrigerant_type,
                            "refrigerant_amount": refrigerant_amount
                        },
                        "scope2": {
                            "electricity": electricity,
                            "grid_region": grid_region,
                            "electricity_source": electricity_source
                        },
                        "scope3": {
                            "business_travel": {
                                "air_travel_short": air_travel_short,
                                "air_travel_medium": air_travel_medium,
                                "air_travel_long": air_travel_long,
                                "car_rental": car_rental,
                                "hotel_stays": hotel_stays
                            },
                            "employee_commuting": {
                                "avg_commute_distance": avg_commute_distance,
                                "commute_days_per_year": commute_days_per_year,
                                "commute_mode": commute_mode
                            },
                            "waste": {
                                "landfill_waste": landfill_waste,
                                "recycled_waste": recycled_waste,
                                "composted_waste": composted_waste,
                                "incinerated_waste": incinerated_waste
                            },
                            "purchased_goods": {
                                "purchased_goods": purchased_goods
                            }
                        }
                    }
                    
                    # Save to database
                    record_id = db.save_carbon_footprint(
                        organization_name=organization_name,
                        industry=industry,
                        reporting_year=reporting_year,
                        num_employees=num_employees,
                        total_emissions=total_emissions,
                        emissions_by_scope=st.session_state.emissions_by_scope,
                        emissions_by_category=st.session_state.emissions_by_category,
                        input_data=input_data
                    )
                    
                    # Store record ID in session state
                    st.session_state.last_saved_id = record_id
                    
                    # Notify user and switch to results tab
                    st.success(f"Calculation complete! Results saved to database (ID: {record_id}). View your results in the 'Results Dashboard' tab.")
                except Exception as e:
                    st.error(f"Error saving to database: {str(e)}")
                    st.success("Calculation complete! View your results in the 'Results Dashboard' tab.")
            elif embedded:
                # In embedded mode, don't save to database and don't show database-related messages
                st.success("Calculation complete! View your results in the 'Results Dashboard' tab.")
            else:
                # Not embedded, but missing organization name
                st.warning("Organization name is required to save results to database.")
                st.success("Calculation complete! View your results in the 'Results Dashboard' tab.")

# Results Dashboard Tab
with tab2:
    if st.session_state.input_complete:
        st.header("Carbon Footprint Results")
        
        # Total emissions card
        st.metric(
            "Total Carbon Footprint", 
            f"{st.session_state.total_emissions:.2f} tonnes CO₂e"
        )
        
        # Key metrics in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Scope 1 Emissions", 
                f"{st.session_state.emissions_by_scope['Scope 1']:.2f} tonnes CO₂e",
                help="Direct emissions from owned or controlled sources"
            )
        with col2:
            st.metric(
                "Scope 2 Emissions", 
                f"{st.session_state.emissions_by_scope['Scope 2']:.2f} tonnes CO₂e",
                help="Indirect emissions from purchased electricity, steam, heating, and cooling"
            )
        with col3:
            st.metric(
                "Scope 3 Emissions", 
                f"{st.session_state.emissions_by_scope['Scope 3']:.2f} tonnes CO₂e",
                help="All other indirect emissions in a company's value chain"
            )
        
        # Emissions visualization
        st.subheader("Emissions by Scope")
        fig_by_scope = viz.create_emissions_by_scope_chart(st.session_state.emissions_by_scope)
        st.plotly_chart(fig_by_scope, use_container_width=True)
        
        st.subheader("Emissions by Category")
        fig_by_category = viz.create_emissions_by_category_chart(st.session_state.emissions_by_category)
        st.plotly_chart(fig_by_category, use_container_width=True)
        
        # Emissions breakdown table
        st.subheader("Detailed Emissions Breakdown")
        emissions_df = pd.DataFrame({
            "Category": list(st.session_state.emissions_by_category.keys()),
            "Emissions (tonnes CO₂e)": list(st.session_state.emissions_by_category.values())
        })
        emissions_df = emissions_df.sort_values("Emissions (tonnes CO₂e)", ascending=False)
        emissions_df["Percentage"] = emissions_df["Emissions (tonnes CO₂e)"] / emissions_df["Emissions (tonnes CO₂e)"].sum() * 100
        emissions_df["Percentage"] = emissions_df["Percentage"].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(
            emissions_df,
            hide_index=True,
            column_config={
                "Emissions (tonnes CO₂e)": st.column_config.NumberColumn(format="%.2f")
            }
        )
        
        # Export functionality
        st.subheader("Export Results")
        
        # Create data for export
        # Summary data
        summary_data = {
            "Metric": ["Total Emissions", "Scope 1 Emissions", "Scope 2 Emissions", "Scope 3 Emissions"],
            "Value (tonnes CO₂e)": [
                st.session_state.total_emissions,
                st.session_state.emissions_by_scope["Scope 1"],
                st.session_state.emissions_by_scope["Scope 2"],
                st.session_state.emissions_by_scope["Scope 3"]
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        
        # Recommendations data
        recommendations_data = {
            "Category": list(st.session_state.recommendations.keys()),
            "Recommendations": [" | ".join(recs) for recs in st.session_state.recommendations.values()]
        }
        recommendations_df = pd.DataFrame(recommendations_data)
        
        # Display data in expandable sections for easy copy-paste
        with st.expander("Summary Report - Click to view and copy"):
            st.dataframe(summary_df)
            
            # Display formatted data
            st.subheader("Copy data as JSON:")
            st.code(summary_df.to_json(orient='records'), language="json")
            
            # Display as plain text for easier copying
            st.subheader("Or as plain text (tab-separated):")
            summary_text = "Metric\tValue (tonnes CO₂e)\n"
            for _, row in summary_df.iterrows():
                summary_text += f"{row['Metric']}\t{row['Value (tonnes CO₂e)']:.2f}\n"
            st.text_area("", summary_text, height=150)
            
        with st.expander("Detailed Report - Click to view and copy"):
            st.dataframe(emissions_df)
            
            # Display formatted data
            st.subheader("Copy data as JSON:")
            st.code(emissions_df.to_json(orient='records'), language="json")
            
            # Display as plain text
            st.subheader("Or as plain text (tab-separated):")
            detailed_text = "Category\tEmissions (tonnes CO₂e)\tPercentage\n"
            for _, row in emissions_df.iterrows():
                detailed_text += f"{row['Category']}\t{row['Emissions (tonnes CO₂e)']:.2f}\t{row['Percentage']}\n"
            st.text_area("", detailed_text, height=200)
            
        with st.expander("Recommendations - Click to view and copy"):
            st.dataframe(recommendations_df)
            
            # Display formatted data
            st.subheader("Copy data as JSON:")
            st.code(recommendations_df.to_json(orient='records'), language="json")
            
            # Display as plain text
            st.subheader("Recommendations as plain text:")
            recs_text = ""
            for category, recs in st.session_state.recommendations.items():
                recs_text += f"## {category}\n"
                for rec in recs:
                    recs_text += f"- {rec}\n"
                recs_text += "\n"
            st.text_area("", recs_text, height=200)
            
        # Downloadable report options (only show if not in embedded mode)
        if not embedded:
            st.subheader("Download Complete Reports")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Generate PDF report
                pdf_data = report.generate_pdf_report(
                    organization_name=organization_name,
                    industry=industry,
                    reporting_year=reporting_year,
                    num_employees=num_employees,
                    total_emissions=st.session_state.total_emissions,
                    emissions_by_scope=st.session_state.emissions_by_scope,
                    emissions_by_category=st.session_state.emissions_by_category,
                    recommendations=st.session_state.recommendations
                )
                
                # Create download link
                pdf_link = report.get_download_link(
                    file_data=pdf_data,
                    file_name=f"carbon_footprint_{organization_name.replace(' ', '_')}_{reporting_year}.pdf",
                    display_text="Download PDF Report"
                )
                
                st.markdown(pdf_link, unsafe_allow_html=True)
                
            with col2:
                # Generate Excel report
                excel_data = report.generate_excel_report(
                    organization_name=organization_name,
                    industry=industry,
                    reporting_year=reporting_year,
                    num_employees=num_employees,
                    total_emissions=st.session_state.total_emissions,
                    emissions_by_scope=st.session_state.emissions_by_scope,
                    emissions_by_category=st.session_state.emissions_by_category,
                    recommendations=st.session_state.recommendations
                )
                
                # Create download link
                excel_link = report.get_download_link(
                    file_data=excel_data,
                    file_name=f"carbon_footprint_{organization_name.replace(' ', '_')}_{reporting_year}.xlsx",
                    display_text="Download Excel Report"
                )
                
                st.markdown(excel_link, unsafe_allow_html=True)
    else:
        st.info("Please complete the 'Input Data' tab and calculate your carbon footprint to see results.")

# Recommendations Tab
with tab3:
    if st.session_state.input_complete:
        st.header("Recommendations to Reduce Your Carbon Footprint")
        
        # Use expanders for each category
        for category, recommendations in st.session_state.recommendations.items():
            with st.expander(f"Recommendations for {category}"):
                for rec in recommendations:
                    st.markdown(f"• {rec}")
        
        # General tips
        st.subheader("General Carbon Reduction Strategies")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Energy Efficiency")
            st.markdown("""
            • Conduct an energy audit to identify saving opportunities
            • Upgrade to energy-efficient equipment and lighting
            • Install smart building controls and sensors
            • Optimize HVAC systems and schedules
            """)
            
            st.markdown("##### Renewable Energy")
            st.markdown("""
            • Install on-site renewable energy generation
            • Purchase renewable energy credits (RECs)
            • Sign power purchase agreements (PPAs) for clean energy
            • Consider community solar projects
            """)
        
        with col2:
            st.markdown("##### Supply Chain Management")
            st.markdown("""
            • Engage suppliers on emissions reduction initiatives
            • Set procurement standards for lower carbon products
            • Optimize logistics and transportation networks
            • Consider product redesign for lower lifecycle emissions
            """)
            
            st.markdown("##### Employee Engagement")
            st.markdown("""
            • Educate employees on carbon reduction practices
            • Incentivize sustainable commuting options
            • Implement hybrid work policies where feasible
            • Create green teams to drive sustainability initiatives
            """)
        
        st.subheader("Carbon Offsets and Climate Action")
        st.markdown("""
        After reducing emissions directly, consider investing in high-quality carbon offset projects to address
        unavoidable emissions. Look for offsets that are:
        
        • Verified by recognized standards (Gold Standard, Verified Carbon Standard)
        • Additional (wouldn't have happened without carbon financing)
        • Permanent and not subject to reversal
        • Contributing to sustainable development goals beyond carbon
        """)
        
    else:
        st.info("Please complete the 'Input Data' tab and calculate your carbon footprint to see recommendations.")

# Carbon Offsets Tab
with tab4:
    st.header("Carbon Offset Recommendations")
    
    if st.session_state.input_complete:
        st.subheader("Offset Your Carbon Footprint")
        
        st.markdown("""
        Carbon offsets are investments in projects that reduce greenhouse gas emissions. 
        These projects can range from renewable energy and reforestation to methane capture 
        and energy efficiency improvements.
        """)
        
        # Offset controls
        col1, col2 = st.columns(2)
        with col1:
            offset_percentage = st.slider("Percentage of emissions to offset", 
                                         min_value=10, max_value=100, value=100, step=10,
                                         help="Choose what percentage of your total emissions you want to offset")
            
            emissions_to_offset = st.session_state.total_emissions * (offset_percentage / 100)
            st.info(f"Emissions to offset: {emissions_to_offset:.2f} tonnes CO₂e")
        
        with col2:
            budget_per_tonne = st.number_input("Maximum budget per tonne (USD)", 
                                              min_value=None, max_value=None, value=None,
                                              help="Optional: Set a maximum price you're willing to pay per tonne of CO₂ offset")
            
            location = st.selectbox("Project location preference", 
                                   ["Global", "North America", "Europe", "Asia Pacific", "Africa", "Latin America"],
                                   help="Choose a geographic region where you prefer offset projects to be located")
        
        # Get carbon offset recommendations
        if st.button("Generate Offset Recommendations"):
            with st.spinner("Generating offset recommendations..."):
                industry = "Other"  # Default value
                if 'industry' in locals():
                    industry = industry
                
                # Get recommendations from the carbon_offsets module
                offset_recommendations = co.get_offset_recommendations(
                    st.session_state.emissions_by_scope,
                    st.session_state.emissions_by_category,
                    industry=industry,
                    budget_per_tonne=budget_per_tonne,
                    location=location,
                    offset_percentage=offset_percentage
                )
                
                # Calculate total offset cost
                total_cost = co.calculate_offset_cost(
                    emissions_to_offset, 
                    price_per_tonne=offset_recommendations.get('avg_price_per_tonne', 15), 
                    offset_percentage=100  # Already applied the percentage when calculating emissions_to_offset
                )
                
                # Display results
                st.success(f"Offsetting {emissions_to_offset:.2f} tonnes CO₂e would cost approximately ${total_cost:,.2f}")
                
                # Format and display recommendations
                st.markdown("### Recommended Offset Projects")
                st.markdown(co.format_offset_results_html(offset_recommendations), unsafe_allow_html=True)
                
                # Display disclaimer
                st.markdown("""
                ---
                **Disclaimer**: These recommendations are for informational purposes only. 
                Actual carbon offset prices and availability may vary. We recommend conducting 
                additional research before making purchasing decisions.
                """)
    else:
        st.info("Please complete the emissions calculation in the 'Input Data' tab first to receive carbon offset recommendations.")

# Eco-Challenge Tab
with tab5:
    eco.display_eco_challenge_tab()

# History Tab - Only display if not in embedded mode
# This code only runs when tab6 exists (non-embedded mode)
if not embedded:
    try:
        with tab6:
            history.display_history_page()
    except NameError:
        # This should never happen as tab6 is defined when not embedded
        st.error("History tab is not available")
