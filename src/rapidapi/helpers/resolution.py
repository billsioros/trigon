import inspect
import itertools
import pkgutil
from collections.abc import Iterable
from types import ModuleType
from typing import Any, TypeVar

T = TypeVar("T", bound=type)


def get_modules(parent_module: ModuleType, public_only: bool = True) -> Iterable[ModuleType]:
    modules: list[ModuleType] = []

    for loader, module_name, _ in pkgutil.walk_packages(parent_module.__path__):
        if module_name.startswith("_") and public_only:
            continue

        module = loader.find_module(module_name).load_module(module_name)

        modules.append(module)

    return sorted(modules, key=lambda module: module.__name__)


def get_types(parent_module: ModuleType, Type_: type[T]) -> list[type[T]]:
    def is_subclass_defined_in_module(Type___: type[T], module: ModuleType) -> bool:
        return (
            inspect.getmodule(Type___) is module
            and inspect.isclass(Type___)
            and issubclass(Type___, Type_)
            and not issubclass(Type_, Type___)
        )

    _types: list[type[T]] = []

    for module in get_modules(parent_module):
        for name, Type__ in inspect.getmembers(
            module,
            lambda Type___: is_subclass_defined_in_module(Type___, module),
        ):
            if name in _types:
                msg = f"class `{name}` is defined multiple times."
                raise KeyError(msg)

            _types.append(Type__)

    return _types


def get_constructor_arguments(Type_: T) -> dict[str, Any]:
    return {
        parameter.name: parameter.annotation
        for parameter in itertools.islice(
            inspect.signature(Type_.__init__).parameters.values(),
            1,
            None,
        )
    }
