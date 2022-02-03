from __future__ import annotations

import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.where import WhereMixin
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.mixins.statement import SupportsStatement
from pgquery.builder.tokens import PGToken

if typing.TYPE_CHECKING:
    from pgquery.builder.clauses.joins import SupportsBeInSelectFrom


@dataclasses.dataclass
class _SelectNonDefault:
    values: typing.Sequence[SupportsBeExpression]


@dataclasses.dataclass
class Select(SupportsStatement, WhereMixin, _SelectNonDefault):
    sources: typing.Sequence[SupportsBeInSelectFrom] = dataclasses.field(
        default_factory=tuple
    )

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.SELECT
        payload.buffer << PGToken.WHITESPACE

        # Values
        self.values[0].render_as_expression(payload)
        for value in self.values[1:]:
            payload.buffer << PGToken.COMMA
            value.render_as_expression(payload)

        # FROM clause with joins fro every source
        if self.sources:
            payload.buffer << PGToken.WHITESPACE
            payload.buffer << PGToken.FROM
            payload.buffer << PGToken.WHITESPACE
            self.sources[0].render_for_from_clause(payload)
            for source in self.sources[1:]:
                payload.buffer << PGToken.COMMA
                source.render_for_from_clause(payload)

        # WHERE
        if self.condition is not None:
            payload.buffer << PGToken.WHITESPACE
            self.render_where(payload)


class SubquerySelect:
    pass


class NamedSubquerySelect:
    pass


class Lateral:
    pass
