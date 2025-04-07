from sqlalchemy import create_engine, Column, String, Float, text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import geojson
from typing import Dict, Any
import os 
from pathlib import Path
import csv 

# DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/census_db"
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class State(Base):
    __tablename__ = 'states'
    
    state_fips = Column(String(2), primary_key=True)
    state_name = Column(String(100), nullable=False)
    census_area = Column(Float)
    geometry = Column(Geometry('GEOMETRY', srid=4326))  # PostGIS geometry

class QuickFact(Base):
    __tablename__ = 'quickfacts'
    
    # id = Column(Integer,autoincrement=True, primary_key=True)
    fips_code = Column(String(5), primary_key=True)
    location_type = Column(String(10), nullable=False)
    fact_name = Column(String(255), primary_key=True)
    fact_value = Column(String(255), nullable=False)
    

class County(Base):
    __tablename__ = 'counties'
    
    county_fips = Column(String(5), primary_key=True)
    county_name = Column(String(100), nullable=False)
    state_fips = Column(String(2), nullable=False)
    census_area = Column(Float)
    geometry = Column(Geometry('GEOMETRY', srid=4326))  # PostGIS geometry




def create_tables():
    """Create tables and enable PostGIS extension"""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        Base.metadata.create_all(conn)
        conn.commit()

def process_state_geojson(geojson_path: str):
    """Load state GeoJSON data into database"""
    with open(geojson_path) as f:
        data = geojson.load(f)
    
    session = Session()
    
    try:
        for feature in data['features']:
            props = feature['properties']
            
            state = State(
                state_fips=props['STATE'],
                state_name=props['NAME'],
                census_area=props['CENSUSAREA'],
                geometry=geojson.dumps(feature['geometry'])
            )
            
            session.merge(state)
            
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def process_county_geojson(geojson_path: str):
    """Load county GeoJSON data into database"""
    with open(geojson_path) as f:
        data = geojson.load(f)
    
    session = Session()
    
    try:
        for feature in data['features']:
            props = feature['properties']
            
            state = County(
                county_fips=props['STATE']+props['COUNTY'],
                state_fips=props['STATE'],
                county_name=props['NAME'],
                census_area=props['CENSUSAREA'],
                geometry=geojson.dumps(feature['geometry'])
            )
            
            # Upsert logic
            session.merge(state)  # Inserts or updates if exists
            
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def load_csv(folder_path: str, location_type: str = "state"):
    for filename in os.listdir(folder_path):
        if not filename.endswith('.csv'):
            continue
            
        fips_code = filename.split('.')[0]  
        filepath = os.path.join(folder_path, filename)
        session = Session()
        
        try:
            with open(filepath, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                
                batch = []
                for row in reader:
                    if len(row) < 4:  # Skip malformed rows
                        continue
                        
                    # Parse values
                    fact_name = row[0].strip()
                    raw_value = row[2].strip()
                    value_note = row[3].strip()
                                        
                    # Add to batch
                    if(fact_name!="" and raw_value!=""):
                        fact = QuickFact(
                            fips_code=fips_code,
                            fact_name=fact_name,
                            location_type=location_type,
                            fact_value=raw_value,
                        )
                        session.merge(fact)
                                        
                session.commit()
                
        except (csv.Error, ValueError) as e:
            session.rollback()
            print(f"Error processing {filename}: {str(e)}")
            continue
            
        finally:
            session.close()


state_boundaries_file_path = os.path.join(Path(__file__).parent,"boundaries_data","gz_2010_us_040_00_20m.json")
county_boundaries_file_path = os.path.join(Path(__file__).parent,"boundaries_data","gz_2010_us_050_00_20m.json")

if __name__ == '__main__':
    create_tables()
    process_state_geojson(state_boundaries_file_path)
    print("State Boundaries loaded successfully!")
    process_county_geojson(county_boundaries_file_path)
    print("County Boundaries loaded successfully!")
    load_csv(os.path.join(Path(__file__).parent,"csv_files","state"),"state")
    print("State CSV file loaded")
    load_csv(os.path.join(Path(__file__).parent,"csv_files","county"),"county")
    print("County CSV file loaded")
    
    
    
    