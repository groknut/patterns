from Src.Core.validator import validator


class balance_dto:
    """DTO строки оборотно-сальдовой ведомости.
        - id:              код номенклатуры
        - name:            наименование
        - unit:            единица измерения (наименование)
        - opening_balance: входящий остаток
        - income:          приход
        - expense:         расход
        - closing_balance: исходящий остаток
    """

    __id: str = ""
    __name: str = ""
    __unit: str = ""
    __opening_balance: float = 0.0
    __income: float = 0.0
    __expense: float = 0.0
    __closing_balance: float = 0.0

    def __init__(
        self,
        id: str = "",
        name: str = "",
        unit: str = "",
        opening_balance: float = 0.0,
        income: float = 0.0,
        expense: float = 0.0,
        closing_balance: float = 0.0,
    ) -> None:
        self.id = id
        self.name = name
        self.unit = unit
        self.opening_balance = opening_balance
        self.income = income
        self.expense = expense
        self.closing_balance = closing_balance

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str) -> None:
        validator.validate(value, str, 255)
        self.__id = value.strip()

    @property
    def name(self) -> str:
        """наименование"""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        validator.validate(value, str, 255)
        self.__name = value.strip()

    @property
    def unit(self) -> str:
        """единица измерения"""
        return self.__unit

    @unit.setter
    def unit(self, value: str) -> None:
        validator.validate(value, str, 50)
        self.__unit = value.strip()

    @property
    def opening_balance(self) -> float:
        """входящий остаток"""
        return self.__opening_balance

    @opening_balance.setter
    def opening_balance(self, value) -> None:
        validator.validate(value, (int, float))
        self.__opening_balance = float(value)

    @property
    def income(self) -> float:
        return self.__income

    @income.setter
    def income(self, value) -> None:
        validator.validate(value, (int, float))
        self.__income = float(value)

    @property
    def expense(self) -> float:
        return self.__expense

    @expense.setter
    def expense(self, value) -> None:
        validator.validate(value, (int, float))
        self.__expense = float(value)

    @property
    def closing_balance(self) -> float:
        """исходящий остаток"""
        return self.__closing_balance

    @closing_balance.setter
    def closing_balance(self, value) -> None:
        validator.validate(value, (int, float))
        self.__closing_balance = float(value)

    def to_dict(self) -> dict:
        """Сериализация для JSON-ответа."""
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "opening_balance": self.opening_balance,
            "income": self.income,
            "expense": self.expense,
            "closing_balance": self.closing_balance,
        }
