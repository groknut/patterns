from Src.Core.abstract_manager import abstract_manager
# from Src.Core.validator import validator
# from Src.Core.validator import operation_exception
import json
from Src.Models.range_model import range_model

"""
storage manager - хранлищие хэш
хранит все ед измерения
группы клады номенклатуры
на взод сеттипг в случае первый старт, формирует базовый набор
флаг старта получается из сетиинг с json

инкапуслировать от settings_manager, наследовать от abstract_manager
без реализации -> тесты -> реализация
"""

class storage_manager(abstract_manager):
    __ranges: dict[str, range_mode]={}

    def __new__(cls):
		if not hasattr(cls, "instance"):
			cls.instance = super(settings_manager, cls).__new__(cls)
		return cls.instance

	def convert(self, is_first_work):
	    pass

	"""
	мука масло номенклатуры
	склад
	мг/г/кг
	"""

"""
- реализация storage_manager
- нарисовать UML-диаграммы (storage_manager и settings_manager)
- написать тесты для обоих менеджеров


ед.изм - граммы - базовая единица для кг
номенклатура: мука (кг)
"""
