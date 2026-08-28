from dataclasses import dataclass
from pathlib import Path


# ─────────────────────────────────────────────
# Template
# ─────────────────────────────────────────────

@dataclass(frozen=True)
class Template:
    name: str
    slug: str
    category: str
    description: str
    path: str


# ─────────────────────────────────────────────
# Framework
# ─────────────────────────────────────────────

@dataclass(frozen=True)
class Framework:
    name: str
    slug: str
    category: str
    description: str
    command: str
    package_managers: tuple[str, ...]


# ─────────────────────────────────────────────
# Templates
# ─────────────────────────────────────────────

TEMPLATES = [
    Template(
        name="Basic Web Project",
        slug="web-basic",
        category="web",
        description="A minimal web project.",
        path="web/basic",
    ),

    Template(
        name="Basic Data / ML Project",
        slug="data-basic",
        category="data",
        description="A minimal data and machine learning project.",
        path="data/basic",
    ),

    Template(
        name="Basic Mobile Project",
        slug="mobile-basic",
        category="mobile",
        description="A minimal mobile project.",
        path="mobile/basic",
    ),

    Template(
        name="Basic CLI Project",
        slug="cli-basic",
        category="cli",
        description="A minimal command-line project.",
        path="cli/basic",
    ),
]


# ─────────────────────────────────────────────
# Frameworks
# ─────────────────────────────────────────────

FRAMEWORKS = [
    # ─────────────────────────────────────────
    # Web
    # ─────────────────────────────────────────

    Framework(
        name="React",
        slug="react",
        category="web",
        description="React application powered by Vite.",
        command=(
            "npm create vite@latest {name} "
            "-- --template react "
            "--no-interactive "
            "--no-immediate"
        ),
        package_managers=(
            "npm",
            "pnpm",
            "yarn",
            "bun",
        ),
    ),

    Framework(
        name="Next.js",
        slug="nextjs",
        category="web",
        description="Full-stack React framework.",
        command=(
            "npx create-next-app@latest {name}"
            " --no-install"
            " --eslint"
            " --src-dir"
            " --app"
        ),
        package_managers=(
            "npm",
            "pnpm",
            "yarn",
            "bun",
        ),
    ),

    Framework(
        name="Vue",
        slug="vue",
        category="web",
        description="Progressive JavaScript framework.",
        command=(
            "npm create vue@latest {name}"
        ),
        package_managers=(
            "npm",
            "pnpm",
            "yarn",
            "bun",
        ),
    ),

    Framework(
        name="Angular",
        slug="angular",
        category="web",
        description="Full-featured web application framework.",
        command=(
            "npx @angular/cli@latest new {name}"
            " --routing"
            " --style=css"
        ),
        package_managers=(
            "npm",
            "pnpm",
            "yarn",
            "bun",
        ),
    ),

    Framework(
        name="SvelteKit",
        slug="sveltekit",
        category="web",
        description="Svelte framework for building modern web applications.",
        command=(
            "npx sv create {name}"
        ),
        package_managers=(
            "npm",
            "pnpm",
            "yarn",
            "bun",
        ),
    ),
]


# ─────────────────────────────────────────────
# Template Functions
# ─────────────────────────────────────────────

def get_template(slug: str) -> Template | None:
    """Find a template by slug."""

    slug = slug.lower()

    for template in TEMPLATES:
        if template.slug == slug:
            return template

    return None


def list_templates() -> list[Template]:
    """Return all available templates."""

    return TEMPLATES


def get_template_path(template: Template) -> Path:
    """Return the filesystem path of a template."""

    project_root = Path(__file__).resolve().parents[3]

    return project_root / "templates" / template.path


# ─────────────────────────────────────────────
# Framework Functions
# ─────────────────────────────────────────────

def get_framework(slug: str) -> Framework | None:
    """Find a framework by slug."""

    slug = slug.lower()

    for framework in FRAMEWORKS:
        if framework.slug == slug:
            return framework

    return None


def get_frameworks_by_category(
    category: str,
) -> list[Framework]:
    """Return frameworks belonging to a category."""

    category = category.lower()

    return [
        framework
        for framework in FRAMEWORKS
        if framework.category == category
    ]


def list_frameworks() -> list[Framework]:
    """Return all available frameworks."""

    return FRAMEWORKS