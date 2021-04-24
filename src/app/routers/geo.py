from typing import Optional
from fastapi import APIRouter
from pyle38.responses import ObjectsResponse
from app.db.db import tile38
from app.models.vehicle import VehiclesResponse, Vehicle

router = APIRouter()


@router.get(
    "/search/within",
    response_model=VehiclesResponse,
    response_model_exclude_none=True,
    tags=["geo-search"],
)
async def get_within(lat: float, lon: float, radius: float) -> VehiclesResponse:
    vehicles: ObjectsResponse[Vehicle] = (
        await tile38.within("fleet").circle(lat, lon, radius).asObjects()
    )
    response = {"data": vehicles.objects}

    return VehiclesResponse(**response)


@router.get(
    "/search/nearby",
    response_model=VehiclesResponse,
    response_model_exclude_none=True,
    tags=["geo-search"],
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

        response = {"data": vehicles_in_radius.objects}

        return VehiclesResponse(**(response))

    vehicles: ObjectsResponse[Vehicle] = (
        await tile38.nearby("fleet").point(lat, lon).distance().nofields().asObjects()
    )

    response = {"data": vehicles.objects}

    return VehiclesResponse(**(response))
