from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pyle38.errors import Tile38IdNotFoundError, Tile38KeyNotFoundError
from pyle38.responses import JSONResponse, ObjectResponse, ObjectsResponse

from app.db.db import tile38
from app.models.vehicle import (
    Vehicle,
    VehicleRequestBody,
    VehicleResponse,
    VehiclesResponse,
)

router = APIRouter()


@router.get(
    "/vehicle/{id}",
    tags=["vehicle"],
    response_model=VehicleResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_vehicle(id: str) -> Optional[VehicleResponse]:
    try:
        vehicle: ObjectResponse[Vehicle] = await tile38.get("fleet", id).asObject()

        response = {"data": vehicle.object}
        return VehicleResponse(**response)

    except (Tile38KeyNotFoundError, Tile38IdNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"vehicle with id '{id}' not found",
        )


@router.get(
    "/vehicle",
    tags=["vehicle"],
    response_model=VehiclesResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_vehicles() -> VehiclesResponse:
    vehicles: ObjectsResponse[Vehicle] = await tile38.scan("fleet").asObjects()

    response = {"data": vehicles.objects}

    return VehiclesResponse(**response)


@router.post(
    "/vehicle",
    response_model=JSONResponse,
    response_model_exclude_none=True,
    tags=["vehicle"],
    status_code=status.HTTP_201_CREATED,
)
async def set_vehicle(body: VehicleRequestBody) -> JSONResponse:
    vehicle = body.data
    response = (
        await tile38.set("fleet", vehicle.properties.id)
        .object(vehicle.model_dump())
        .exec()
    )

    return JSONResponse(**response.dict())
