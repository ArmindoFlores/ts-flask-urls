__all__ = [
    "TSType",
    "TSSimpleType",
    "TSRecord",
    "TSObject",
    "TSArray",
    "TSUnion",
    "TSTuple",
    "is_signal",
]

from abc import ABC, abstractmethod
from functools import cache
from typing import Sequence


class TSType(ABC):
    def __str__(self):
        return self._generate()

    def __repr__(self):
        return f"<TSType {self.generate()}>"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, TSType):
            return str(self) == str(other)
        return False

    def __hash__(self):
        return hash(str(self))

    @abstractmethod
    def _generate(self) -> str:
        raise NotImplementedError

    @cache
    def generate(self) -> str:
        return str(self)


class TSSimpleType(TSType):
    def __init__(self, type_: str):
        self.type_ = type_

    def _generate(self) -> str:
        if self.type_ == "...":
            return "never"
        return self.type_


class TSRecord(TSType):
    def __init__(self, key_type: TSType, value_type: TSType):
        self.key_type: TSType = key_type
        self.value_type: TSType = value_type

    def _generate(self) -> str:
        return f"Record<{self.key_type.generate()}, {self.value_type.generate()}>"


class TSObject(TSType):
    def __init__(self, keys: Sequence[str], value_types: Sequence[TSType], required: Sequence[bool] | None = None):
        self.keys: Sequence[str] = keys
        self.value_types: Sequence[TSType] = value_types
        self.required: Sequence[bool] = required or [True for _ in self.keys]

    def _generate(self) -> str:
        string = ""
        first = True
        for key, value_type, required in zip(self.keys, self.value_types, self.required):
            string += f"{'' if first else ' '}{key}{'' if required else '?'}: {value_type.generate()};"
            first = False
        return f"{{{string}}}"


class TSAggregatorType(TSType):
    def __init__(self, types: Sequence[TSType]):
        self.types: Sequence[TSType] = types


class TSUnion(TSAggregatorType):
    def _generate(self) -> str:
        return " | ".join([t.generate() for t in self.types])


class TSTuple(TSAggregatorType):
    def _generate(self) -> str:
        return "[" + ", ".join([t.generate() for t in self.types]) + "]"


class TSArray(TSType):
    def __init__(self, type_: TSType):
        self.type_: TSType = type_

    def _generate(self) -> str:
        if isinstance(self.type_, TSUnion):
            return f"({self.type_.generate()})[]"
        return f"{self.type_.generate()}[]"


def is_signal(t: TSType):
    return isinstance(t, TSSimpleType) and t.type_ == "..."
