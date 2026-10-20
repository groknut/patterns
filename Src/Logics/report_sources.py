from Src.Core.report_source import report_source
from Src.Core.validator import argument_exception
from Src.Dtos.report_type_dto import entity_type_enum
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.recipe_model import recipe_model


class recipe_report_source(report_source):
    """Источник данных для отчёта по рецепту."""

    def __init__(self, recipe: recipe_model) -> None:
        self.__recipe = recipe

    def report_headers(self) -> list[str]:
        return ["Код", "Наименование", "Брутто", "Нетто"]

    def report_rows(self) -> list[list[str]]:
        return [
            [item.id, item.name, str(item.gross_weight), str(item.net_weight)]
            for item in self.__recipe.ingredients
        ]


class nomenclature_report_source(report_source):
    """Источник данных для отчёта по номенклатуре."""

    def __init__(self, nom: nomenclature_model) -> None:
        self.__nom = nom

    def report_headers(self) -> list[str]:
        return ["Код", "Наименование", "Полное наименование", "Группа", "Ед. изм."]

    def report_rows(self) -> list[list[str]]:
        return [
            [
                self.__nom.id,
                self.__nom.name,
                self.__nom.full_name,
                self.__nom.group.name if self.__nom.group else "",
                self.__nom.range.name if self.__nom.range else "",
            ]
        ]


class range_report_source(report_source):
    """Источник данных для отчёта по единице измерения."""

    def __init__(self, rng: range_model) -> None:
        self.__rng = rng

    def report_headers(self) -> list[str]:
        return ["Код", "Наименование", "Коэффициент", "Базовая единица"]

    def report_rows(self) -> list[list[str]]:
        return [
            [
                self.__rng.id,
                self.__rng.name,
                str(self.__rng.coef),
                self.__rng.base.name if self.__rng.base else "-",
            ]
        ]


class report_source_factory:
    """Фабрика источников данных отчёта.

    Новый тип сущности — новый класс выше + одна строка в __mapping.
    """

    __mapping: dict

    def __init__(self):
        self.__mapping = {
            entity_type_enum.RECIPE: recipe_report_source,
            entity_type_enum.NOMENCLATURE: nomenclature_report_source,
            entity_type_enum.RANGE: range_report_source,
        }

    def create(self, etype: entity_type_enum, entity) -> report_source:
        source_cls = self.__mapping.get(etype)
        if source_cls is None:
            raise argument_exception(
                f"Для типа {etype.value} не зарегистрирован report_source"
            )
        return source_cls(entity)
