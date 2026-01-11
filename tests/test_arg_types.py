from flask import Flask

from ts_flask_urls.ts_types import TSObject, TSSimpleType

from conftest import ParserFixture


def test_args_int(app: Flask, args_parser: ParserFixture) -> None:
    @app.route("/<int:test>")
    def main(test) -> list:
        return []
    
    assert args_parser(app, "main") == TSObject(
        ("test",),
        (TSSimpleType("number"),)
    )

def test_args_float(app: Flask, args_parser: ParserFixture) -> None:
    @app.route("/<float:test>")
    def main(test) -> list:
        return []
    
    assert args_parser(app, "main") == TSObject(
        ("test",),
        (TSSimpleType("number"),)
    )

def test_args_path(app: Flask, args_parser: ParserFixture) -> None:
    @app.route("/<path:test>")
    def main(test) -> list:
        return []
    
    assert args_parser(app, "main") == TSObject(
        ("test",),
        (TSSimpleType("string"),)
    )

def test_args_uuid(app: Flask, args_parser: ParserFixture) -> None:
    @app.route("/<uuid:test>")
    def main(test) -> list:
        return []
    
    assert args_parser(app, "main") == TSObject(
        ("test",),
        (TSSimpleType("string"),)
    )

def test_args_unspecified(app: Flask, args_parser: ParserFixture) -> None:
    @app.route("/<test>")
    def main(test) -> list:
        return []
    
    assert args_parser(app, "main") == TSObject(
        ("test",),
        (TSSimpleType("string"),)
    )
