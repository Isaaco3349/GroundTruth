"""CLI entrypoint."""

import uuid

import typer
from rich.console import Console

from groundtruth.agent.loop import run_task

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    task: str | None = typer.Option(None, help="Task description for the agent"),
) -> None:
    if ctx.invoked_subcommand is not None:
        return
    if not task:
        console.print("Pass --task with a description.")
        raise typer.Exit(code=2)
    run_id = str(uuid.uuid4())
    record = run_task(task, run_id)
    console.print(record.model_dump_json(indent=2))


def entry() -> None:
    app()


if __name__ == "__main__":
    entry()
