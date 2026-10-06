from Src.Core.abstract_manager import abstract_manager
import json
from Src.Models.range_model import range_model

from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator, argument_exception
from Src.Logics.settings_manager import settings_manager
from Src.Models.range_model import range_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Models.storage_model import storage_model

class storage_manager(abstract_manager):
	"""
	Менеджер хранения доменных моделей
	При первом старте формируются первичные значения.
	"""

	__ranges: dict[str, range_model] = None
	__storages: dict = None
	__nomenclatures: dict = None
	__groups: dict = None
	__is_initialized: bool = False


	def __new__(cls):
		if not hasattr(cls, "instance"):
			obj = super(storage_manager, cls).__new__(cls)
			obj.__ranges = {}
			obj.__storages = {}
			obj.__nomenclatures = {}
			obj.__groups = {}
			obj.__is_initialized = False
			cls.instance = obj
		return cls.instance

	def convert(self, is_first: bool) -> bool:
		"""Если запуск первый - генерирует первичные данные"""

		if self.__is_initialized:
			return True
		try:
			if is_first:
				self.__initialize_primary_data()
			self.__is_initialized = True
			return True
		except:
			return False

	def __initialize_primary_data(self) -> None:
		"""Инициализация первичных данных"""
		self.__create_ranges()
		self.__create_groups()
		self.__create_nomenclatures()
		self.__create_storages()
		self.__is_initialized = True

	def __create_nomenclatures(self) -> None:
		"""Генерация номенклатуры (ингредиенты для рецепта и готовые блюда"""

		groups_by_name = {g.name: g for g in self.__groups.values()}
		ranges_by_name = {r.name: r for r in self.__ranges.values()}

		grocery = groups_by_name.get("Бакалея")
		dairy = groups_by_name.get("Молочные продукты")
		dishes = groups_by_name.get("Блюда")

		kg = ranges_by_name.get("килограмм")
		liter = ranges_by_name.get("литр")
		piece = ranges_by_name.get("штука")

		items = [
			nomenclature_model("Мука ржаная", "Мука ржаная обдирная", grocery, kg),
			nomenclature_model("Кефир 1%", "Кефир коровий пастеризованный 1%", dairy, liter),
			nomenclature_model("Яйца перепелиные", "Яйца перепелиные столовые", dairy, piece),
			nomenclature_model("Масло топлёное", "Масло топлёное ГОСТ 72.5%", dairy, kg),
			nomenclature_model("Сахарная пудра", "Сахарная пудра М50", grocery, kg),
			nomenclature_model("Сода пищевая", "Сода пищевая двууглекислая", grocery, kg),
			nomenclature_model("Оладьи пышные", "Оладьи пышные на кефире", dishes, piece),
		]

		for item in items:
			self.add_object(
				nomenclature_model,
				self.__nomenclatures,
				item
			)

	def __create_groups(self) -> None:
		"""Генерация групп"""
		grocery = group_model(name="Бакалея")
		dairy = group_model(name="Молочные продукты")
		dishes = group_model(name="Блюда")

		for item in [grocery, dairy, dishes]:
			self.add_object(
				group_model,
				self.__groups,
				item
			)

	def __create_ranges(self) -> None:
		"""Генерация базовых и производных ед. изм."""
		specs = [
			("грамм",     1,     None),
			("килограмм", 1000,  "грамм"),
			("штука",     1,     None),
			("литр",      1,     None),
			("миллилитр", 0.001, "литр"),
		]
		for name, factor, base in specs:
			base_obj = next((r for r in self.__ranges.values() if r.name == base), None, ) if base else None
			self.add_object(
				range_model,
				self.__ranges,
				range_model(name=name, conversion_factor=factor, base_range=base_obj)
			)

	def add_object(self, type_, group, item) -> bool:
		"""Добавить объект в группу"""
		try:
			validator.validate(item, type_)
			if item.id in group:
				return False
			group[item.id] = item
			return True
		except argument_exception:
			return False

	def __create_storages(self) -> None:
		"""Генерация складов."""
		self.add_object(
			storage_model,
			self.__storages,
			storage_model(name="Основной склад",   address="ул. Складская, 9, пом. 90")
		)
		self.add_object(
			storage_model,
			self.__storages,
			storage_model(name="Холодильник цеха", address="ул. Складская, 9, пом. 107")
		)

	@property
	def ranges(self) -> dict:
		"""Словарь единиц измерения {id: range_model}."""
		return self.__ranges

	@property
	def storages(self) -> dict:
		"""Словарь складов"""
		return self.__storages

	@property
	def groups(self) -> dict:
		"""Словарь групп номенклатуры"""
		return self.__groups

	@property
	def nomenclatures(self) -> dict:
		"""Словарь номенклатур"""
		return self.__nomenclatures

	@property
	def data(self) -> dict:
		"""Все данные хранилиша по категориям"""
		return {
			"storages": self.__storages,
			"ranges": self.__ranges,
			"nomenclatures": self.__nomenclatures,
			"groups": self.__groups
		}

	@property
	def is_initialized(self) -> bool:
		"""Флаг завершения инициализации."""
		return self.__is_initialized
