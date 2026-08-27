from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Framework:
    name: str
    slug: str
    category: str
    command: str


@dataclass(frozen=True)
class Template:
    name: str
    slug: str
    category: str
    framework: str
    description: str
    path: str


FRAMEWORKS = [
    Framework(
        name="React",
        slug="react",
        category="web",
        command="npm create vite@latest {name} -- --template react --no-interactive --no-immediate",
    ),
    Framework(
        name="Next.js",
        slug="nextjs",
        category="web",
        command="npx create-next-app@latest {name}",
    ),
    Framework(
        name="Vue",
        slug="vue",
        category="web",
        command="npm create vue@latest {name}",
    ),
    Framework(
        name="Angular",
        slug="angular",
        category="web",
        command="npx @angular/cli@latest new {name}",
    ),
    Framework(
        name="SvelteKit",
        slug="sveltekit",
        category="web",
        command="npx sv create {name}",
    ),
]


TEMPLATES = [
    Template(
        name="Basic Web Project",
        slug="web-basic",
        category="web",
        framework="vanilla",
        description="A minimal web project.",
        path="web/basic",
    ),
]


def get_framework(slug: str) -> Framework | None:
    """Find a framework by its slug."""

    slug = slug.lower()

    for framework in FRAMEWORKS:
        if framework.slug == slug:
            return framework

    return None


def get_frameworks_by_category(category: str) -> list[Framework]:
    """Return frameworks available for a category."""

    category = category.lower()

    return [
        framework
        for framework in FRAMEWORKS
        if framework.category == category
    ]


def get_template(slug: str) -> Template | None:
    """Find a template by its slug."""

    slug = slug.lower()

    for template in TEMPLATES:
        if template.slug == slug:
            return template

    return None


def get_templates_by_category(category: str) -> list[Template]:
    """Return templates available for a category."""

    category = category.lower()

    return [
        template
        for template in TEMPLATES
        if template.category == category
    ]


def list_templates() -> list[Template]:
    """Return all available templates."""

    return TEMPLATES


def get_template_path(template: Template) -> Path:
    """Return the filesystem path of a template."""

    project_root = Path(__file__).resolve().parents[3]

    return project_root / "templates" / template.path