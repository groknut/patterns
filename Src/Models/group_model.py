from Src.Core.abstract_model import abstract_model

class group_model(abstract_model):
    """Модель группы номенклатуры
    Содержит определение: наименование
    """
    def __init__(self, name: str = "") -> None:
        """Инициализирует группу"""
        super().__init__()
        self.name = name
