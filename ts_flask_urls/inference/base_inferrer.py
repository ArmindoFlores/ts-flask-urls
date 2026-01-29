import abc
import typing

from ts_flask_urls.logger import Logger


class BaseInferrer(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self, base_path: str, app_entry: str, logger: Logger | None = None
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def infer(self, subpath: str, function_name: str) -> typing.Any:
        raise NotImplementedError
