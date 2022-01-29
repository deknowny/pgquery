import abc
import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.impl.tokens import PGToken
from pgquery.builder.lexeme import BaseLexeme, double_quoted

ColumnPyType = typing.TypeVar("ColumnPyType")


@dataclasses.dataclass
class BaseColumn(BaseLexeme, typing.Generic[ColumnPyType], abc.ABC):
    pk: bool = False
    unique: bool = False
    nullable: bool = False
    references: typing.Optional[str] = None


@dataclasses.dataclass
class ColumnData(BaseLexeme):
    name: str
    schema: BaseColumn

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << double_quoted(self.name)
        payload.buffer << PGToken.WHITESPACE
        # Render column type
        self.schema.render(payload)
        # TODO: cascade, defaults, not null


@dataclasses.dataclass
class Integer(BaseColumn[int]):
    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << "INTEGER"


@dataclasses.dataclass
class Serial(BaseColumn[int]):
    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << "SERIAL"


@dataclasses.dataclass
class Text(BaseColumn[str]):
    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << "TEXT"


@dataclasses.dataclass
class _VarcharMixin:
    limit: int


@dataclasses.dataclass
class Varchar(BaseColumn[str], _VarcharMixin):
    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << f"VARCHAR ({self.limit})"
