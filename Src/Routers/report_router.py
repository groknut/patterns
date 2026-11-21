from Src.Dtos.filter_dto import filter_dto
from Src.Services.report_service import ReportService
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from Src.Core.validator import argument_exception
from Src.Dtos.report_type_dto import entity_type_enum, report_type_enum
from Src.Logics.report_factory import report_factory
from Src.Logics.report_sources import report_source_factory
from Src.Logics.storage_manager import storage_manager

router = APIRouter(prefix="/api/report", tags=["Reports"])

_COLLECTIONS = {
    entity_type_enum.NOMENCLATURE: "nomenclatures",
    entity_type_enum.RANGE: "ranges",
    entity_type_enum.RECIPE: "recipes",
}


def _get_entity(etype: entity_type_enum, code: str):
    coll = storage_manager().data[_COLLECTIONS[etype]]
    entity = coll.get(code)
    if entity is None:
        raise argument_exception(f"Сущность {etype.value} с кодом {code} не найдена")
    return entity


def _render(report, result, etype, code):
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


@router.get("/formats", status_code=200)
def get_report_formats():
    return [fmt.value for fmt in report_type_enum]


@router.get("/default/{entity_type}/{code}", status_code=200)
def get_report_default(entity_type: str, code: str):
    try:
        etype = entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(400, str(e))
    try:
        entity = _get_entity(etype, code)
    except argument_exception as e:
        raise HTTPException(404, str(e))
    source = report_source_factory().create(etype, entity)
    report = report_factory().create_default()
    return _render(report, report.build(source), etype, code)


@router.get("/{format}/{entity_type}/{code}", status_code=200)
def get_report_in_format(format: str, entity_type: str, code: str):
    try:
        etype = entity_type_enum.from_str(entity_type)
        fmt = report_type_enum.from_str(format)
    except ValueError as e:
        raise HTTPException(400, str(e))
    try:
        entity = _get_entity(etype, code)
    except argument_exception as e:
        raise HTTPException(404, str(e))
    source = report_source_factory().create(etype, entity)
    report = report_factory().create(fmt)
    return _render(report, report.build(source), etype, code)


@router.post("/{entity_type}/balance", status_code=200, summary="ОСВ с фильтрацией")
def get_balance(entity_type: str, payload: filter_dto):
    """Формирует ОСВ по отфильтрованным объектам."""
    try:
        etype = entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(400, str(e))
    service = ReportService(storage_manager(), report_source_factory())
    return service.get_balance(etype, payload)
