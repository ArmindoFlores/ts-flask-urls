import typing

import click


class Logger(typing.Protocol):
    def info(self, text: str) -> None: ...
    def warning(self, text: str) -> None: ...
    def error(self, text: str) -> None: ...


class ClickLogger:
    @staticmethod
    def info(text: str) -> None:
        click.echo(f"Info: {text}")

    @staticmethod
    def warning(text: str) -> None:
        click.secho(f"Warning: {text}", fg="yellow")

    @staticmethod
    def error(text: str) -> None:
        click.secho(f"Error: {text}", fg="red")
