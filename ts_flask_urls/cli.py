import os

import click
from flask import current_app
from flask.cli import AppGroup
from werkzeug.routing.rules import Rule

from .codegen import FlaskAnnotationsParser, CodeWriter
from .inference.mypy_inferrer import BaseInferrer, MypyInferrer


cli = AppGroup("ts-flask-urls")


def get_inferrer(inferrer_name: str) -> type[BaseInferrer] | None:
    if inferrer_name == "mypy":
        return MypyInferrer
    return None


@cli.command(help="Generate Typescript types based on Flask routes.")
@click.argument("out_dir", type=click.Path(file_okay=False, resolve_path=True))
@click.option("--endpoint", "-E", help="The base endpoint", default="")
@click.option(
    "--inference-mode",
    "-M",
    type=click.Choice(["always", "never", "fallback"], case_sensitive=False),
    default="never",
    help=(
        "Type inference mode: always (use type checker only), "
        "never (use annotations only), "
        "fallback (use type checker when annotations are absent)"
    ),
)
@click.option(
    "--inferrer",
    "-I",
    type=click.Choice(["mypy"], case_sensitive=False),
    default="mypy",
    help="Python typechecker to use during inference",
)
def map_urls(out_dir: str, endpoint: str, inference_mode: str, inferrer: str):
    rules: list[Rule] = list(current_app.url_map.iter_rules())

    os.makedirs(out_dir, exist_ok=True)

    with (
        open(os.path.join(out_dir, "types.ts"), "w") as types_f,
        open(os.path.join(out_dir, "apis.ts"), "w") as api_f,
    ):
        app_entry_file = current_app.import_name + ".py"
        inferrer_cls = get_inferrer(inferrer)
        inferrence_engine = (
            inferrer_cls(current_app.root_path, app_entry_file)
            if inferrer_cls is not None
            else None
        )
        code_writer = CodeWriter(types_f, api_f, endpoint)
        result = code_writer.write(
            FlaskAnnotationsParser(
                current_app,
                rule,
                inferrer=inferrence_engine,
                inference_mode=inference_mode,
            )
            for rule in rules
        )
        if not result:
            click.secho("Errors occurred during file generation", fg="red")
