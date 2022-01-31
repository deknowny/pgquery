import dataclasses
import typing


@dataclasses.dataclass(eq=False)
class BaseColumn(abc.ABC):
    pk: bool = False
    unique: bool = False
    nullable: bool = False
    default: typing.Optional[StaticLiteral] = None  # TODO: DynamicLiteral
    references: typing.Optional[str] = None

    # Set later from Table
    column_data: typing.Optional[ColumnData] = None

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << double_quoted(
            self.column_data.table.__table_preferences__.name
        )
        payload.buffer << PGToken.DOT
        payload.buffer << double_quoted(self.column_data.name)

    @abc.abstractmethod
    def render_column_type(self, payload: BuildingPayload):
        pass

    def __eq__(self: Renderable, other: Renderable) -> BinaryOp:
        return EqOpMixin.__eq__(self, other)


@dataclasses.dataclass
class ColumnData:
    name: str
    schema: BaseColumn
    table: typing.Type[Table]

    def render_for_table_creation(self, payload: BuildingPayload) -> None:
        payload.buffer << double_quoted(self.name)
        payload.buffer << PGToken.WHITESPACE
        # Render column type
        self.schema.render_column_type(payload)

        # Default
        if self.schema.default is not None:
            payload.buffer << PGToken.WHITESPACE
            payload.buffer << PGToken.DEFAULT
            payload.buffer << PGToken.WHITESPACE
            self.schema.default.render(payload)

        # Primary key
        if self.schema.pk:
            payload.buffer << PGToken.WHITESPACE
            payload.buffer << PGToken.PRIMARY_KEY

        # References
        if self.schema.references:
            table, column = self.schema.references.split(".")
            payload.buffer << PGToken.WHITESPACE
            payload.buffer << PGToken.REFERENCES
            payload.buffer << PGToken.WHITESPACE,
            payload.buffer << double_quoted(table),
            payload.buffer << PGToken.WHITESPACE,
            payload.buffer << PGToken.LEFT_PARENTHESIS,
            payload.buffer << double_quoted(column)
            payload.buffer << PGToken.RIGHT_PARENTHESIS

        # TODO: cascade, not null


@dataclasses.dataclass(eq=False)
class Integer(BaseColumn[int]):
    def render_column_type(self, payload: BuildingPayload) -> None:
        payload.buffer << "INTEGER"


@dataclasses.dataclass(eq=False)
class Serial(BaseColumn[int]):
    def render_column_type(self, payload: BuildingPayload) -> None:
        payload.buffer << "SERIAL"


@dataclasses.dataclass(eq=False)
class Text(BaseColumn[str]):
    def render_column_type(self, payload: BuildingPayload) -> None:
        payload.buffer << "TEXT"


@dataclasses.dataclass(eq=False)
class _VarcharMixin:
    limit: int


@dataclasses.dataclass(eq=False)
class Varchar(BaseColumn[str], _VarcharMixin):
    def render_column_type(self, payload: BuildingPayload) -> None:
        payload.buffer << f"VARCHAR ({self.limit})"
