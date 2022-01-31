from __future__ import annotations

import dataclasses
import functools
import typing

from pgquery.builder.buffer import BaseSQLBuffer, JoinSQlBuffer

if typing.TYPE_CHECKING:
    from pgquery.builder.clause import Renderable


@dataclasses.dataclass
class BuildingPayload:
    actor: BuildingActor
    buffer: BaseSQLBuffer
    indentation_level: int = 0


@dataclasses.dataclass
class QueryBuildingResult:
    payload: BuildingPayload

    @functools.cached_property
    def sql(self) -> str:
        return self.payload.buffer.collect()


@dataclasses.dataclass
class BuildingActor:
    debug: bool = False
    colorize: bool = False  # TODO
    indent_spaces: int = 4
    sql_buffer_class: typing.Type[BaseSQLBuffer] = dataclasses.field(
        default=JoinSQlBuffer
    )

    def build(self, query: Renderable) -> QueryBuildingResult:
        buffer = self.sql_buffer_class()
        payload = BuildingPayload(actor=self, buffer=buffer)
        query.render(payload)
        payload.buffer << ";"
        return QueryBuildingResult(payload=payload)
