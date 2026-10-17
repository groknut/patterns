import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response

from Src.Dtos.report_type_dto import entity_type_enum, report_type_enum
from Src.Logics.report_factory import report_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report

app = FastAPI()


setting_manager = settings_manager()
setting_manager.load()
storage = storage_manager()
storage.convert(setting_manager.settings.is_first)


def _find_entity(etype: entity_type_enum, code: str):
    if etype == entity_type_enum.NOMENCLATURE:
        return storage.nomenclatures.get(code)
    if etype == entity_type_enum.RANGE:
        return storage.ranges.get(code)
    if etype == entity_type_enum.RECIPE:
        return storage.recipes.get(code)
    return None


def _render(fmt: report_type_enum, source):
    report = report_factory().create(fmt)
    result = report.build(source)

    if fmt in (report_type_enum.CSV, report_type_enum.MARKDOWN):
        media = (
            "text/csv; charset=utf-8"
            if fmt == report_type_enum.CSV
            else "text/markdown; charset=utf-8"
        )
        return Response(content=bytes(result.binary), media_type=media)

    media_map = {
        report_type_enum.TXT: "text/plain; charset=utf-8",
        report_type_enum.XML: "application/xml; charset=utf-8",
        report_type_enum.HTML: "text/html; charset=utf-8",
    }
    return Response(content=result.text, media_type=media_map[fmt])


@app.post("/")
async def main():
    return "Hello, world"


@app.get("/api/get_report", status_code=status.HTTP_200_OK)
def get_report():
    recipe = next(iter(storage.recipes.values()))
    report = text_report()
    rep = report.build(recipe)

    assert rep.binary == []
    assert rep.text != ""
    return rep.text


@app.get(
    "/api/report/{format}/{entity_type}/{code}",
    summary="Сформировать отчет в указанном формате",
    description="Формат: TXT, CSV, Markdown, XML, HTML. "
                "Тип: nomenclature, range, recipe. Код — id сущности.",
    status_code=status.HTTP_200_OK,
)
def get_report_in_format(format: str, entity_type: str, code: str):
    try:
        fmt = report_type_enum.from_str(format)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        etype = entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    source = _find_entity(etype, code)
    if source is None:
        raise HTTPException(
            status_code=404,
            detail=f"Сущность {etype.value} с кодом {code} не найдена",
        )

    return _render(fmt, source)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
