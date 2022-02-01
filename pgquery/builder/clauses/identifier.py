import dataclasses
import typing

from pgquery.builder.actor import BuildingPayload


@dataclasses.dataclass
class Identifier:
    names: typing.List[str]

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << f'"{self.names[0]}"'
        for name in self.names[1:]:
            payload.buffer << f'."{name}"'
