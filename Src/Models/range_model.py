from Src.Core.entity_model import entity
from Src.Core.exception import arguments_exception

class range_model(entity):
    """Модель единицы измерения
    Содержит:
        - базовая единица измерения
        - коэффициент пересчета
    """

    __base: "range_model" = None
    __coef: float = 1.0

    def __init__(
        self,
        name: str = "",
        coef: float = 1.0,
        base: "range_model" = None
    ) -> None:
        """Инициализирует единицу измерения"""
        super().__init__()
        self.name = name
        self.coef = coef
        self.__base = None
        if base is not None:
            self.base = base

    @property
    def base(self)->"range_model":
        """Возвращает базовую единицу измерения"""
        return self.__base

    @base.setter
    def base(
        self,
        value: "range_model"
    ) -> None:
        """Устанавливает базовую единицу измерения"""
        if value is None or not isinstance(value, range_model):
            raise arguments_exception(
                field="base"
            )
        self.__base = value

    @property
    def coef(self)->float:
        """Возвращает коэффициент пересчета"""
        return self.__coef

    @coef.setter
    def coef(self, value: float) -> None:
        """Устанваливает коэффициент пересчета"""
        if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
            raise arguments_exception(
                field="coef",
                message="Wrong argument: (int, float)"
            )
        if value <= 0:
            raise arguments_exception(
                field="coef",
                message="coef > 0!"
            )
        self.__coef = float(value)
