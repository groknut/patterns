from abc import ABC


class abstract_manager(ABC):
    """Абстрактный класс для реализации загрузки и обработки данных"""

    # полный путь к файлу
    __file_name: str = ""
    # подготовлены ли данные
    __is_loaded: bool = False
    # сами данные
    __data: list = []

    def load(self, filename: str = "") -> None:
        """Загрузить данные"""
        pass

    def convert(self) -> bool:
        """обработать внутренние данные"""
        return False

    @property
    def is_loaded(self) -> None:
        """Флаг, данные подготовлены"""
        return self.__is_loaded
