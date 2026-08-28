from pathlib import Path

import questionary
import typer
from rich.console import Console
from emerge.core.coderabbit import setup_coderabbit

from emerge.core.generator import ProjectGenerator
from emerge.core.registry import (
    get_framework,
    get_frameworks_by_category,
    get_template,
    get_template_path,
)
from emerge.core.runner import (
    connect_github,
    detect_package_managers,
    ensure_package_manager,
    install_dependencies,
    publish_to_github,
    run_framework,
    setup_git,
)


console = Console()


# ─────────────────────────────────────────────
# Emerge Interactive Theme
# ─────────────────────────────────────────────

QUESTIONARY_STYLE = questionary.Style(
    [
        ("qmark", "fg:#FF6500 bold"),
        ("question", "fg:#F2F2F2 bold"),
        ("answer", "fg:#FFB52E bold"),
        ("pointer", "fg:#FF6500 bold"),
        ("highlighted", "fg:#FFB52E bold"),
        ("selected", "fg:#56C8FF bold"),
        ("text", "fg:#D8D8D8"),
        ("instruction", "fg:#8F8F8F"),
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
# Project Type
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
# Framework
# ─────────────────────────────────────────────

def choose_framework(
    project_type: str,
) -> str:
    """Prompt the user to choose a framework."""

    frameworks = get_frameworks_by_category(
        project_type
    )

    if not frameworks:
        console.print(
            f"[bold red]"
            f"No frameworks available for "
            f"{project_type}."
            f"[/bold red]"
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
# Package Manager
# ─────────────────────────────────────────────

def choose_package_manager(
    supported: tuple[str, ...],
) -> str:
    """Choose a package manager."""

    managers = detect_package_managers(
        supported
    )

    if not managers:
        console.print(
            "[bold red]"
            "No package managers are supported "
            "by this framework."
            "[/bold red]"
        )
        raise typer.Exit(code=1)

    labels = {
        "npm": "npm",
        "pnpm": "pnpm",
        "yarn": "Yarn",
        "bun": "Bun",
    }

    choices = []

    for manager in managers:

        label = labels.get(
            manager,
            manager,
        )

        choices.append(
            questionary.Choice(
                label,
                value=manager,
            )
        )

    choice = questionary.select(
        "Choose a package manager",
        choices=choices,
        style=QUESTIONARY_STYLE,
    ).ask()

    if choice is None:
        raise typer.Exit()

    return choice


# ─────────────────────────────────────────────
# Project Name
# ─────────────────────────────────────────────

def choose_project_name() -> str:
    """Prompt for a project name."""

    name = questionary.text(
        "Project name",
        style=QUESTIONARY_STYLE,
    ).ask()

    if name is None:
        raise typer.Exit()

    name = name.strip()

    if not name:
        console.print(
            "[bold red]"
            "Project name cannot be empty."
            "[/bold red]"
        )
        raise typer.Exit(code=1)

    return name


# ─────────────────────────────────────────────
# Create
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

        framework_slug = choose_framework(
            project_type
        )

        framework = get_framework(
            framework_slug
        )

        if framework is None:
            console.print(
                "[bold red]"
                "Selected framework could not be found."
                "[/bold red]"
            )
            raise typer.Exit(code=1)

    # ─────────────────────────────────────────
    # Project Path
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

    package_manager = None

    if framework is not None:

        console.print(
            "[bold]Framework:[/bold] "
            f"[#56C8FF]{framework.name}[/#56C8FF]"
        )

        console.print()

        package_manager = choose_package_manager(
            framework.package_managers
        )

        console.print()

        console.print(
            "[bold]Package manager:[/bold] "
            f"[#B58CFF]{package_manager}[/#B58CFF]"
        )

        # Install selected package manager
        if not ensure_package_manager(
            package_manager
        ):

            console.print(
                "[bold red]"
                f"Unable to install {package_manager}."
                "[/bold red]"
            )

            raise typer.Exit(code=1)

        console.print()

        # Scaffold project
        run_framework(
            framework=framework,
            name=name,
        )

        # Install dependencies
        console.print()

        console.print(
            "[bold #FF6500]"
            f"Installing dependencies with "
            f"{package_manager}..."
            "[/bold #FF6500]"
        )

        dependencies_installed = (
            install_dependencies(
                project_path=output_path,
                package_manager=package_manager,
            )
        )

        if dependencies_installed:

            console.print(
                "[bold #56C8FF]"
                "✓ Dependencies installed"
                "[/bold #56C8FF]"
            )

        else:

            console.print(
                "[bold red]"
                "✗ Dependency installation failed."
                "[/bold red]"
            )

            raise typer.Exit(code=1)

    # ─────────────────────────────────────────
    # Emerge Template Project
    # ─────────────────────────────────────────

    else:

        template_slug = (
            f"{project_type}-basic"
        )

        template = get_template(
            template_slug
        )

        if template is None:
            console.print(
                f"[bold red]"
                f"No template available for "
                f"{project_type}."
                f"[/bold red]"
            )
            raise typer.Exit(code=1)

        template_path = get_template_path(
            template
        )

        generator = ProjectGenerator(
            template_path
        )

        generator.generate(
            output_path=output_path,
            context={
                "project_name": name,
            },
        )

    # ─────────────────────────────────────────
    # Git
    # ─────────────────────────────────────────

    console.print()

    git_enabled = questionary.confirm(
        "Initialize Git?",
        default=True,
        style=QUESTIONARY_STYLE,
    ).ask()

    if git_enabled is None:
        raise typer.Exit()

    git_initialized = False

    if git_enabled:

        console.print()

        console.print(
            "[bold #FF6500]"
            "Setting up Git..."
            "[/bold #FF6500]"
        )

        git_initialized = setup_git(
            output_path
        )

        if git_initialized:

            console.print(
                "[bold #56C8FF]"
                "✓ Git initialized"
                "[/bold #56C8FF]"
            )

            console.print(
                "[bold #56C8FF]"
                "✓ Initial commit created"
                "[/bold #56C8FF]"
            )

        else:

            console.print(
                "[bold yellow]"
                "Git setup was skipped or failed."
                "[/bold yellow]"
            )

    # ─────────────────────────────────────────
    # GitHub
    # ─────────────────────────────────────────

    github_url = None

    if git_initialized:

        console.print()

        publish = questionary.confirm(
            "Publish to GitHub?",
            default=True,
            style=QUESTIONARY_STYLE,
        ).ask()

        if publish is None:
            raise typer.Exit()

        if publish:

            console.print()

            console.print(
                "[bold #FF6500]"
                "Checking GitHub..."
                "[/bold #FF6500]"
            )

            if connect_github():

                console.print(
                    "[bold #56C8FF]"
                    "✓ GitHub account connected"
                    "[/bold #56C8FF]"
                )

                visibility = questionary.select(
                    "Repository visibility",
                    choices=[
                        questionary.Choice(
                            "Public",
                            value=False,
                        ),
                        questionary.Choice(
                            "Private",
                            value=True,
                        ),
                    ],
                    style=QUESTIONARY_STYLE,
                ).ask()

                if visibility is None:
                    raise typer.Exit()

                console.print()

                console.print(
                    "[bold #FF6500]"
                    "Creating GitHub repository..."
                    "[/bold #FF6500]"
                )

                github_url = (
                    publish_to_github(
                        project_path=output_path,
                        repository_name=name,
                        private=visibility,
                    )
                )

                if github_url:

                    console.print(
                        "[bold #56C8FF]"
                        "✓ Repository created"
                        "[/bold #56C8FF]"
                    )

                    console.print(
                        "[bold #56C8FF]"
                        "✓ Project pushed to GitHub"
                        "[/bold #56C8FF]"
                    )

                else:

                    console.print(
                        "[bold yellow]"
                        "✗ GitHub publishing failed."
                        "[/bold yellow]"
                    )

            else:

                console.print(
                    "[bold yellow]"
                    "GitHub setup was skipped or failed."
                    "[/bold yellow]"
                )
    # ─────────────────────────────────────────
    # CodeRabbit
    # ─────────────────────────────────────────

    if github_url:
        setup_coderabbit()
    # ─────────────────────────────────────────
    # Final Result
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

        if package_manager == "npm":
            console.print(
                "  npm run dev"
            )

        elif package_manager == "pnpm":
            console.print(
                "  pnpm dev"
            )

        elif package_manager == "yarn":
            console.print(
                "  yarn dev"
            )

        elif package_manager == "bun":
            console.print(
                "  bun dev"
            )

    if github_url:

        console.print()

        console.print(
            f"  GitHub: {github_url}"
        )

    console.print()