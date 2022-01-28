from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    from genorm.builder.actor import BuildingPayload


TokensGenerator = typing.Generator[str, None, None]


class BaseLexeme(abc.ABC):
    @abc.abstractmethod
    def render(self, payload: BuildingPayload) -> TokensGenerator:
        pass


def double_quoted(name: str):
    return f'"{name}"'
