from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDial,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .common import make_body_label


def build_feedback_content(parent: QWidget, layout: QGridLayout) -> None:
    status_group = QGroupBox("Progress and intensity", parent)
    status_layout = QGridLayout(status_group)
    status_layout.setContentsMargins(12, 12, 12, 12)
    status_layout.setHorizontalSpacing(10)
    status_layout.setVerticalSpacing(10)
    progress_bar = QProgressBar(status_group)
    progress_bar.setRange(0, 100)
    progress_bar.setValue(72)
    status_layout.addWidget(make_body_label("Progress", status_group), 0, 0)
    status_layout.addWidget(progress_bar, 0, 1)
    queued_bar = QProgressBar(status_group)
    queued_bar.setRange(0, 100)
    queued_bar.setValue(38)
    status_layout.addWidget(make_body_label("Queue", status_group), 1, 0)
    status_layout.addWidget(queued_bar, 1, 1)
    opacity_slider = QSlider(Qt.Orientation.Horizontal, status_group)
    opacity_slider.setRange(0, 100)
    opacity_slider.setValue(58)
    status_layout.addWidget(make_body_label("Opacity", status_group), 2, 0)
    status_layout.addWidget(opacity_slider, 2, 1)
    accent_dial = QDial(status_group)
    accent_dial.setRange(0, 100)
    accent_dial.setValue(33)
    status_layout.addWidget(make_body_label("Accent", status_group), 3, 0)
    status_layout.addWidget(accent_dial, 3, 1)

    alerts_group = QGroupBox("Alerts and notes", parent)
    alerts_layout = QVBoxLayout(alerts_group)
    alerts_layout.setContentsMargins(12, 12, 12, 12)
    alerts_layout.setSpacing(10)
    alerts_layout.addWidget(
        make_body_label(
            "Success, info, warning and error colors should all stay readable here.",
            alerts_group,
        )
    )
    alerts_log = QPlainTextEdit(alerts_group)
    alerts_log.setPlainText(
        "[success] Gallery regenerated\n"
        "[info] Preview synchronized\n"
        "[warning] Contrast threshold near limit\n"
        "[error] None"
    )
    alerts_log.setMaximumHeight(140)
    alerts_layout.addWidget(alerts_log)

    queue_group = QGroupBox("Upload queue", parent)
    queue_layout = QVBoxLayout(queue_group)
    queue_layout.setContentsMargins(12, 12, 12, 12)
    queue_layout.setSpacing(10)
    queue_table = QTableWidget(4, 3, queue_group)
    queue_table.setHorizontalHeaderLabels(["File", "State", "ETA"])
    for row_index, row_values in enumerate(
        [
            ("light.json", "Done", "0s"),
            ("dark.json", "Queued", "12s"),
            ("gallery.png", "Uploading", "4s"),
            ("preview.log", "Waiting", "18s"),
        ]
    ):
        for column_index, value in enumerate(row_values):
            queue_table.setItem(row_index, column_index, QTableWidgetItem(value))
    queue_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    queue_table.verticalHeader().setVisible(False)
    queue_layout.addWidget(queue_table)
    toggles_row = QHBoxLayout()
    sticky_check = QCheckBox("Keep notifications visible", queue_group)
    sticky_check.setChecked(True)
    toggles_row.addWidget(sticky_check)
    toggles_row.addWidget(QCheckBox("Mute sounds", queue_group))
    toggles_row.addStretch(1)
    queue_layout.addLayout(toggles_row)

    states_group = QGroupBox("State matrix", parent)
    states_layout = QGridLayout(states_group)
    states_layout.setContentsMargins(12, 12, 12, 12)
    states_layout.setHorizontalSpacing(10)
    states_layout.setVerticalSpacing(10)
    ready_check = QCheckBox("Ready", states_group)
    ready_check.setChecked(True)
    states_layout.addWidget(ready_check, 0, 0)
    states_layout.addWidget(QCheckBox("Warning", states_group), 0, 1)
    ok_radio = QRadioButton("Primary", states_group)
    ok_radio.setChecked(True)
    states_layout.addWidget(ok_radio, 1, 0)
    states_layout.addWidget(QRadioButton("Alternative", states_group), 1, 1)
    disabled_toggle = QCheckBox("Disabled sample", states_group)
    disabled_toggle.setEnabled(False)
    states_layout.addWidget(disabled_toggle, 2, 0)
    states_layout.addWidget(QPushButton("Retry failed upload", states_group), 2, 1)

    layout.addWidget(status_group, 0, 0)
    layout.addWidget(alerts_group, 0, 1)
    layout.addWidget(queue_group, 1, 0)
    layout.addWidget(states_group, 1, 1)
    layout.setColumnStretch(0, 1)
    layout.setColumnStretch(1, 1)
    layout.setRowStretch(1, 1)