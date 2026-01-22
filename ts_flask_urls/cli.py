import os

import click
from flask import current_app
from flask.cli import AppGroup
from werkzeug.routing.rules import Rule

from .codegen import FlaskAnnotationsParser, CodeWriter


cli = AppGroup("ts-flask-urls")


@cli.command(help="Generate Typescript types based on Flask routes.")
@click.argument("out_dir", type=click.Path(file_okay=False, resolve_path=True))
@click.option("--endpoint", "-E", help="The base endpoint.", default="")
def map_urls(out_dir: str, endpoint: str):
    rules: list[Rule] = list(current_app.url_map.iter_rules())

    os.makedirs(out_dir, exist_ok=True)

    with (
        open(os.path.join(out_dir, "types.ts"), "w") as types_f,
        open(os.path.join(out_dir, "apis.ts"), "w") as api_f,
    ):
        code_writer = CodeWriter(types_f, api_f, endpoint)
        result = code_writer.write(
            FlaskAnnotationsParser(current_app, rule) for rule in rules
        )
        if not result:
            click.secho("Errors occurred during file generation", fg="red")
