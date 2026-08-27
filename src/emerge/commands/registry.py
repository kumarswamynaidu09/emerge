from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    name: str
    slug: str
    category: str
    description: str


TEMPLATES = [
    Template(
        name="Web",
        slug="web",
        category="web",
        description="Web application projects",
    ),
    Template(
        name="Data / ML",
        slug="data",
        category="data",
        description="Data science and machine learning projects",
    ),
    Template(
        name="Mobile",
        slug="mobile",
        category="mobile",
        description="Mobile application projects",
    ),
    Template(
        name="CLI",
        slug="cli",
        category="cli",
        description="Command-line application projects",
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