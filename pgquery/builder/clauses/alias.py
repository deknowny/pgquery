from __future__ import annotations

import dataclasses
import typing

from pgquery.builder.clauses.identifier import Identifier
from pgquery.builder.clauses.joins import SupportsBeInSelectFrom
from pgquery.builder.tokens import PGToken

if typing.TYPE_CHECKING:
    from pgquery.builder.actor import BuildingPayload
    from pgquery.builder.clauses.column import BaseColumn
    from pgquery.builder.clauses.table import Table
    from pgquery.builder.mixins.identifier import SupportsRenderAsIdentifier


@dataclasses.dataclass
class TableAlias(SupportsBeInSelectFrom):
    alias: str
    source: typing.Type[Table]

    def __call__(self, column: BaseColumn) -> Identifier:
        return Identifier(self.alias, *column.as_id(short=True).names)

    def render_for_from_clause(self, payload: BuildingPayload) -> None:
        self.source.render_for_from_clause(payload)
        payload.buffer << PGToken.WHITESPACE
        Identifier(self.alias).render(payload)

    def __getattr__(self, item: str) -> typing.Any:
        requested_column = getattr(self.source, item)
        new_column_data = dataclasses.replace(
            requested_column.column_data, table_name=self.alias
        )
        mocked_column = dataclasses.replace(
            requested_column, column_data=new_column_data
        )
        return mocked_column
