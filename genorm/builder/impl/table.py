import dataclasses
import re
import typing

from genorm.builder.actor import BuildingPayload
from genorm.builder.impl.column import BaseColumn, ColumnData
from genorm.builder.lexeme import BaseLexeme, TokensGenerator

# Pattern for converting CamelCase to snake_case
_camel2snake_convert_pattern = pattern = re.compile(r"(?<!^)(?=[A-Z])")


@dataclasses.dataclass
class TablePreferences:
    name: str
    if_not_exist: bool


class Table(BaseLexeme):

    __table_preferences__: TablePreferences
    __table_columns__: typing.Tuple[ColumnData, ...]

    def __init_subclass__(
        cls,
        name: typing.Optional[str] = None,
        if_not_exist: bool = True,
        **kwargs
    ):
        cls.__table_preferences__ = TablePreferences(
            name=cls._build_table_name(name), if_not_exist=if_not_exist
        )
        cls.__table_columns__ = tuple(cls._parse_columns())
        return super().__init_subclass__(**kwargs)

    @classmethod
    def render(cls, payload: BuildingPayload) -> TokensGenerator:
        yield "CREATE TABLE"
        if cls.__table_preferences__.if_not_exist:
            yield payload.separator.stable_whitespace
            yield "IF NOT EXISTS"

        yield payload.separator.stable_whitespace
        yield cls.__table_preferences__.name
        yield "("
        yield payload.separator.no_space_or_new_tab

    @classmethod
    def _parse_columns(cls) -> typing.Generator[ColumnData, None, None]:
        for class_var_name, class_var_value in vars(cls).items():
            if isinstance(class_var_value, BaseColumn):
                full_column_data = ColumnData(
                    name=class_var_name, schema=class_var_value
                )
                yield full_column_data

    @classmethod
    def _build_table_name(cls, name: typing.Optional[str]) -> str:
        return _camel2snake_convert_pattern.sub("_", cls.__name__).lower()
