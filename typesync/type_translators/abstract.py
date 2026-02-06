import abc
import typing


if typing.TYPE_CHECKING:
    from . import TypeNode
    from .context import TranslationContext
    from typesync.ts_types import TSType


class Translator(abc.ABC):
    DEFAULT_PRIORITY: int = 0
    ID: str

    def __init__(
        self,
        translate: typing.Callable[
            ["TypeNode", dict[typing.TypeVar, "TSType"] | None], "TSType"
        ],
        ctx: "TranslationContext",
    ) -> None:
        self._translate = translate
        self.ctx = ctx

    @abc.abstractmethod
    def translate(
        self, node: "TypeNode", generics: dict[typing.TypeVar, "TSType"] | None
    ) -> "TSType | None": ...
