from Src.Dtos.report_type_dto import entity_type_enum, report_type_enum
from Src.Logics.report_factory import report_factory
from Src.Logics.report_sources import report_source_factory
from Src.Logics.storage_manager import storage_manager
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.recipe_model import recipe_model


class ReportService:
    """Service Layer для отчётов."""

    __MODELS = {
        entity_type_enum.NOMENCLATURE: nomenclature_model,
        entity_type_enum.RANGE: range_model,
        entity_type_enum.RECIPE: recipe_model,
    }

    def __init__(self, storage: storage_manager, source_factory: report_source_factory) -> None:
        self.__storage = storage
        self.__source_factory = source_factory

    def list_formats(self) -> list[str]:
        return [fmt.value for fmt in report_type_enum]

    def get_default(self, etype: entity_type_enum, code: str):
        entity = self.__get_entity(etype, code)
        source = self.__source_factory.create(etype, entity)
        return report_factory().create_default().build(source)

    def get_in_format(self, etype: entity_type_enum, code: str, fmt: report_type_enum):
        entity = self.__get_entity(etype, code)
        source = self.__source_factory.create(etype, entity)
        return report_factory().create(fmt).build(source)

    def __get_entity(self, etype: entity_type_enum, code: str):
        coll = self.__storage.data[self.__coll_name(etype)]
        entity = coll.get(code)
        if entity is None:
            from Src.Core.validator import argument_exception
            raise argument_exception(f"Сущность {etype.value} с кодом {code} не найдена")
        return entity

    @staticmethod
    def __coll_name(etype: entity_type_enum) -> str:
        return {
            entity_type_enum.NOMENCLATURE: "nomenclatures",
            entity_type_enum.RANGE: "ranges",
            entity_type_enum.RECIPE: "recipes",
        }[etype]
