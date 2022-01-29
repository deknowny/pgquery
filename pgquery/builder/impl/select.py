from __future__ import annotations

import abc
import dataclasses
import itertools
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import Renderable
from pgquery.builder.impl.alias import Alias
from pgquery.builder.impl.func import FuncCall
from pgquery.builder.impl.literal import StaticLiteral, literal
from pgquery.builder.impl.parentheses import Parentheses
from pgquery.builder.impl.raw import Raw
from pgquery.builder.impl.tokens import PGToken
from pgquery.builder.impl.where import WhereMixin

SelectSchemaType = typing.TypeVar("SelectSchemaType")
SelectSchema = typing.Dict[str, typing.Union[Renderable, SelectSchemaType]]


@dataclasses.dataclass
class SelectableMixin(abc.ABC):
    @abc.abstractmethod
    def render_as_selectable(self, payload: BuildingPayload) -> None:
        pass

    def select(self, schema, **aliased_values) -> Select:
        return Select(schema=schema or aliased_values, tables=[self])


@dataclasses.dataclass
class _NestedField(Renderable):
    unwrapped_mapping: typing.List[typing.Tuple[StaticLiteral, Renderable]]

    @classmethod
    def from_mapping(
        cls, mapping: typing.Dict[str, Renderable]
    ) -> _NestedField:
        fields_iterable = list(
            (literal(k), cls.cast_to_renderable(v))
            for k, v in mapping.items()
        )
        return cls(fields_iterable)

    @staticmethod
    def cast_to_renderable(
        value: typing.Union[Renderable, dict]
    ) -> Renderable:
        if isinstance(value, dict):
            return _NestedField.from_mapping(value)
        return value

    def render(self, payload: BuildingPayload) -> None:
        funcs_args = itertools.chain.from_iterable(self.unwrapped_mapping)
        funcs_args = list(funcs_args)
        funcs_call = FuncCall("jsonb_build_object", funcs_args)
        funcs_call.render(payload)

    def pop_selects(
        self,
    ) -> typing.List[typing.Tuple[StaticLiteral, LateralSubSelect]]:
        selects = []
        for ind, pair in enumerate(self.unwrapped_mapping):
            k, v = pair
            if isinstance(v, Select):
                lateral = LateralSubSelect(select=v, alias=f"r{ind}")
                selects.append((k, lateral))
                del self.unwrapped_mapping[ind]

        return selects


@dataclasses.dataclass
class LateralSubSelect(SelectableMixin):
    alias: str
    select: Select

    def render_as_selectable(self, payload: BuildingPayload) -> None:
        payload.buffer << "LATERAL "
        entity = Alias(Parentheses(value=self.select), alias=self.alias)
        entity.render(payload)


@dataclasses.dataclass
class _SelectInit:
    tables: typing.List[SelectableMixin]
    schema: SelectSchema


@dataclasses.dataclass
class Select(Renderable, WhereMixin, _SelectInit):
    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << "SELECT jsonb_agg(r.r) r FROM (SELECT "

        current_fields = _NestedField.from_mapping(self.schema)

        selects = current_fields.pop_selects()

        for sub_select_field, sub_select_result in selects:
            self.tables.append(sub_select_result)
            current_fields.unwrapped_mapping.append(
                (sub_select_field, Raw(sub_select_result.alias + ".r"))
            )

        nest_with_alias = Alias(current_fields, "r")
        nest_with_alias.render(payload)

        payload.buffer << " FROM "

        tables_count = len(self.tables)
        for ind, table in enumerate(self.tables):
            table.render_as_selectable(payload)
            if tables_count - 1 != ind:
                payload.buffer << PGToken.COMMA

        if self.where_clause is not None:
            payload.buffer << PGToken.WHITESPACE
            self.where_clause.render(payload)

        payload.buffer << ") r"
