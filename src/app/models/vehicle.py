from typing import List

from pydantic import BaseModel, Field
from pyle38.responses import Object


class Geometry(BaseModel):
    type: str = "Point"
    coordinates: List[float] = Field(..., min_length=2, max_length=2)


class Properties(BaseModel):
    id: str


class Vehicle(BaseModel):
    type: str = "Feature"
    geometry: Geometry
    properties: Properties


class VehicleRequestBody(BaseModel):
    data: Vehicle


class VehicleResponse(BaseModel):
    data: Vehicle


class VehiclesResponse(BaseModel):
    data: List[Object[Vehicle]]
