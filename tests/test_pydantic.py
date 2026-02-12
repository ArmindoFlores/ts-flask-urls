from flask import Flask
from pydantic import BaseModel

from typesync.ts_types import TSObject, TSSimpleType, TSArray, TSRecursiveType
from typesync.utils import Loadable, deferred, with_json_body

from conftest import ParserFixture


def test_simple_model(app: Flask, json_body_parser: ParserFixture) -> None:
    class SimpleModel(BaseModel):
        id: int
        name: str = "John"
        friends: list["SimpleModel"]

    @app.route("/main", methods=("POST",))
    @with_json_body(loader=SimpleModel.model_validate)
    def main(json: SimpleModel):
        return {}

    assert json_body_parser(app, "main") == TSObject(
        keys=("id", "name", "friends"),
        value_types=(
            TSSimpleType("number"),
            TSSimpleType("string"),
            TSArray(TSRecursiveType()),
        ),
        required=(True, False, True),
    )


def test_deferred(app: Flask, json_body_parser: ParserFixture) -> None:
    class SimpleModel(BaseModel):
        id: int
        name: str = "John"
        friends: list["SimpleModel"]

    @app.route("/main", methods=("POST",))
    @with_json_body(loader=deferred(SimpleModel.model_validate))
    def main(json: Loadable[SimpleModel]):
        return {}

    assert json_body_parser(app, "main") == TSObject(
        keys=("id", "name", "friends"),
        value_types=(
            TSSimpleType("number"),
            TSSimpleType("string"),
            TSArray(TSRecursiveType()),
        ),
        required=(True, False, True),
    )
