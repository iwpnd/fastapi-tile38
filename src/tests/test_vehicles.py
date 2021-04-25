import pytest
from httpx import AsyncClient
from fastapi import status
from pyle38 import Tile38

key = "fleet"
id = "truck1"
lat = 52.25
lon = 13.37

feature = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [lon, lat]},
    "properties": {"id": id},
}

valid_key = {"x-api-key": "test"}
invalid_key = {"x-api-key": "invalid"}


@pytest.mark.asyncio
async def test_ping(ac: AsyncClient):
    response = await ac.get("/ping", headers=valid_key)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ping": "pong!"}


@pytest.mark.asyncio
async def test_get_vehicle_unauthorized(ac: AsyncClient):
    response = await ac.get("/vehicle/truck1", headers=invalid_key)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_vehicle(ac: AsyncClient, tile38: Tile38):
    await tile38.set(key, id).object(feature).exec()

    response = await ac.get(f"/vehicle/{id}", headers=valid_key)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_vehicle_notfound(ac: AsyncClient):
    response = await ac.get("/vehicle/truck1", headers=valid_key)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "vehicle with id 'truck1' not found"}


@pytest.mark.asyncio
async def test_set_vehicle(ac: AsyncClient, tile38: Tile38):
    post = await ac.post("/vehicle", json={"data": feature}, headers=valid_key)

    assert post.status_code == status.HTTP_201_CREATED

    response = await tile38.get(key, id).asObject()

    assert response.object == feature
