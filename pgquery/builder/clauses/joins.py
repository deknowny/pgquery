from __future__ import annotations

import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.select import SupportsBeInSelectFrom
from pgquery.builder.tokens import PGToken


class JoinsMixin:
    def join(
        self: SupportsBeInSelectFrom, other: SupportsBeInSelectFrom
    ) -> InnerJoin:
        return InnerJoin(left=self, right=other)


@dataclasses.dataclass
class BaseJoin(SupportsBeInSelectFrom):
    join_name: typing.ClassVar[str]

    left: SupportsBeInSelectFrom
    right: SupportsBeInSelectFrom

    def render_for_from_clause(self, payload: BuildingPayload) -> None:
        self.left.render_for_from_clause(payload)
        payload.buffer << PGToken.WHITESPACE
        payload.buffer << self.join_name
        payload.buffer << PGToken.WHITESPACE
        self.right.render_for_from_clause(payload)


@dataclasses.dataclass
class InnerJoin(SupportsBeInSelectFrom):
    join_name: typing.ClassVar[str] = PGToken.JOIN
