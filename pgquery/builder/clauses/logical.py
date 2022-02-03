import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.tokens import PGToken


class BaseLogical(SupportsBeExpression):
    operator: typing.ClassVar[str]

    def __init__(
        self,
        *operands: SupportsBeExpression,
    ) -> None:
        self.operands = operands

    def render_as_expression(self, payload: BuildingPayload) -> None:
        if self._is_and_inside_or(self.operands[0]):
            payload.buffer << PGToken.LEFT_PARENTHESIS
        self.operands[0].render_as_expression(payload)
        if self._is_and_inside_or(self.operands[0]):
            payload.buffer << PGToken.RIGHT_PARENTHESIS
        for operand in self.operands[1:]:
            payload.buffer << PGToken.WHITESPACE
            payload.buffer << self.operator
            payload.buffer << PGToken.WHITESPACE
            if self._is_and_inside_or(operand):
                payload.buffer << PGToken.LEFT_PARENTHESIS
            operand.render_as_expression(payload)
            if self._is_and_inside_or(operand):
                payload.buffer << PGToken.RIGHT_PARENTHESIS

    def _is_and_inside_or(self, operand: SupportsBeExpression) -> bool:
        return isinstance(self, Or) and isinstance(operand, And)


class And(BaseLogical):
    operator: typing.ClassVar[str] = PGToken.AND


class Or(BaseLogical):
    operator: typing.ClassVar[str] = PGToken.OR
