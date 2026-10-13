from Src.Core.entity_model import entity_model
from Src.Core.validator import argument_exception, validator


class range_model(entity_model):
    """Модель единицы измерения
    Содержит:
        - базовую единицу измерения
        - коэффициент пересчёта к базовой
    """

    __base: "range_model" = None
    __coef: float = 1.0

    def __init__(
        self,
        name: str = "",
        coef: float = 1.0,
        base: "range_model" = None,
    ) -> None:
        """Инициализирует единицу измерения"""
        super().__init__()
        self.name = name
        self.coef = coef
        self.__base = None
        if base is not None:
            self.base = base

    @property
    def base(self) -> "range_model":
        """Возвращает базовую единицу измерения"""
        return self.__base

    @base.setter
    def base(self, value: "range_model") -> None:
        """Устанавливает базовую единицу измерения"""
        validator.validate(value, range_model)
        if value is self:
            raise argument_exception("Единица не может быть базовой сама для себя")
        self.__base = value

    @property
    def coef(self) -> float:
        """Возвращает коэффициент пересчёта"""
        return self.__coef

    @coef.setter
    def coef(self, value: float) -> None:
        """Устанавливает коэффициент пересчёта"""
        validator.validate(value, (int, float))
        if value <= 0:
            raise argument_exception("coef должен быть больше нуля")
        self.__coef = float(value)

    @property
    def grams_per_unit(self) -> float:
        """Сколько базовых единиц в одной этой: произведение coef по цепочке base."""
        factor = 1.0
        node = self
        while node is not None:
            factor *= node.coef
            node = node.base
        return factor

    # фабричные методы
    @staticmethod
    def create_gramm() -> "range_model":
        return range_model(name="грамм", coef=1)

    @staticmethod
    def create_kilogram() -> "range_model":
        return range_model(name="килограмм", coef=1000, base=range_model.create_gramm())

    @staticmethod
    def create_liter() -> "range_model":
        # условная плотность 1 л ≈ 1000 г
        return range_model(name="литр", coef=1000, base=range_model.create_gramm())

    @staticmethod
    def create_milliliter() -> "range_model":
        return range_model(
            name="миллилитр", coef=0.001, base=range_model.create_liter()
        )

    @staticmethod
    def create_piece() -> "range_model":
        return range_model(name="штука", coef=1)
