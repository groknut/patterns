from Src.Core.abstract_manager import abstract_manager
# from Src.Core.validator import validator
# from Src.Core.validator import operation_exception
import json
from Src.Models.settings_model import settings_model
from Src.Models.company_model import company_model

class settings_manager(abstract_manager):
	__default_file_name: str = "settings.json"
	__settings: settings_model = None

	def load(self, filename:str=''):
		inner_file_name = filename if filename.strip() != '' else  self.__default_file_name
		# validator.validate(inner_file_name)
		try:
			with open(inner_file_name, mode='r', encoding='utf-8') as f:
				self.__data = json.load(f)
				self.__is_loaded = self.convert()
		except Exception as e:
			raise ValueError()

	def __new__(cls):
		if not hasattr(cls, "instance"):
			cls.instance = super(settings_manager, cls).__new__(cls)
		return cls.instance

	@property
	def settings(self) -> settings_model:
		return self.__settings

	def convert(self) -> bool:
		try:
			self.__settings = settings_model()
			org_data = self.__data.get("organization", {}) or {}
			self.__settings.organization = company_model(
				name=org_data.get("name", ""),
				inn=org_data.get("inn", ""),
				bic=org_data.get("bic", ""),
				account=org_data.get("account", ""),
				owner=org_data.get("owner", "")
			)

			self.__settings.boss_name = self.__data.get("boss_name", "")
			self.__settings.account_name = self.__data.get("account_name", "")
			self.__settings.is_first_work = self.__data.get("is_first_work", False)

			return True
		except (KeyError, TypeError, ValueError) as e:
			# print(f"[warn] Ошибка конвертации: {e}")
			return False

	@property
	def is_loaded(self) -> None:
		"""Флаг, данные подготовлены"""
		return self.__is_loaded
