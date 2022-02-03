from __future__ import annotations

import dataclasses
import re
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.alias import TableAlias
from pgquery.builder.clauses.column import BaseColumn, ColumnData
from pgquery.builder.clauses.creation import Create
from pgquery.builder.clauses.identifier import Identifier
from pgquery.builder.clauses.joins import (
    BaseJoin,
    JoinsMixin,
    SupportsBeInSelectFrom,
    SupportsJoinType,
)
from pgquery.builder.clauses.select import Select
from pgquery.builder.mixins.creation import SupportsCreation
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.mixins.identifier import SupportsRenderAsIdentifier
from pgquery.builder.tokens import PGToken

# Pattern for converting CamelCase to snake_case
_camel2snake_convert_pattern = pattern = re.compile(r"(?<!^)(?=[A-Z])")


@dataclasses.dataclass
class TablePreferences:
    name: str
    if_not_exist: bool


class Table(
    SupportsCreation, SupportsRenderAsIdentifier, SupportsBeInSelectFrom
):

    __table_preferences__: TablePreferences
    __table_columns__: typing.Tuple[ColumnData, ...]

    def __init_subclass__(
        cls,
        title: typing.Optional[str] = None,
        if_not_exist: bool = True,
        **kwargs
    ):
        cls.__table_preferences__ = TablePreferences(
            name=cls._build_table_name(title),
            if_not_exist=if_not_exist,
        )
        cls.__table_columns__ = tuple(cls._parse_columns())
        return super().__init_subclass__(**kwargs)

    def __class_getitem__(cls, alias_name: str) -> TableAlias:
        return TableAlias(alias=alias_name, source=cls)

    @classmethod
    def join_on(
        cls: SupportsBeInSelectFrom,
        entity: SupportsJoinType,
        condition: SupportsBeExpression,
    ) -> BaseJoin:
        return JoinsMixin.join_on(cls, entity, condition)

    @classmethod
    def join_using(
        cls: SupportsBeInSelectFrom,
        entity: SupportsJoinType,
        condition: Identifier,
    ) -> BaseJoin:
        return JoinsMixin.join_using(cls, entity, condition)

    @classmethod
    def natural_join(
        cls: SupportsBeInSelectFrom,
        entity: SupportsJoinType,
    ) -> BaseJoin:
        return JoinsMixin.natural_join(cls, entity)

    @classmethod
    def as_id(cls) -> Identifier:
        return Identifier(cls.__table_preferences__.name)

    @classmethod
    def select(cls, *values: SupportsBeExpression) -> Select:
        return SupportsBeInSelectFrom.select(
            typing.cast(SupportsBeInSelectFrom, cls), *values
        )

    @classmethod
    def render_for_creation(cls, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.TABLE
        if cls.__table_preferences__.if_not_exist:
            payload.buffer << PGToken.WHITESPACE
            payload.buffer << PGToken.IF_NOT_EXIST

        # Render table name
        payload.buffer << PGToken.WHITESPACE
        payload.buffer << cls.__table_preferences__.name
        payload.buffer << PGToken.LEFT_PARENTHESIS

        cls.__table_columns__[0].render_for_table_creation(payload)
        for column in cls.__table_columns__[1:]:
            payload.buffer << PGToken.COMMA
            column.render_for_table_creation(payload)
        payload.buffer << PGToken.RIGHT_PARENTHESIS

    @classmethod
    def render_for_from_clause(cls, payload: BuildingPayload) -> None:
        cls.as_id().render(payload)

    @classmethod
    def create(cls) -> Create:
        return SupportsCreation.create(typing.cast(SupportsCreation, cls))

    @classmethod
    def _parse_columns(cls) -> typing.Generator[ColumnData, None, None]:
        for class_var_name, class_var_value in vars(cls).items():
            if isinstance(class_var_value, BaseColumn):
                full_column_data = ColumnData(
                    name=class_var_name,
                    schema=class_var_value,
                    table=cls,
                    table_name=cls.__table_preferences__.name,
                )
                class_var_value.column_data = full_column_data
                yield full_column_data

    @classmethod
    def _build_table_name(cls, name: typing.Optional[str]) -> str:
        return _camel2snake_convert_pattern.sub(
            "_", name or cls.__name__
        ).lower()
