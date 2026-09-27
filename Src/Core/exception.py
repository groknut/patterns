
class base_exception(Exception):

    def __init__(
        self,
        field: str = "",
        message: str = "",
        stack_trace: str = ""
    ) -> None:
        """Инициализирует исключение
        """
        self.__field = field.strip()
        self.__message = message.strip()
        self.__stack_trace = stack_trace.strip()

    @property
    def field(self) -> str:
        """Возвращает имя поле, где ошибка"""
        return self.__field

    @property
    def message(self) -> str:
        """Возвращает текст сообщения об ошибке."""
        return self.__message

    @property
    def stack_trace(self) -> str:
        """Возвращает трассировку стека (при наличии)."""
        return self.__stack_trace

    def __str__(self) -> str:
        """Возвращает строковое представление исключения."""
        return f"""Wrong argument
field: {self.__field}
message: {self.__message}
stack_trace: {self.__stack_trace}
        """

class arguments_exception(base_exception):
    """Исключение о некорректно переданном аргументе."""
    def __init__(
        self,
        field: str,
        message: str = "",
        stack_trace: str = ""
    ) -> None:
        """Инициализирует исключение."""
        message = f"Wrong argument: {field}"
        super().__init__(field, message, stack_trace)

class max_length_exception(base_exception):
    """Исключение о превышении максимальной длины поля."""

    def __init__(
        self,
        field: str,
        max_length: int,
        stack_trace: str = ""
    ) -> None:
        """Инициализирует исключение."""
        message = f"Max length ({max_length})"
        super().__init__(field, message, stack_trace)
