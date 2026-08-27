from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class ProjectGenerator:
    """Generate a project from an Emerge template."""

    def __init__(self, template_path: Path):
        self.template_path = template_path
        self.files_path = template_path / "files"

        self.environment = Environment(
            loader=FileSystemLoader(self.files_path),
            keep_trailing_newline=True,
        )

    def generate(
        self,
        output_path: Path,
        context: dict,
    ) -> None:
        """Generate all template files into the output directory."""

        output_path.mkdir(parents=True, exist_ok=True)

        for template_file in self.files_path.rglob("*"):
            if not template_file.is_file():
                continue

            relative_path = template_file.relative_to(self.files_path)

            template_name = relative_path.as_posix()
            template = self.environment.get_template(template_name)

            rendered_content = template.render(**context)

            destination = output_path / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)

            destination.write_text(
                rendered_content,
                encoding="utf-8",
            )