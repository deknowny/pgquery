from __future__ import annotations

import abc
import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.identifier import Identifier
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.tokens import PGToken

if typing.TYPE_CHECKING:
    from pgquery.builder.clauses.select import SupportsBeInSelectFrom


SourceType = typing.TypeVar("SourceType", bound="SupportsBeInSelectFrom")


@dataclasses.dataclass
class BaseJoin:
    join_name: typing.ClassVar[str]

    left: SupportsBeInSelectFrom
    right: SupportsBeInSelectFrom
    concat: BaseJoinConcatenation

    def render_for_from_clause(self, payload: BuildingPayload) -> None:
        self.left.render_for_from_clause(payload)
        payload.buffer << PGToken.WHITESPACE
        self.concat.render_before_join_concat(payload)
        payload.buffer << self.join_name
        payload.buffer << PGToken.WHITESPACE
        self.right.render_for_from_clause(payload)
        self.concat.render_after_join_concat(payload)


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
    join_chain: typing.Optional[BaseJoin] = None

    def join_on(
        self: SourceType,
        entity: typing.Union[
            typing.Type[SupportsBeInSelectFrom], SupportsBeInSelectFrom
        ],
        condition: SupportsBeExpression,
    ) -> SourceType:
        self.join_chain = BaseJoin(
            left=self.join_chain or self,
            right=entity,
            concat=JoinConcatenationThroughOn(condition),
        )
        return self

    def join_using(
        self: SourceType,
        entity: typing.Union[
            typing.Type[SupportsBeInSelectFrom], SupportsBeInSelectFrom
        ],
        field: SupportsBeExpression,
    ) -> SourceType:
        self.join_chain = BaseJoin(
            left=self.join_chain or self,
            right=entity,
            concat=JoinConcatenationThroughUsing(field),
        )
        return self

    def natural_join(
        self: SourceType,
        entity: typing.Union[
            typing.Type[SupportsBeInSelectFrom], SupportsBeInSelectFrom
        ],
    ) -> SourceType:
        self.join_chain = BaseJoin(
            left=self.join_chain or self,
            right=entity,
            concat=JoinConcatenationThroughNatural(),
        )
        return self
