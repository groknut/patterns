from collections import defaultdict
from typing import Iterator

from Src.Core.abstract_model import abstract_model
from Src.Core.entity_reference import EntityReference
from Src.Core.validator import argument_exception
from Src.Dtos.report_type_dto import entity_type_enum
from Src.Logics.convert_factory import convert_factory
from Src.Logics.storage_manager import storage_manager
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.recipe_model import recipe_model


class EntityService:
    """Service Layer для доменных сущностей (Фаулер).

    Отвечает за CRUD-операции и проверку связей.
    Хранение — в storage_manager (репозиторий).
    """

    __MODELS = {
        entity_type_enum.NOMENCLATURE: nomenclature_model,
        entity_type_enum.RANGE: range_model,
        entity_type_enum.RECIPE: recipe_model,
    }

    def __init__(self, storage: storage_manager, factory: convert_factory) -> None:
        self.__storage = storage
        self.__factory = factory
        self.__ref_index: dict[str, list[EntityReference]] | None = None

    # ---------------- Read ----------------
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
            raise self.__not_found(code)
        return self.__factory.convert(obj)

    # ---------------- Write ----------------
    def create(self, etype: entity_type_enum, payload: dict) -> dict:
        coll = self.__collection(etype)
        new_obj = self.__factory.deserialize(payload, self.__MODELS[etype])
        if new_obj.id in coll:
            raise self.__conflict(f"Объект {new_obj.id} уже существует")
        coll[new_obj.id] = new_obj
        self.__ref_index = None
        return self.__factory.convert(new_obj)

    def update(self, etype: entity_type_enum, code: str, payload: dict) -> dict:
        coll = self.__collection(etype)
        if code not in coll:
            raise self.__not_found(code)

        updated = self.__factory.deserialize(payload, self.__MODELS[etype])

        # Смена кода — проверить входящие ссылки
        if updated.id != code:
            self.__check_refs(code, "Нельзя изменить код")
            coll.pop(code)

        coll[updated.id] = updated
        self.__ref_index = None
        return self.__factory.convert(updated)

    def delete(self, etype: entity_type_enum, code: str) -> None:
        coll = self.__collection(etype)
        if code not in coll:
            raise self.__not_found(code)
        self.__check_refs(code, "Нельзя удалить")
        del coll[code]
        self.__ref_index = None

    # ---------------- References ----------------
    def find_references(self, target_id: str) -> list[EntityReference]:
        """O(1) — индекс строится лениво и кэшируется до следующей мутации."""
        if self.__ref_index is None:
            self.__ref_index = self.__build_index()
        return self.__ref_index.get(target_id, [])

    def __build_index(self) -> dict[str, list[EntityReference]]:
        """Один проход по всем объектам через ленивый генератор storage."""
        index: dict[str, list[EntityReference]] = defaultdict(list)
        for coll_name, obj in self.__storage.iter_all_objects():
            for field_name, target in self.__iter_obj_refs(obj):
                index[target.id].append(
                    EntityReference(coll_name, obj.id, obj.name, field_name)
                )
        return dict(index)

    def __iter_obj_refs(self, obj) -> Iterator[tuple[str, abstract_model]]:
        """Исходящие ссылки одного объекта: (поле, целевая_модель)."""
        for name, value in self.__iter_fields(obj):
            if isinstance(value, abstract_model):
                yield name, value
            elif isinstance(value, (list, tuple)):
                for item in value:
                    if isinstance(item, abstract_model):
                        yield name, item

    def __iter_fields(self, obj) -> Iterator[tuple[str, object]]:
        """Обход @property по MRO + instance-атрибуты."""
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

    def __check_refs(self, code: str, prefix: str) -> None:
        """Бросает 409-конфликт, если на сущность есть ссылки."""
        refs = self.find_references(code)
        if refs:
            raise self.__conflict(
                f"{prefix}: на сущность есть {len(refs)} ссылок",
                references=refs,
            )

    # ---------------- Утилиты ----------------
    @staticmethod
    def __not_found(code: str) -> argument_exception:
        e = argument_exception(f"Объект {code} не найден")
        e.http_status = 404
        return e

    @staticmethod
    def __conflict(
        message: str, references: list[EntityReference] | None = None
    ) -> argument_exception:
        e = argument_exception(message)
        e.http_status = 409
        e.references = references or []
        return e

    def __collection(self, etype: entity_type_enum) -> dict:
        """Коллекция storage для указанного типа (без доступа к .data)."""
        st = self.__storage
        return {
            entity_type_enum.NOMENCLATURE: st.nomenclatures,
            entity_type_enum.RANGE: st.ranges,
            entity_type_enum.RECIPE: st.recipes,
        }[etype]

    @staticmethod
    def __brief(data: dict) -> list[dict]:
        return [{"id": x.id, "name": x.name} for x in data.values()]
