from src.schemas.request_schemas import BoundaryTypeEnum
from src.daos.state_dao import StateDAO
from src.daos.county_dao import CountyDAO
from src.schemas.response_schemas import State, County, EncompassingArea, GeoJSONFeature, GeoJSONResponse
import json 
from fastapi import HTTPException, status


class BoundariesService:
    def __init__(self):
        self.state_dao = StateDAO()
        self.county_dao = CountyDAO()

    def get_encompassing_areas(self, geo_id: str, db):
        if not geo_id or (len(geo_id) not in (2, 5)):
            raise HTTPException(detail="Invalid geo_id - must be 2 or 5 characters", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # get the boundary of region
        if(len(geo_id)==2):
            data = self.state_dao.find_by_fips_code(db, geo_id)
        elif(len(geo_id)==5):
            data = self.county_dao.find_by_fips_code(db, geo_id)
        
        if not data:
            raise HTTPException(detail=f"No area found with geo_id: {geo_id}", status_code=status.HTTP_404_NOT_FOUND)
        
        county_list = self.county_dao.find_counties_in_enclosing_area(db, data.geometry)
        state_list = self.state_dao.find_states_in_enclosing_area(db, data.geometry)
        
        encompassing_area = EncompassingArea(
            counties = [County(name=c.county_name, fips_code=c.county_fips) for c in county_list],
            states = [State(name=s.state_name, fips_code=s.state_fips) for s in state_list]
        )
        
        return encompassing_area
    
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