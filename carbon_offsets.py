"""
Carbon Offset Recommendation Engine
Provides tailored recommendations for carbon offset projects based on:
- Emissions profile (scope breakdown and categories)
- Industry type
- Geographic location
- Budget considerations
"""

import pandas as pd
import numpy as np

# Dictionary of verified carbon offset projects with detailed information
CARBON_OFFSET_PROJECTS = {
    # Renewable Energy Projects
    "wind_energy": {
        "name": "Wind Energy Projects",
        "description": "Large-scale wind farms that generate clean electricity and displace fossil fuel generation.",
        "price_range": (8, 20),  # USD per tonne CO2e
        "verification_standards": ["Gold Standard", "VCS"],
        "project_locations": ["USA", "India", "China", "Brazil", "South Africa"],
        "co_benefits": ["Job creation", "Energy independence", "Air quality improvement"],
        "best_for_industries": ["Manufacturing", "Technology", "Financial Services"],
        "best_for_emissions": ["Scope 2", "Purchased Electricity"]
    },
    "solar_energy": {
        "name": "Solar Energy Projects",
        "description": "Solar farms and distributed solar installations that generate clean electricity.",
        "price_range": (10, 25),  # USD per tonne CO2e
        "verification_standards": ["Gold Standard", "VCS"],
        "project_locations": ["USA", "India", "Mexico", "Egypt", "Australia"],
        "co_benefits": ["Job creation", "Energy access", "Technology transfer"],
        "best_for_industries": ["Technology", "Retail", "Healthcare"],
        "best_for_emissions": ["Scope 2", "Purchased Electricity"]
    },
    
    # Forestry and Land Use
    "reforestation": {
        "name": "Reforestation Projects",
        "description": "Planting trees in previously forested areas to sequester carbon and restore ecosystems.",
        "price_range": (12, 30),  # USD per tonne CO2e
        "verification_standards": ["Gold Standard", "VCS", "Plan Vivo"],
        "project_locations": ["Brazil", "Indonesia", "Kenya", "USA", "Costa Rica"],
        "co_benefits": ["Biodiversity", "Watershed protection", "Community benefits"],
        "best_for_industries": ["Food & Beverage", "Retail", "Financial Services"],
        "best_for_emissions": ["Scope 1", "Scope 3", "Mobile Combustion", "Business Travel"]
    },
    "avoided_deforestation": {
        "name": "Avoided Deforestation (REDD+)",
        "description": "Protecting standing forests that would otherwise be cleared, preserving carbon stocks.",
        "price_range": (5, 18),  # USD per tonne CO2e
        "verification_standards": ["VCS", "CCB", "REDD+"],
        "project_locations": ["Brazil", "Indonesia", "Peru", "Congo Basin", "Colombia"],
        "co_benefits": ["Biodiversity conservation", "Indigenous rights", "Community development"],
        "best_for_industries": ["Retail", "Food & Beverage", "Financial Services"],
        "best_for_emissions": ["Scope 3", "Purchased Goods & Services"]
    },
    
    # Methane Capture
    "landfill_methane": {
        "name": "Landfill Methane Capture",
        "description": "Capturing methane emissions from landfills for flaring or energy production.",
        "price_range": (5, 15),  # USD per tonne CO2e
        "verification_standards": ["VCS", "CAR", "ACR"],
        "project_locations": ["USA", "Brazil", "China", "South Africa", "Mexico"],
        "co_benefits": ["Local air quality", "Energy generation", "Health benefits"],
        "best_for_industries": ["Retail", "Food & Beverage", "Manufacturing"],
        "best_for_emissions": ["Scope 3", "Waste Generation"]
    },
    
    # Community-Based Projects
    "cookstoves": {
        "name": "Clean Cookstoves",
        "description": "Distributing efficient cookstoves that reduce fuel consumption and indoor air pollution.",
        "price_range": (8, 22),  # USD per tonne CO2e
        "verification_standards": ["Gold Standard", "CDM"],
        "project_locations": ["Kenya", "India", "Guatemala", "Uganda", "Nepal"],
        "co_benefits": ["Health benefits", "Women's empowerment", "Reduced fuel costs", "Reduced deforestation"],
        "best_for_industries": ["Retail", "Healthcare", "Food & Beverage"],
        "best_for_emissions": ["Scope 3", "Purchased Goods & Services"]
    },
    
    # Industrial Processes
    "industrial_efficiency": {
        "name": "Industrial Energy Efficiency",
        "description": "Implementing energy efficiency measures in industrial facilities to reduce emissions.",
        "price_range": (10, 28),  # USD per tonne CO2e
        "verification_standards": ["VCS", "CDM"],
        "project_locations": ["China", "India", "USA", "Mexico", "Vietnam"],
        "co_benefits": ["Technology transfer", "Cost savings", "Local pollution reduction"],
        "best_for_industries": ["Manufacturing", "Technology", "Other"],
        "best_for_emissions": ["Scope 1", "Stationary Combustion"]
    },
    
    # Transportation
    "transportation": {
        "name": "Low-Carbon Transportation",
        "description": "Projects that reduce emissions from transportation through fuel switching or efficiency.",
        "price_range": (15, 35),  # USD per tonne CO2e
        "verification_standards": ["VCS", "Gold Standard"],
        "project_locations": ["USA", "Europe", "Brazil", "India", "China"],
        "co_benefits": ["Air quality improvement", "Reduced congestion", "Technology advancement"],
        "best_for_industries": ["Technology", "Retail", "Healthcare"],
        "best_for_emissions": ["Scope 1", "Scope 3", "Mobile Combustion", "Business Travel", "Employee Commuting"]
    },
    
    # Blue Carbon
    "blue_carbon": {
        "name": "Blue Carbon (Coastal Ecosystems)",
        "description": "Protecting and restoring mangroves, seagrass, and salt marshes which sequester large amounts of carbon.",
        "price_range": (15, 40),  # USD per tonne CO2e
        "verification_standards": ["VCS", "Plan Vivo"],
        "project_locations": ["Indonesia", "Philippines", "Mexico", "Kenya", "Madagascar"],
        "co_benefits": ["Biodiversity", "Coastal protection", "Fisheries support", "Community livelihoods"],
        "best_for_industries": ["Food & Beverage", "Retail", "Financial Services"],
        "best_for_emissions": ["Scope 3", "Purchased Goods & Services"]
    },
    
    # Direct Air Capture
    "direct_air_capture": {
        "name": "Direct Air Capture (DAC)",
        "description": "Technology that removes CO2 directly from the atmosphere for permanent storage.",
        "price_range": (200, 600),  # USD per tonne CO2e
        "verification_standards": ["Puro.earth", "Carbon Engineering"],
        "project_locations": ["USA", "Canada", "Switzerland", "Iceland"],
        "co_benefits": ["Technology development", "Permanent removal", "Scalable solution"],
        "best_for_industries": ["Technology", "Financial Services", "Other"],
        "best_for_emissions": ["All scopes", "Hard-to-abate emissions"]
    }
}

# Constants for recommendation logic
VERIFICATION_STANDARDS = {
    "Gold Standard": "The Gold Standard for the Global Goals (GS4GG) is a standard for climate and development interventions that enables quantification of climate impacts and verification of SDG outcomes.",
    "VCS": "Verified Carbon Standard (Verra) is the world's most widely used voluntary GHG program.",
    "CDM": "Clean Development Mechanism is defined in the Kyoto Protocol for emission-reduction projects in developing countries.",
    "CAR": "Climate Action Reserve is a national offsets program focused on GHG reduction in North America.",
    "Plan Vivo": "Plan Vivo is a standard for community land use projects with a focus on smallholders and community groups.",
    "ACR": "American Carbon Registry (ACR) is the first private voluntary GHG registry in the United States.",
    "CCB": "Climate, Community & Biodiversity Standards evaluate land management projects from the beginning to development.",
    "Puro.earth": "Puro.earth focuses on carbon removal methods with long-term storage and industrial carbon sequestration."
}

def get_offset_recommendations(emissions_by_scope, emissions_by_category, industry="Other", 
                              budget_per_tonne=None, location="Global", offset_percentage=100):
    """
    Generate tailored carbon offset recommendations based on emissions profile.
    
    Parameters:
    - emissions_by_scope: Dictionary with emissions by scope
    - emissions_by_category: Dictionary with emissions by category
    - industry: Industry type
    - budget_per_tonne: Maximum price per tonne CO2e (USD)
    - location: Geographic location for project preference
    - offset_percentage: Percentage of emissions to offset (default 100%)
    
    Returns:
    - Dictionary with recommended carbon offset projects and details
    """
    total_emissions = sum(emissions_by_scope.values())
    emissions_to_offset = total_emissions * (offset_percentage / 100)
    
    # Initialize scores for each project
    project_scores = {project_id: 0 for project_id in CARBON_OFFSET_PROJECTS.keys()}
    
    # Score based on emissions profile (scope breakdown)
    largest_scope = max(emissions_by_scope.items(), key=lambda x: x[1])[0]
    
    # Score based on emissions categories
    sorted_categories = sorted(emissions_by_category.items(), key=lambda x: x[1], reverse=True)
    top_3_categories = [cat[0] for cat in sorted_categories[:3] if cat[1] > 0]
    
    # Calculate scores for each project
    for project_id, project in CARBON_OFFSET_PROJECTS.items():
        # Budget filter
        if budget_per_tonne and project["price_range"][0] > budget_per_tonne:
            continue
            
        # Industry match
        if industry in project["best_for_industries"]:
            project_scores[project_id] += 5
            
        # Emissions scope match
        if largest_scope in project["best_for_emissions"] or "All scopes" in project["best_for_emissions"]:
            project_scores[project_id] += 4
            
        # Emissions category match
        for category in top_3_categories:
            if category in project["best_for_emissions"]:
                project_scores[project_id] += 3
                
        # Location match
        if location in project["project_locations"] or "Global" in project["project_locations"]:
            project_scores[project_id] += 2
            
    # Get top recommendations
    recommended_projects = sorted([(project_id, score) for project_id, score in project_scores.items() if score > 0], 
                                 key=lambda x: x[1], reverse=True)
    
    # Format recommendations with portfolio approach
    portfolio_recommendations = []
    remaining_emissions = emissions_to_offset
    
    if not recommended_projects:
        # If no projects match the criteria, return general recommendations
        return get_general_recommendations(emissions_to_offset, budget_per_tonne)
    
    for project_id, score in recommended_projects[:4]:  # Top 4 projects for a portfolio
        project = CARBON_OFFSET_PROJECTS[project_id].copy()
        
        # Calculate suggested allocation percentage based on score relative to total scores
        total_score = sum([score for _, score in recommended_projects[:4]])
        allocation_percentage = (score / total_score) * 100 if total_score > 0 else 25
        
        # Calculate tonnes to offset with this project
        tonnes_to_offset = (allocation_percentage / 100) * emissions_to_offset
        
        # Calculate cost range
        min_cost = tonnes_to_offset * project["price_range"][0]
        max_cost = tonnes_to_offset * project["price_range"][1]
        
        project.update({
            "id": project_id,
            "score": score,
            "allocation_percentage": round(allocation_percentage, 1),
            "tonnes_to_offset": round(tonnes_to_offset, 2),
            "cost_range": (round(min_cost, 2), round(max_cost, 2))
        })
        
        portfolio_recommendations.append(project)
        
    return {
        "total_emissions": total_emissions,
        "emissions_to_offset": emissions_to_offset,
        "portfolio_approach": portfolio_recommendations,
        "verification_standards": VERIFICATION_STANDARDS
    }

def get_general_recommendations(emissions_to_offset, budget_per_tonne=None):
    """
    Provide general recommendations when no specific matches are found
    """
    # Select a diverse set of projects
    diverse_projects = ["wind_energy", "reforestation", "landfill_methane", "cookstoves"]
    
    if budget_per_tonne:
        diverse_projects = [p for p in diverse_projects if CARBON_OFFSET_PROJECTS[p]["price_range"][0] <= budget_per_tonne]
    
    if not diverse_projects:
        diverse_projects = ["wind_energy"]  # Default to wind if budget is too restrictive
    
    portfolio_recommendations = []
    
    for project_id in diverse_projects:
        project = CARBON_OFFSET_PROJECTS[project_id].copy()
        
        # Equal allocation among projects
        allocation_percentage = 100 / len(diverse_projects)
        tonnes_to_offset = (allocation_percentage / 100) * emissions_to_offset
        
        # Calculate cost range
        min_cost = tonnes_to_offset * project["price_range"][0]
        max_cost = tonnes_to_offset * project["price_range"][1]
        
        project.update({
            "id": project_id,
            "score": "N/A",
            "allocation_percentage": round(allocation_percentage, 1),
            "tonnes_to_offset": round(tonnes_to_offset, 2),
            "cost_range": (round(min_cost, 2), round(max_cost, 2))
        })
        
        portfolio_recommendations.append(project)
    
    return {
        "total_emissions": emissions_to_offset,
        "emissions_to_offset": emissions_to_offset,
        "portfolio_approach": portfolio_recommendations,
        "verification_standards": VERIFICATION_STANDARDS,
        "note": "These are general recommendations since no specific matching projects were found."
    }

def calculate_offset_cost(emissions, price_per_tonne=15, offset_percentage=100):
    """
    Calculate the cost to offset a given amount of emissions
    
    Parameters:
    - emissions: Amount of emissions in tonnes CO2e
    - price_per_tonne: Price per tonne CO2e (USD)
    - offset_percentage: Percentage of emissions to offset
    
    Returns:
    - Total cost in USD
    """
    emissions_to_offset = emissions * (offset_percentage / 100)
    return round(emissions_to_offset * price_per_tonne, 2)

def format_offset_results_html(recommendations):
    """
    Format offset recommendations as HTML for display in Streamlit
    """
    html = f"""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px;">
        <h3>Carbon Offset Portfolio Recommendation</h3>
        <p>Total emissions: {recommendations['total_emissions']:.2f} tonnes CO₂e</p>
        <p>Emissions to offset: {recommendations['emissions_to_offset']:.2f} tonnes CO₂e</p>
        
        <hr style="margin: 15px 0;">
        
        <h4>Recommended Portfolio of Carbon Offset Projects</h4>
        <p>We recommend a diverse portfolio approach to maximize co-benefits and reduce risk:</p>
    """
    
    for project in recommendations['portfolio_approach']:
        html += f"""
        <div style="margin-bottom: 15px; padding: 10px; border-left: 4px solid #4CAF50; background-color: white;">
            <h5>{project['name']} ({project['allocation_percentage']}% of portfolio)</h5>
            <p>{project['description']}</p>
            <p><strong>Verification Standards:</strong> {', '.join(project['verification_standards'])}</p>
            <p><strong>Co-benefits:</strong> {', '.join(project['co_benefits'])}</p>
            <p><strong>Project Locations:</strong> {', '.join(project['project_locations'])}</p>
            <p><strong>Recommended Allocation:</strong> {project['tonnes_to_offset']:.2f} tonnes CO₂e</p>
            <p><strong>Estimated Cost:</strong> ${project['cost_range'][0]:,.2f} - ${project['cost_range'][1]:,.2f}</p>
        </div>
        """
    
    html += """
        <hr style="margin: 15px 0;">
        <h4>About Carbon Offset Verification Standards</h4>
        <p>Verification standards ensure the quality, additionality, and real impact of offset projects:</p>
    """
    
    for standard, description in recommendations['verification_standards'].items():
        html += f"""
        <div style="margin-bottom: 10px;">
            <p><strong>{standard}:</strong> {description}</p>
        </div>
        """
    
    if 'note' in recommendations:
        html += f"""
        <div style="margin-top: 15px; padding: 10px; background-color: #fff3cd; border-left: 4px solid #ffc107;">
            <p><strong>Note:</strong> {recommendations['note']}</p>
        </div>
        """
    
    html += """
    </div>
    """
    return html