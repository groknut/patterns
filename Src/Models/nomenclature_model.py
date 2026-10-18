from Src.Core.entity_model import entity_model
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator


class nomenclature_model(entity_model):
    """Модель номенклатуры
    Содержит:
        - полное наименование
        - краткое наименование
        - группу номенклатуры
        - единицу измерения
    """

    __full_name: str = ""
    __full_name_max_len: int = 255
    __group: group_model = None
    __range: range_model = None

    def __init__(
        self,
        full_name: str = "",
        name: str = "",
        group: group_model = None,
        range: range_model = None,
    ) -> None:
        """Инициализирует номенклатуру"""
        super().__init__()
        self.name = name
        self.full_name = full_name
        self.group = group
        self.range = range

    @property
    def full_name(self) -> str:
        """Возвращает полное наименовныие номенклатуры"""
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        """Устанавливает полное наименование номенклатуры"""
        validator.validate(value, str, self.__full_name_max_len)
        self.__full_name = value

    @property
    def group(self) -> group_model:
        """Возвращает группу номенклатуры"""
        return self.__group

    @group.setter
    def group(self, value: group_model) -> None:
        """Устанавливает группу номенклатуры"""
        validator.validate(value, group_model)
        self.__group = value

    @property
    def range(self) -> range_model:
        """Возвращает единицу измерения номенклатуры"""
        return self.__range

    @range.setter
    def range(self, value: range_model) -> None:
        """Устанавливает единицу измерения номенклатуры"""
        validator.validate(value, range_model)
        self.__range = value


    @staticmethod
    def create_ingredient(
        name: str,
        full_name: str,
        group: group_model,
        rng: range_model,
    ) -> "nomenclature_model":
        """Универсальная фабрика: ингредиент с заданными именем, группой, единицей."""
        return nomenclature_model(full_name, name, group, rng)

    @staticmethod
    def create_pancake_portion(
        group: group_model,
        rng: range_model,
    ) -> "nomenclature_model":
        """Результат карты: 1 порция оладий."""
        return nomenclature_model(
            "Оладьи пышные на кефире, 1 порция",
            "Порция оладий пышных на кефире",
            group,
            rng,
        )
