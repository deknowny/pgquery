import dataclasses
import functools

from pgquery.builder.actor import BuildingPayload


@dataclasses.dataclass
class TokensSeparator:
    payload: BuildingPayload

    @functools.cached_property
    def stable_whitespace(self) -> str:
        return " "

    @property
    def no_space_or_new_tab(self) -> str:
        if self.payload.actor.debug:
            self.payload.indentation_level += 1
            yield "\n" + self.stable_whitespace * self.payload.indentation_level * self.payload.actor.indent_spaces

        yield ""
