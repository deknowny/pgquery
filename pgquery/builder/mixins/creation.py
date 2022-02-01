import abc

from pgquery.builder.actor import BuildingPayload
from pgquery.builder.clauses.creation import Create
from pgquery.builder.tokens import PGToken


class SupportsCreation(abc.ABC):
    @abc.abstractmethod
    def render_for_creation(self, payload: BuildingPayload):
        pass

    def create(self) -> Create:
        return Create(creatable=self)
