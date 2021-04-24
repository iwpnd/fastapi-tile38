import pytest
from asyncio import get_event_loop
from typing import AsyncGenerator
from pyle38 import Tile38
from httpx import AsyncClient

from app.main import app
from app.config.settings import settings

default_tile38_leader_url = settings.TILE38_URI or "redis://localhost:9851"


@pytest.fixture(scope="session")
def event_loop():

    loop = get_event_loop()

    yield loop


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


@pytest.fixture(scope="module")
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
