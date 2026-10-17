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


def _render(fmt, source, etype, code):
    """CSV/Markdown — файл (attachment); TXT/XML/HTML — структурированный текст."""
    result = report_factory().create(fmt).build(source)

    if fmt in (report_type_enum.CSV, report_type_enum.MARKDOWN):
        ext = "csv" if fmt == report_type_enum.CSV else "md"
        return Response(
            content=bytes(result.binary),
            media_type=f"text/{fmt.value.lower()}; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="report_{etype.value}_{code[:8]}.{ext}"'
            },
        )

    media = {
        report_type_enum.TXT: "text/plain",
        report_type_enum.XML: "application/xml",
        report_type_enum.HTML: "text/html",
    }[fmt]
    return Response(content=result.text, media_type=f"{media}; charset=utf-8")


@app.post("/")
async def main():
    return "Hello, world"


@app.get("/api/get_report", status_code=status.HTTP_200_OK)
def get_report():
    rep = text_report().build(next(iter(storage.recipes.values())))
    assert rep.binary == [] and rep.text != ""
    return rep.text


@app.get(
    "/api/report/{format}/{entity_type}/{code}",
    status_code=200,
    summary="Отчет в указанном формате",
)
def get_report_in_format(format: str, entity_type: str, code: str):
    fmt, source, etype = _resolve(entity_type, code, format)
    return _render(fmt, source, etype, code)


@app.get(
    "/api/report/default/{entity_type}/{code}",
    status_code=200,
    summary="Отчет в формате из настроек (create_default)",
)
def get_report_default(entity_type: str, code: str):
    _, source, etype = _resolve(entity_type, code)
    fmt = (
        setting_manager.settings.response_format
        if setting_manager.settings
        else report_type_enum.TXT
    )
    return _render(fmt, source, etype, code)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
