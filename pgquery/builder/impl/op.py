from __future__ import annotations

import dataclasses

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import Renderable


@dataclasses.dataclass
class BinaryOp(Renderable):
    sign: str
    left: Renderable
    right: Renderable

    def render(self, payload: BuildingPayload) -> None:
        self.left.render(payload)
        payload.buffer << self.sign
        self.right.render(payload)


class EqOpMixin:
    def __eq__(self: Renderable, other: Renderable) -> BinaryOp:
        return BinaryOp(sign="=", left=self, right=other)
