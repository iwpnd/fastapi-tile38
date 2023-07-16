from typing import Optional

from fastapi import APIRouter, status
from pyle38.responses import ObjectsResponse

from app.db.db import tile38
from app.models.vehicle import Vehicle, VehiclesResponse

router = APIRouter()


@router.get(
    "/search/within",
    response_model=VehiclesResponse,
    response_model_exclude_none=True,
    tags=["geo-search"],
    status_code=status.HTTP_200_OK,
)
async def get_within(lat: float, lon: float, radius: float) -> VehiclesResponse:
    vehicles: ObjectsResponse[Vehicle] = (
        await tile38.within("fleet").circle(lat, lon, radius).asObjects()
    )
    return VehiclesResponse(data=vehicles.dict()["objects"])


@router.get(
    "/search/nearby",
    response_model=VehiclesResponse,
    response_model_exclude_none=True,
    tags=["geo-search"],
    status_code=status.HTTP_200_OK,
)
async def get_nearby(
    lat: float, lon: float, radius: Optional[int] = None
) -> VehiclesResponse:
    if radius:
        vehicles_in_radius: ObjectsResponse[Vehicle] = (
            await tile38.nearby("fleet")
            .point(lat, lon, radius)
            .distance()
            .nofields()
            .asObjects()
        )

        return VehiclesResponse(data=vehicles_in_radius.model_dump()["objects"])

    vehicles: ObjectsResponse[Vehicle] = (
        await tile38.nearby("fleet").point(lat, lon).distance().nofields().asObjects()
    )

    return VehiclesResponse(data=vehicles.dict()["objects"])
