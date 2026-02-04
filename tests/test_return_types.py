from flask import Flask

from typesync.ts_types import TSArray, TSSimpleType, TSRecord

from conftest import ParserFixture


def test_return_dict(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> dict[str, int]:
        return {"result": 42}

    assert return_parser(app, "main") == TSRecord(
        TSSimpleType("string"), TSSimpleType("number")
    )


def test_return_dict_complex(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> dict[str, dict[int, bool]]:
        return {"result": {1: True}}

    assert return_parser(app, "main") == TSRecord(
        TSSimpleType("string"),
        TSRecord(
            TSSimpleType("number"),
            TSSimpleType("boolean"),
        ),
    )


def test_return_dict_missing_params(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> dict:
        return {"result": 42}

    assert return_parser(app, "main") == TSSimpleType("object")


def test_return_list(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> list[int]:
        return [1, 2, 3]

    assert return_parser(app, "main") == TSArray(TSSimpleType("number"))


def test_return_list_complex(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> list[list[str]]:
        return [[""]]

    assert return_parser(app, "main") == TSArray(TSArray(TSSimpleType("string")))


def test_return_list_missing_params(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> list:
        return []

    assert return_parser(app, "main") == TSArray(TSSimpleType("any"))


def test_return_tuple1(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> tuple[str, int]:
        return ("Status", 200)

    assert return_parser(app, "main") == TSSimpleType("string")


def test_return_tuple2(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> tuple[str, int, tuple]:
        return ("Status", 200, ())

    assert return_parser(app, "main") == TSSimpleType("string")
