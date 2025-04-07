from pydantic import BaseModel
from enum import Enum


class BoundaryTypeEnum(str, Enum):
    STATE = 'state'
    COUNTY = 'county'

class GetBoundariesRequest(BaseModel):
    type: BoundaryTypeEnum 
    
class GetDataRequest(BaseModel):
    geoid: str 