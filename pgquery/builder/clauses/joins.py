from __future__ import annotations

import abc
import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.identifier import Identifier
from pgquery.builder.clauses.select import Select
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.tokens import PGToken

SupportsJoinType = typing.Union[
    typing.Type["SupportsBeInSelectFrom"], "SupportsBeInSelectFrom"
]


@dataclasses.dataclass
class _BaseJoinNonDefaultInit:
    left: SupportsBeInSelectFrom
    right: SupportsBeInSelectFrom
    concat: BaseJoinConcatenation
    join_name: str


@dataclasses.dataclass
class BaseJoinConcatenation(abc.ABC):
    def render_before_join_concat(self, payload: BuildingPayload) -> None:
        pass

    def render_after_join_concat(self, payload: BuildingPayload) -> None:
        pass


@dataclasses.dataclass
class JoinConcatenationThroughOn(BaseJoinConcatenation):
    condition: SupportsBeExpression

    def render_after_join_concat(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.ON
        payload.buffer << PGToken.WHITESPACE
        self.condition.render_as_expression(payload)


@dataclasses.dataclass
class JoinConcatenationThroughUsing(BaseJoinConcatenation):
    shared_field: Identifier

    def render_after_join_concat(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.USING
        payload.buffer << PGToken.WHITESPACE
        self.shared_field.render(payload)


@dataclasses.dataclass
class JoinConcatenationThroughNatural(BaseJoinConcatenation):
    def render_before_join_concat(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.NATURAL


@dataclasses.dataclass
class JoinsMixin:
    def join_on(
        self: SupportsBeInSelectFrom,
        entity: SupportsJoinType,
        condition: SupportsBeExpression,
    ) -> BaseJoin:
        return BaseJoin(
            left=self,
            right=entity,
            concat=JoinConcatenationThroughOn(condition),
            join_name=PGToken.JOIN,
        )

    def join_using(
        self: SupportsBeInSelectFrom,
        entity: SupportsJoinType,
        field: Identifier,
    ) -> BaseJoin:
        return BaseJoin(
            left=self,
            right=entity,
            concat=JoinConcatenationThroughUsing(field),
            join_name=PGToken.JOIN,
        )

    def natural_join(
        self: SupportsBeInSelectFrom,
        entity: SupportsJoinType,
    ) -> BaseJoin:
        return BaseJoin(
            left=self,
            right=entity,
            concat=JoinConcatenationThroughNatural(),
            join_name=PGToken.JOIN,
        )


@dataclasses.dataclass
class SupportsBeInSelectFrom(JoinsMixin, abc.ABC):
    @abc.abstractmethod
    def render_for_from_clause(self, payload: BuildingPayload) -> None:
        pass

    def select(self, *values: SupportsBeExpression) -> Select:
        return Select(values=values, sources=[self])


@dataclasses.dataclass
class BaseJoin(SupportsBeInSelectFrom, _BaseJoinNonDefaultInit):
    def render_for_from_clause(self, payload: BuildingPayload) -> None:
        self.left.render_for_from_clause(payload)
        payload.buffer << PGToken.WHITESPACE
        self.concat.render_before_join_concat(payload)
        payload.buffer << self.join_name
        payload.buffer << PGToken.WHITESPACE
        self.right.render_for_from_clause(payload)
        payload.buffer << PGToken.WHITESPACE
        self.concat.render_after_join_concat(payload)
