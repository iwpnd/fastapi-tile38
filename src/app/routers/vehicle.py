from fastapi import APIRouter
from pyle38.responses import JSONResponse, ObjectResponse, ObjectsResponse
from app.db.db import tile38
from app.models.vehicle import Vehicle, VehicleResponse, VehiclesResponse

router = APIRouter()


@router.get(
    "/vehicle/{id}",
    tags=["vehicle"],
    response_model=VehicleResponse,
    response_model_exclude_none=True,
)
async def get_vehicle(id: str) -> VehicleResponse:
    vehicle: ObjectResponse[Vehicle] = await tile38.get("fleet", id).asObject()

    response = {"data": vehicle.object}

    return VehicleResponse(**response)


@router.get(
    "/vehicle",
    tags=["vehicle"],
    response_model=VehiclesResponse,
    response_model_exclude_none=True,
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
)
async def set_vehicle(vehicle: Vehicle) -> JSONResponse:
    response = (
        await tile38.set("fleet", vehicle.properties.id).object(vehicle.dict()).exec()
    )

    return JSONResponse(**response.dict())
