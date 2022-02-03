from pgquery.builder.actor import BuildingPayload
from pgquery.builder.mixins.expression import SupportsBeExpression


class Identifier(SupportsBeExpression):
    def __init__(self, *names: str) -> None:
        self.names = names

    def render(self, payload: BuildingPayload) -> None:
        payload.buffer << f'"{self.names[0]}"'
        for name in self.names[1:]:
            payload.buffer << f'."{name}"'

    def render_as_expression(self, payload: BuildingPayload) -> None:
        self.render(payload)
