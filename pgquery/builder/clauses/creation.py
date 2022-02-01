from __future__ import annotations

import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.mixins.statement import SupportsStatement
from pgquery.builder.tokens import PGToken

if typing.TYPE_CHECKING:
    from pgquery.builder.mixins.creation import SupportsCreation


@dataclasses.dataclass
class Create(SupportsStatement):
    creatable: SupportsCreation

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.CREATE
        payload.buffer << PGToken.WHITESPACE
        self.creatable.render_for_creation(payload)
