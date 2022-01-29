import abc
import typing


class BaseSQLBuffer(abc.ABC):
    @abc.abstractmethod
    def push(self, string: str) -> None:
        pass

    @abc.abstractmethod
    def collect(self) -> str:
        pass

    def __lshift__(self, other: str):
        self.push(other)


class JoinSQlBuffer(BaseSQLBuffer):

    __slots__ = ("__buffer",)

    def __init__(self, initial_string: typing.Optional[str] = None) -> None:
        self.__buffer = []
        if initial_string is not None:
            self.__buffer.append(initial_string)

    def push(self, string: str) -> None:
        self.__buffer.append(string)

    def collect(self) -> str:
        return "".join(self.__buffer)
