from __future__ import annotations

from PySide6.QtCore import QDate, QTime, Qt
from PySide6.QtWidgets import (
    QCalendarWidget,
    QCheckBox,
    QComboBox,
    QCommandLinkButton,
    QDateEdit,
    QDoubleSpinBox,
    QFontComboBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QTextEdit,
    QTimeEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


def build_forms_content(parent: QWidget, layout: QGridLayout) -> None:
    profile_group = QGroupBox("Profile form", parent)
    profile_layout = QGridLayout(profile_group)
    profile_layout.setContentsMargins(12, 12, 12, 12)
    profile_layout.setHorizontalSpacing(10)
    profile_layout.setVerticalSpacing(10)
    profile_layout.addWidget(QLabel("Search"), 0, 0)
    profile_layout.addWidget(
        QLineEdit("Search themes, controls, icons...", profile_group), 0, 1
    )
    profile_layout.addWidget(QLabel("Password"), 1, 0)
    password_edit = QLineEdit(profile_group)
    password_edit.setText("supersafe")
    password_edit.setEchoMode(QLineEdit.EchoMode.Password)
    profile_layout.addWidget(password_edit, 1, 1)
    profile_layout.addWidget(QLabel("Mode"), 2, 0)
    mode_combo = QComboBox(profile_group)
    mode_combo.addItems(["Desktop", "Tablet", "Compact", "Presentation"])
    mode_combo.setCurrentIndex(1)
    profile_layout.addWidget(mode_combo, 2, 1)
    profile_layout.addWidget(QLabel("Zoom"), 3, 0)
    zoom_spin = QSpinBox(profile_group)
    zoom_spin.setRange(50, 200)
    zoom_spin.setSuffix("%")
    zoom_spin.setValue(125)
    profile_layout.addWidget(zoom_spin, 3, 1)
    profile_layout.addWidget(QLabel("Scale"), 4, 0)
    scale_spin = QDoubleSpinBox(profile_group)
    scale_spin.setRange(0.5, 3.0)
    scale_spin.setSingleStep(0.1)
    scale_spin.setValue(1.4)
    profile_layout.addWidget(scale_spin, 4, 1)
    profile_layout.addWidget(QLabel("Font family"), 5, 0)
    profile_layout.addWidget(QFontComboBox(profile_group), 5, 1)
    profile_layout.addWidget(QLabel("Review date"), 6, 0)
    review_date = QDateEdit(profile_group)
    review_date.setDate(QDate.currentDate())
    profile_layout.addWidget(review_date, 6, 1)
    profile_layout.addWidget(QLabel("Publish time"), 7, 0)
    publish_time = QTimeEdit(profile_group)
    publish_time.setTime(QTime(14, 30))
    profile_layout.addWidget(publish_time, 7, 1)
    profile_layout.addWidget(QLabel("Notes"), 8, 0, Qt.AlignmentFlag.AlignTop)
    notes_edit = QTextEdit(profile_group)
    notes_edit.setPlainText(
        "Theme preview workspace with richer form controls, mixed states and denser grouping."
    )
    notes_edit.setMaximumHeight(120)
    profile_layout.addWidget(notes_edit, 8, 1)

    actions_group = QGroupBox("Actions and toggles", parent)
    actions_layout = QGridLayout(actions_group)
    actions_layout.setContentsMargins(12, 12, 12, 12)
    actions_layout.setHorizontalSpacing(10)
    actions_layout.setVerticalSpacing(10)
    actions_layout.addWidget(QPushButton("Publish theme", actions_group), 0, 0)
    disabled_button = QPushButton("Disabled action", actions_group)
    disabled_button.setEnabled(False)
    actions_layout.addWidget(disabled_button, 0, 1)
    export_button = QToolButton(actions_group)
    export_button.setText("Export")
    actions_layout.addWidget(export_button, 1, 0)
    actions_layout.addWidget(QCheckBox("Live preview enabled", actions_group), 1, 1)
    selected_radio = QRadioButton("Gallery mode", actions_group)
    selected_radio.setChecked(True)
    actions_layout.addWidget(selected_radio, 2, 0)
    actions_layout.addWidget(QRadioButton("Single theme", actions_group), 2, 1)
    compact_check = QCheckBox("Use compact density", actions_group)
    compact_check.setChecked(True)
    actions_layout.addWidget(compact_check, 3, 0)
    actions_layout.addWidget(QCheckBox("Pin editor sidebar", actions_group), 3, 1)
    actions_layout.addWidget(
        QCommandLinkButton(
            "Review palette contrast",
            "Inspect disabled, hover and focus states before exporting.",
            actions_group,
        ),
        4,
        0,
        1,
        2,
    )

    calendar_group = QGroupBox("Calendar and reminders", parent)
    calendar_layout = QVBoxLayout(calendar_group)
    calendar_layout.setContentsMargins(12, 12, 12, 12)
    calendar_layout.setSpacing(10)
    calendar_layout.addWidget(QCalendarWidget(calendar_group))

    layout.addWidget(profile_group, 0, 0)
    layout.addWidget(actions_group, 0, 1)
    layout.addWidget(calendar_group, 1, 0, 1, 2)
    layout.setColumnStretch(0, 3)
    layout.setColumnStretch(1, 2)
    layout.setRowStretch(1, 1)