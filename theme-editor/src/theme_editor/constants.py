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
APP_ICON_PATH = PROJECT_ROOT / "src" / "theme_editor" / "assets" / "icon.ico"
