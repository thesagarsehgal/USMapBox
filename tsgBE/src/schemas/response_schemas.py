from pydantic import BaseModel
from typing import Optional, List, Dict


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    properties: dict
    geometry: dict

class GeoJSONResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]

class FactData(BaseModel):
    fact_name: str
    fact_value: str
    
class LocationDataResponse(BaseModel):
    location_id: str
    location_name: Optional[str]
    facts: List[FactData]

class State(BaseModel):
    name: str 
    fips_code: str 
    
class County(BaseModel):
    name: str 
    fips_code: str 
    
class EncompassingAreaResponse(BaseModel):
    states: List[State]
    counties: List[County]