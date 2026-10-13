from Src.Core.entity_model import entity_model
from Src.Core.validator import validator


"""
Модель склада
"""


class storage_model(entity_model):
	__address: str = ""

	"""
	Адрес
	"""

	def __init__(self, name: str = "", address: str = "") -> None:
		super().__init__()
		self.address = address
		if name.strip() != "":
			self.name = name

	@property
	def address(self) -> str:
		return self.__address.strip()

	@address.setter
	def address(self, value: str):
		if value == "":
		    self.__address = ""
		else:
		    validator.validate(value, str, 255)
		    self.__address = value.strip()

	@staticmethod
	def create_main() -> "storage_model":
		return storage_model(name="Основной склад", address="ул. Складская, 9, пом. 90")

	@staticmethod
	def create_fridge() -> "storage_model":
		return storage_model(name="Холодильник цеха", address="ул. Складская, 9, пом. 107")
