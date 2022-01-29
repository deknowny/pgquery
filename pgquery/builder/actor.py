from __future__ import annotations

import dataclasses
import functools
import typing

from pgquery.builder.buffer import BaseSQLBuffer, JoinSQlBuffer

if typing.TYPE_CHECKING:
    from pgquery.builder.lexeme import BaseLexeme


@dataclasses.dataclass
class BuildingPayload:
    actor: BuildingActor
    indentation_level: int = 0

    @functools.cached_property
    def buffer(self) -> BaseSQLBuffer:
        return self.actor.sql_buffer


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
    sql_buffer: BaseSQLBuffer = dataclasses.field(
        default_factory=JoinSQlBuffer
    )

    def build(
        self, query: typing.Union[BaseLexeme, typing.Type[BaseLexeme]]
    ) -> QueryBuildingResult:
        payload = BuildingPayload(actor=self)
        query.render(payload)
        result = QueryBuildingResult(payload=payload)
        return result
