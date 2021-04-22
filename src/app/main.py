import os
from fastapi import FastAPI
from fastapi_key_auth import AuthorizerMiddleware
from app.db.db import tile38
from app.routers import geo, vehicle

app = FastAPI()

if os.getenv("SCOPE") and os.getenv("SCOPE") != "dev":
    app.add_middleware(AuthorizerMiddleware)

app.include_router(vehicle.router)
app.include_router(geo.router)


@app.on_event("shutdown")
async def shutdown_event():
    await tile38.quit()


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
