from __future__ import annotations

import abc
import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import Renderable
from pgquery.builder.impl.tokens import PGToken


AliasType = typing.TypeVar("AliasType")


@dataclasses.dataclass
class SupportsAliasMixin(abc.ABC):
    @abc.abstractmethod
    def render_for_alias(self, payload: BuildingPayload) -> None:
        pass

    def alias(self, new_name: str, add_as: bool = False) -> Alias:
        return Alias(value=self, new_name=new_name, add_as=add_as)


@dataclasses.dataclass
class Alias(Renderable):

    value: SupportsAliasMixin
    new_name: str
    add_as: bool = False

    def render(self, payload: BuildingPayload) -> None:
        pass
        # self.value.render_for_alias(payload)
        # payload.buffer << PGToken.WHITESPACE
        # payload.buffer << self.alias
