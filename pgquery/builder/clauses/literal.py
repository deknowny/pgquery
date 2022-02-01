from __future__ import annotations

import abc
import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.op import BinaryOp, EqMixin
from pgquery.builder.mixins.expression import SupportsBeExpression

SupportedPythonLiterals = typing.Union[str, int]
SupportedPythonLiteralType = typing.TypeVar(
    "SupportedPythonLiteralType", bound=SupportedPythonLiterals
)


class BaseLiteralProcessor(
    typing.Generic[SupportedPythonLiteralType], abc.ABC
):
    @abc.abstractmethod
    def render_py_value(
        self, payload: BuildingPayload, py_value: SupportedPythonLiteralType
    ) -> None:
        pass


class IntegerLiteralProcessor(BaseLiteralProcessor[int]):
    def render_py_value(
        self, payload: BuildingPayload, py_value: int
    ) -> None:
        payload.buffer << repr(py_value)


class StringLiteralProcessor(BaseLiteralProcessor[str]):
    def render_py_value(
        self, payload: BuildingPayload, py_value: str
    ) -> None:
        payload.buffer << repr(py_value)
        # TODO: escapes, $$


@dataclasses.dataclass
class Literal(
    typing.Generic[SupportedPythonLiteralType], SupportsBeExpression, EqMixin
):
    py_value: SupportedPythonLiteralType
    processor: BaseLiteralProcessor[SupportedPythonLiteralType]

    def __eq__(self, other: SupportsBeExpression) -> BinaryOp:
        return self._eq_impl(other)

    @classmethod
    def new(cls, py_value: SupportedPythonLiteralType) -> Literal:
        if isinstance(py_value, str):
            processor = StringLiteralProcessor()
        elif isinstance(py_value, int):
            processor = IntegerLiteralProcessor()
        else:
            raise SuchLiteralIsNotSupportedError(py_value)

        return cls(py_value=py_value, processor=processor)

    def render_literal(self, payload: BuildingPayload) -> None:
        self.processor.render_py_value(payload, self.py_value)

    def render_as_expression(self, payload: BuildingPayload) -> None:
        self.render_literal(payload)


@dataclasses.dataclass
class SuchLiteralIsNotSupportedError(Exception):
    value: typing.Any

    def __repr__(self) -> str:
        return f"Cannot make literal from python value {self.value}"
