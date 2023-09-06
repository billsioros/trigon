from typing import TypeVar

from lagom import Container as BaseContainer

from rapidapi.helpers.resolution import get_constructor_arguments

T = TypeVar("T")


class Container:
    def __init__(self) -> None:
        self.container = BaseContainer()

    def singleton(self, dependency: T):
        self.container[type(dependency)] = dependency

        return self

    def factory(self, dependecy: type[T]):
        arguments = get_constructor_arguments(dependecy)

        resolved_arguments = {}
        for arg_name, arg_type in arguments.items():
            try:
                resolved_arguments[arg_name] = self.container[arg_type]
            except KeyError as e:
                msg = f"Missing dependency for argument '{arg_name}' of type '{arg_type}'"
                raise KeyError(
                    msg,
                ) from e

        def _(container: BaseContainer):
            return dependecy(**resolved_arguments)

        self.container[type(dependecy)] = _

        return self

    def _build(self) -> BaseContainer:
        return self.container
