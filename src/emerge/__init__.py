import typer

from emerge.commands.create import create
from emerge.ui.banner import show_banner


app = typer.Typer(
    name="emerge",
    help="From idea to project.",
    add_completion=False,
    invoke_without_command=True,
)


app.command(name="create")(create)


@app.callback()
def main(ctx: typer.Context):
    """Emerge — From idea to project."""

    if ctx.invoked_subcommand is None:
        show_banner()


if __name__ == "__main__":
    app()