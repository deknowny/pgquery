import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload

SupportedPythonLiterals = typing.Union[str, int]


@dataclasses.dataclass
class Literal:
    py_value: SupportedPythonLiterals

    def render_literal(self, payload: BuildingPayload) -> None:
        payload.buffer
