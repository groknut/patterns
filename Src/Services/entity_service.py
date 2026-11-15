from Src.Core.abstract_model import abstract_model
from Src.Core.validator import argument_exception
from Src.Dtos.report_type_dto import entity_type_enum
from Src.Logics.convert_factory import convert_factory
from Src.Logics.storage_manager import storage_manager
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.recipe_model import recipe_model


class EntityService:
    """Service Layer для доменных сущностей (Фаулер).

    Отвечает за CRUD-операции и проверку связей. Хранение — в storage_manager.
    """

    __COLLECTIONS = {
        entity_type_enum.NOMENCLATURE: "nomenclatures",
        entity_type_enum.RANGE: "ranges",
        entity_type_enum.RECIPE: "recipes",
    }
    __MODELS = {
        entity_type_enum.NOMENCLATURE: nomenclature_model,
        entity_type_enum.RANGE: range_model,
        entity_type_enum.RECIPE: recipe_model,
    }

    def __init__(self, storage: storage_manager, factory: convert_factory) -> None:
        self.__storage = storage
        self.__factory = factory
        self.__ref_index: dict[str, list[dict]] | None = None

    # ---------------- Read ----------------
    def list_all(self) -> dict:
        st = self.__storage
        return {
            "nomenclature": self.__brief(st.nomenclatures),
            "range": self.__brief(st.ranges),
            "recipe": self.__brief(st.recipes),
        }

    def list_by_type(self, etype: entity_type_enum) -> list[dict]:
        coll = self.__collection(etype)
        return [self.__factory.convert(o) for o in coll.values()]

    def get(self, etype: entity_type_enum, code: str) -> dict:
        obj = self.__collection(etype).get(code)
        if obj is None:
            raise self.__not_found(code)
        return self.__factory.convert(obj)

    # ---------------- Write ----------------
    def create(self, etype: entity_type_enum, payload: dict) -> dict:
        coll = self.__collection(etype)
        model_cls = self.__MODELS[etype]

        new_obj = self.__factory.deserialize(payload, model_cls)
        if new_obj.id in coll:
            raise self.__conflict(f"Объект {new_obj.id} уже существует")

        coll[new_obj.id] = new_obj
        self.__ref_index = None
        return self.__factory.convert(new_obj)

    def update(self, etype: entity_type_enum, code: str, payload: dict) -> dict:
        coll = self.__collection(etype)
        if code not in coll:
            raise self.__not_found(code)

        model_cls = self.__MODELS[etype]
        updated = self.__factory.deserialize(payload, model_cls)

        # Смена кода — проверить входящие ссылки
        if updated.id != code:
            refs = self.find_references(code)
            if refs:
                raise self.__conflict(
                    f"Нельзя изменить код: на сущность есть {len(refs)} ссылок",
                    references=refs,
                )
            coll.pop(code)
            coll[updated.id] = updated
        else:
            coll[code] = updated

        self.__ref_index = None
        return self.__factory.convert(updated)

    def delete(self, etype: entity_type_enum, code: str) -> None:
        coll = self.__collection(etype)
        if code not in coll:
            raise self.__not_found(code)

        refs = self.find_references(code)
        if refs:
            raise self.__conflict(
                f"Нельзя удалить: на сущность есть {len(refs)} ссылок",
                references=refs,
            )

        del coll[code]
        self.__ref_index = None

    # ---------------- References (инвертированный индекс) ----------------
    def find_references(self, target_id: str) -> list[dict]:
        """O(1) lookup — индекс строится лениво и кэшируется до следующей мутации."""
        if self.__ref_index is None:
            self.__ref_index = self.__build_index()
        return self.__ref_index.get(target_id, [])

    def __build_index(self) -> dict[str, list[dict]]:
        """Один проход по всем объектам — O(N×K). Кэшируется до следующей мутации."""
        index: dict[str, list[dict]] = {}
        for coll_name, coll in self.__storage.data.items():
            for obj in coll.values():
                for field_name, ref in self.__iter_refs(obj):
                    index.setdefault(ref.id, []).append({
                        "entity_type": coll_name,
                        "entity_id": obj.id,
                        "entity_name": getattr(obj, "name", ""),
                        "field": field_name,
                    })
        return index

    def __iter_refs(self, obj):
        """Генератор ссылок: (имя_поля, целевая_модель)."""
        for field_name, value in self.__iter_fields(obj):
            if isinstance(value, abstract_model):
                yield field_name, value
            elif isinstance(value, (list, tuple)):
                for item in value:
                    if isinstance(item, abstract_model):
                        yield field_name, item

    def __iter_fields(self, obj):
        """Обходит @property по MRO + instance-атрибуты."""
        seen = set()
        for cls in type(obj).__mro__:
            for name, attr in vars(cls).items():
                if name in seen or not isinstance(attr, property):
                    continue
                seen.add(name)
                yield name, getattr(obj, name)
        for name, value in vars(obj).items():
            if name.startswith("_") or name in seen:
                continue
            seen.add(name)
            yield name, value

    # ---------------- Утилиты ----------------
    @staticmethod
    def __not_found(code: str) -> argument_exception:
        """argument_exception с http_status=404 (роутер превратит в HTTP 404)."""
        e = argument_exception(f"Объект {code} не найден")
        e.http_status = 404
        return e

    @staticmethod
    def __conflict(
        message: str, references: list[dict] | None = None
    ) -> argument_exception:
        """argument_exception с http_status=409 и списком ссылок (для CRUD-конфликтов)."""
        e = argument_exception(message)
        e.http_status = 409
        e.references = references or []
        return e

    def __collection(self, etype: entity_type_enum) -> dict:
        return self.__storage.data[self.__COLLECTIONS[etype]]

    @staticmethod
    def __brief(data: dict) -> list[dict]:
        return [{"id": x.id, "name": x.name} for x in data.values()]
