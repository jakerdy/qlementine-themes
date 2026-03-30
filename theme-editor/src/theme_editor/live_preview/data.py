from __future__ import annotations

from PySide6.QtCore import QStringListModel
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHeaderView,
    QListView,
    QPlainTextEdit,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTreeView,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


def build_data_content(parent: QWidget, layout: QGridLayout) -> None:
    overview_group = QGroupBox("Overview table", parent)
    overview_layout = QVBoxLayout(overview_group)
    overview_layout.setContentsMargins(12, 12, 12, 12)
    overview_layout.setSpacing(10)
    preview_table = QTableWidget(5, 4, overview_group)
    preview_table.setHorizontalHeaderLabels(["State", "Tokens", "Updated", "Owner"])
    rows = [
        ("Ready", "24", "just now", "UI"),
        ("Warnings", "3", "2 min ago", "Docs"),
        ("Errors", "0", "today", "Build"),
        ("Disabled", "8", "today", "States"),
        ("Pending", "2", "tomorrow", "Review"),
    ]
    for row_index, row_values in enumerate(rows):
        for column_index, value in enumerate(row_values):
            preview_table.setItem(row_index, column_index, QTableWidgetItem(value))
    preview_table.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch
    )
    preview_table.verticalHeader().setVisible(False)
    overview_layout.addWidget(preview_table)

    models_group = QGroupBox("Model/View surfaces", parent)
    models_layout = QGridLayout(models_group)
    models_layout.setContentsMargins(12, 12, 12, 12)
    models_layout.setHorizontalSpacing(10)
    models_layout.setVerticalSpacing(10)
    table_view = QTableView(models_group)
    table_model = QStandardItemModel(4, 3, table_view)
    table_model.setHorizontalHeaderLabels(["Palette", "Value", "Status"])
    for row_index, row_values in enumerate(
        [
            ("Primary", "#1890ff", "ready"),
            ("Secondary", "#404040", "ready"),
            ("Error", "#e96b72", "checked"),
            ("Success", "#2bb5a0", "checked"),
        ]
    ):
        for column_index, value in enumerate(row_values):
            table_model.setItem(row_index, column_index, QStandardItem(value))
    table_view.setModel(table_model)
    table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    models_layout.addWidget(table_view, 0, 0)
    list_view = QListView(models_group)
    list_view.setModel(
        QStringListModel(
            [
                "Theme loaded from repository preset",
                "Common defaults merged from _common_.json",
                "Preview widgets repainted",
                "Color overrides ready for export",
                "No validation errors detected",
            ],
            list_view,
        )
    )
    models_layout.addWidget(list_view, 0, 1)

    details_group = QGroupBox("Hierarchy and logs", parent)
    details_layout = QGridLayout(details_group)
    details_layout.setContentsMargins(12, 12, 12, 12)
    details_layout.setHorizontalSpacing(10)
    details_layout.setVerticalSpacing(10)
    tree_view = QTreeView(details_group)
    tree_model = QStandardItemModel(tree_view)
    tree_model.setHorizontalHeaderLabels(["Component", "State"])
    appearance_item = QStandardItem("Appearance")
    appearance_item.appendRow([QStandardItem("Corners"), QStandardItem("6 px")])
    appearance_item.appendRow([QStandardItem("Spacing"), QStandardItem("Comfortable")])
    appearance_item.appendRow([QStandardItem("Contrast"), QStandardItem("Balanced")])
    widgets_item = QStandardItem("Widgets")
    widgets_item.appendRow([QStandardItem("Buttons"), QStandardItem("Ready")])
    widgets_item.appendRow([QStandardItem("Inputs"), QStandardItem("Ready")])
    widgets_item.appendRow([QStandardItem("Views"), QStandardItem("Previewed")])
    tree_model.appendRow([appearance_item, QStandardItem("Configured")])
    tree_model.appendRow([widgets_item, QStandardItem("Previewed")])
    tree_view.setModel(tree_model)
    tree_view.expandAll()
    details_layout.addWidget(tree_view, 0, 0)
    tree_widget = QTreeWidget(details_group)
    tree_widget.setHeaderLabels(["Asset", "State"])
    root = QTreeWidgetItem(["Exports", "Ready"])
    root.addChild(QTreeWidgetItem(["Gallery PNG", "Up to date"]))
    root.addChild(QTreeWidgetItem(["Theme JSON", "Writable"]))
    tree_widget.addTopLevelItem(root)
    tree_widget.addTopLevelItem(QTreeWidgetItem(["Validation", "Passed"]))
    tree_widget.expandAll()
    details_layout.addWidget(tree_widget, 0, 1)
    activity_log = QPlainTextEdit(details_group)
    activity_log.setPlainText(
        "Recent checks:\n"
        "- Focus ring visible on inputs\n"
        "- Disabled foreground remains legible\n"
        "- Table headers inherit accent-neutral contrast"
    )
    activity_log.setMaximumHeight(120)
    details_layout.addWidget(activity_log, 1, 0, 1, 2)

    layout.addWidget(overview_group, 0, 0)
    layout.addWidget(models_group, 0, 1)
    layout.addWidget(details_group, 1, 0, 1, 2)
    layout.setColumnStretch(0, 11)
    layout.setColumnStretch(1, 10)
    layout.setRowStretch(1, 1)