"""
Module for displaying historical carbon footprint calculations
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import get_all_footprints, get_footprint_by_id
import visualizations as viz

def display_history_page():
    """
    Display history of carbon footprint calculations
    """
    st.title("Carbon Footprint History")
    
    # Get all footprints from database
    try:
        footprints_df = get_all_footprints()
        
        if footprints_df.empty:
            st.info("No carbon footprint calculations have been saved yet.")
            return
        
        # Display table of all footprints
        st.subheader("Saved Calculations")
        st.dataframe(
            footprints_df,
            column_config={
                "id": st.column_config.NumberColumn("ID"),
                "organization_name": st.column_config.TextColumn("Organization"),
                "industry": st.column_config.TextColumn("Industry"),
                "reporting_year": st.column_config.NumberColumn("Year"),
                "created_at": st.column_config.DatetimeColumn("Created At"),
                "total_emissions": st.column_config.NumberColumn(
                    "Total Emissions (tonnes CO₂e)",
                    format="%.2f"
                ),
                "scope1_emissions": st.column_config.NumberColumn(
                    "Scope 1 (tonnes CO₂e)",
                    format="%.2f"
                ),
                "scope2_emissions": st.column_config.NumberColumn(
                    "Scope 2 (tonnes CO₂e)",
                    format="%.2f"
                ),
                "scope3_emissions": st.column_config.NumberColumn(
                    "Scope 3 (tonnes CO₂e)",
                    format="%.2f"
                )
            },
            hide_index=True
        )
        
        # Allow user to select a record to view in detail
        record_id = st.selectbox(
            "Select a record to view details",
            footprints_df["id"].tolist(),
            format_func=lambda x: f"ID: {x} - {footprints_df[footprints_df['id'] == x]['organization_name'].values[0]} ({footprints_df[footprints_df['id'] == x]['reporting_year'].values[0]})"
        )
        
        if record_id:
            display_footprint_detail(record_id)
        
        # Comparison visualization if more than one record
        if len(footprints_df) > 1:
            display_comparison_visualizations(footprints_df)
            
    except Exception as e:
        st.error(f"Error retrieving carbon footprint history: {str(e)}")

def display_footprint_detail(record_id):
    """
    Display detailed view of a specific carbon footprint record
    
    Parameters:
    - record_id: ID of the record to display
    """
    # Get the record
    footprint = get_footprint_by_id(record_id)
    
    if not footprint:
        st.error(f"Record with ID {record_id} not found.")
        return
    
    # Display organization info
    st.subheader(f"Details for {footprint['organization_name']} ({footprint['reporting_year']})")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Total Emissions", 
            f"{footprint['total_emissions']:.2f} t CO₂e"
        )
    with col2:
        st.metric(
            "Scope 1", 
            f"{footprint['scope1_emissions']:.2f} t CO₂e"
        )
    with col3:
        st.metric(
            "Scope 2", 
            f"{footprint['scope2_emissions']:.2f} t CO₂e"
        )
    with col4:
        st.metric(
            "Scope 3", 
            f"{footprint['scope3_emissions']:.2f} t CO₂e"
        )
    
    # Emissions by scope chart
    st.subheader("Emissions by Scope")
    emissions_by_scope = {
        "Scope 1": footprint["scope1_emissions"],
        "Scope 2": footprint["scope2_emissions"],
        "Scope 3": footprint["scope3_emissions"]
    }
    fig_by_scope = viz.create_emissions_by_scope_chart(emissions_by_scope)
    st.plotly_chart(fig_by_scope, use_container_width=True)
    
    # Emissions by category chart
    st.subheader("Emissions by Category")
    fig_by_category = viz.create_emissions_by_category_chart(footprint["emissions_by_category"])
    st.plotly_chart(fig_by_category, use_container_width=True)
    
    # Detailed breakdown table
    st.subheader("Detailed Emissions Breakdown")
    emissions_df = pd.DataFrame({
        "Category": list(footprint["emissions_by_category"].keys()),
        "Emissions (tonnes CO₂e)": list(footprint["emissions_by_category"].values())
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

def display_comparison_visualizations(footprints_df):
    """
    Display visualizations comparing multiple carbon footprint records
    
    Parameters:
    - footprints_df: DataFrame with footprint records
    """
    st.subheader("Comparison Across Calculations")
    
    # Create a combined label for better readability
    footprints_df["label"] = footprints_df.apply(
        lambda row: f"{row['organization_name']} ({row['reporting_year']})", 
        axis=1
    )
    
    # Total emissions comparison
    fig_total = px.bar(
        footprints_df,
        x="label",
        y="total_emissions",
        title="Total Emissions Comparison",
        labels={"total_emissions": "Total Emissions (tonnes CO₂e)", "label": "Organization"},
        color="industry"
    )
    fig_total.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_total, use_container_width=True)
    
    # Emissions by scope comparison
    scope_data = []
    for _, row in footprints_df.iterrows():
        scope_data.extend([
            {"Organization": row["label"], "Scope": "Scope 1", "Emissions": row["scope1_emissions"]},
            {"Organization": row["label"], "Scope": "Scope 2", "Emissions": row["scope2_emissions"]},
            {"Organization": row["label"], "Scope": "Scope 3", "Emissions": row["scope3_emissions"]}
        ])
    
    scope_df = pd.DataFrame(scope_data)
    
    fig_scope = px.bar(
        scope_df,
        x="Organization",
        y="Emissions",
        color="Scope",
        title="Emissions by Scope Comparison",
        labels={"Emissions": "Emissions (tonnes CO₂e)"},
        barmode="group"
    )
    fig_scope.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_scope, use_container_width=True)