from Src.Core.abstract_model import abstract_model


class group_model(abstract_model):
    """Модель группы номенклатуры
    Содержит определение: наименование
    """

    def __init__(self, name: str = "") -> None:
        """Инициализирует группу"""
        super().__init__()
        self.name = name

    @staticmethod
    def create_grocery() -> "group_model":
        return group_model(name="Бакалея")

    @staticmethod
    def create_dairy() -> "group_model":
        return group_model(name="Молочные продукты")

    @staticmethod
    def create_dishes() -> "group_model":
        return group_model(name="Блюда")

    @staticmethod
    def create_packaging() -> "group_model":
        return group_model(name="Упаковка")
