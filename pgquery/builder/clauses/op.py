from __future__ import annotations

import abc
import dataclasses

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.tokens import PGToken


@dataclasses.dataclass
class BinaryOp(SupportsBeExpression):
    sign: str
    left: SupportsBeExpression
    right: SupportsBeExpression

    def render(self, payload: BuildingPayload) -> None:
        self.left.render_as_expression(payload)
        payload.buffer << self.sign
        self.right.render_as_expression(payload)

    def render_as_expression(self, payload: BuildingPayload) -> None:
        self.render(payload)


# There are some troubles with inheritance of __eq__
# It should be always defined manually in child scope
# For more convenience _eq_impl is defined with __eq__ implementation
class EqMixin(abc.ABC):
    @abc.abstractmethod
    def __eq__(
        self: SupportsBeExpression, other: SupportsBeExpression
    ) -> BinaryOp:
        pass

    def _eq_impl(
        self: SupportsBeExpression, other: SupportsBeExpression
    ) -> BinaryOp:
        return BinaryOp(left=self, right=other, sign="=")
