import typing
from typing import Any

from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstract_model
from Src.Core.validator import argument_exception


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
            return {"__class__": type(object).__name__, "id": object.id}

        _seen.add(object.id)

        try:
            result = {"__class__": type(object).__name__}
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
        self, source: dict, target_type: type | None = None, _seen: set | None = None
    ) -> Any:

        if not isinstance(source, dict):
            return source
        if not source:
            return None

        cls = (
            self.__factory.resolve_class(source["__class__"])
            if "__class__" in source
            else target_type
        )
        if cls is None or not (isinstance(cls, type) and issubclass(cls, abstract_model)):
            return {
                k: self.deserialize(v, _seen=_seen)
                for k, v in source.items() if k != "__class__"
            }

        instance = cls.empty()
        abstract_model.__init__(instance)

        for c in cls.__mro__:
            annotations = c.__dict__.get("__annotations__", {})
            for name, val in vars(c).items():
                if name in vars(instance) or not name.startswith(f"_{c.__name__}__"):
                    continue
                ann = annotations.get(name)
                if ann is dict or isinstance(val, dict):
                    instance.__dict__[name] = {}
                elif ann is list or isinstance(val, list):
                    instance.__dict__[name] = []

        for key, value in source.items():
            if key.startswith("_") or key == "__class__" or value is None or key in self.__SKIP_FIELDS:
                continue
            expected_type = None
            prop = getattr(type(instance), key, None)
            if isinstance(prop, property) and prop.fset:
                expected_type = typing.get_type_hints(prop.fset).get("value")
            self.__assign(instance, key, self.__decode(value, _seen, expected_type))

        return instance

    def __decode(self, value: Any, _seen: set | None, expected_type: type | None = None) -> Any:
        """Рекурсивно десериализует значение (dict/list/scalar)."""
        if isinstance(value, dict):
            if "__class__" in value:
                return self.deserialize(value, _seen=_seen)
            if len(value) == 1 and "value" in value:
                return value["value"]
            if len(value) == 1 and "iso" in value:
                return value["iso"]
            if (
                expected_type
                and isinstance(expected_type, type)
                and issubclass(expected_type, abstract_model)
            ):
                return self.deserialize(value, expected_type, _seen=_seen)
            return {k: self.__decode(v, _seen) for k, v in value.items()}

        if isinstance(value, list):
            return [self.__decode(v, _seen) for v in value]
        return value

    @staticmethod
    def __assign(instance, key: str, value: Any) -> None:
        """Устанавливает значение через setter, add_<singular> или setattr."""
        prop = getattr(type(instance), key, None)

        if isinstance(prop, property) and prop.fset:
            setattr(instance, key, value)
            return

        if isinstance(value, list):
            adder = getattr(instance, f"add_{key[:-1]}", None)
            if adder:
                for item in value:
                    try:
                        adder(item)
                    except argument_exception:
                        pass
                return

        if isinstance(prop, property):
            return

        setattr(instance, key, value)
