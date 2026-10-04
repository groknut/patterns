from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator
import json
from Src.Models.settings_model import settings_model
from Src.Models.company_model import company_model

class settings_manager(abstract_manager):
	__default_file_name: str = "settings.json"
	__settings: settings_model = None
	__is_loaded: bool = False

	def load(self, filename:str=''):
		inner_file_name = filename if filename.strip() != '' else  self.__default_file_name
		validator.validate(inner_file_name, str)
		with open(inner_file_name, mode='r', encoding='utf-8') as f:
			self.__data = json.load(f)
			self.__is_loaded = self.convert()

	def __new__(cls):
		if not hasattr(cls, "instance"):
			cls.instance = super(settings_manager, cls).__new__(cls)
		return cls.instance

	@property
	def settings(self) -> settings_model:
		return self.__settings

	def _to_int(self, value, default: int = 0) -> int:
		try:
			return int(value)
		except (TypeError, ValueError):
			return default

	def _require(self, data: dict, key: str):
		"""Достать обязательный ключ или бросить KeyError с понятным текстом."""
		if not isinstance(data, dict):
			raise TypeError(f"Ожидался объект, получено {type(data).__name__}")
		if key not in data:
			raise KeyError(f"Обязательный ключ '{key}' отсутствует в файле настроек")
		return data[key]

	def convert(self) -> bool:
		try:
			self.__settings = settings_model()
			org_data = self._require(self.__data, "organization")
			if not isinstance(org_data, dict):
				raise TypeError("Секция 'organization' должна быть объектом")

			self.__settings.organization = company_model(
				name       = self._require(org_data, "name"),
				inn        = self._to_int(self._require(org_data, "inn")),
				bic        = self._to_int(self._require(org_data, "bic")),
				account    = self._to_int(self._require(org_data, "account")),
				ownership  = self._require(org_data, "ownership"),
			)

			self.__settings.boss_name    = self._require(self.__data, "boss_name")
			self.__settings.account_name = self._require(self.__data, "account_name")
			self.__settings.is_first     = bool(self.__data.get("is_first", False))

			return True
		except (KeyError, TypeError, ValueError, AttributeError) as e:
			import traceback
			traceback.print_exc()
			print(f"[warn] Ошибка конвертации: {e}")
			return False

	@property
	def is_loaded(self) -> bool:
		"""Флаг, данные подготовлены"""
		return self.__is_loaded
