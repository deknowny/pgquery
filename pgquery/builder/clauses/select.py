from __future__ import annotations

import abc
import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.joins import JoinsMixin
from pgquery.builder.clauses.where import WhereMixin
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.mixins.statement import SupportsStatement
from pgquery.builder.tokens import PGToken


@dataclasses.dataclass
class SupportsBeInSelectFrom(JoinsMixin, abc.ABC):
    @abc.abstractmethod
    def render_for_from_clause(self, payload: BuildingPayload) -> None:
        pass

    def render_for_from_clause_with_joins(
        self, payload: BuildingPayload
    ) -> None:
        if self.join_chain is None:
            self.render_for_from_clause(payload)
        else:
            self.join_chain.render_for_from_clause(payload)

    def select(self, *values: SupportsBeExpression) -> Select:
        return Select(values=values, sources=[self])


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
            self.sources[0].render_for_from_clause_with_joins(payload)
            for source in self.sources[1:]:
                payload.buffer << PGToken.COMMA
                source.render_for_from_clause_with_joins(payload)

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
