"""
Functions for generating carbon footprint reduction recommendations
"""

def generate_recommendations(emissions_by_category, industry="Other"):
    """
    Generate tailored recommendations based on emissions profile and industry.
    
    Parameters:
    - emissions_by_category: Dictionary with emissions by category
    - industry: Industry type
    
    Returns a dictionary of recommendations by category
    """
    recommendations = {}
    
    # Get the top 3 emission categories
    sorted_categories = sorted(emissions_by_category.items(), key=lambda x: x[1], reverse=True)
    top_categories = [category for category, emissions in sorted_categories if emissions > 0][:3]
    
    # Generate recommendations for each major category
    for category in emissions_by_category:
        if emissions_by_category[category] > 0:
            category_recommendations = get_category_recommendations(category, industry, 
                                                                   category in top_categories)
            if category_recommendations:
                recommendations[category] = category_recommendations
    
    return recommendations

def get_category_recommendations(category, industry, is_priority):
    """
    Get category-specific recommendations.
    
    Parameters:
    - category: Emission category
    - industry: Industry type
    - is_priority: Whether this is a priority category (top 3)
    
    Returns a list of recommendations
    """
    # Common recommendations by category
    recommendations = []
    
    if category == "Stationary Combustion":
        recommendations = [
            "Conduct an energy audit to identify heating system inefficiencies",
            "Implement a preventive maintenance program for combustion equipment",
            "Upgrade to high-efficiency boilers and furnaces",
            "Improve building insulation and seal air leaks",
            "Install programmable thermostats and optimize temperature settings"
        ]
        
        # Add industry-specific recommendations
        if industry == "Manufacturing":
            recommendations.append("Recover and reuse waste heat from industrial processes")
            recommendations.append("Explore fuel switching to lower-carbon alternatives")
        
    elif category == "Mobile Combustion":
        recommendations = [
            "Develop a green fleet management strategy",
            "Replace older vehicles with fuel-efficient or electric models",
            "Implement driver training for fuel-efficient driving techniques",
            "Optimize delivery routes and logistics planning",
            "Consider alternative-fuel vehicles where appropriate"
        ]
        
        if industry == "Retail" or industry == "Food & Beverage":
            recommendations.append("Optimize delivery schedules to reduce empty miles")
            
    elif category == "Refrigerants":
        recommendations = [
            "Implement a refrigerant management and leak detection program",
            "Transition to refrigerants with lower global warming potential",
            "Ensure proper maintenance of cooling equipment",
            "Train technicians on best practices for refrigerant handling",
            "Consider natural refrigerants for new equipment purchases"
        ]
        
    elif category == "Purchased Electricity":
        recommendations = [
            "Conduct a lighting audit and upgrade to LED technology",
            "Install occupancy sensors and daylight harvesting systems",
            "Purchase renewable energy or renewable energy credits",
            "Optimize HVAC scheduling and operations",
            "Investigate on-site renewable energy generation"
        ]
        
        if industry == "Technology":
            recommendations.append("Implement server virtualization and data center efficiency measures")
            
    elif category == "Business Travel":
        recommendations = [
            "Develop a sustainable travel policy",
            "Increase use of video conferencing to reduce non-essential travel",
            "When travel is necessary, prioritize direct flights over connections",
            "Consider carbon offsets for unavoidable air travel",
            "Choose hotels with green certifications"
        ]
        
    elif category == "Employee Commuting":
        recommendations = [
            "Implement a flexible work policy including remote work options",
            "Offer incentives for carpooling and public transit use",
            "Install EV charging stations at your facility",
            "Create a bike-friendly workplace with secure storage and showers",
            "Consider a compressed work week (e.g., 4 day/10 hour schedule)"
        ]
        
    elif category == "Waste Generation":
        recommendations = [
            "Conduct a waste audit to identify reduction opportunities",
            "Implement a comprehensive recycling program",
            "Start composting organic waste",
            "Set targets for zero waste to landfill",
            "Engage employees in waste reduction initiatives"
        ]
        
        if industry == "Food & Beverage":
            recommendations.append("Donate excess food to local food banks")
            recommendations.append("Implement food waste tracking and prevention measures")
            
    elif category == "Purchased Goods & Services":
        recommendations = [
            "Develop sustainable procurement guidelines",
            "Engage suppliers on their emissions reduction efforts",
            "Select products with environmental certifications",
            "Reduce packaging or switch to sustainable packaging",
            "Conduct lifecycle assessments for key products"
        ]
        
        if industry == "Manufacturing":
            recommendations.append("Redesign products for reduced material use and longer lifespan")
    
    # If this is a priority category, add a stronger recommendation
    if is_priority:
        if category == "Stationary Combustion":
            recommendations.insert(0, "PRIORITY: Consider a comprehensive energy efficiency retrofit")
        elif category == "Mobile Combustion":
            recommendations.insert(0, "PRIORITY: Develop a fleet electrification strategy and timeline")
        elif category == "Purchased Electricity":
            recommendations.insert(0, "PRIORITY: Consider a power purchase agreement (PPA) for renewable energy")
        elif category == "Business Travel":
            recommendations.insert(0, "PRIORITY: Set a business travel carbon budget with reduction targets")
        elif category == "Employee Commuting":
            recommendations.insert(0, "PRIORITY: Implement a comprehensive sustainable commuting program")
        elif category == "Waste Generation":
            recommendations.insert(0, "PRIORITY: Establish a formal zero waste program with measurable targets")
        elif category == "Purchased Goods & Services":
            recommendations.insert(0, "PRIORITY: Engage top suppliers on science-based emissions reduction targets")
    
    return recommendations
