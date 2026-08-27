from pathlib import Path

import typer
from rich.console import Console

from emerge.core.generator import ProjectGenerator
from emerge.core.registry import get_template, get_template_path

console = Console()


def create(
    template_slug: str = typer.Argument(
        ...,
        help="Template to use.",
    ),
    name: str = typer.Argument(
        ...,
        help="Name of the project.",
    ),
):
    """Create a new project from a template."""

    template = get_template(template_slug)

    if template is None:
        console.print(
            f"[bold red]Unknown template:[/bold red] {template_slug}"
        )
        console.print(
            "[bold]Available:[/bold] web-basic"
        )
        raise typer.Exit(code=1)

    template_path = get_template_path(template)
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
    console.print(f"[bold]Template:[/bold] {template.name}")
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