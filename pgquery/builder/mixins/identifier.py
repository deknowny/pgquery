import abc
import dataclasses

from pgquery.builder.clauses.identifier import Identifier


@dataclasses.dataclass
class SupportsRenderAsIdentifier(abc.ABC):
    @abc.abstractmethod
    def as_id(self) -> Identifier:
        pass
