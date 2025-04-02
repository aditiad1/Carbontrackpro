# GHG Protocol Calculation Functions
import emission_factors as ef

def calculate_stationary_combustion(natural_gas=0, diesel=0, propane=0, fuel_oil=0):
    """
    Calculate emissions from stationary combustion sources.
    All inputs should be in their respective units (m³ for natural gas, liters for others)
    Returns tonnes CO2e
    """
    # Convert to tonnes CO2e using emission factors
    natural_gas_emissions = natural_gas * ef.STATIONARY_COMBUSTION['natural_gas']
    diesel_emissions = diesel * ef.STATIONARY_COMBUSTION['diesel']
    propane_emissions = propane * ef.STATIONARY_COMBUSTION['propane']
    fuel_oil_emissions = fuel_oil * ef.STATIONARY_COMBUSTION['fuel_oil']
    
    total_emissions = natural_gas_emissions + diesel_emissions + propane_emissions + fuel_oil_emissions
    return total_emissions

def calculate_mobile_combustion(gasoline=0, diesel=0, jet_fuel=0):
    """
    Calculate emissions from mobile combustion (vehicles, aircraft).
    All inputs should be in liters.
    Returns tonnes CO2e
    """
    gasoline_emissions = gasoline * ef.MOBILE_COMBUSTION['gasoline']
    diesel_emissions = diesel * ef.MOBILE_COMBUSTION['diesel']
    jet_fuel_emissions = jet_fuel * ef.MOBILE_COMBUSTION['jet_fuel']
    
    total_emissions = gasoline_emissions + diesel_emissions + jet_fuel_emissions
    return total_emissions

def calculate_refrigerant_emissions(refrigerant_type="None", amount=0.0):
    """
    Calculate emissions from refrigerant leakage.
    
    Parameters:
    - refrigerant_type: Type of refrigerant
    - amount: Amount in kg (can be float)
    
    Returns emissions in tonnes CO2e
    """
    if refrigerant_type == "None" or amount == 0:
        return 0
    
    # GWP values from emission_factors.py
    emissions = amount * ef.REFRIGERANTS.get(refrigerant_type, 0) / 1000  # Convert to tonnes
    return emissions

def calculate_electricity_emissions(electricity=0, grid_region="Other", electricity_source="Grid Electricity"):
    """
    Calculate emissions from electricity consumption.
    
    Parameters:
    - electricity: Electricity consumption in kWh
    - grid_region: Region of the electricity grid
    - electricity_source: Source of electricity
    
    Returns emissions in tonnes CO2e
    """
    # Apply different emission factors based on source
    if electricity_source == "Renewable Energy":
        # Even renewables have some lifecycle emissions
        emissions_factor = ef.ELECTRICITY['renewable']
    elif electricity_source == "Mixed Sources":
        emissions_factor = ef.ELECTRICITY['mixed']
    else:  # Grid Electricity
        # Use region-specific factors if available
        emissions_factor = ef.ELECTRICITY.get(grid_region.lower().replace(" ", "_"), ef.ELECTRICITY['default'])
    
    emissions = electricity * emissions_factor / 1000  # Convert to tonnes
    return emissions

def calculate_business_travel_emissions(air_travel_short=0, air_travel_medium=0, air_travel_long=0, 
                                        car_rental=0, hotel_stays=0):
    """
    Calculate emissions from business travel.
    
    Parameters:
    - air_travel_short: Short-haul flights in passenger miles
    - air_travel_medium: Medium-haul flights in passenger miles
    - air_travel_long: Long-haul flights in passenger miles
    - car_rental: Car rental miles
    - hotel_stays: Number of hotel nights
    
    Returns emissions in tonnes CO2e
    """
    air_short_emissions = air_travel_short * ef.BUSINESS_TRAVEL['air_short_haul']
    air_medium_emissions = air_travel_medium * ef.BUSINESS_TRAVEL['air_medium_haul']
    air_long_emissions = air_travel_long * ef.BUSINESS_TRAVEL['air_long_haul']
    car_rental_emissions = car_rental * ef.BUSINESS_TRAVEL['car_rental']
    hotel_emissions = hotel_stays * ef.BUSINESS_TRAVEL['hotel_stay']
    
    total_emissions = (air_short_emissions + air_medium_emissions + air_long_emissions + 
                      car_rental_emissions + hotel_emissions)
    
    return total_emissions

def calculate_employee_commuting_emissions(avg_commute_distance=0, num_employees=0, 
                                           commute_days_per_year=230, commute_mode="Car (Single Occupancy)",
                                           mode_breakdown=None):
    """
    Calculate emissions from employee commuting.
    
    Parameters:
    - avg_commute_distance: Average one-way commute distance in miles
    - num_employees: Number of employees
    - commute_days_per_year: Number of commuting days per year
    - commute_mode: Primary commute mode
    - mode_breakdown: Dictionary with mode percentages if mixed mode
    
    Returns emissions in tonnes CO2e
    """
    # Calculate total annual commute miles (round trip)
    total_annual_miles = avg_commute_distance * 2 * num_employees * commute_days_per_year
    
    if commute_mode == "Mixed" and mode_breakdown:
        # Calculate weighted emissions based on mode breakdown
        car_emissions = total_annual_miles * mode_breakdown["car"] * ef.COMMUTING['car']
        carpool_emissions = total_annual_miles * mode_breakdown["carpool"] * ef.COMMUTING['carpool']
        transit_emissions = total_annual_miles * mode_breakdown["public_transit"] * ef.COMMUTING['public_transit']
        walking_biking_emissions = total_annual_miles * mode_breakdown["walking_biking"] * ef.COMMUTING['walking_biking']
        wfh_emissions = total_annual_miles * mode_breakdown["wfh"] * ef.COMMUTING['wfh']
        
        total_emissions = car_emissions + carpool_emissions + transit_emissions + walking_biking_emissions + wfh_emissions
    else:
        # Use single mode emission factor
        mode_mapping = {
            "Car (Single Occupancy)": "car",
            "Carpool": "carpool",
            "Public Transit": "public_transit",
            "Walking/Biking": "walking_biking",
            "Work from Home": "wfh"
        }
        
        emission_factor = ef.COMMUTING[mode_mapping.get(commute_mode, "car")]
        total_emissions = total_annual_miles * emission_factor
    
    return total_emissions

def calculate_waste_emissions(landfill_waste=0, recycled_waste=0, composted_waste=0, incinerated_waste=0):
    """
    Calculate emissions from waste disposal.
    
    Parameters:
    - landfill_waste: Waste sent to landfill in tons
    - recycled_waste: Waste recycled in tons
    - composted_waste: Waste composted in tons
    - incinerated_waste: Waste incinerated in tons
    
    Returns emissions in tonnes CO2e
    """
    landfill_emissions = landfill_waste * ef.WASTE['landfill']
    recycled_emissions = recycled_waste * ef.WASTE['recycled']
    composted_emissions = composted_waste * ef.WASTE['composted']
    incinerated_emissions = incinerated_waste * ef.WASTE['incinerated']
    
    total_emissions = landfill_emissions + recycled_emissions + composted_emissions + incinerated_emissions
    
    return total_emissions

def calculate_purchased_goods_emissions(purchased_goods=0, industry="Other"):
    """
    Calculate emissions from purchased goods and services using
    Economic Input-Output (EIO) method with industry-specific factors.
    
    Parameters:
    - purchased_goods: Annual procurement spend in USD
    - industry: Industry type
    
    Returns emissions in tonnes CO2e
    """
    # Get industry-specific emission factor
    industry_factor = ef.PURCHASED_GOODS.get(industry.lower().replace(" & ", "_").replace(" ", "_"), 
                                            ef.PURCHASED_GOODS['default'])
    
    # Calculate emissions (convert USD to millions of USD)
    emissions = purchased_goods / 1000000 * industry_factor
    
    return emissions
