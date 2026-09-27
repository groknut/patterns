from Src.Core.abstract_model import abstract_model
from Src.Core.exception import arguments_exception, max_length_exception

class entity(abstract_model):
    """Общий класс для наследования доменных моделей
    Содержит определения:
        - уникальный код
        - наименование
    """

    __name: str = ""
    __max_length: int = 50

    @property
    def name(self) -> str:
        """Возвращает наименование"""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Установка наименования сущности"""
        if value == '' or value is None or not isinstance(value, str):
            raise arguments_exception(
                field="name"
            )

        if len(value.strip()) > self.__max_length:
            raise max_length_exception(
                field="name",
                max_length=50
            )
        self.__name = value.strip()

    @property
    def max_length(self) -> int:
        """Возвращает максимально допустимую длину наименвоания"""
        return self.__max_length
