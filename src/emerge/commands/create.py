from pathlib import Path

import typer
from rich.console import Console

from emerge.core.generator import ProjectGenerator
from emerge.core.registry import get_template

console = Console()


TEMPLATE_ROOT = Path(__file__).resolve().parents[3] / "templates"


def create(
    project_type: str = typer.Argument(
        ...,
        help="Type of project to create.",
    ),
    name: str = typer.Argument(
        ...,
        help="Name of the project.",
    ),
):
    """Create a new Emerge project."""

    template = get_template(project_type)

    if template is None:
        console.print(
            f"[bold red]Unknown project type:[/bold red] {project_type}"
        )
        console.print(
            "[bold]Available:[/bold] web, data, mobile, cli"
        )
        raise typer.Exit(code=1)

    if template.slug == "web":
        template_path = TEMPLATE_ROOT / "web" / "basic"
    else:
        console.print(
            f"[yellow]No generator template exists yet for "
            f"{template.name}.[/yellow]"
        )
        raise typer.Exit(code=1)

    output_path = Path.cwd() / name

    if output_path.exists():
        console.print(
            f"[bold red]Error:[/bold red] "
            f"Directory '{name}' already exists."
        )
        raise typer.Exit(code=1)

    console.print()
    console.print("[bold #FF6B00]EMERGE[/bold #FF6B00]")
    console.print("From idea to project.")
    console.print()

    console.print(f"[bold]Creating:[/bold] {name}")
    console.print(f"[bold]Type:[/bold] {template.name}")
    console.print()

    generator = ProjectGenerator(template_path)

    generator.generate(
        output_path=output_path,
        context={
            "project_name": name,
        },
    )

    console.print(
        "[bold #FF6B00]✓ Project emerged successfully![/bold #FF6B00]"
    )
    console.print()
    console.print(f"  cd {name}")
    console.print()