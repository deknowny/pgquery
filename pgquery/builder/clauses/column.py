from __future__ import annotations

import abc
import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.identifier import Identifier
from pgquery.builder.clauses.literal import Literal
from pgquery.builder.clauses.op import BinaryOp, EqMixin
from pgquery.builder.mixins.expression import SupportsBeExpression
from pgquery.builder.mixins.identifier import SupportsRenderAsIdentifier
from pgquery.builder.tokens import PGToken

if typing.TYPE_CHECKING:
    from pgquery.builder.clauses.table import Table, TablePreferences


@dataclasses.dataclass
class References:
    table: typing.Type[Table]
    field: BaseColumn

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.REFERENCES
        payload.buffer << PGToken.WHITESPACE
        self.table.as_id().render(payload)
        payload.buffer << PGToken.WHITESPACE
        payload.buffer << PGToken.LEFT_PARENTHESIS
        self.field.as_id(short=True).render(payload)
        payload.buffer << PGToken.RIGHT_PARENTHESIS


@dataclasses.dataclass(eq=False)
class BaseColumn(SupportsRenderAsIdentifier, SupportsBeExpression, abc.ABC):
    pk: bool = False
    unique: bool = False
    nullable: bool = False
    default: typing.Optional[Literal] = None  # TOOD: DynamicLiteral
    references: typing.Optional[References] = None

    # Set later from Table
    column_data: typing.Optional[ColumnData] = None

    def render_as_expression(self, payload: BuildingPayload):
        self.as_id().render(payload)

    def as_id(self, short: bool = False) -> Identifier:
        chain = [self.column_data.name]
        if not short:
            chain.insert(0, self.column_data.table_name)
        return Identifier(*chain)

    @abc.abstractmethod
    def render_column_type(self, payload: BuildingPayload) -> None:
        pass


@dataclasses.dataclass
class ColumnData:
    name: str
    schema: BaseColumn
    table: typing.Type[Table]
    # Individually because could be mocked
    table_name: str

    def render_for_table_creation(self, payload: BuildingPayload) -> None:
        self.schema.as_id(short=True).render(payload)
        payload.buffer << PGToken.WHITESPACE

        # Render column type
        self.schema.render_column_type(payload)

        # Default
        if self.schema.default is not None:
            payload.buffer << PGToken.WHITESPACE
            payload.buffer << PGToken.DEFAULT
            payload.buffer << PGToken.WHITESPACE
            self.schema.default.render_literal(payload)

        # Primary key
        if self.schema.pk:
            payload.buffer << PGToken.WHITESPACE
            payload.buffer << PGToken.PRIMARY_KEY

        # References
        if self.schema.references:
            payload.buffer << PGToken.WHITESPACE
            self.schema.references.render(payload)

        # TODO: cascade, not null


@dataclasses.dataclass(eq=False)
class Integer(BaseColumn, EqMixin):
    def __eq__(self, other: SupportsBeExpression) -> BinaryOp:
        return self._eq_impl(other)

    def render_column_type(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.INTEGER


@dataclasses.dataclass(eq=False)
class Serial(BaseColumn, EqMixin):
    def __eq__(self, other: SupportsBeExpression) -> BinaryOp:
        return self._eq_impl(other)

    def render_column_type(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.SERIAL


@dataclasses.dataclass(eq=False)
class Text(BaseColumn):
    def render_column_type(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.TEXT


@dataclasses.dataclass(eq=False)
class _VarcharMixin:
    limit: int


@dataclasses.dataclass(eq=False)
class Varchar(BaseColumn, _VarcharMixin):
    def render_column_type(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.VARCHAR
        payload.buffer << PGToken.LEFT_PARENTHESIS
        payload.buffer << repr(self.limit)
        payload.buffer << PGToken.RIGHT_PARENTHESIS
