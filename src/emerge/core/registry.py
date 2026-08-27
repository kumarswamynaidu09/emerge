from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Template:
    name: str
    slug: str
    category: str
    description: str
    path: str

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


def get_template(slug: str) -> Template | None:
    """Find a template by its slug."""

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