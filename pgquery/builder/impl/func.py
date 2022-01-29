from __future__ import annotations

import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import PyType, PyTypeReference, Renderable
from pgquery.builder.impl.tokens import PGToken


def func(name: str, *args: Renderable) -> FuncCall:
    return FuncCall(name, args)


@dataclasses.dataclass
class FuncCall(Renderable, PyTypeReference[PyType]):
    name: str
    args: typing.Collection[Renderable]

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << self.name
        payload.buffer << PGToken.LEFT_PARENTHESIS

        args_length = len(self.args)
        for ind, arg in enumerate(self.args):
            arg.render(payload)
            if args_length - 1 != ind:
                payload.buffer << ","

        payload.buffer << PGToken.RIGHT_PARENTHESIS
