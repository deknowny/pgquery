import abc
import dataclasses

from pgquery.builder.actor import BuildingPayload


@dataclasses.dataclass
class SupportsBeExpression(abc.ABC):
    @abc.abstractmethod
    def render_as_expression(self, payload: BuildingPayload) -> None:
        pass
