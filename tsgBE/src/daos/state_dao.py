from sqlalchemy.orm import Session
from sqlalchemy import func

from src.schemas.response_schemas import GeoJSONFeature
from src.models.entities import State, County
import json 

class StateDAO:
    def find_all(self, db: Session):
        results = db.query(
            State.state_fips,
            State.state_name,
            func.ST_AsGeoJSON(State.geometry).label('geometry')
        ).all()
        return results

    def find_by_fips_code(self, db: Session, state_fips_code: str):
        result = db.query(State).filter(State.state_fips == state_fips_code).first()
        return result
    