from fastapi import FastAPI, status
from fastapi_key_auth import AuthorizerMiddleware
from app.db.db import tile38
from app.routers import geo, vehicle

app = FastAPI()

app.add_middleware(AuthorizerMiddleware, public_paths=["/ping", "^/"])

app.include_router(vehicle.router)
app.include_router(geo.router)


@app.on_event("shutdown")
async def shutdown_event():
    await tile38.quit()


@app.get("/ping", tags=["public"], status_code=status.HTTP_200_OK)
def ping():
    return {"ping": "pong!"}
