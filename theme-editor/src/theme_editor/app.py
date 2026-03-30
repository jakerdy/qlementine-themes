from __future__ import annotations

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .constants import APP_ICON_PATH, APP_NAME, APP_USER_MODEL_ID
from .main_window import ThemeEditorWindow
from .theme_utils import ensure_qlementine_style


def main() -> int:
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)

    app = QApplication(sys.argv)
    app.setOrganizationName("Qlementine Themes")
    app.setApplicationName(APP_NAME)
    ensure_qlementine_style(app)
    if APP_ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(APP_ICON_PATH)))

    window = ThemeEditorWindow()
    if APP_ICON_PATH.exists():
        window.setWindowIcon(QIcon(str(APP_ICON_PATH)))
    window.show()
    return app.exec()
