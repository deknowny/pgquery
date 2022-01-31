import abc

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.tokens import PGToken


class SupportsCreation(abc.ABC):
    @abc.abstractmethod
    def render_for_creation(self, payload: BuildingPayload):
        pass

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << PGToken.CREATE
        self.render_for_creation(payload)
