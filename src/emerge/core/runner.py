import subprocess

from emerge.core.registry import Framework


def run_framework(
    framework: Framework,
    name: str,
) -> None:
    """Run the official framework scaffolder."""

    command = framework.command.format(name=name)

    subprocess.run(
        command,
        shell=True,
        check=True,
    )