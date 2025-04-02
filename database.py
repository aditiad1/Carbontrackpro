"""
Database module for Carbon Footprint Calculator
"""
import os
import datetime
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class CarbonFootprint(Base):
    """
    Model for storing carbon footprint calculation results
    """
    __tablename__ = 'carbon_footprint'

    id = Column(Integer, primary_key=True)
    
    # Organization info
    organization_name = Column(String(255))
    industry = Column(String(100))
    reporting_year = Column(Integer)
    num_employees = Column(Integer)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Emissions totals
    total_emissions = Column(Float)
    scope1_emissions = Column(Float)
    scope2_emissions = Column(Float)
    scope3_emissions = Column(Float)
    
    # Emissions by category (JSON for flexibility)
    emissions_by_category = Column(JSON)
    
    # Input data (for reference)
    input_data = Column(JSON)

def init_db():
    """
    Initialize the database by creating all tables
    """
    Base.metadata.create_all(engine)

def save_carbon_footprint(
    organization_name,
    industry,
    reporting_year,
    num_employees,
    total_emissions,
    emissions_by_scope,
    emissions_by_category,
    input_data
):
    """
    Save carbon footprint results to database
    
    Parameters:
    - organization_name: Name of the organization
    - industry: Industry type
    - reporting_year: Year of the report
    - num_employees: Number of employees
    - total_emissions: Total emissions in tonnes CO2e
    - emissions_by_scope: Dictionary with emissions by scope
    - emissions_by_category: Dictionary with emissions by category
    - input_data: Dictionary with all input data
    
    Returns:
    - id: ID of the saved record
    """
    session = Session()
    
    # Create new record
    footprint = CarbonFootprint(
        organization_name=organization_name,
        industry=industry,
        reporting_year=reporting_year,
        num_employees=num_employees,
        total_emissions=total_emissions,
        scope1_emissions=emissions_by_scope["Scope 1"],
        scope2_emissions=emissions_by_scope["Scope 2"],
        scope3_emissions=emissions_by_scope["Scope 3"],
        emissions_by_category=emissions_by_category,
        input_data=input_data
    )
    
    # Add and commit
    session.add(footprint)
    session.commit()
    
    # Get ID
    record_id = footprint.id
    
    # Close session
    session.close()
    
    return record_id

def get_all_footprints():
    """
    Get all carbon footprint records
    
    Returns:
    - DataFrame with all records
    """
    session = Session()
    
    # Query all records
    footprints = session.query(CarbonFootprint).all()
    
    # Convert to list of dicts
    results = []
    for fp in footprints:
        results.append({
            "id": fp.id,
            "organization_name": fp.organization_name,
            "industry": fp.industry,
            "reporting_year": fp.reporting_year,
            "created_at": fp.created_at,
            "total_emissions": fp.total_emissions,
            "scope1_emissions": fp.scope1_emissions,
            "scope2_emissions": fp.scope2_emissions,
            "scope3_emissions": fp.scope3_emissions
        })
    
    # Close session
    session.close()
    
    # Return as DataFrame
    return pd.DataFrame(results)

def get_footprint_by_id(record_id):
    """
    Get a specific carbon footprint record by ID
    
    Parameters:
    - record_id: ID of the record to retrieve
    
    Returns:
    - Dictionary with record data or None if not found
    """
    session = Session()
    
    # Query the record
    footprint = session.query(CarbonFootprint).filter(CarbonFootprint.id == record_id).first()
    
    # If not found, return None
    if not footprint:
        session.close()
        return None
    
    # Convert to dict
    result = {
        "id": footprint.id,
        "organization_name": footprint.organization_name,
        "industry": footprint.industry,
        "reporting_year": footprint.reporting_year,
        "created_at": footprint.created_at,
        "total_emissions": footprint.total_emissions,
        "scope1_emissions": footprint.scope1_emissions,
        "scope2_emissions": footprint.scope2_emissions,
        "scope3_emissions": footprint.scope3_emissions,
        "emissions_by_category": footprint.emissions_by_category,
        "input_data": footprint.input_data
    }
    
    # Close session
    session.close()
    
    return result

# Initialize the database when this module is imported
init_db()