from Src.Core.entity_model import entity_model
from Src.Core.validator import validator


class report_result_model(entity_model):
    __text: str = ""
    __binary: list

    def __init__(self, text: str = "", binary: list | None = None) -> None:
        if binary is None:
            binary = []
        self.__text = text if len(binary) == 0 else ""
        self.__binary = binary if len(text.strip()) == 0 else []

    @property
    def text(self) -> str:
        return self.__text

    @property
    def binary(self) -> list:
        return self.__binary

    @text.setter
    def text(self, value: str) -> None:
        validator.validate(value, str)
        self.__text = value
        self.__binary = []

    @binary.setter
    def binary(self, value: list) -> None:
        validator.validate(value, list)
        self.__binary = value
        self.__text = ""
