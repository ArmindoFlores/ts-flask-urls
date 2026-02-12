import typing

from typesync.ts_types import TSObject, TSType
from .abstract import Translator
from .type_node import TypeNode, to_type_node


class PydanticTranslator(Translator):
    DEFAULT_PRIORITY = -20
    ID = "typesync.PydanticTranslator"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        try:
            import pydantic  # noqa: PLC0415
        except ImportError as exc:
            raise RuntimeError(  # noqa: TRY003
                "Pydantic support requires 'pydantic'. "
                "Install with `pip install typesync[pydantic]`."
            ) from exc

        self._pydantic = pydantic

    def translate(
        self, node: TypeNode, generics: dict[typing.TypeVar, TSType] | None
    ) -> TSType | None:
        if not isinstance(node.origin, type) or not issubclass(
            node.origin, self._pydantic.BaseModel
        ):
            return None

        keys = tuple(node.origin.model_fields.keys())
        value_types = tuple(
            self._translate(to_type_node(value.annotation, node), generics)
            for value in node.origin.model_fields.values()
        )
        required = tuple(
            value.is_required() for value in node.origin.model_fields.values()
        )
        # TODO: Handle other Pydantic properties

        return TSObject(keys, value_types, required)
