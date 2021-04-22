from fastapi import FastAPI
from fastapi_key_auth import AuthorizerMiddleware
from app.db.db import tile38
from app.routers import vehicle

app = FastAPI()

app.add_middleware(AuthorizerMiddleware)


app.include_router(vehicle.router)


@app.on_event("shutdown")
async def shutdown_event():
    await tile38.quit()


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
