from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from Src.Dtos.report_type_dto import entity_type_enum, report_type_enum
from Src.Logics.report_factory import report_factory
from Src.Routers.common import get_collection_and_model, get_source_factory

router = APIRouter(prefix="/api/report", tags=["Reports"])

def _resolve(entity_type: str, code: str, format: str | None = None):
    try:
        etype = entity_type_enum.from_str(entity_type)
        fmt = report_type_enum.from_str(format) if format else None
    except ValueError as e:
        raise HTTPException(400, str(e))

    collection, _ = get_collection_and_model(etype)
    entity = collection.get(code)
    if entity is None:
        raise HTTPException(404, f"Сущность {etype.value} с кодом {code} не найдена")
    return fmt, entity, etype


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


@router.get("/formats", status_code=200, summary="Список форматов отчётов")
def get_report_formats():
    """Возвращает список доступных форматов отчётов."""
    return [fmt.value for fmt in report_type_enum]


@router.get("/default/{entity_type}/{code}", status_code=200,
            summary="Отчёт в формате из настроек")
def get_report_default(entity_type: str, code: str):
    _, entity, etype = _resolve(entity_type, code)
    source = get_source_factory().create(etype, entity)
    report = report_factory().create_default()
    return _render(report, source, etype, code)


@router.get("/{format}/{entity_type}/{code}", status_code=200,
            summary="Отчёт в явно указанном формате")
def get_report_in_format(format: str, entity_type: str, code: str):
    fmt, entity, etype = _resolve(entity_type, code, format)
    source = get_source_factory().create(etype, entity)
    report = report_factory().create(fmt)
    return _render(report, source, etype, code)
