from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas.request_schemas import BoundaryTypeEnum, GetBoundariesRequest
from src.services.boundaries_service import BoundariesService
from src.schemas.response_schemas import GeoJSONResponse, EncompassingAreaResponse
from src.dependencies import get_db

router = APIRouter(prefix="/api/v1")

@router.get("/boundaries", response_model=GeoJSONResponse)
async def get_boundaries(
    boundary_type: BoundaryTypeEnum,
    db: Session = Depends(get_db)
):
    service = BoundariesService()
    return service.get_boundaries(boundary_type, db)


@router.get("/encompassing", response_model=EncompassingAreaResponse)
async def get_encompassing_areas(
    geo_id: str,
    db: Session = Depends(get_db)
):
    service = BoundariesService()
    return service.get_encompassing_areas(geo_id, db)

