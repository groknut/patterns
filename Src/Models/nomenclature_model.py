from Src.Core.entity_model import entity
from Src.Models.group_model import group_model
from Src.Models.range_model import range_model
from Src.Core.exception import arguments_exception, max_len_exception

class nomenclature_model(entity):
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
        range: range_model = None
    ) -> None:
        """Инициализирует номенклатуру"""
        super().__init__()
        self.name = name
        self.full_name = full_name
        self.group = group
        self.range = range

    @property
    def full_name(self)->str:
        """Возвращает полное наименовныие номенклатуры"""
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        """Устанавливает полное наименование номенклатуры"""
        if value is None or not isinstance(value, str):
            raise arguments_exception(
                field="full_name",
                message="Wrong argument: str"
            )
        if len(value.strip()) > self.__full_name_max_len:
            raise max_len_exception(
                field="full_name",
                max_length=self.__full_name_max_len
            )
        self.__full_name = value

    @property
    def group(self)->group_model:
        """Возвращает группу номенклатуры"""
        return self.__group

    @group.setter
    def group(self, value: group_model) -> None:
        """Устанавливает группу номенклатуры"""
        if value is not None and not isinstance(value, group_model):
            raise arguments_exception(
                field="group",
                message="Wrong argument: group_model"
            )
        self.__group = value

    @property
    def range(self)->range_model:
        """Возвращает единицу измерения номенклатуры"""
        return self.__range

    @range.setter
    def range(self, value: range_model) -> None:
        """Устанавливает единицу измерения номенклатуры"""
        if value is not None and not isinstance(value, range_model):
            raise arguments_exception(
                field="range",
                message="Wrong argument: range_model"
            )
        self.__range = value
