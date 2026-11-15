from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import Response

from Src.Core.validator import argument_exception
from Src.Dtos.report_type_dto import entity_type_enum
from Src.Logics.convert_factory import convert_factory
from Src.Logics.storage_manager import storage_manager
from Src.Services.entity_service import EntityService

router = APIRouter(prefix="/api/entities", tags=["Entities"])
_service = EntityService(storage_manager(), convert_factory())


def _etype(entity_type: str) -> entity_type_enum:
    try:
        return entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(400, str(e))


def _to_http(e: argument_exception) -> HTTPException:
    status = getattr(e, "http_status", 400)
    detail = str(e)
    refs = getattr(e, "references", None)
    if refs:
        detail = {"message": str(e), "references": refs}
    return HTTPException(status, detail)


@router.get("", status_code=200)
def list_all_entities():
    return _service.list_all()


@router.get("/{entity_type}", status_code=200)
def list_entities_by_type(entity_type: str):
    return _service.list_by_type(_etype(entity_type))


@router.get("/{entity_type}/{code}", status_code=200)
def read_entity(entity_type: str, code: str):
    try:
        return _service.get(_etype(entity_type), code)
    except argument_exception as e:
        raise _to_http(e)


@router.post("/{entity_type}", status_code=201)
def create_entity(entity_type: str, payload: dict = Body(...)):
    try:
        return _service.create(_etype(entity_type), payload)
    except argument_exception as e:
        raise _to_http(e)


@router.put("/{entity_type}/{code}", status_code=200)
def update_entity(entity_type: str, code: str, payload: dict = Body(...)):
    try:
        return _service.update(_etype(entity_type), code, payload)
    except argument_exception as e:
        raise _to_http(e)


@router.delete("/{entity_type}/{code}", status_code=204)
def delete_entity(entity_type: str, code: str):
    try:
        _service.delete(_etype(entity_type), code)
    except argument_exception as e:
        raise _to_http(e)
    return Response(status_code=204)
