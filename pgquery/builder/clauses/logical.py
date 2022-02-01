import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.tokens import PGToken


@dataclasses.dataclass
class BaseLogical(SupportsBeExpression):
    operator: typing.ClassVar[str]

    left: SupportsBeExpression
    right: SupportsBeExpression

    def render_as_expression(self, payload: BuildingPayload) -> None:
        self.left.render_as_expression(payload)
        payload.buffer << PGToken.WHITESPACE
        payload.buffer << self.operator
        payload.buffer << PGToken.WHITESPACE
        self.right.render_as_expression(payload)


@dataclasses.dataclass
class And(BaseLogical):
    operator: typing.ClassVar[str] = PGToken.AND


@dataclasses.dataclass
class Or(BaseLogical):
    operator: typing.ClassVar[str] = PGToken.OR
