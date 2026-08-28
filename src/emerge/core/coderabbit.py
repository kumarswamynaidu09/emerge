import webbrowser

import questionary
from rich.console import Console


console = Console()


CODERABBIT_URL = "https://app.coderabbit.ai/"


CODERABBIT_STYLE = questionary.Style(
    [
        ("qmark", "fg:#FF6500 bold"),
        ("question", "fg:#F2F2F2 bold"),
        ("answer", "fg:#FFB52E bold"),
        ("pointer", "fg:#FF6500 bold"),
        ("highlighted", "fg:#FFB52E bold"),
        ("selected", "fg:#56C8FF bold"),
        ("text", "fg:#D8D8D8"),
        ("instruction", "fg:#8F8F8F"),
    ]
)


def show_coderabbit_offer() -> None:
    """Show the CodeRabbit promotion."""

    console.print()

    console.print(
        "╭─────────────── [bold #FF6500]Emerge[/bold #FF6500] ───────────────╮"
    )
    console.print(
        "│                                                              │"
    )
    console.print(
        "│  [bold #56C8FF]Your project is ready.[/bold #56C8FF]              │"
    )
    console.print(
        "│                                                              │"
    )
    console.print(
        "│  Want AI-powered code reviews?                               │"
    )
    console.print(
        "│                                                              │"
    )
    console.print(
        "│  CodeRabbit reviews pull requests,                          │"
    )
    console.print(
        "│  catches issues and gives feedback                            │"
    )
    console.print(
        "│  automatically.                                              │"
    )
    console.print(
        "│                                                              │"
    )
    console.print(
        "╰──────────────────────────────────────────────────────────────╯"
    )

    console.print()


def setup_coderabbit() -> None:
    """Offer CodeRabbit integration."""

    show_coderabbit_offer()

    choice = questionary.select(
        "Add CodeRabbit?",
        choices=[
            questionary.Choice(
                "Yes",
                value="yes",
            ),
            questionary.Choice(
                "No",
                value="no",
            ),
            questionary.Choice(
                "Learn more",
                value="learn",
            ),
        ],
        style=CODERABBIT_STYLE,
    ).ask()

    if choice is None:
        return

    if choice == "no":
        console.print()
        return

    if choice == "learn":

        console.print()
        console.print(
            "[bold #56C8FF]"
            "Opening CodeRabbit..."
            "[/bold #56C8FF]"
        )

        webbrowser.open(CODERABBIT_URL)

        console.print()
        console.print(
            "CodeRabbit: "
            f"{CODERABBIT_URL}"
        )

        console.print()

        return

    if choice == "yes":

        console.print()

        console.print(
            "[bold #FF6500]"
            "Opening CodeRabbit..."
            "[/bold #FF6500]"
        )

        console.print()

        console.print(
            "1. Sign in with GitHub"
        )

        console.print(
            "2. Select the repository you want "
            "CodeRabbit to review"
        )

        console.print(
            "3. Install & Authorize CodeRabbit"
        )

        console.print()

        webbrowser.open(CODERABBIT_URL)

        console.print(
            "[bold #56C8FF]"
            "✓ CodeRabbit setup opened in your browser."
            "[/bold #56C8FF]"
        )

        console.print()