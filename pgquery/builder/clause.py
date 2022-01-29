from __future__ import annotations

import abc
import dataclasses
import typing

if typing.TYPE_CHECKING:
    from pgquery.builder.actor import BuildingPayload


PyType = typing.TypeVar("PyType")


@dataclasses.dataclass
class Renderable(abc.ABC):
    @abc.abstractmethod
    def render(self, payload: BuildingPayload) -> None:
        pass


class PyTypeReference(typing.Generic[PyType]):
    pass


def double_quoted(name: str):
    return f'"{name}"'
