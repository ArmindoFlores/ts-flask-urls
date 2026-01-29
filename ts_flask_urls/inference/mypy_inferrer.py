import importlib
import os
import typing

import mypy.types
from mypy.build import build, BuildSource, BuildResult
from mypy.options import Options

from .base_inferrer import BaseInferrer
from ts_flask_urls.logger import ClickLogger, Logger


def resolve_fullname_to_type(fullname: str) -> type | None:
    try:
        parts = fullname.rsplit(".", 1)
        if len(parts) == 2:
            module_name, class_name = parts
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        else:
            return importlib.import_module(fullname)
    except (ImportError, AttributeError):
        return None


class MypyInferrer(BaseInferrer):
    def __init__(
        self, base_path: str, app_entry: str, logger: Logger | None = None
    ) -> None:
        self.base_path = base_path
        self.app_entry = app_entry
        self.app_name = app_entry.removesuffix(".py")
        self.location = os.path.join(base_path, app_entry)
        self.logger = ClickLogger() if logger is None else logger
        self.build: BuildResult | None = None

    def mypy_type_to_python_type(self, mypy_type: mypy.types.Type) -> typing.Any:
        mypy_type = mypy.types.get_proper_type(mypy_type)

        if isinstance(mypy_type, mypy.types.Instance):
            base_type = resolve_fullname_to_type(mypy_type.type.fullname)
            if mypy_type.args and base_type is not None:
                arg_types = tuple(
                    self.mypy_type_to_python_type(arg) for arg in mypy_type.args
                )
                try:
                    return (
                        base_type[arg_types]
                        if len(arg_types) > 1
                        else base_type[arg_types[0]]
                    )
                except (TypeError, AttributeError):
                    return base_type

            return typing.Any if base_type is None else base_type

        elif isinstance(mypy_type, mypy.types.UnionType):
            items = tuple(
                self.mypy_type_to_python_type(item) for item in mypy_type.items
            )
            return typing.Union[items]  # noqa: UP007

        elif isinstance(mypy_type, mypy.types.NoneType):
            return type(None)

        elif isinstance(mypy_type, mypy.types.TupleType):
            items = tuple(
                self.mypy_type_to_python_type(item) for item in mypy_type.items
            )
            return tuple[items]

        return typing.Any

    def rebuild(self) -> None:
        options = Options()
        options.incremental = False
        self.build = build([BuildSource(self.location, self.app_name)], options=options)

    def infer(self, subpath: str, function_name: str) -> typing.Any:
        if self.build is None:
            self.rebuild()

        types = self.build.graph[self.app_name].tree.names
        if function_name not in types:
            self.logger.warning(f"'{function_name}' in '{subpath}' was not found")
            return typing.Any
        route_func = types[function_name].type
        if not isinstance(route_func, mypy.types.CallableType):
            self.logger.warning(f"'{function_name}' in '{subpath}' must be a function")
            return typing.Any
        route_func_ret_type = route_func.ret_type
        return self.mypy_type_to_python_type(route_func_ret_type)
