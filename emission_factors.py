"""
Emission factors for GHG Protocol calculations based on recognized sources.
All emission factors return tonnes CO2e per unit specified.

Primary sources:
- EPA Emission Factors Hub
- IPCC AR5 Global Warming Potentials
- IEA Electricity Emission Factors
- DEFRA Conversion Factors
"""

# Stationary Combustion (tonnes CO2e per unit)
STATIONARY_COMBUSTION = {
    'natural_gas': 0.00195,  # per m³
    'diesel': 0.00273,       # per liter
    'propane': 0.00153,      # per liter
    'fuel_oil': 0.00281      # per liter
}

# Mobile Combustion (tonnes CO2e per liter)
MOBILE_COMBUSTION = {
    'gasoline': 0.00234,
    'diesel': 0.00267,
    'jet_fuel': 0.00259
}

# Refrigerants Global Warming Potentials (GWP) for 100-year time horizon
# Values from IPCC AR5
REFRIGERANTS = {
    'R-134a': 1430,    # HFC-134a
    'R-410A': 2088,    # Blend of HFC-32 and HFC-125
    'R-404A': 3922,    # Blend of HFCs
    'R-22': 1810,      # HCFC-22
    'None': 0
}

# Electricity (tonnes CO2e per kWh)
ELECTRICITY = {
    # Grid region-specific factors
    'northeast_us': 0.000254,
    'midwest_us': 0.000481,
    'south_us': 0.000427,
    'west_us': 0.000221,
    'western_europe': 0.000276,
    'eastern_europe': 0.000483,
    'asia': 0.000562,
    
    # Source-specific factors
    'renewable': 0.000016,  # Some lifecycle emissions
    'mixed': 0.000320,
    
    # Default factor
    'default': 0.000431
}

# Business Travel (tonnes CO2e per passenger-mile or per night)
BUSINESS_TRAVEL = {
    'air_short_haul': 0.000258,
    'air_medium_haul': 0.000168,
    'air_long_haul': 0.000153,
    'car_rental': 0.000348,
    'hotel_stay': 0.021  # per night
}

# Employee Commuting (tonnes CO2e per mile)
COMMUTING = {
    'car': 0.000348,
    'carpool': 0.000162,
    'public_transit': 0.000096,
    'walking_biking': 0,
    'wfh': 0.000032  # Home office energy use
}

# Waste Disposal (tonnes CO2e per ton)
WASTE = {
    'landfill': 0.458,
    'recycled': 0.021,
    'composted': 0.023,
    'incinerated': 0.0136
}

# Purchased Goods & Services
# Economic Input-Output factors (tonnes CO2e per million USD spent)
PURCHASED_GOODS = {
    'manufacturing': 563,
    'technology': 386,
    'retail': 274,
    'healthcare': 221,
    'education': 176,
    'financial_services': 143,
    'food_beverage': 498,
    'default': 412
}
