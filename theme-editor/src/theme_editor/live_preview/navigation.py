from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QScrollBar,
    QSplitter,
    QToolBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from .common import make_body_label


def build_navigation_content(parent: QWidget, layout: QGridLayout) -> None:
    toolbox_group = QGroupBox("Panels and toolbox", parent)
    toolbox_layout = QVBoxLayout(toolbox_group)
    toolbox_layout.setContentsMargins(12, 12, 12, 12)
    toolbox_layout.setSpacing(10)
    toolbox = QToolBox(toolbox_group)

    inspector_page = QWidget(toolbox)
    inspector_layout = QVBoxLayout(inspector_page)
    inspector_layout.setContentsMargins(8, 8, 8, 8)
    inspector_layout.setSpacing(8)
    inspector_layout.addWidget(QCheckBox("Show disabled states", inspector_page))
    inspector_layout.addWidget(QCheckBox("Show focus rings", inspector_page))
    inspector_layout.addWidget(QCheckBox("Lock aspect ratios", inspector_page))
    inspector_layout.addStretch(1)

    queue_page = QWidget(toolbox)
    queue_page_layout = QVBoxLayout(queue_page)
    queue_page_layout.setContentsMargins(8, 8, 8, 8)
    queue_page_layout.setSpacing(8)
    queue_list = QListWidget(queue_page)
    for text in [
        "Compile preview",
        "Render gallery",
        "Export icons",
        "Publish bundle",
    ]:
        QListWidgetItem(text, queue_list)
    queue_page_layout.addWidget(queue_list)

    toolbox.addItem(inspector_page, "Inspector")
    toolbox.addItem(queue_page, "Queue")
    toolbox_layout.addWidget(toolbox)

    split_group = QGroupBox("Split navigation", parent)
    split_layout = QVBoxLayout(split_group)
    split_layout.setContentsMargins(12, 12, 12, 12)
    split_layout.setSpacing(10)
    nested_splitter = QSplitter(Qt.Orientation.Horizontal, split_group)
    sidebar = QListWidget(nested_splitter)
    for text in ["General", "Colors", "Typography", "Views", "Exports"]:
        QListWidgetItem(text, sidebar)

    detail_panel = QWidget(nested_splitter)
    detail_layout = QVBoxLayout(detail_panel)
    detail_layout.setContentsMargins(8, 8, 8, 8)
    detail_layout.setSpacing(8)
    detail_layout.addWidget(make_body_label("Active section", detail_panel))
    detail_layout.addWidget(QLineEdit("Colors / semantic roles", detail_panel))
    tool_row = QHBoxLayout()
    for text in ["Back", "Forward", "Refresh"]:
        button = QToolButton(detail_panel)
        button.setText(text)
        tool_row.addWidget(button)
    tool_row.addStretch(1)
    detail_layout.addLayout(tool_row)
    split_layout.addWidget(nested_splitter)

    scroll_group = QGroupBox("Scrolling surfaces", parent)
    scroll_layout = QGridLayout(scroll_group)
    scroll_layout.setContentsMargins(12, 12, 12, 12)
    scroll_layout.setHorizontalSpacing(10)
    scroll_layout.setVerticalSpacing(10)
    scroll_layout.addWidget(make_body_label("Horizontal", scroll_group), 0, 0)
    horizontal_scroll = QScrollBar(Qt.Orientation.Horizontal, scroll_group)
    horizontal_scroll.setValue(40)
    scroll_layout.addWidget(horizontal_scroll, 0, 1)
    scroll_layout.addWidget(make_body_label("Vertical", scroll_group), 1, 0)
    vertical_scroll = QScrollBar(Qt.Orientation.Vertical, scroll_group)
    vertical_scroll.setValue(60)
    scroll_layout.addWidget(vertical_scroll, 1, 1, Qt.AlignmentFlag.AlignLeft)

    layout.addWidget(toolbox_group, 0, 0)
    layout.addWidget(split_group, 0, 1)
    layout.addWidget(scroll_group, 1, 0, 1, 2)
    layout.setColumnStretch(0, 2)
    layout.setColumnStretch(1, 3)
    layout.setRowStretch(0, 1)