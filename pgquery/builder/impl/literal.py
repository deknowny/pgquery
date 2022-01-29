from __future__ import annotations

import dataclasses

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import PyType, PyTypeReference, Renderable


def literal(value: PyType) -> StaticLiteral[PyType]:
    return StaticLiteral(value=value)


@dataclasses.dataclass
class StaticLiteral(Renderable, PyTypeReference[PyType]):

    value: PyType

    def render(self, payload: BuildingPayload) -> None:
        if isinstance(self.value, (int, str)):
            payload.buffer << repr(self.value)

        else:
            # TODO
            raise NotImplementedError()
