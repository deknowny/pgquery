import dataclasses
import typing

from genorm.builder.actor import BuildingPayload
from genorm.builder.lexeme import BaseLexeme, TokensGenerator, double_quoted

ColumnPyType = typing.TypeVar("ColumnPyType")


@dataclasses.dataclass
class BaseColumn(typing.Generic[ColumnPyType]):
    pk: bool = False
    unique: bool = False
    references: typing.Optional[str] = None


@dataclasses.dataclass
class ColumnData(BaseLexeme):
    name: str
    schema: BaseColumn

    def render(self, payload: BuildingPayload) -> TokensGenerator:
        yield double_quoted(self.name)  # TODO


class Integer(BaseColumn[int]):
    pass


class Text(BaseColumn[str]):
    pass


@dataclasses.dataclass
class _VarcharMixin:
    limit: int = dataclasses.field()


class Varchar(_VarcharMixin, BaseColumn[str]):
    pass
