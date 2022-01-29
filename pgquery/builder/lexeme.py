from __future__ import annotations

import abc
import dataclasses
import typing

if typing.TYPE_CHECKING:
    from pgquery.builder.actor import BuildingPayload


@dataclasses.dataclass
class BaseLexeme(abc.ABC):
    @abc.abstractmethod
    def render(self, payload: BuildingPayload) -> None:
        pass


def double_quoted(name: str):
    return f'"{name}"'
