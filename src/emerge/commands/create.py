from pathlib import Path

import questionary
import typer
from rich.console import Console

from emerge.core.generator import ProjectGenerator
from emerge.core.registry import (
    get_framework,
    get_frameworks_by_category,
    get_template,
    get_template_path,
)
from emerge.core.runner import run_framework


console = Console()


# ─────────────────────────────────────────────
# Emerge Theme
# ─────────────────────────────────────────────

QUESTIONARY_STYLE = questionary.Style(
    [
        # Prompt marker
        ("qmark", "fg:#FF6500 bold"),

        # Question text
        ("question", "fg:#F2F2F2 bold"),

        # Typed answer
        ("answer", "fg:#FFB52E bold"),

        # Selection pointer
        ("pointer", "fg:#FF6500 bold"),

        # Currently highlighted option
        ("highlighted", "fg:#FFB52E bold"),

        # Selected items
        ("selected", "fg:#56C8FF bold"),

        # Normal option text
        ("text", "fg:#D8D8D8"),

        # Instructions
        ("instruction", "fg:#8F8F8F"),

        # Disabled options
        ("disabled", "fg:#666666"),
    ]
)

# ─────────────────────────────────────────────
# Project Types
# ─────────────────────────────────────────────

PROJECT_TYPES = {
    "Web": "web",
    "Data / ML": "data",
    "Mobile": "mobile",
    "CLI": "cli",
}


# ─────────────────────────────────────────────
# Project Type Selection
# ─────────────────────────────────────────────

def choose_project_type() -> str:
    """Prompt the user to choose a project type."""

    choice = questionary.select(
        "What do you want to create?",
        choices=[
            questionary.Choice(
                label,
                value=value,
            )
            for label, value in PROJECT_TYPES.items()
        ],
        style=QUESTIONARY_STYLE,
    ).ask()

    if choice is None:
        raise typer.Exit()

    return choice


# ─────────────────────────────────────────────
# Framework Selection
# ─────────────────────────────────────────────

def choose_framework(project_type: str) -> str:
    """Prompt the user to choose a framework."""

    frameworks = get_frameworks_by_category(project_type)

    if not frameworks:
        console.print(
            f"[bold red]No frameworks available for "
            f"{project_type}.[/bold red]"
        )
        raise typer.Exit(code=1)

    choice = questionary.select(
        "Choose a framework",
        choices=[
            questionary.Choice(
                framework.name,
                value=framework.slug,
            )
            for framework in frameworks
        ],
        style=QUESTIONARY_STYLE,
    ).ask()

    if choice is None:
        raise typer.Exit()

    return choice


# ─────────────────────────────────────────────
# Project Name
# ─────────────────────────────────────────────

def choose_project_name() -> str:
    """Prompt the user for a project name."""

    name = questionary.text(
        "Project name",
        style=QUESTIONARY_STYLE,
    ).ask()

    if name is None:
        raise typer.Exit()

    name = name.strip()

    if not name:
        console.print(
            "[bold red]Project name cannot be empty.[/bold red]"
        )
        raise typer.Exit(code=1)

    return name


# ─────────────────────────────────────────────
# Create Command
# ─────────────────────────────────────────────

def create(
    project_type: str | None = typer.Argument(
        None,
        help="Type of project to create.",
    ),
    name: str | None = typer.Argument(
        None,
        help="Name of the project.",
    ),
):
    """Create a new project."""

    # ─────────────────────────────────────────
    # Project Type
    # ─────────────────────────────────────────

    if project_type is None:
        project_type = choose_project_type()

    project_type = project_type.lower()

    # ─────────────────────────────────────────
    # Project Name
    # ─────────────────────────────────────────

    if name is None:
        name = choose_project_name()

    # ─────────────────────────────────────────
    # Framework
    # ─────────────────────────────────────────

    framework = None

    if project_type == "web":
        framework_slug = choose_framework(project_type)

        framework = get_framework(framework_slug)

        if framework is None:
            console.print(
                "[bold red]"
                "Selected framework could not be found."
                "[/bold red]"
            )
            raise typer.Exit(code=1)

    # ─────────────────────────────────────────
    # Output Path
    # ─────────────────────────────────────────

    output_path = Path.cwd() / name

    if output_path.exists():
        console.print(
            f"[bold red]Error:[/bold red] "
            f"Directory '{name}' already exists."
        )
        raise typer.Exit(code=1)

    # ─────────────────────────────────────────
    # Creation Header
    # ─────────────────────────────────────────

    console.print()

    console.print(
        "[bold #FF6500]"
        f"Creating {project_type} project..."
        "[/bold #FF6500]"
    )

    console.print()

    # ─────────────────────────────────────────
    # Framework Project
    # ─────────────────────────────────────────

    if framework is not None:

        console.print(
            "[bold]Framework:[/bold] "
            f"[#56C8FF]{framework.name}[/#56C8FF]"
        )

        console.print()

        run_framework(
            framework=framework,
            name=name,
        )

    # ─────────────────────────────────────────
    # Emerge Template Project
    # ─────────────────────────────────────────

    else:

        template_slug = f"{project_type}-basic"

        template = get_template(template_slug)

        if template is None:
            console.print(
                f"[bold red]No template available for "
                f"{project_type}.[/bold red]"
            )
            raise typer.Exit(code=1)

        template_path = get_template_path(template)

        generator = ProjectGenerator(template_path)

        generator.generate(
            output_path=output_path,
            context={
                "project_name": name,
            },
        )

    # ─────────────────────────────────────────
    # Success
    # ─────────────────────────────────────────

    console.print()

    console.print(
        "[bold #FF6500]"
        "✓ Project emerged successfully!"
        "[/bold #FF6500]"
    )

    console.print()

    console.print(
        f"  cd {name}"
    )

    if framework is not None:
        console.print(
            "  npm run dev"
        )

    console.print()