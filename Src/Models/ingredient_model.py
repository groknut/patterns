from Src.Core.entity_model import entity_model
from Src.Core.validator import validator, argument_exception
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model


class ingredient_model(entity_model):
    """Строка состава технологической карты.

    Веса Брутто/Нетто не хранятся, а вычисляются: изменение количества,
    потерь или единицы сразу отражается в расчёте.
    """

    __nomenclature: nomenclature_model = None
    __range: range_model = None
    __quantity: float = 0.0
    __loss_ratio: float = 0.0
    __grams_per_unit: float = None

    def __init__(
        self,
        nomenclature: nomenclature_model = None,
        range_: range_model = None,
        quantity: float = 0.0,
        loss_ratio: float = 0.0,
        grams_per_unit: float = None,
    ) -> None:
        super().__init__()
        if nomenclature is not None:
            self.nomenclature = nomenclature
            self.name = nomenclature.name
        if range_ is not None:
            self.range = range_
        self.quantity = quantity
        self.loss_ratio = loss_ratio
        if grams_per_unit is not None:
            validator.validate(grams_per_unit, (int, float))
            if grams_per_unit <= 0:
                raise argument_exception("grams_per_unit должен быть больше нуля")
            self.__grams_per_unit = float(grams_per_unit)

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value) -> None:
        validator.validate(value, (int, float))
        if value <= 0:
            raise argument_exception("Количество должно быть больше нуля")
        self.__quantity = float(value)

    @property
    def loss_ratio(self) -> float:
        return self.__loss_ratio

    @loss_ratio.setter
    def loss_ratio(self, value) -> None:
        validator.validate(value, (int, float))
        if not (0 <= value < 1):
            raise argument_exception("Доля потерь должна быть в [0, 1)")
        self.__loss_ratio = float(value)

    @property
    def grams_per_unit(self) -> float:
        if self.__grams_per_unit is not None:
            return self.__grams_per_unit
        if self.__range is None:
            return 1.0
        return self.__range.grams_per_unit

    @property
    def gross_weight(self) -> float:
        """Брутто в граммах — до потерь."""
        return self.__quantity * self.grams_per_unit

    @property
    def net_weight(self) -> float:
        """Нетто в граммах — после потерь."""
        return self.gross_weight * (1 - self.__loss_ratio)
