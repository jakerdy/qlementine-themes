from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from .constants import JETBRAINS_MONO_FONT_PATH, OPEN_SANS_FONT_PATH


@dataclass(frozen=True)
class FontFamilies:
    ui: str
    mono: str


_font_families: FontFamilies | None = None


def _load_font_family(path: str, fallback_family: str) -> str:
    font_id = QFontDatabase.addApplicationFont(path)
    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            return families[0]
    return fallback_family


def font_families() -> FontFamilies:
    global _font_families
    if _font_families is not None:
        return _font_families

    default_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)
    fixed_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
    _font_families = FontFamilies(
        ui=_load_font_family(str(OPEN_SANS_FONT_PATH), default_font.family()),
        mono=_load_font_family(str(JETBRAINS_MONO_FONT_PATH), fixed_font.family()),
    )
    return _font_families


def install_application_fonts(app: QApplication) -> None:
    families = font_families()
    app_font = QFont(app.font())
    app_font.setFamilies([families.ui])
    app.setFont(app_font)


def monospace_font(base_font: QFont | None = None) -> QFont:
    families = font_families()
    font = QFont(base_font) if base_font is not None else QFont()
    font.setFamilies([families.mono])
    font.setStyleHint(QFont.StyleHint.Monospace)
    return font
