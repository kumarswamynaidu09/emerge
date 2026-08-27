import typer

from emerge.commands.create import create

app = typer.Typer(
    name="emerge",
    help="From idea to project.",
    add_completion=False,
)

app.command(name="create")(create)


@app.callback()
def main():
    """Emerge — From idea to project."""
    pass


if __name__ == "__main__":
    app()