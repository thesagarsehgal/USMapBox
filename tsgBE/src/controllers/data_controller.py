from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas.request_schemas import GetDataRequest
from src.services.data_service import DataService
from src.schemas.response_schemas import LocationDataResponse
from src.dependencies import get_db

router = APIRouter(prefix="/api/v1")

@router.get("/data", response_model=LocationDataResponse)
async def get_data(
    geo_id: str,
    db: Session = Depends(get_db)
):
    service = DataService()
    result = service.get_location_data(geo_id, db)
    return result