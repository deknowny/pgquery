from __future__ import annotations

import dataclasses

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import Renderable
from pgquery.builder.impl.tokens import PGToken


def alias(value: Renderable, alias: str) -> Alias:
    return Alias(value=value, alias=alias)


@dataclasses.dataclass
class Alias(Renderable):

    value: Renderable
    alias: str

    def render(self, payload: BuildingPayload) -> None:
        self.value.render(payload)
        payload.buffer << PGToken.WHITESPACE
        payload.buffer << self.alias
