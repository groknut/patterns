import json

from Src.Core.abstract_manager import abstract_manager
from Src.Core.validator import validator
from Src.Dtos.report_type_dto import report_type_enum
from Src.Logics.convert_factory import convert_factory
from Src.Models.company_model import company_model
from Src.Models.settings_model import settings_model


class settings_manager(abstract_manager):
    __default_file_name: str = "settings.json"
    __settings: settings_model = None
    __is_loaded: bool = False

    def load(self, filename: str = ""):
        inner_file_name = (
            filename if filename.strip() != "" else self.__default_file_name
        )
        validator.validate(inner_file_name, str)
        try:
            with open(inner_file_name, mode="r", encoding="utf-8") as f:
                self.__data = json.load(f)
                self.__is_loaded = self.convert()

                if not self.__is_loaded:
                    self.__settings = self.__create_default_data()
        except FileNotFoundError:
            print("[error] File not found")
        except:
            print("[error] Wrong data in file")

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
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
        """Десериализует settings.json через общий convert_factory."""
        try:

            data = self._normalize(self.__data)
            self.__settings = convert_factory().deserialize(data, settings_model)
            return self.__settings is not None
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[warn] Ошибка конвертации: {e}")
            return False

    @staticmethod
    def _normalize(data: dict) -> dict:
        """Строковые числа в organization → int (settings.json хранит их строками)."""
        import copy
        result = copy.deepcopy(data)
        org = result.get("organization")
        if isinstance(org, dict):
            for key in ("inn", "bic", "account", "corr_account"):
                if key in org and isinstance(org[key], str):
                    try:
                        org[key] = int(org[key])
                    except ValueError:
                        org[key] = 0
        return result

    @property
    def is_loaded(self) -> bool:
        """Флаг, данные подготовлены"""
        return self.__is_loaded

    def __create_default_data(self) -> settings_model:
        result = settings_model()

        company = company_model(
            name="ООО Ромашка",
            inn=7736050003,
            bic=44525225,
            account=40812810400000000225,
            ownership="ООО",
        )

        result.organization = company
        result.boss_name = "Воловиков Александр Сергеевич"
        result.account_name = "Балахчи Анна Георгиевна"
        result.is_first = True
        return result
