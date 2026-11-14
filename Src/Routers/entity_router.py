from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import Response

from Src.Dtos.report_type_dto import entity_type_enum
from Src.Routers.common import (
    get_collection_and_model,
    get_convert_factory,
    get_storage,
)

router = APIRouter(prefix="/api/entities", tags=["Entities"])


@router.get("", status_code=200, summary="Список всех сущностей по группам")
def list_all_entities():
    """id и name всех сущностей — краткая сводка."""
    st = get_storage()

    def brief(data: dict):
        return [{"id": x.id, "name": x.name} for x in data.values()]

    return {
        "nomenclature": brief(st.nomenclatures),
        "range": brief(st.ranges),
        "recipe": brief(st.recipes),
    }


@router.get("/{entity_type}", status_code=200, summary="Список объектов типа")
def list_entities_by_type(entity_type: str):
    try:
        etype = entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(400, str(e))

    collection, _ = get_collection_and_model(etype)
    factory = get_convert_factory()
    return [factory.convert(obj) for obj in collection.values()]


@router.get("/{entity_type}/{code}", status_code=200, summary="Получить объект")
def read_entity(entity_type: str, code: str):
    try:
        etype = entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(400, str(e))

    collection, _ = get_collection_and_model(etype)
    obj = collection.get(code)
    if obj is None:
        raise HTTPException(404, f"Объект {code} не найден")
    return get_convert_factory().convert(obj)


@router.post("/{entity_type}", status_code=201, summary="Создать объект")
def create_entity(entity_type: str, payload: dict = Body(...)):
    try:
        etype = entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(400, str(e))

    collection, model_cls = get_collection_and_model(etype)
    factory = get_convert_factory()
    try:
        new_obj = factory.deserialize(payload, model_cls)
        if new_obj.id in collection:
            raise HTTPException(400, f"Объект {new_obj.id} уже существует")
        collection[new_obj.id] = new_obj
        return factory.convert(new_obj)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Ошибка создания: {e}")


@router.put("/{entity_type}/{code}", status_code=200, summary="Обновить объект")
def update_entity(entity_type: str, code: str, payload: dict = Body(...)):
    try:
        etype = entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(400, str(e))

    collection, model_cls = get_collection_and_model(etype)
    if code not in collection:
        raise HTTPException(404, f"Объект {code} не найден")

    factory = get_convert_factory()
    try:
        updated = factory.deserialize(payload, model_cls)
    except Exception as e:
        raise HTTPException(400, f"Ошибка обновления: {e}")

    if updated.id != code:
        refs = get_storage().find_references(code)
        if refs:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": f"Нельзя изменить код: на сущность есть {len(refs)} ссылок",
                    "references": refs,
                },
            )
        collection.pop(code)
        collection[updated.id] = updated
    else:
        collection[code] = updated

    return factory.convert(updated)

@router.delete("/{entity_type}/{code}", status_code=204, summary="Удалить объект")
def delete_entity(entity_type: str, code: str):
    try:
        etype = entity_type_enum.from_str(entity_type)
    except ValueError as e:
        raise HTTPException(400, str(e))

    collection, _ = get_collection_and_model(etype)
    if code not in collection:
        raise HTTPException(404, f"Объект {code} не найден")

    refs = get_storage().find_references(code)
    if refs:
        raise HTTPException(
            status_code=409,
            detail={
                "message": f"Нельзя удалить: на сущность есть {len(refs)} ссылок",
                "references": refs,
            },
        )

    del collection[code]
    return Response(status_code=204)
