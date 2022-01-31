import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import Renderable
from pgquery.builder.impl.tokens import PGToken

SelectType = typing.TypeVar("SelectType")


@dataclasses.dataclass
class WhereClause(Renderable):

    condition: Renderable

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.WHERE
        payload.buffer << PGToken.WHITESPACE
        self.condition.render(payload)


@dataclasses.dataclass
class WhereMixin:

    where_clause: typing.Optional[WhereClause] = None

    def where(self: SelectType, condition: Renderable) -> SelectType:
        self.where_clause = WhereClause(condition=condition)
        return self
