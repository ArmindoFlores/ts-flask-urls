import functools
import typing
from collections.abc import Callable

import flask


class Response[T](flask.Response):
    """A typed `flask.Response`.
    This exists to let `typesync` know the response contains JSON shaped like T.
    At runtime it behaves exactly like `flask.Response`.
    """


def jsonify[T](data: T) -> Response[T]:
    """A typed wrapper around `flask.jsonify`.
    Use this instead of `flask.jsonify` so that `typesync`can track the shape
    of the JSON you're returning. It does not validate or transform `data`.
    """
    return typing.cast(Response[T], flask.jsonify(data))


def _json_kwarg_decorator[**P, R](func: Callable[P, R], key: str) -> Callable[P, R]:
    # Tag this route as accepting a JSON parameter
    func._typesync = key  # type: ignore[attr-defined]

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        kwargs[key] = flask.request.json
        return func(*args, **kwargs)

    return wrapper


@typing.overload
def json_kwarg[**P, R](func_or_key: Callable[P, R]) -> Callable[P, R]:
    """Decorate a view function to receive the request JSON as a `json` keyword
    argument.

    Use this form as `@json_kwarg` directly on a Flask view. When the
    view is called, `flask.request.json` is injected into the function call under
    the keyword name `"json"`.
    """


@typing.overload
def json_kwarg[**P, R](func_or_key: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Create a decorator that injects the request JSON under a custom keyword name.

    Use this form as `@json_kwarg("arg")` (or any other string). The returned decorator
    wraps a Flask view so that `flask.request.json` is passed into the function under
    as a keyword argument with the given name.
    """


def json_kwarg[**P, R](
    func_or_key: Callable[P, R] | str,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    if isinstance(func_or_key, str):

        def wrapper(func: Callable[P, R]):
            return _json_kwarg_decorator(func, func_or_key)

        return wrapper

    return _json_kwarg_decorator(func_or_key, "json")
