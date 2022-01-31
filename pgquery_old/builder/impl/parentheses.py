import dataclasses

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import Renderable
from pgquery.builder.impl.tokens import PGToken


@dataclasses.dataclass
class Parentheses(Renderable):
    value: Renderable

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.LEFT_PARENTHESIS
        self.value.render(payload)
        payload.buffer << PGToken.RIGHT_PARENTHESIS
