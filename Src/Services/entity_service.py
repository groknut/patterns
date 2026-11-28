from collections import defaultdict
from typing import Iterator

from Src.Core.event_type import event_type
from Src.Logics.observer import observer
from Src.Logics.prototypes import filter_prototype, balance_prototype

from Src.Core.abstract_model import abstract_model
from Src.Core.entity_reference import EntityReference
from Src.Core.validator import argument_exception
from Src.Dtos.filter_dto import filter_dto
from Src.Dtos.report_type_dto import entity_type_enum
from Src.Logics.convert_factory import convert_factory
from Src.Logics.storage_manager import storage_manager
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.recipe_model import recipe_model


class EntityService:
    """Service Layer для доменных сущностей (CRUD + проверка связей)."""

    __MODELS = {
        entity_type_enum.NOMENCLATURE: nomenclature_model,
        entity_type_enum.RANGE: range_model,
        entity_type_enum.RECIPE: recipe_model,
    }

    def __init__(self, storage: storage_manager, factory: convert_factory) -> None:
        self.__storage = storage
        self.__factory = factory
        self.__refs: dict[str, list[EntityReference]] | None = None

    def list_all(self) -> dict:
        st = self.__storage
        return {
            "nomenclature": self.__brief(st.nomenclatures),
            "range": self.__brief(st.ranges),
            "recipe": self.__brief(st.recipes),
        }

    def list_by_type(self, etype: entity_type_enum) -> list[dict]:
        return [self.__factory.convert(o) for o in self.__collection(etype).values()]

    def get(self, etype: entity_type_enum, code: str) -> dict:
        obj = self.__collection(etype).get(code)
        if obj is None:
            raise self.__err(404, f"Объект {code} не найден")
        return self.__factory.convert(obj)

    def create(self, etype: entity_type_enum, payload: dict) -> dict:
        coll = self.__collection(etype)
        obj = self.__factory.deserialize(payload, self.__MODELS[etype])
        if obj.id in coll:
            raise self.__err(409, f"Объект {obj.id} уже существует")
        coll[obj.id] = obj
        self.__refs = None
        observer.create(
            event_type.crud_operation(),
            {"action": "create", "type": etype.value, "id": obj.id, "name": obj.name},
        )
        return self.__factory.convert(obj)

    def update(self, etype: entity_type_enum, code: str, payload: dict) -> dict:
        coll = self.__collection(etype)
        if code not in coll:
            raise self.__err(404, f"Объект {code} не найден")

        obj = self.__factory.deserialize(payload, self.__MODELS[etype])
        if obj.id != code:
            self.__guard(code, "Нельзя изменить код")
            coll.pop(code)
        coll[obj.id] = obj
        self.__refs = None
        observer.create(
            event_type.crud_operation(),
            {"action": "update", "type": etype.value, "id": obj.id, "name": obj.name},
        )
        return self.__factory.convert(obj)

    def delete(self, etype: entity_type_enum, code: str) -> None:
        coll = self.__collection(etype)
        if code not in coll:
            raise self.__err(404, f"Объект {code} не найден")
        self.__guard(code, "Нельзя удалить")
        del coll[code]
        observer.create(
            event_type.crud_operation(),
            {"action": "delete", "type": etype.value, "id": code},
        )
        self.__refs = None

    def find_references(self, target_id: str) -> list[EntityReference]:
        """O(1) lookup — индекс строится лениво"""
        if self.__refs is None:
            self.__refs = defaultdict(list)
            for coll_name, obj in self.__storage.iter_all_objects():
                for field_name, model in self.__iter_object_refs(obj):
                    self.__refs[model.id].append(
                        EntityReference(coll_name, obj.id, obj.name, field_name)
                    )
        return self.__refs.get(target_id, [])

    def __guard(self, code: str, prefix: str) -> None:
        """Бросает 409, если на объект есть ссылки."""
        refs = self.find_references(code)
        if refs:
            raise self.__err(409, f"{prefix}: {len(refs)} ссылок", references=refs)

    def __iter_object_refs(self, obj) -> Iterator[tuple[str, abstract_model]]:
        """Исходящие ссылки объекта: (имя_поля, целевая_модель)."""
        for name, value in self.__iter_fields(obj):
            if isinstance(value, abstract_model):
                yield name, value
            elif isinstance(value, (list, tuple)):
                for item in value:
                    if isinstance(item, abstract_model):
                        yield name, item

    def __iter_fields(self, obj) -> Iterator[tuple[str, object]]:
        """@property по MRO + instance-атрибуты (без _)."""
        seen = set()
        for cls in type(obj).__mro__:
            for name, attr in vars(cls).items():
                if name not in seen and isinstance(attr, property):
                    seen.add(name)
                    yield name, getattr(obj, name)
        for name, value in vars(obj).items():
            if not name.startswith("_") and name not in seen:
                seen.add(name)
                yield name, value

    # ---------------- Helpers ----------------
    def __collection(self, etype: entity_type_enum) -> dict:
        st = self.__storage
        return {
            entity_type_enum.NOMENCLATURE: st.nomenclatures,
            entity_type_enum.RANGE: st.ranges,
            entity_type_enum.RECIPE: st.recipes,
        }[etype]

    @staticmethod
    def __brief(data: dict) -> list[dict]:
        return [{"id": x.id, "name": x.name} for x in data.values()]

    @staticmethod
    def __err(status: int, message: str, references=None) -> argument_exception:
        e = argument_exception(message)
        e.http_status = status
        e.references = references or []
        return e


    # ---------------- Filter & Balance ----------------
    def filter(self, etype: entity_type_enum, dto: filter_dto) -> list[dict]:
        """Фильтрует объекты указанного типа согласно DTO."""
        objects = list(self.__collection(etype).values())
        filtered = filter_prototype(objects).filter(dto).data
        observer.create(
            event_type.crud_operation(),
            {"action": "filter", "type": etype.value, "filters": len(dto.filters) if dto else 0},
        )
        return [self.__factory.convert(o) for o in filtered]
