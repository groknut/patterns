from Src.Core.event_type import event_type
from Src.Logics.observer import observer
import uvicorn
import yaml
from fastapi import FastAPI

from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Services.logger_service import logger_service

_sm = settings_manager()
_sm.load()
_storage = storage_manager()
_storage.convert(_sm.settings.is_first)

from Src.Routers import entity_router, report_router

app = FastAPI()

logger_service(log_file="logs/app.log")

@app.middleware("http")
async def log_web_calls(request, call_next):
    """Логирование каждого HTTP-запроса."""
    try:
        observer.create(
            event_type.web_call(),
            {"method": request.method, "path": request.url.path},
        )
    except Exception as e:
        print(f"[logger] web_call error: {e}")
    return await call_next(request)

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
app.include_router(report_router)
app.include_router(entity_router)


@app.post("/")
async def main():
    return "Hello, world"


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
