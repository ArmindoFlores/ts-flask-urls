import typing

type HTTPMethodStrict = typing.Literal[
    "GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"
]

type HTTPMethod = HTTPMethodStrict | str
