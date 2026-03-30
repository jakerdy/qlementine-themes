from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QCommandLinkButton,
    QGridLayout,
    QGroupBox,
    QKeySequenceEdit,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


def build_overview_content(parent: QWidget, layout: QGridLayout) -> None:
    summary_group = QGroupBox("Preview snapshot", parent)
    summary_layout = QGridLayout(summary_group)
    summary_layout.setContentsMargins(12, 12, 12, 12)
    summary_layout.setHorizontalSpacing(10)
    summary_layout.setVerticalSpacing(10)
    summary_layout.addWidget(QLabel("Current preset"), 0, 0)
    preset_edit = QLineEdit("Nord / repository preset", summary_group)
    preset_edit.setReadOnly(True)
    summary_layout.addWidget(preset_edit, 0, 1)
    summary_layout.addWidget(QLabel("Quick action"), 1, 0)
    summary_layout.addWidget(QPushButton("Export preset", summary_group), 1, 1)
    summary_layout.addWidget(QLabel("Shortcut"), 2, 0)
    summary_layout.addWidget(QKeySequenceEdit(summary_group), 2, 1)

    hero_group = QGroupBox("Primary actions", parent)
    hero_layout = QVBoxLayout(hero_group)
    hero_layout.setContentsMargins(12, 12, 12, 12)
    hero_layout.setSpacing(10)
    hero_layout.addWidget(
        QCommandLinkButton(
            "Publish theme bundle",
            "Push JSON, gallery assets and preview metadata together.",
            hero_group,
        )
    )
    hero_layout.addWidget(
        QCommandLinkButton(
            "Open review checklist",
            "Verify hover, disabled and focus colors before release.",
            hero_group,
        )
    )

    browser_group = QGroupBox("Release notes", parent)
    browser_layout = QVBoxLayout(browser_group)
    browser_layout.setContentsMargins(12, 12, 12, 12)
    browser_layout.setSpacing(10)
    browser = QTextBrowser(browser_group)
    browser.setHtml(
        "<h3>Theme Review</h3>"
        "<p>Use this panel to inspect typography, spacing, borders and semantic states.</p>"
        "<ul><li>Accent contrast</li><li>Disabled legibility</li><li>Window icon branding</li></ul>"
    )
    browser_layout.addWidget(browser)

    metrics_group = QGroupBox("Metrics", parent)
    metrics_layout = QGridLayout(metrics_group)
    metrics_layout.setContentsMargins(12, 12, 12, 12)
    metrics_layout.setHorizontalSpacing(10)
    metrics_layout.setVerticalSpacing(10)
    metrics_layout.addWidget(QLabel("Tokens"), 0, 0)
    lcd = QLCDNumber(metrics_group)
    lcd.display(128)
    metrics_layout.addWidget(lcd, 0, 1)
    metrics_layout.addWidget(QLabel("Density"), 1, 0)
    density_combo = QComboBox(metrics_group)
    density_combo.addItems(["Comfortable", "Dense", "Compact"])
    metrics_layout.addWidget(density_combo, 1, 1)
    metrics_layout.addWidget(QLabel("Pinned"), 2, 0)
    pinned = QCheckBox("Sidebar active", metrics_group)
    pinned.setChecked(True)
    metrics_layout.addWidget(pinned, 2, 1)

    layout.addWidget(summary_group, 0, 0)
    layout.addWidget(hero_group, 0, 1)
    layout.addWidget(browser_group, 1, 0)
    layout.addWidget(metrics_group, 1, 1)
    layout.setColumnStretch(0, 3)
    layout.setColumnStretch(1, 2)
    layout.setRowStretch(1, 1)