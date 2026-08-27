from pathlib import Path

import typer
from rich.console import Console

from emerge.core.generator import ProjectGenerator
from emerge.core.registry import get_template, get_template_path


console = Console()


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
    """Create a new project."""

    template_slug = f"{project_type}-basic"
    template = get_template(template_slug)

    if template is None:
        console.print(
            f"[bold red]Unknown project type:[/bold red] {project_type}"
        )
        console.print(
            "[bold]Available types:[/bold] web"
        )
        raise typer.Exit(code=1)

    output_path = Path.cwd() / name

    if output_path.exists():
        console.print(
            f"[bold red]Error:[/bold red] "
            f"Directory '{name}' already exists."
        )
        raise typer.Exit(code=1)

    template_path = get_template_path(template)

    console.print()
    console.print(
        f"[bold #FF6500]Creating {project_type} project...[/bold #FF6500]"
    )
    console.print()

    generator = ProjectGenerator(template_path)

    generator.generate(
        output_path=output_path,
        context={
            "project_name": name,
        },
    )

    console.print(
        "[bold #FF6500]✓ Project emerged successfully![/bold #FF6500]"
    )
    console.print()
    console.print(f"  cd {name}")
    console.print()