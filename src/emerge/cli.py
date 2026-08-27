import typer
from rich.console import Console

app = typer.Typer(
    name="emerge",
    help="From idea to project.",
    add_completion=False,
)

console = Console()


@app.command()
def main():
    """Start Emerge."""
    console.print("[bold #FF6B00]EMERGE[/bold #FF6B00]")
    console.print("From idea to project.")


if __name__ == "__main__":
    app()