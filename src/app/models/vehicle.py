from typing import List
from pydantic import BaseModel, Field


class Geometry(BaseModel):
    type: str = "Point"
    coordinates: List[float] = Field(..., min_items=2, max_items=2)


class Properties(BaseModel):
    id: str


class Vehicle(BaseModel):
    type: str = "Feature"
    geometry: Geometry
    properties: Properties


class VehicleResponse(BaseModel):
    data: Vehicle


class VehiclesResponse(BaseModel):
    data: List[Vehicle]
