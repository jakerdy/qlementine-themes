from __future__ import annotations

from html import escape

from PySide6.QtWidgets import QWidget
from PySide6Qlementine import Label as ThemeLabel


def set_heading_text(label: ThemeLabel, text: str, level: str) -> None:
    label.setText(f"<{level}>{escape(text)}</{level}>")


def make_heading(text: str, level: str, parent: QWidget) -> ThemeLabel:
    label = ThemeLabel(parent)
    set_heading_text(label, text, level)
    label.setWordWrap(True)
    return label


def make_body_label(text: str, parent: QWidget) -> ThemeLabel:
    label = ThemeLabel(escape(text), parent)
    label.setWordWrap(True)
    return label