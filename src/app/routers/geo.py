from fastapi import APIRouter
from app.db.db import tile38
from app.models.vehicle import VehiclesResponse

router = APIRouter()


@router.get(
    "/search/within", response_model=VehiclesResponse, response_model_exclude_none=True
)
async def get_within(lat: float, lon: float, radius: float) -> VehiclesResponse:
    vehicles = await tile38.within("fleet").circle(lat, lon, radius).asObjects()
    response = VehiclesResponse(**({"data": [v.object for v in vehicles.objects]}))

    return response
