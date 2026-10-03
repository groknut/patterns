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

	def convert(self) -> bool:
		try:
			self.__settings = settings_model()
			org_data = self.__data.get("organization", {}) or {}

			self.__settings.organization = company_model(
				name=org_data.get("name", ""),
				inn=self._to_int(org_data.get("inn")),
				bic=self._to_int(org_data.get("bic")),
				account=self._to_int(org_data.get("account")),
				ownership=org_data.get("ownership", ""),
			)

			self.__settings.boss_name    = self.__data.get("boss_name", "")
			self.__settings.account_name = self.__data.get("account_name", "")
			self.__settings.is_first     = self.__data.get("is_first", False)

			return True
		except (KeyError, TypeError, ValueError) as e:
			import traceback
			traceback.print_exc()
			print(f"[warn] Ошибка конвертации: {e}")
			return False

	@property
	def is_loaded(self) -> bool:
		"""Флаг, данные подготовлены"""
		return self.__is_loaded
