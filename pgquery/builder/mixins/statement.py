import abc
import dataclasses

from pgquery.builder.actor import BuildingPayload


@dataclasses.dataclass
class SupportsStatement(abc.ABC):
    @abc.abstractmethod
    def render(self, payload: BuildingPayload) -> None:
        pass
