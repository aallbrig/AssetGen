"""assetgen — root CLI entry point.

Command hierarchy (post-restructure)::

    assetgen gen visual      → concept, blockout, model, uv, texture, rig, animate, vfx, ui
    assetgen gen audio       → sfx, music, voice
    assetgen gen scene       → physics, lighting
    assetgen gen pipeline    → workflow, batch, integrate
    assetgen gen support     → narrative, data
    assetgen gen qa          → validate, perf, style, report
    assetgen tasks           → full task tree with configured models
    assetgen jobs            → list, status, wait, cancel, clean
    assetgen models          → list, status, install
    assetgen server          → start, stop, status, config
    assetgen client          → config (show/set-server/unset-server)
    assetgen config          → list, show, set, remove, search
    assetgen upgrade         → check for and install latest release
    assetgen version         → print version info
"""

from __future__ import annotations

import logging

import typer
from rich.console import Console

from assetgen.client import context as _ctx
from assetgen.client.commands.client_cmd import app as client_app
from assetgen.client.commands.compose import app as compose_app
from assetgen.client.commands.config import app as config_app
from assetgen.client.commands.gen import app as gen_app
from assetgen.client.commands.jobs import app as jobs_app
from assetgen.client.commands.models import app as models_app
from assetgen.client.commands.server import app as server_app
from assetgen.client.commands.tasks import app as tasks_app
from assetgen.client.commands.upgrade import app as upgrade_app

console = Console(highlight=False)

app = typer.Typer(
    name="assetgen",
    help="AI-driven game asset generation pipeline.",
    no_args_is_help=True,
    add_completion=True,
    rich_markup_mode=None,
)

app.add_typer(
    gen_app, name="gen", help="Generate assets: visual · audio · scene · pipeline · support · qa"
)
app.add_typer(
    compose_app,
    name="compose",
    help="Multi-step asset pipelines: npc, weapon, prop, material, soundscape, ui-kit, environment",
)
app.add_typer(tasks_app, name="tasks", help="Browse all game dev tasks and their configured models")
app.add_typer(jobs_app, name="jobs", help="Job queue management")
app.add_typer(models_app, name="models", help="Model catalog and installation")
app.add_typer(server_app, name="server", help="Local server process management")
app.add_typer(
    client_app, name="client", help="Client configuration: server targeting and connection settings"
)
app.add_typer(config_app, name="config", help="Configure job-type → model mappings")
app.add_typer(upgrade_app, name="upgrade", help="Check for and install the latest assetgen release")


def _version_callback(value: bool) -> None:
    if value:
        from assetgen.version import format_version_string

        typer.echo(format_version_string("assetgen"))
        raise typer.Exit()


@app.callback()
def _root_callback(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable debug logging (shows server communication, model resolution, etc.)",
        is_eager=True,
    ),
    version: bool = typer.Option(  # noqa: ARG001
        None,
        "--version",
        "-V",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON to stdout.  Disables progress bars. "
        "Ideal for CI pipelines and scripting.",
    ),
    yaml_output: bool = typer.Option(
        False,
        "--yaml",
        help="Emit machine-readable YAML to stdout.  Disables progress bars. "
        "Human-friendly alternative to --json.",
    ),
    variants: int = typer.Option(
        1,
        "--variants",
        "-n",
        min=1,
        help="Submit N identical jobs (batch generation).  Use with --wait to collect all outputs.",
    ),
    quality: str = typer.Option(
        "standard",
        "--quality",
        "-q",
        help="Model quality tier: draft (fastest/smallest), standard, high (best/largest).  "
        "Maps to model size variants where available.",
    ),
    from_job: str | None = typer.Option(
        None,
        "--from-job",
        help="Chain from a completed job's outputs.  Pass the upstream job ID; "
        "its output files are forwarded as inputs to this job.",
    ),
    context: list[str] = typer.Option(
        [],
        "--context",
        help="Named context from a prior job: 'key=job_id'.  Repeatable.  "
        "Loads that job's primary text output into params['context_map']['key'] "
        "so handlers can incorporate prior narrative/lore content.",
    ),
) -> None:
    """AI-driven game asset generation pipeline."""
    if json_output:
        _ctx.set_json_mode(True)
    if yaml_output:
        _ctx.set_yaml_mode(True)
    if variants > 1:
        _ctx.set_variants(variants)
    if quality != "standard":
        _ctx.set_quality(quality)
    if from_job:
        _ctx.set_from_job(from_job)
    if context:
        _ctx.set_context_map(context)
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
            datefmt="%H:%M:%S",
        )
        # Quiet down extremely chatty libraries even in verbose mode
        for noisy in ("httpcore", "httpx", "urllib3", "hpack"):
            logging.getLogger(noisy).setLevel(logging.WARNING)
    else:
        logging.disable(logging.CRITICAL)


@app.command("version")
def version_cmd() -> None:
    """Print version information and exit."""
    from assetgen.version import format_version_string

    console.print(format_version_string("assetgen"))
