from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QGridLayout, QTabWidget, QVBoxLayout, QWidget
from PySide6Qlementine import Label as ThemeLabel

from .common import make_body_label, make_heading, set_heading_text
from .data import build_data_content
from .feedback import build_feedback_content
from .forms import build_forms_content
from .navigation import build_navigation_content
from .overview import build_overview_content


class LivePreviewWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.theme_title: ThemeLabel
        self.theme_caption: ThemeLabel
        self._build_ui()

    def set_theme_name(self, name: str) -> None:
        set_heading_text(self.theme_title, f"{name} - controls gallery", "h1")

    def set_caption(self, text: str) -> None:
        set_heading_text(self.theme_caption, text, "h4")

    def _build_ui(self) -> None:
        self.setMinimumWidth(860)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(4, 4, 15, 4)
        root_layout.setSpacing(16)

        self.theme_title = make_heading("Theme preview", "h1", self)
        self.theme_caption = make_heading(
            "PySide6 controls showcase rendered with qlementine-themes", "h4", self
        )

        root_layout.addWidget(self.theme_title)
        root_layout.addWidget(self.theme_caption)

        tabs = QTabWidget(self)
        tabs.addTab(
            self._create_tab_page(
                "Overview",
                "High-level snapshot, shortcuts and branding surfaces.",
                build_overview_content,
            ),
            "Overview",
        )
        tabs.addTab(
            self._create_tab_page(
                "Forms",
                "Dense input controls, date and time editing, and typography-sensitive widgets.",
                build_forms_content,
            ),
            "Forms",
        )
        tabs.addTab(
            self._create_tab_page(
                "Data",
                "Lists, trees, tables, and model-view heavy widgets.",
                build_data_content,
            ),
            "Data",
        )
        tabs.addTab(
            self._create_tab_page(
                "Navigation",
                "Panels, splitters, toolboxes, and scrolling surfaces.",
                build_navigation_content,
            ),
            "Navigation",
        )
        tabs.addTab(
            self._create_tab_page(
                "Feedback",
                "Progress, alerts, toggles, and state-driven controls.",
                build_feedback_content,
            ),
            "Feedback",
        )
        root_layout.addWidget(tabs, 1)

    def _create_tab_page(
        self,
        title: str,
        intro: str,
        builder: Callable[[QWidget, QGridLayout], None],
    ) -> QWidget:
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setSpacing(12)
        layout.addWidget(make_heading(title, "h2", page))

        intro_label = make_body_label(intro, page)
        layout.addWidget(intro_label)

        content = QWidget(page)
        content_layout = QGridLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setHorizontalSpacing(12)
        content_layout.setVerticalSpacing(12)
        builder(content, content_layout)
        layout.addWidget(content, 1)
        return page