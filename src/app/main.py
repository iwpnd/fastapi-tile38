from fastapi import FastAPI, status, Depends
from fastapi_key_auth import AuthorizerDependency
from app.db.db import tile38
from app.routers import geo, vehicle

authorizer = AuthorizerDependency(key_pattern="API_KEY_")

app = FastAPI(dependencies=[Depends(authorizer)])
app.include_router(vehicle.router)
app.include_router(geo.router)


@app.on_event("shutdown")
async def shutdown_event():
    await tile38.quit()


@app.get("/ping", tags=["public"], status_code=status.HTTP_200_OK)
def ping():
    return {"ping": "pong!"}
