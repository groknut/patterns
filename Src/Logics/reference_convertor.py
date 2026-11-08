from typing import Any
import typing
import inspect

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstract_model


class reference_convertor(abstract_convertor):
    """Глубокий конвертор доменной модели, списков и словарей."""

    __SKIP_FIELDS = {"sub_recipe", "gross_weight", "net_weight"}

    @property
    def types(self) -> tuple[type, ...]:
        return (abstract_model,)

    def __init__(self, factory: abstract_convertor) -> None:
        self.__factory = factory

    def convert(self, object: Any, _seen: set | None = None) -> Any:
        """Запускает конвертацию."""
        if _seen is None:
            _seen = set()

        if object.id in _seen:
            return {"id": object.id}

        _seen.add(object.id)

        try:
            result = {}
            for name, value in self.__iter_properties(object):
                if name in self.__SKIP_FIELDS:
                    continue
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


    def deserialize(
        self, source: dict, target_type: type[abstract_model], _seen: set | None = None
    ) -> abstract_model | None:

        if not source:
            return None

        instance = target_type.empty()
        abstract_model.__init__(instance)

        for cls in target_type.__mro__:
            annotations = cls.__dict__.get("__annotations__", {})
            for name, val in vars(cls).items():
                if name in vars(instance) or name in self.__SKIP_FIELDS:
                    continue
                if not name.startswith(f"_{cls.__name__}__"):
                    continue
                ann = annotations.get(name)
                if ann is dict or isinstance(val, dict):
                    instance.__dict__[name] = {}
                elif ann is list or isinstance(val, list):
                    instance.__dict__[name] = []

        class_hints = typing.get_type_hints(target_type)

        for key, value in source.items():
            if key.startswith("_") or value is None:
                continue

            if key in self.__SKIP_FIELDS:
                continue

            prop = getattr(type(instance), key, None)

            if isinstance(prop, property) and prop.fset:
                hints = typing.get_type_hints(prop.fset)
                expected_type = hints.get("value")
                if not expected_type:
                    if isinstance(value, list):
                        value = [
                            item["value"]
                            if isinstance(item, dict) and "value" in item
                            else item
                            for item in value
                        ]
                    setattr(instance, key, value)
                    continue
                converted = self.__factory.deserialize(value, expected_type, _seen)
                setattr(instance, key, converted)
            else:
                if isinstance(prop, property) and not prop.fset:
                    # Getter-only + список → через add_<singular>()
                    if isinstance(value, list):
                        adder_name = f"add_{key[:-1]}"   # ingredients → add_ingredient
                        adder = getattr(instance, adder_name, None)
                        if adder is not None:
                            sig = inspect.signature(adder)
                            params = list(sig.parameters.values())
                            item_type = params[0].annotation if params else None
                            if item_type is inspect.Parameter.empty:
                                item_type = None
                            for item in value:
                                converted = (
                                    self.__factory.deserialize(item, item_type, _seen)
                                    if item_type else item
                                )
                                adder(converted)
                    continue

                expected_type = class_hints.get(key)
                if expected_type is None:
                    setattr(instance, key, value)
                else:
                    converted = self.__factory.deserialize(value, expected_type, _seen)
                    setattr(instance, key, converted)

        return instance
