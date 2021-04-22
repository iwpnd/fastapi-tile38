from typing import List
from pydantic import BaseModel


class Geometry(BaseModel):
    type: str = "Point"
    coordinates: List[float]


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
