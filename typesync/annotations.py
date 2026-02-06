import typing

from typesync.misc import HTTPMethod


class TypesyncAnnotation: ...


class TypesyncSkipGenerationAnnotation(TypesyncAnnotation): ...


class TypesyncHTTPMethodAnnotation(TypesyncAnnotation):
    def __init__(self, methods: set[HTTPMethod]) -> None:
        self.methods = methods


type SkipGeneration[T] = typing.Annotated[T, TypesyncSkipGenerationAnnotation()]

type ForHTTPGet[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"GET"})]
type ForHTTPHead[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"HEAD"})]
type ForHTTPPost[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"POST"})]
type ForHTTPPut[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"PUT"})]
type ForHTTPDelete[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"DELETE"})]
type ForHTTPConnect[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"CONNECT"})]
type ForHTTPOptions[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"OPTIONS"})]
type ForHTTPTrace[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"TRACE"})]
type ForHTTPPatch[T] = typing.Annotated[T, TypesyncHTTPMethodAnnotation({"PATCH"})]
