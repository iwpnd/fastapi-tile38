import os
from fastapi import FastAPI
from pyle38 import Tile38

app = FastAPI(title="test app")
tile38 = Tile38(os.getenv("TILE38_URI"))


@app.on_event("shutdown")
async def shutdown_event():
    await tile38.quit()


@app.post("/vehicle")
async def set_vehicle():
    response = await tile38.set("fleet", "truck").point(1, 1).exec()

    return response.dict()


@app.get("/vehicle")
async def get_vehicle():
    response = await tile38.get("fleet", "truck").asObject()

    return response.dict()


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
