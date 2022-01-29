# import abc
# import dataclasses
# import functools
# import typing
#
# from pgquery.builder.actor import BuildingPayload
#
#
# @dataclasses.dataclass
# class BaseTokensSeparator(abc.ABC):
#     payload: BuildingPayload
#     stable_whitespace: typing.ClassVar[str] = " "
#     stable_newline: typing.ClassVar[str] = "\n"
#
#     @property
#     @abc.abstractmethod
#     def nothing_or_new_line(self) -> str:
#         pass
#
#     @property
#     @abc.abstractmethod
#     def nothing_or_new_expanded_line(self) -> str:
#         pass
#
#     @property
#     @abc.abstractmethod
#     def nothing_or_new_narrowed_line(self) -> str:
#         pass
#
#
# class DebugTokensSeparator(BaseTokensSeparator):
#     def increment_indent_level(self) -> int:
#         self.payload.indentation_level += 1
#         return self.payload.indentation_level
#
#     def decrement_indent_level(self) -> int:
#         self.payload.indentation_level -= 1
#         return self.payload.indentation_level
#
#     @functools.cached_property
#     def indent_block(self) -> str:
#         """
#         How many spaces a "tab" contains
#         """
#         return self.stable_whitespace * self.payload.actor.indent_spaces
#
#     @property
#     def current_indent(self) -> str:
#         """
#         Current "tab" indent (full)
#         """
#         return self.indent_block * self.payload.indentation_level
#
#     @property
#     def expanded_indent(self) -> str:
#         """
#         Expended "tab" indent (full) with 1 new tab
#         """
#         return self.indent_block * self.increment_indent_level()
#
#     @property
#     def narrowed_indent(self) -> str:
#         """
#         Narrowed "tab" indent (full) with 1 new tab
#         """
#         return self.indent_block * self.decrement_indent_level()
#
#     @property
#     def nothing_or_new_line(self) -> str:
#         return self.stable_newline + self.current_indent
#
#     @property
#     def nothing_or_new_expanded_line(self) -> str:
#         return self.stable_newline + self.expanded_indent
#
#     @property
#     def nothing_or_new_narrowed_line(self) -> str:
#         return self.stable_newline + self.narrowed_indent
#
#
# class ProductionTokensSeparator(BaseTokensSeparator):
#     @functools.cached_property
#     def nothing_or_new_line(self) -> str:
#         return ""
#
#     @functools.cached_property
#     def nothing_or_new_expanded_line(self) -> str:
#         return ""
#
#     @functools.cached_property
#     def nothing_or_new_narrowed_line(self) -> str:
#         return ""
