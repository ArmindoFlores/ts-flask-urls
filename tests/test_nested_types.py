from flask import Flask

from ts_flask_urls.ts_types import (
    TSArray,
    TSSimpleType,
    TSRecord,
    TSTuple,
    TSUnion,
    TSRecursiveType,
)

from conftest import ParserFixture


type Alias1[A] = list[A]
type Alias2[B] = Alias1[B]
type AliasedArgs[A, B] = dict[str, tuple[Alias1[B], Alias2[A]]]
type Recursive1[A] = tuple[A | Recursive1[A], ...]
type Recursive2[A, B] = tuple[A | Recursive2[B, A], ...]
type Recursive3[A, B, C] = tuple[A | Recursive3[C, A, B], ...]


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


def test_recursive_args_1(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> Recursive1[int]:
        return ()

    assert return_parser(app, "main") == TSArray(
        TSUnion(
            (
                TSSimpleType("number"),
                TSRecursiveType(),
            )
        )
    )


def test_recursive_args_2(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> Recursive2[bool, str]:
        return ()

    assert return_parser(app, "main") == TSArray(
        TSUnion(
            (
                TSSimpleType("boolean"),
                TSArray(
                    TSUnion(
                        (
                            TSSimpleType("string"),
                            TSRecursiveType(),
                        )
                    )
                ),
            )
        )
    )


def test_recursive_args_3(app: Flask, return_parser: ParserFixture) -> None:
    @app.route("/main")
    def main() -> Recursive3[bool, str, int]:
        return ()

    assert return_parser(app, "main") == TSArray(
        TSUnion(
            (
                TSSimpleType("boolean"),
                TSArray(
                    TSUnion(
                        (
                            TSSimpleType("number"),
                            TSArray(
                                TSUnion(
                                    (
                                        TSSimpleType("string"),
                                        TSRecursiveType(),
                                    )
                                )
                            ),
                        )
                    )
                ),
            )
        )
    )
