from src.daos.quick_facts_dao import QuickFactDAO
from src.daos.state_dao import StateDAO
from src.daos.county_dao import CountyDAO
from src.schemas.response_schemas import LocationDataResponse, FactData

class DataService:
    def __init__(self):
        self.quick_fact_dao = QuickFactDAO()
        self.state_dao = StateDAO()
        self.county_dao = CountyDAO()

    def get_location_data(self, geoid: str, db):
        quick_facts = self.quick_fact_dao.find_all_by_geoid(db, geoid)
        
        location_name = None
        if(len(geoid)==2):
            # is state 
            state_response = self.state_dao.find_by_fips_code(db, geoid)
            if(state_response):
                location_name = state_response.state_name
        elif(len(geoid)==5):
            # is county
            county_response = self.county_dao.find_by_fips_code(db, geoid)
            if(county_response):
                location_name = county_response.county_name 
        
        return LocationDataResponse(
            location_id=geoid,
            location_name=location_name,
            facts=[
                FactData(
                    fact_name=fact.fact_name,
                    fact_value=fact.fact_value,
                ) for fact in quick_facts
            ]
        )