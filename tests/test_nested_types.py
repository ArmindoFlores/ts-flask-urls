from flask import Flask

from ts_flask_urls.ts_types import TSArray, TSSimpleType, TSRecord, TSTuple

from conftest import ParserFixture


type Alias1[A] = list[A]
type Alias2[B] = Alias1[B]
type AliasedArgs[A, B] = dict[str, tuple[Alias1[B], Alias2[A]]]


def test_nested_depth_1(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> Alias1[str]:
        return []

    assert return_parser(app, "main") == TSArray(TSSimpleType("string"))


def test_nested_depth_2(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> Alias2[str]:
        return []

    assert return_parser(app, "main") == TSArray(TSSimpleType("string"))


def test_nested_args(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> AliasedArgs[int, bool]:
        return {}

    assert return_parser(app, "main") == TSRecord(
        TSSimpleType("string"),
        TSTuple(
            (
                TSArray(TSSimpleType("boolean")),
                TSArray(TSSimpleType("number")),
            )
        ),
    )
