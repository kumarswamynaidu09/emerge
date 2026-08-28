import os
import shutil
import subprocess
from pathlib import Path

import questionary

from emerge.core.registry import Framework


# ─────────────────────────────────────────────
# Prompt Theme
# ─────────────────────────────────────────────

GIT_STYLE = questionary.Style(
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
# Framework Runner
# ─────────────────────────────────────────────

def run_framework(
    framework: Framework,
    name: str,
) -> None:
    """Run the framework scaffolding command."""

    command = framework.command.format(
        name=name
    )

    subprocess.run(
        command,
        shell=True,
        check=True,
    )


# ─────────────────────────────────────────────
# Package Managers
# ─────────────────────────────────────────────

PACKAGE_MANAGER_COMMANDS = {
    "npm": "npm install",
    "pnpm": "pnpm install",
    "yarn": "yarn install",
    "bun": "bun install",
}


PACKAGE_MANAGER_INSTALL_COMMANDS = {
    "pnpm": "npm install -g pnpm",
    "yarn": "npm install -g yarn",
    "bun": (
        'powershell -ExecutionPolicy Bypass '
        '-Command "irm bun.sh/install.ps1 | iex"'
    ),
}


# ─────────────────────────────────────────────
# Package Manager Paths
# ─────────────────────────────────────────────

def get_package_manager_path(
    manager: str,
) -> str | None:
    """
    Find the executable for a package manager.

    This handles Windows installations where the
    executable may not yet be available through PATH.
    """

    # Normal PATH lookup
    executable = shutil.which(manager)

    if executable:
        return executable

    # Windows-specific locations
    if os.name == "nt":

        home = Path.home()

        candidates = {
            "bun": [
                home / ".bun" / "bin" / "bun.exe",
            ],
            "pnpm": [
                home / "AppData" / "Roaming" / "npm" / "pnpm.cmd",
                home / "AppData" / "Local" / "pnpm" / "pnpm.exe",
            ],
            "yarn": [
                home / "AppData" / "Roaming" / "npm" / "yarn.cmd",
            ],
            "npm": [
                home / "AppData" / "Roaming" / "npm" / "npm.cmd",
            ],
        }

        for candidate in candidates.get(
            manager,
            [],
        ):
            if candidate.exists():
                return str(candidate)

    return None


def package_manager_available(
    manager: str,
) -> bool:
    """Check whether a package manager is installed."""

    return (
        get_package_manager_path(manager)
        is not None
    )


def detect_package_managers(
    supported: tuple[str, ...],
) -> list[str]:
    """
    Return all package managers supported
    by the selected framework.
    """

    return [
        manager
        for manager in supported
        if manager in PACKAGE_MANAGER_COMMANDS
    ]


# ─────────────────────────────────────────────
# Package Manager Installation
# ─────────────────────────────────────────────

def install_package_manager(
    manager: str,
) -> bool:
    """Install a package manager."""

    command = PACKAGE_MANAGER_INSTALL_COMMANDS.get(
        manager
    )

    if command is None:
        return False

    try:

        result = subprocess.run(
            command,
            shell=True,
            check=False,
        )

        if result.returncode != 0:
            return False

        # Give Windows a moment to finish writing
        # the executable.
        executable = get_package_manager_path(
            manager
        )

        if executable:
            return True

        # Bun installer may successfully install
        # while PATH remains unchanged.
        if manager == "bun":

            bun_path = (
                Path.home()
                / ".bun"
                / "bin"
                / "bun.exe"
            )

            if bun_path.exists():
                return True

        return False

    except FileNotFoundError:
        return False


def ensure_package_manager(
    manager: str,
) -> bool:
    """Ensure the selected package manager exists."""

    # Already installed
    if package_manager_available(manager):
        return True

    install = questionary.confirm(
        f"{manager} is not installed. "
        f"Install it now?",
        default=True,
        style=GIT_STYLE,
    ).ask()

    if install is None or not install:
        return False

    if not install_package_manager(manager):
        return False

    # Check again using known installation paths.
    return package_manager_available(manager)


# ─────────────────────────────────────────────
# Dependency Installation
# ─────────────────────────────────────────────

def install_dependencies(
    project_path: Path,
    package_manager: str,
) -> bool:
    """Install project dependencies."""

    executable = get_package_manager_path(
        package_manager
    )

    if executable is None:
        return False

    try:

        if package_manager == "npm":

            command = [
                executable,
                "install",
            ]

        elif package_manager == "pnpm":

            command = [
                executable,
                "install",
            ]

        elif package_manager == "yarn":

            command = [
                executable,
                "install",
            ]

        elif package_manager == "bun":

            command = [
                executable,
                "install",
            ]

        else:
            return False

        subprocess.run(
            command,
            cwd=project_path,
            check=True,
        )

        return True

    except subprocess.CalledProcessError:
        return False

    except FileNotFoundError:
        return False


# ─────────────────────────────────────────────
# Git
# ─────────────────────────────────────────────

def git_available() -> bool:
    """Return True if Git is available."""

    return shutil.which("git") is not None


def install_git() -> bool:
    """Install Git on Windows using WinGet."""

    if shutil.which("winget") is None:
        return False

    result = subprocess.run(
        [
            "winget",
            "install",
            "--id",
            "Git.Git",
            "--exact",
            "--source",
            "winget",
        ],
        check=False,
    )

    return result.returncode == 0


def initialize_git(
    project_path: Path,
) -> bool:
    """Initialize Git and create the initial commit."""

    try:

        subprocess.run(
            ["git", "init"],
            cwd=project_path,
            check=True,
        )

        subprocess.run(
            ["git", "add", "."],
            cwd=project_path,
            check=True,
        )

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "Initial commit",
            ],
            cwd=project_path,
            check=True,
        )

        return True

    except subprocess.CalledProcessError:
        return False

    except FileNotFoundError:
        return False


def setup_git(
    project_path: Path,
) -> bool:
    """Install Git if necessary and initialize the repository."""

    if not git_available():

        install = questionary.confirm(
            "Git was not found. "
            "Install Git now?",
            default=True,
            style=GIT_STYLE,
        ).ask()

        if install is None or not install:
            return False

        if not install_git():
            return False

        git_candidates = [
            Path(
                r"C:\Program Files\Git\cmd\git.exe"
            ),
            Path(
                r"C:\Program Files\Git\bin\git.exe"
            ),
        ]

        git_executable = next(
            (
                path
                for path in git_candidates
                if path.exists()
            ),
            None,
        )

        if git_executable is None:
            return False

        try:

            subprocess.run(
                [str(git_executable), "init"],
                cwd=project_path,
                check=True,
            )

            subprocess.run(
                [str(git_executable), "add", "."],
                cwd=project_path,
                check=True,
            )

            subprocess.run(
                [
                    str(git_executable),
                    "commit",
                    "-m",
                    "Initial commit",
                ],
                cwd=project_path,
                check=True,
            )

            return True

        except subprocess.CalledProcessError:
            return False

        except FileNotFoundError:
            return False

    return initialize_git(project_path)


# ─────────────────────────────────────────────
# GitHub CLI
# ─────────────────────────────────────────────

def github_available() -> bool:
    """Return True if GitHub CLI is available."""

    return shutil.which("gh") is not None


def install_github_cli() -> bool:
    """Install GitHub CLI using WinGet."""

    if shutil.which("winget") is None:
        return False

    result = subprocess.run(
        [
            "winget",
            "install",
            "--id",
            "GitHub.cli",
            "--exact",
            "--source",
            "winget",
        ],
        check=False,
    )

    return result.returncode == 0


def github_authenticated() -> bool:
    """Return True if GitHub CLI is authenticated."""

    result = subprocess.run(
        [
            "gh",
            "auth",
            "status",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    return result.returncode == 0


def connect_github() -> bool:
    """Ensure GitHub CLI exists and the user is authenticated."""

    if not github_available():

        install = questionary.confirm(
            "GitHub CLI was not found. "
            "Install it now?",
            default=True,
            style=GIT_STYLE,
        ).ask()

        if install is None or not install:
            return False

        if not install_github_cli():
            return False

        if not github_available():
            return False

    if github_authenticated():
        return True

    login = questionary.confirm(
        "GitHub account is not connected. "
        "Connect now?",
        default=True,
        style=GIT_STYLE,
    ).ask()

    if login is None or not login:
        return False

    result = subprocess.run(
        ["gh", "auth", "login"],
        check=False,
    )

    return result.returncode == 0


# ─────────────────────────────────────────────
# GitHub Repository
# ─────────────────────────────────────────────

def publish_to_github(
    project_path: Path,
    repository_name: str,
    private: bool = False,
) -> str | None:
    """Create a GitHub repository and push the project."""

    visibility = (
        "--private"
        if private
        else "--public"
    )

    result = subprocess.run(
        [
            "gh",
            "repo",
            "create",
            repository_name,
            visibility,
            "--source",
            ".",
            "--remote",
            "origin",
            "--push",
        ],
        cwd=project_path,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None

    remote = subprocess.run(
        [
            "git",
            "remote",
            "get-url",
            "origin",
        ],
        cwd=project_path,
        check=False,
        capture_output=True,
        text=True,
    )

    if remote.returncode != 0:
        return None

    url = remote.stdout.strip()

    if url.endswith(".git"):
        url = url[:-4]

    return url