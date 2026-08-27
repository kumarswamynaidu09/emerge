from rich.console import Group, Text
from rich.panel import Panel
from rich.table import Table

from emerge.ui.theme import console


# ─────────────────────────────────────────────
# Emerge Logo
# ─────────────────────────────────────────────

LINES = [
    " ███████╗███╗   ███╗███████╗██████╗   ██████╗ ███████╗",
    " ██╔════╝████╗ ████║██╔════╝██╔══██╗ ██╔════╝ ██╔════╝",
    " █████╗  ██╔████╔██║█████╗  ██████╔╝ ██║  ███╗█████╗  ",
    " ██╔══╝  ██║╚██╔╝██║██╔══╝  ██╔══██╗ ██║   ██║██╔══╝  ",
    " ███████╗██║ ╚═╝ ██║███████╗██║  ██║ ╚██████╔╝███████╗",
    " ╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝  ╚═════╝╚══════╝",
]

LOGO_COLORS = [
    "#FFB52E",
    "#FFA31A",
    "#FF8F0A",
    "#FF7A00",
    "#FF6500",
    "#E95500",
]

TAGLINE = "◆  FROM IDEA TO PROJECT  ◆"


# ─────────────────────────────────────────────
# Usage
# ─────────────────────────────────────────────

USAGE = [
    ("emerge create <type> <name>", "create a new project"),
    ("emerge list", "list available templates"),
    ("emerge search <query>", "search templates"),
    ("emerge info <template>", "show template information"),
    ("emerge doctor", "check environment"),
    ("emerge update", "update Emerge CLI"),
    ("emerge --help", "show help"),
]


# ─────────────────────────────────────────────
# Available Project Types
# ─────────────────────────────────────────────

CATEGORIES = [
    ("◈", "WEB", "Web applications", "#FF6500"),
    ("◆", "DATA / ML", "Data & ML projects", "#FF8A33"),
    ("▣", "MOBILE", "Mobile applications", "#FF9A45"),
    (">_", "CLI", "Command-line tools", "#FFB52E"),
]


def build_logo() -> Group:
    """Build the Emerge logo and tagline."""

    logo_lines = []

    for line, color in zip(LINES, LOGO_COLORS):
        text = Text(
            line,
            style=f"bold {color}",
        )
        logo_lines.append(text)

    # Small separation before tagline.
    logo_lines.append(Text(" "))

    logo_lines.append(
        Text(
            TAGLINE,
            style="bold #FF8A33",
            justify="center",
        )
    )

    return Group(*logo_lines)


def build_usage() -> Group:
    """Build the usage section."""

    content = [
        Text(
            "USAGE",
            style="bold #FF8A33",
        )
    ]

    for command, description in USAGE:
        line = Text()

        line.append(
            f"  {command:<34}",
            style="bold #FF8A33",
        )

        line.append(
            description,
            style="#A8A8A8",
        )

        content.append(line)

    return Group(*content)


def build_categories() -> Group:
    """Build the available project types section."""

    content = [
        Text(
            "AVAILABLE TYPES",
            style="bold #FF8A33",
        ),
        Text(""),
    ]

    table = Table(
        show_header=False,
        show_edge=False,
        box=None,
        expand=True,
        padding=(0, 2),
    )

    for _ in CATEGORIES:
        table.add_column(
            justify="center",
            no_wrap=True,
        )

    icons = []
    names = []
    descriptions = []

    for icon, name, description, color in CATEGORIES:
        icons.append(
            Text(
                icon,
                style=f"bold {color}",
            )
        )

        names.append(
            Text(
                name,
                style=f"bold {color}",
            )
        )

        descriptions.append(
            Text(
                description,
                style="#8F8F8F",
            )
        )

    table.add_row(*icons)
    table.add_row(*names)
    table.add_row(*descriptions)

    content.append(table)

    return Group(*content)


def build_footer() -> Text:
    """Build the bottom command prompt."""

    footer = Text()

    footer.append(
        "› ",
        style="bold #FF6500",
    )

    footer.append(
        " " * 28,
    )

    footer.append(
        "v0.1.0",
        style="#777777",
    )

    return footer


def show_banner() -> None:
    """Display the complete Emerge home screen."""

    body = Group(
        build_logo(),
        Text(""),
        build_usage(),
        Text(""),
        build_categories(),
        Text(""),
        build_footer(),
    )

    console.print()

    console.print(
        Panel(
            body,
            border_style="#FF6500",
            padding=(1, 4),
            expand=False,
            title="[#FF8A33]◆[/#FF8A33]",
            title_align="center",
        )
    )

    console.print()