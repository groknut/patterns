import uvicorn
import yaml
from fastapi import FastAPI

from Src.Routers import entity_router, report_router
from Src.Routers.common import get_storage

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    try:
        with open("openapi.yaml", "r", encoding="utf-8") as f:
            app.openapi_schema = yaml.safe_load(f)
        return app.openapi_schema
    except FileNotFoundError:
        return FastAPI.openapi(app)


app.openapi = custom_openapi

get_storage()

app.include_router(report_router)
app.include_router(entity_router)


@app.post("/")
async def main():
    return "Hello, world"


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
