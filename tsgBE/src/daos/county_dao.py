from sqlalchemy.orm import Session
from sqlalchemy import func

from src.schemas.response_schemas import GeoJSONFeature
from src.models.entities import State, County
import json 

class CountyDAO:
    def find_all(self, db: Session):
        results = db.query(
            County.county_fips,
            County.county_name,
            func.ST_AsGeoJSON(County.geometry).label('geometry')
        ).all()
        return results

    def find_by_fips_code(self, db: Session, county_fips_code:str):
        result = db.query(County).filter(County.county_fips == county_fips_code).first()
        return result

    def find_all_by_state_fips_code(self, db:Session, state_fips_code:str):
        result = db.query(County).filter(County.state_fips == state_fips_code).all()
        return result

    def find_counties_in_enclosing_area(self, db:Session, enclosing_area):
        return db.query(County).filter(
            func.ST_Within(
                County.geometry, 
                func.ST_Transform(enclosing_area, 4326)
            )
        ).all()



    