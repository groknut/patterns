from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstract_model

class reference_convertor(abstract_convertor):
    """Глубокий конвертор доменной модели, списков и словарей."""

    @property
    def types(self) -> tuple[type, ...]:
        return (abstract_model,)

    def __init__(self, factory) -> None:
        self.__factory = factory

    def convert(self, object: Any, _seen: set = None) -> Any:
        """Запускает конвертацию."""
        if _seen is None:
            _seen = set()

        if object.id in _seen:
            return {"id": object.id}

        _seen.add(object.id)

        try:
            result = {}
            for name, value in self.__iter_properties(object):

                if value is None:
                    result[name] = None
                    continue

                converted = self.__factory.convert(value, _seen)

                if isinstance(converted, dict) and len(converted) == 1:
                    key = next(iter(converted))
                    if key in ("value", "iso"):
                        result[name] = converted[key]
                        continue

                result[name] = converted
            return result
        finally:
            _seen.discard(object.id)

    def __iter_properties(self, obj):
        """Обходит @property и instance-атрибуты."""
        seen = set()
        for cls in type(obj).__mro__:
            for name, attr in vars(cls).items():
                if name in seen:
                    continue
                if isinstance(attr, property):
                    seen.add(name)
                    yield name, getattr(obj, name)
        for name, value in vars(obj).items():
            if name.startswith("_") or name in seen:
                continue
            seen.add(name)
            yield name, value
