import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from pyle38 import Tile38

from app.config.settings import settings
from app.main import app

default_tile38_leader_url = settings.TILE38_URI or "redis://localhost:9851"


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def create_tile38(request, event_loop):
    async def f(url: str = default_tile38_leader_url):
        tile38 = Tile38(url)

        def teardown():
            async def ateardown():
                try:
                    await tile38.flushdb()
                # TODO: find explicit exception
                except Exception:
                    await tile38.flushdb()

                await tile38.quit()

            if event_loop.is_running():
                event_loop.create_task(ateardown())
            else:
                event_loop.run_until_complete(ateardown())

        request.addfinalizer(teardown)
        return tile38

    return f


@pytest.fixture()
async def ac() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture()
async def tile38(create_tile38):
    yield await create_tile38()


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("API_KEY_DEV", "test")
    monkeypatch.setenv("TILE38_URI", "redis://localhost:9851")
    monkeypatch.setenv("ENVIRONMENT", "test")
