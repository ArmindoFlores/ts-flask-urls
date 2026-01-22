import typing

import flask
import pytest

from ts_flask_urls.ts_types import TSType
from ts_flask_urls.codegen import FlaskAnnotationsParser


@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app


type ParserFixture = typing.Callable[[flask.Flask, str], TSType | None]


@pytest.fixture
def args_parser():
    def inner(app: flask.Flask, endpoint: str) -> TSType | None:
        rules = app.url_map.iter_rules()
        for rule in rules:
            if rule.endpoint == endpoint:
                return FlaskAnnotationsParser(app, rule).parse_args_type()
        return None

    return inner


@pytest.fixture
def return_parser():
    def inner(app: flask.Flask, endpoint: str) -> TSType | None:
        rules = app.url_map.iter_rules()
        for rule in rules:
            if rule.endpoint == endpoint:
                return FlaskAnnotationsParser(app, rule).parse_return_type()
        return None

    return inner
