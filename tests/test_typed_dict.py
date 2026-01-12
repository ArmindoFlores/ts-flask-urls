from typing import TypedDict

from flask import Flask

from ts_flask_urls.ts_types import TSObject, TSRecord, TSSimpleType, TSTuple

from conftest import ParserFixture


def test_simple_typed_dict(app: Flask, return_parser: ParserFixture) -> None:
    class SimpleTypedDict(TypedDict):
        dictfield: dict[str, float]
        flag: bool
        items: tuple[str, int]

    @app.route("/main")
    def main() -> SimpleTypedDict:
        return {
            "dictfield": {
                "hello": 1.3,
                "world": -0.5
            },
            "flag": False,
            "items": ("1", 2)
        }
    
    assert return_parser(app, "main") == TSObject(
        keys=("dictfield", "flag", "items"),
        value_types=(
            TSRecord(TSSimpleType("string"), TSSimpleType("number")),
            TSSimpleType("boolean"),
            TSTuple((TSSimpleType("string"), TSSimpleType("number")))
        )
    )

def test_generic_typed_dict(app: Flask, return_parser: ParserFixture) -> None:
    class GenericTypedDict[X, Y](TypedDict):
        dictfield: dict[str, Y]
        flag: bool
        items: tuple[Y, X]

    @app.route("/main")
    def main() -> GenericTypedDict[str, float]:
        return {
            "dictfield": {
                "hello": 1.3,
                "world": -0.5
            },
            "flag": False,
            "items": (2.0, "str")
        }
    
    assert return_parser(app, "main") == TSObject(
        keys=("dictfield", "flag", "items"),
        value_types=(
            TSRecord(TSSimpleType("string"), TSSimpleType("number")),
            TSSimpleType("boolean"),
            TSTuple((TSSimpleType("number"), TSSimpleType("string")))
        )
    )
