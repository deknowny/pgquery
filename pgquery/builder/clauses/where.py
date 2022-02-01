import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.tokens import PGToken

UsedWhereType = typing.TypeVar("UsedWhereType")


@dataclasses.dataclass
class WhereMixin:
    condition: typing.Optional[SupportsBeExpression] = None

    def render_where(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.WHERE
        payload.buffer << PGToken.WHITESPACE
        self.condition.render_as_expression(payload)

    def where(
        self: UsedWhereType, condition: SupportsBeExpression
    ) -> UsedWhereType:
        self.condition = condition
        return self
