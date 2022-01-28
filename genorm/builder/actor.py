from __future__ import annotations

import ctypes
import dataclasses
import functools
import typing

from genorm.builder.separator import TokensSeparator

if typing.TYPE_CHECKING:
    from genorm.builder.lexeme import BaseLexeme


@dataclasses.dataclass
class BuildingPayload:
    actor: BuildingActor
    indentation_level: int = 0
    sql_buffer: ctypes.Array[ctypes.c_char] = dataclasses.field(
        default_factory=ctypes.create_string_buffer
    )

    @functools.cached_property
    def separator(self) -> TokensSeparator:
        return TokensSeparator(payload=self)


@dataclasses.dataclass
class QueryBuildingResult:
    payload: BuildingPayload

    @functools.cached_property
    def sql(self) -> str:
        return repr(self.payload.sql_buffer)


@dataclasses.dataclass
class BuildingActor:
    query: BaseLexeme
    debug: bool
    colorize: bool  # TODO
    indent_spaces: int = 4

    def build(self) -> QueryBuildingResult:
        payload = BuildingPayload(actor=self)
        self.query.render(payload)
        result = QueryBuildingResult(payload=payload)
        return result
