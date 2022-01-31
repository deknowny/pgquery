from __future__ import annotations

import abc
import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import Renderable


def select(*values) -> SelectClause:
    return SelectClause(values=values)


@dataclasses.dataclass
class AllowedBeInFromClauseMixin(abc.ABC):
    @abc.abstractmethod
    def render_for_from_clause(self, payload: BuildingPayload) -> None:
        pass
    #
    # def select(self, *values: AllowedBeSelectedMixin) -> SelectClause:
    #     return SelectClause(sources=[self], values=values)


@dataclasses.dataclass
class AllowedBeSelectedMixin(abc.ABC):
    @abc.abstractmethod
    def render_for_selecting(self, payload: BuildingPayload) -> None:
        pass


@dataclasses.dataclass
class SelectClause:
    values: typing.Collection[AllowedBeSelectedMixin]
    sources: typing.Collection[AllowedBeInFromClauseMixin] = dataclasses.field(default_factory=list)


class SubquerySelect:
    pass


class NamedSubquerySelect:
    pass


class Lateral:
    pass
