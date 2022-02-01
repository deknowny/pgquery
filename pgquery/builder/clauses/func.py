from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.op import BinaryOp, EqMixin
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.tokens import PGToken


class Func(SupportsBeExpression, EqMixin):
    def __init__(self, name: str, *args: SupportsBeExpression) -> None:
        self.name = name
        self.args = args

    def __eq__(self, other: SupportsBeExpression) -> BinaryOp:
        return self._eq_impl(other)

    def render_as_expression(self, payload: BuildingPayload) -> None:
        payload.buffer << self.name
        payload.buffer << PGToken.LEFT_PARENTHESIS
        if self.args:
            self.args[0].render_as_expression(payload)
            for arg in self.args[1:]:
                arg.render_as_expression(payload)
        payload.buffer << PGToken.RIGHT_PARENTHESIS
