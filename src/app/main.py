from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from fastapi_key_auth import AuthorizerDependency

from app.db.db import tile38
from app.routers import geo, vehicle

authorizer = AuthorizerDependency(key_pattern="API_KEY_")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await tile38.quit()


app = FastAPI(lifespan=lifespan, dependencies=[Depends(authorizer)])
app.include_router(vehicle.router)
app.include_router(geo.router)


@app.get("/ping", tags=["public"], status_code=status.HTTP_200_OK)
def ping():
    return {"ping": "pong!"}
