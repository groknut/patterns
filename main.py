import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response

from Src.Dtos.report_type_dto import report_type_enum, entity_type_enum
from Src.Logics.report_factory import report_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report

app = FastAPI()

setting_manager = settings_manager()
setting_manager.load()
storage = storage_manager()
storage.convert(setting_manager.settings.is_first)


def _resolve(entity_type: str, code: str, format: str = None):
    """Возвращает (fmt, source, etype) или бросает 400/404."""
    try:
        etype = entity_type_enum.from_str(entity_type)
        fmt = report_type_enum.from_str(format) if format else None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    source = {
        entity_type_enum.NOMENCLATURE: storage.nomenclatures,
        entity_type_enum.RANGE: storage.ranges,
        entity_type_enum.RECIPE: storage.recipes,
    }[etype].get(code)
    if source is None:
        raise HTTPException(
            status_code=404,
            detail=f"Сущность {etype.value} с кодом {code} не найдена",
        )
    return fmt, source, etype


def _render(report, source, etype, code):
    result = report.build(source)

    if report.is_binary:
        return Response(
            content=bytes(result.binary),
            media_type=report.media_type,
            headers={
                "Content-Disposition":
                    f'attachment; filename="report_{etype.value}_{code[:8]}.{report.file_extension}"'
            },
        )
    return Response(content=result.text, media_type=report.media_type)


@app.post("/")
async def main():
    return "Hello, world"


@app.get("/api/get_report", status_code=status.HTTP_200_OK)
def get_report():
    rep = text_report().build(next(iter(storage.recipes.values())))
    assert rep.binary == [] and rep.text != ""
    return rep.text

@app.get("/api/report/default/{entity_type}/{code}")
def get_report_default(entity_type: str, code: str):
    fmt, source, etype = _resolve(entity_type, code)
    report = report_factory().create_default()
    return _render(report, source, etype, code)

@app.get("/api/report/{format}/{entity_type}/{code}")
def get_report_in_format(format: str, entity_type: str, code: str):
    fmt, source, etype = _resolve(entity_type, code, format)
    report = report_factory().create(fmt)
    return _render(report, source, etype, code)

@app.get("/api/entities", summary="Список кодов всех сущностей")
def list_entities():
    """Возвращает id всех сущностей — удобно для демонстрации."""
    def brief(data: dict):
        return [{"id": x.id, "name": x.name} for x in data.values()]

    return {
        "nomenclature": brief(storage.nomenclatures),
        "range": brief(storage.ranges),
        "recipe": brief(storage.recipes),
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
