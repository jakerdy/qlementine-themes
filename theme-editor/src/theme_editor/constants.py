from __future__ import annotations

from pathlib import Path

APP_NAME = "Qlementine Theme Editor"
APP_VERSION = "0.1.0"
APP_AUTHOR = "JakErdy"
APP_REPOSITORY_URL = "https://github.com/jakerdy/qlementine-themes"
APP_USER_MODEL_ID = "JakErdy.QlementineThemeEditor"
PREVIOUS_PATH_SETTINGS_KEY = "previousPath"
DEFAULT_FILE_NAME = "theme.json"
DEFAULT_THEME_ID = "light"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(__file__).resolve().parents[3]
THEMES_DIR = REPO_ROOT / "themes"
ASSETS_DIR = PROJECT_ROOT / "src" / "theme_editor" / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
APP_ICON_PATH = ASSETS_DIR / "icon.ico"
OPEN_SANS_FONT_PATH = FONTS_DIR / "OpenSans-Variable.ttf"
JETBRAINS_MONO_FONT_PATH = FONTS_DIR / "JetBrainsMono-Regular.ttf"
