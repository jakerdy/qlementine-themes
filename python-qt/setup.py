from __future__ import annotations

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


PROJECT_ROOT = Path(__file__).resolve().parent
REPO_THEMES_DIR = PROJECT_ROOT.parent / "themes"
PACKAGE_THEMES_RELATIVE_DIR = Path("src") / "jakerdy" / "qlementine_themes" / "themes"
SOURCE_PACKAGE_THEMES_DIR = PROJECT_ROOT / PACKAGE_THEMES_RELATIVE_DIR


def _theme_source_dir() -> Path:
    if SOURCE_PACKAGE_THEMES_DIR.is_dir():
        return SOURCE_PACKAGE_THEMES_DIR
    if REPO_THEMES_DIR.is_dir():
        return REPO_THEMES_DIR
    raise FileNotFoundError(
        "Theme directory not found in either the repository root or the package source tree."
    )


def _copy_theme_files(destination: Path) -> None:
    source_dir = _theme_source_dir()

    if destination.exists() and destination.is_file():
        destination.unlink()

    destination.mkdir(parents=True, exist_ok=True)
    for source_path in sorted(source_dir.glob("*.json")):
        shutil.copy2(source_path, destination / source_path.name)


class build_py(_build_py):
    def run(self) -> None:
        super().run()
        if not SOURCE_PACKAGE_THEMES_DIR.is_dir():
            _copy_theme_files(Path(self.build_lib) / "jakerdy" / "qlementine_themes" / "themes")


class sdist(_sdist):
    def make_release_tree(self, base_dir: str, files: list[str]) -> None:
        super().make_release_tree(base_dir, files)
        _copy_theme_files(Path(base_dir) / PACKAGE_THEMES_RELATIVE_DIR)


setup(
    cmdclass={
        "build_py": build_py,
        "sdist": sdist,
    }
)