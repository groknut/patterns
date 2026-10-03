
from Src.Core.entity_model import entity
from Src.Core.exception import arguments_exception, max_len_exception

class warehouse_model(entity):
    """Модель склада

    Содержит определения:
        - наименование
        - адрес
        - максимальная длина адреса
    """
    __address: str = ""
    __max_len: int = 255

    def __init__(
        self,
        name: str = "",
        address: str = ""
    ) -> None:
        """Инициализирует склад
        """
        super().__init__()
        self.__name = name
        self.__address = address

    @property
    def address(self)->str:
        """Возвращает адрес"""
        return self.__address

    @address.setter
    def address(
        self,
        value: str
    ) -> None:
        """Устанавливает адрес склада
        """
        if value is None or not isinstance(value, str) or value == '':
            raise arguments_exception(
                field="address",
                message="Wrong  argument"
            )
        if len(value.strip()) > self.__max_len:
            raise max_len_exception(
                field="name",
                max_length=self.__max_len
            )
        self.__address = value.strip()
