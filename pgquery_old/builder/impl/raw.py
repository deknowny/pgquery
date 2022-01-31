import dataclasses

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clause import Renderable


@dataclasses.dataclass
class Raw(Renderable):
    value: str

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << self.value
