"""
Visualization functions for the carbon footprint calculator
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_emissions_by_scope_chart(emissions_by_scope):
    """
    Create a pie chart showing emissions by scope.
    
    Parameters:
    - emissions_by_scope: Dictionary with scope names as keys and emissions as values
    
    Returns a plotly figure
    """
    labels = list(emissions_by_scope.keys())
    values = list(emissions_by_scope.values())
    
    # Custom colors for the scopes
    colors = ['#3366CC', '#DC3912', '#FF9900']
    
    fig = px.pie(
        names=labels,
        values=values,
        title="Carbon Footprint by Scope",
        color_discrete_sequence=colors,
        hole=0.4
    )
    
    # Improve layout and appearance
    fig.update_traces(
        textinfo='percent+label',
        textposition='outside',
        hoverinfo='label+value',
        hovertemplate='%{label}: %{value:.2f} tonnes CO₂e<extra></extra>'
    )
    
    # Add annotations for total emissions
    total = sum(values)
    fig.add_annotation(
        text=f"Total<br>{total:.1f} t CO₂e",
        x=0.5, y=0.5,
        font_size=14,
        showarrow=False
    )
    
    return fig

def create_emissions_by_category_chart(emissions_by_category):
    """
    Create a horizontal bar chart showing emissions by category.
    
    Parameters:
    - emissions_by_category: Dictionary with category names as keys and emissions as values
    
    Returns a plotly figure
    """
    # Create dataframe from emissions dictionary
    df = pd.DataFrame({
        'Category': list(emissions_by_category.keys()),
        'Emissions': list(emissions_by_category.values())
    })
    
    # Sort by emissions value (descending)
    df = df.sort_values('Emissions', ascending=True)
    
    # Create horizontal bar chart
    fig = px.bar(
        df,
        y='Category',
        x='Emissions',
        orientation='h',
        title="Emissions by Category (tonnes CO₂e)",
        labels={'Emissions': 'Emissions (tonnes CO₂e)', 'Category': ''},
        text_auto='.2f'
    )
    
    # Improve appearance
    fig.update_traces(
        marker_color='#4CAF50',
        texttemplate='%{x:.2f}',
        textposition='outside',
        hovertemplate='%{y}: %{x:.2f} tonnes CO₂e<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title="Tonnes CO₂e",
        uniformtext_minsize=10,
        uniformtext_mode='hide'
    )
    
    return fig

def create_emission_reduction_potential_chart(recommendations, emissions_by_category):
    """
    Create a waterfall chart showing potential emission reductions.
    This is a more advanced visualization that could be added later.
    
    Parameters:
    - recommendations: Dictionary with recommendations and estimated reduction percentages
    - emissions_by_category: Current emissions by category
    
    Returns a plotly figure
    """
    # This would be implemented when we have actual reduction potential data
    # For now, just return a placeholder
    fig = go.Figure()
    fig.add_annotation(
        text="Emission reduction potential chart will appear here<br>when reduction data is available",
        x=0.5, y=0.5,
        showarrow=False
    )
    
    return fig
