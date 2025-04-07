from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

from src.models.base import Base  # Import base class from base.py

class State(Base):
    __tablename__ = 'states'
    
    state_fips = Column(String(2), primary_key=True)
    state_name = Column(String(100), nullable=False)
    census_area = Column(Float)
    geometry = Column(Geometry('GEOMETRY', srid=4326))

class County(Base):
    __tablename__ = 'counties'
    
    county_fips = Column(String(5), primary_key=True)
    county_name = Column(String(100), nullable=False)
    state_fips = Column(String(2), ForeignKey('states.state_fips'), nullable=False)
    census_area = Column(Float)
    geometry = Column(Geometry('GEOMETRY', srid=4326))

class QuickFact(Base):
    __tablename__ = 'quickfacts'
    
    fips_code = Column(String(5), primary_key=True)
    location_type = Column(String(10), nullable=False)
    fact_name = Column(String(255), primary_key=True)
    fact_value = Column(String(255), nullable=False)
    