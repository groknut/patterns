from Src.Core.entity_model import entity
from Src.Core.exception import (
    arguments_exception,
    max_len_exception,
    len_exception,
    validation_exception,
)

class organization_model(entity):
    """Модель организации
    Содержит:
        - наименование
        - ИНН
        - БИК
        - счёт
        - форму собственности
    """

    __inn: str = ""
    __bic: str = ""
    __account: str = ""
    __owner: str = ""
    __len_inn: int = 10
    __len_bic: int = 9
    __len_account: int = 20
    __max_len_owner: int = 50

    def __init__(
        self,
        name: str = "",
        inn: str = "",
        bic: str = "",
        account: str = "",
        owner: str = ""
    ) -> None:
        """Инициализирует организацию"""
        super().__init__()
        self.name = name
        self.inn = inn
        self.bic = bic
        self.account = account
        self.owner = owner

    def __check_inn(self, value: str) -> bool:
        """Проверяет контрольную сумму ИНН"""
        total = (2 * int(value[0]) + 4 * int(value[1]) + 10 * int(value[2]) +
                 3 * int(value[3]) + 5 * int(value[4]) + 9 * int(value[5]) +
                 4 * int(value[6]) + 6 * int(value[7]) + 8 * int(value[8]))
        result = total % 11
        if result > 9:
            result %= 10
        return result == int(value[-1])

    def __check_account(self, value: str) -> bool:
        """Проверяет контрольную сумму расчётного счёта"""
        last = self.bic[-3:]
        new_value = last + value
        cnt = 1
        total = 0
        for i in range(23):
            match cnt:
                case 1:
                    total += 7 * int(new_value[i])
                    cnt += 1
                case 2:
                    total += 1 * int(new_value[i])
                    cnt += 1
                case 3:
                    total += 3 * int(new_value[i])
                    cnt = 1
        return total % 10 == 0

    @property
    def inn(self)->str:
        """Возвращает ИНН организации"""
        return self.__inn

    @inn.setter
    def inn(self, value: str) -> None:
        """Устанавливает ИНН организации"""
        if value is None or not isinstance(value, str):
            raise arguments_exception(
                field="inn",
                message="Некорректно переданный аргумент!"
            )
        if len(value.strip()) != self.__len_inn:
            raise len_exception(
                field="inn",
                length=self.__len_inn,
                message="Неверная длина ИНН"
            )
        if value.isdigit() == False:
            raise validation_exception(
                field="inn",
                message="ИНН должен состоять только из цифр!"
            )
        if self.__check_inn(value) == False:
            raise validation_exception(
                field="inn",
                message="Некорректный ИНН!"
            )
        self.__inn = value

    @property
    def bic(self)->str:
        """Возвращает БИК банка"""
        return self.__bic

    @bic.setter
    def bic(self, value: str) -> None:
        """Устанавливает БИК банка"""
        if value is None or not isinstance(value, str):
            raise arguments_exception(
                field="bic",
                message="Некорректно переданный аргумент!"
            )
        if len(value.strip()) != self.__len_bic:
            raise len_exception(
                field="bic",
                length=self.__len_bic,
                message="Неверная длина БИК"
            )
        if value.isdigit() == False:
            raise validation_exception(
                field="bic",
                message="БИК должен состоять только из цифр!"
            )
        self.__bic = value

    @property
    def account(self)->str:
        """Возвращает расчётный счёт"""
        return self.__account

    @account.setter
    def account(self, value: str) -> None:
        """Устанавливает расчётный счёт"""
        if value is None or not isinstance(value, str):
            raise arguments_exception(
                field="account",
                message="Некорректно переданный аргумент!"
            )
        if len(value.strip()) != self.__len_account:
            raise len_exception(
                field="account",
                length=self.__len_account,
                message="Неверная длина счёта"
            )
        if value.isdigit() == False:
            raise validation_exception(
                field="account",
                message="Счет должен состоять только из цифр!"
            )
        if self.__check_account(value) == False:
            raise validation_exception(
                field="account",
                message="Некорректный Счет!"
            )
        self.__account = value

    @property
    def owner(self)->str:
        """Возвращает форму собственности / владельца"""
        return self.__owner

    @owner.setter
    def owner(self, value: str) -> None:
        """Устанавливает форму собственности / владельца"""
        if value is None or not isinstance(value, str):
            raise arguments_exception(
                field="owner",
                message="Некорректно переданный аргумент!"
            )
        if len(value.strip()) > self.__max_len_owner:
            raise max_len_exception(
                field="owner",
                max_length=self.__max_len_owner,
                message="Превышена максимальная длина"
            )
        self.__owner = value
