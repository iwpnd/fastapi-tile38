import pytest
from httpx import AsyncClient
from fastapi import status
from pyle38 import Tile38

key = "fleet"
id = "truck"
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
async def test_within_unauthorized(ac: AsyncClient):
    response = await ac.get(
        "/search/within",
        params={"lon": lon, "lat": lat, "radius": 100},
        headers=invalid_key,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_within_empty(ac: AsyncClient):
    response = await ac.get(
        "/search/within", headers=valid_key, params={"lon": 1, "lat": 1, "radius": 1000}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"data": []}


@pytest.mark.asyncio
async def test_within(ac: AsyncClient, tile38: Tile38):
    await tile38.set(key, id).object(feature).exec()

    response = await ac.get(
        "/search/within",
        headers=valid_key,
        params={"lon": lon, "lat": lat, "radius": 100},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"data": [{"id": id, "object": feature}]}


@pytest.mark.asyncio
async def test_nearby_unauthorized(ac: AsyncClient):
    response = await ac.get(
        "/search/nearby",
        params={"lon": lon, "lat": lat, "radius": 100},
        headers=invalid_key,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_nearby_without_radius(ac: AsyncClient, tile38: Tile38):
    await tile38.set(key, id).object(feature).exec()

    response = await ac.get(
        "/search/nearby", headers=valid_key, params={"lon": 13.38, "lat": 52.26}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "data": [{"id": id, "object": feature, "distance": pytest.approx(1300, 5)}]
    }


@pytest.mark.asyncio
async def test_nearby_with_radius(ac: AsyncClient, tile38: Tile38):
    await tile38.set(key, id).object(feature).exec()

    response = await ac.get(
        "/search/nearby",
        headers=valid_key,
        params={"lon": 13.38, "lat": 52.26, "radius": 1000},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"data": []}
