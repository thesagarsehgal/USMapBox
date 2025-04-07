from src.schemas.request_schemas import BoundaryTypeEnum
from src.daos.state_dao import StateDAO
from src.daos.county_dao import CountyDAO
from src.schemas.response_schemas import GeoJSONFeature, GeoJSONResponse
import json 

class BoundariesService:
    def __init__(self):
        self.state_dao = StateDAO()
        self.county_dao = CountyDAO()

    def get_boundaries(self, boundary_type, db):
        if boundary_type == BoundaryTypeEnum.STATE:
            results = self.state_dao.find_all(db)
            features = [
                GeoJSONFeature(
                    properties={"id": state.state_fips, "name": state.state_name},
                    geometry=json.loads(state.geometry)
                ) for state in results
            ]
        elif boundary_type == BoundaryTypeEnum.COUNTY:
            results = self.county_dao.find_all(db)
            features = [
                GeoJSONFeature(
                    properties={"id": county.county_fips, "name": county.county_name},
                    geometry=json.loads(county.geometry)
                ) for county in results
            ]
        else:
            raise ValueError("Invalid boundary type")
        
        return GeoJSONResponse(features=features)