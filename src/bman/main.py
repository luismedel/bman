import os
import re
import click
import orjson
import typing as t
import os.path
from datetime import datetime


ROOT_PATH = os.environ.get("BMAN_ROOT_PATH", "~/.bman")
CONF_FILE = "config.json"
LIBRARY_FILE = "library.json"
DEFAULT_OUTPUT_MODE = "full"
DEFAULT_OUTPUT_COLOR = "white"

# Keys used for the config dict
KEY_COLORS = "output_colors"
KEY_DEFAULT_OUTPUT_MODE = "output_mode"

DEFAULT_CONFIG = {
    KEY_COLORS: {
        "url": "cyan",
        "description": "bright_white",
        "tags": "yellow",
        "date": "white",
    },
    KEY_DEFAULT_OUTPUT_MODE: DEFAULT_OUTPUT_MODE,
}


def _load_json(file: str) -> t.Dict[str, t.Any]:
    try:
        path = os.path.expanduser(os.path.join(ROOT_PATH, file))
        with open(path, "r") as f:
            contents = f.read().strip()
            if len(contents) == 0:
                return {}
            return orjson.loads(contents)
    except FileNotFoundError:
        return {}


def _save_json(file: str, data: t.Dict[str, t.Any]) -> None:
    os.makedirs(os.path.expanduser(ROOT_PATH), exist_ok=True)
    path = os.path.expanduser(os.path.join(ROOT_PATH, file))
    with open(path, "w") as f:
        f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2).decode())


def _load_config() -> t.Dict[str, t.Any]:
    result = dict(DEFAULT_CONFIG)

    try:
        loaded = _load_json("config.json")
        if len(loaded):
            result.update(loaded)
        else:
            # Save the default conf
            _save_json("config.json", result)
        return result
    except Exception as ex:
        raise click.ClickException(f"Cannot load configuration: {str(ex)}")


def _load_library() -> t.Dict[str, t.Any]:
    try:
        return _load_json("library.json")
    except Exception as ex:
        raise click.ClickException(f"Cannot load library: {str(ex)}")


def _save_library(data: t.Dict[str, t.Any]) -> None:
    try:
        _save_json("library.json", data)
    except Exception as ex:
        raise click.ClickException(f"Cannot save library: {str(ex)}")


@click.group(
    name="bman",
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Your command line bookmark manager.",
)
def bman() -> None:
    pass


@bman.command(name="ls", help="Lists stored entries")
@click.option(
    "--format",
    type=click.Choice(["only-url", "full", "json"]),
    default=DEFAULT_OUTPUT_MODE,
    required=False,
    help="Set the output format",
)
@click.argument("filter", type=str, required=False)
@click.option(
    "--use-regex",
    is_flag=True,
    default=False,
    required=False,
    help="Treat the search filter as a regex pattern",
)
@click.option(
    "--fields",
    type=str,
    required=False,
    help="Comma separated list of fields to show (and to apply filter to)",
)
def command_ls(
    format: str, filter: str | None, use_regex: bool, fields: str | None
) -> None:
    config = _load_config()
    lib = _load_library()

    colors: t.Dict[str, t.Any] = config.get(KEY_COLORS, {})
    get_color = lambda k: colors.get(k, DEFAULT_OUTPUT_COLOR)

    if fields:
        show_fields = [f.strip().lower() for f in fields.split(",")]
        for k, data in tuple(lib.items()):
            lib[k] = {dk: dv for dk, dv in data.items() if dk.lower() in show_fields}

    if filter:
        pattern: re.Pattern = re.compile(filter if use_regex else re.escape(filter))

        def value_match(v: t.Any) -> bool:
            return pattern.search(str(v)) is not None

        def list_match(lst: list) -> bool:
            return any(pattern.search(i) is not None for i in lst)

        def emntry_matches_filter(url: str, data: t.Dict[str, t.Any]) -> bool:
            return pattern.search(url) is not None or any(
                list_match(v) if isinstance(v, list) else value_match(v)
                for v in data.values()
            )

        lib = dict(
            (k, data) for k, data in lib.items() if emntry_matches_filter(k, data)
        )

    if format == "json":
        click.echo(orjson.dumps(lib).decode())

    elif format == "full":
        for k, data in lib.items():
            click.secho(k, fg=get_color("url"))

            for k, v in data.items():
                click.echo(f"{k.capitalize()}: ", nl=False)
                click.secho(v, fg=get_color(k))

            click.echo()

    elif format == "only-url":
        for k in lib.keys():
            click.secho(k, fg=get_color("url"))


@bman.command(name="add", help="Adds a new entry")
@click.option(
    "--force",
    is_flag=True,
    default=False,
    required=False,
    help="Force insertion (if the url exists, replace it)",
)
@click.argument("url", type=str, required=True)
@click.argument("description", type=str, required=False)
@click.argument("tags", type=str, required=False)
def command_add(
    force: bool, url: str, description: str | None, tags: str | None
) -> None:
    lib = _load_library()
    if url in lib and not force:
        click.secho(
            "Url already exists in the library. Please, use --force"
            "to update it with the new values.",
            fg="red",
        )
        return

    data: t.Dict[str, t.Any] = {"date": datetime.now().isoformat()}

    if description:
        data["description"] = description

    if tags:
        data["tags"] = [t.strip() for t in tags.split(",")]

    lib[url] = data

    _save_library(lib)


@bman.command(name="rm", help="Removes an entry")
@click.argument("url", type=str, required=True)
def command_rm(url: str) -> None:
    lib = _load_library()
    if url not in lib:
        click.secho("Url not in the library.", fg="red")
        return

    del lib[url]
    _save_library(lib)


if __name__ == "__main__":
    bman()
