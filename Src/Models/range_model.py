from Src.Core.entity_model import entity_model
from Src.Core.validator import argument_exception, validator

class range_model(entity_model):
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
        validator.validate(value, range_model)
        self.__base = value

    @property
    def coef(self)->float:
        """Возвращает коэффициент пересчета"""
        return self.__coef

    @coef.setter
    def coef(self, value: float) -> None:
        """Устанваливает коэффициент пересчета"""
        validator.validate(value, int | float)
        if value <= 0:
            raise argument_exception("coef > 0!")
        self.__coef = float(value)
