from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from jakerdy.qlementine_themes import QtBinding, ThemeId, apply_theme, available_themes, load_theme

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_IMAGE_DIR = REPO_ROOT / "gallery" / "img"


@dataclass(frozen=True)
class ScreenshotJob:
    theme_id: ThemeId
    output_path: Path

    @property
    def relative_path(self) -> Path:
        try:
            return self.output_path.relative_to(REPO_ROOT)
        except ValueError:
            return self.output_path


def screenshot_jobs(
    output_dir: Path = DEFAULT_IMAGE_DIR,
    themes: Sequence[ThemeId] | None = None,
) -> tuple[ScreenshotJob, ...]:
    selected_themes = tuple(themes or available_themes())
    return tuple(
        ScreenshotJob(theme_id=theme_id, output_path=output_dir / f"{theme_id.value}.png")
        for theme_id in selected_themes
    )


def jobs_to_render(
    output_dir: Path = DEFAULT_IMAGE_DIR,
    themes: Sequence[ThemeId] | None = None,
    *,
    force: bool = False,
) -> tuple[ScreenshotJob, ...]:
    return tuple(job for job in screenshot_jobs(output_dir=output_dir, themes=themes) if force or not job.output_path.exists())


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate qlementine theme gallery screenshots with a PySide6 controls showcase."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_IMAGE_DIR,
        help="Directory where PNG screenshots will be written.",
    )
    parser.add_argument(
        "--theme",
        dest="themes",
        action="append",
        default=[],
        help="Theme id to render. Repeat to render multiple themes. Defaults to all themes.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite screenshots even if they already exist.",
    )
    return parser.parse_args(argv)


def resolve_themes(theme_names: Sequence[str]) -> tuple[ThemeId, ...]:
    if not theme_names:
        return available_themes()
    return tuple(ThemeId(theme_name) for theme_name in theme_names)


def build_gallery_window():
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QStandardItem, QStandardItemModel
    from PySide6.QtWidgets import (
        QCheckBox,
        QComboBox,
        QDial,
        QFrame,
        QGridLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QListWidget,
        QListWidgetItem,
        QPlainTextEdit,
        QProgressBar,
        QPushButton,
        QRadioButton,
        QSlider,
        QSpinBox,
        QSplitter,
        QTableWidget,
        QTableWidgetItem,
        QTabWidget,
        QToolButton,
        QTreeView,
        QVBoxLayout,
        QWidget,
    )

    window = QWidget()
    window.setWindowTitle("qlementine-themes gallery")
    window.resize(1400, 920)

    root_layout = QVBoxLayout(window)
    root_layout.setContentsMargins(24, 24, 24, 24)
    root_layout.setSpacing(16)

    theme_title = QLabel("Theme preview")
    theme_title.setObjectName("themeTitle")
    theme_title.setStyleSheet("font-size: 28px; font-weight: 700;")

    theme_caption = QLabel("PySide6 controls showcase rendered with qlementine-themes")
    theme_caption.setWordWrap(True)

    root_layout.addWidget(theme_title)
    root_layout.addWidget(theme_caption)

    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.setChildrenCollapsible(False)
    root_layout.addWidget(splitter, 1)

    left_column = QWidget()
    left_layout = QVBoxLayout(left_column)
    left_layout.setSpacing(14)

    right_column = QWidget()
    right_layout = QVBoxLayout(right_column)
    right_layout.setSpacing(14)

    splitter.addWidget(left_column)
    splitter.addWidget(right_column)
    splitter.setSizes([680, 680])

    inputs_group = QGroupBox("Inputs")
    inputs_layout = QGridLayout(inputs_group)
    inputs_layout.addWidget(QLabel("Line edit"), 0, 0)
    line_edit = QLineEdit("Search themes, controls, icons…")
    inputs_layout.addWidget(line_edit, 0, 1)
    inputs_layout.addWidget(QLabel("Combo box"), 1, 0)
    combo_box = QComboBox()
    combo_box.addItems(["Desktop", "Tablet", "Compact"])
    combo_box.setCurrentIndex(1)
    inputs_layout.addWidget(combo_box, 1, 1)
    inputs_layout.addWidget(QLabel("Spin box"), 2, 0)
    spin_box = QSpinBox()
    spin_box.setRange(0, 100)
    spin_box.setValue(42)
    inputs_layout.addWidget(spin_box, 2, 1)
    inputs_layout.addWidget(QLabel("Notes"), 3, 0, Qt.AlignmentFlag.AlignTop)
    notes_edit = QPlainTextEdit()
    notes_edit.setPlainText("Previewing all repository themes.\nDisabled states and view widgets are shown too.")
    notes_edit.setMaximumBlockCount(10)
    inputs_layout.addWidget(notes_edit, 3, 1)

    actions_group = QGroupBox("Actions")
    actions_layout = QGridLayout(actions_group)
    actions_layout.addWidget(QPushButton("Primary action"), 0, 0)
    secondary_button = QPushButton("Disabled")
    secondary_button.setEnabled(False)
    actions_layout.addWidget(secondary_button, 0, 1)
    tool_button = QToolButton()
    tool_button.setText("Tool")
    actions_layout.addWidget(tool_button, 1, 0)
    actions_layout.addWidget(QCheckBox("Live preview"), 1, 1)
    checked_radio = QRadioButton("Gallery mode")
    checked_radio.setChecked(True)
    actions_layout.addWidget(checked_radio, 2, 0)
    actions_layout.addWidget(QRadioButton("Single theme"), 2, 1)

    progress_group = QGroupBox("Status")
    progress_layout = QGridLayout(progress_group)
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    progress_bar.setValue(72)
    progress_layout.addWidget(QLabel("Progress"), 0, 0)
    progress_layout.addWidget(progress_bar, 0, 1)
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(0, 100)
    slider.setValue(58)
    progress_layout.addWidget(QLabel("Opacity"), 1, 0)
    progress_layout.addWidget(slider, 1, 1)
    dial = QDial()
    dial.setRange(0, 100)
    dial.setValue(33)
    progress_layout.addWidget(QLabel("Accent"), 2, 0)
    progress_layout.addWidget(dial, 2, 1)

    left_layout.addWidget(inputs_group)
    left_layout.addWidget(actions_group)
    left_layout.addWidget(progress_group)
    left_layout.addStretch(1)

    tabs = QTabWidget()
    overview_tab = QWidget()
    overview_layout = QHBoxLayout(overview_tab)

    preview_list = QListWidget()
    for label in ["Buttons", "Inputs", "Navigation", "Tables", "Feedback"]:
        preview_list.addItem(QListWidgetItem(label))
    preview_list.setCurrentRow(0)
    overview_layout.addWidget(preview_list, 1)

    preview_table = QTableWidget(4, 3)
    preview_table.setHorizontalHeaderLabels(["State", "Tokens", "Updated"])
    rows = [
        ("Ready", "24", "just now"),
        ("Warnings", "3", "2 min ago"),
        ("Errors", "0", "today"),
        ("Disabled", "8", "today"),
    ]
    for row_index, row_values in enumerate(rows):
        for column_index, value in enumerate(row_values):
            preview_table.setItem(row_index, column_index, QTableWidgetItem(value))
    preview_table.horizontalHeader().setStretchLastSection(True)
    preview_table.verticalHeader().setVisible(False)
    overview_layout.addWidget(preview_table, 2)

    tabs.addTab(overview_tab, "Overview")

    details_tab = QWidget()
    details_layout = QHBoxLayout(details_tab)
    tree_view = QTreeView()
    tree_model = QStandardItemModel()
    tree_model.setHorizontalHeaderLabels(["Component", "State"])
    appearance_item = QStandardItem("Appearance")
    appearance_item.appendRow([QStandardItem("Corners"), QStandardItem("6 px")])
    appearance_item.appendRow([QStandardItem("Spacing"), QStandardItem("Comfortable")])
    widgets_item = QStandardItem("Widgets")
    widgets_item.appendRow([QStandardItem("Buttons"), QStandardItem("Ready")])
    widgets_item.appendRow([QStandardItem("Inputs"), QStandardItem("Ready")])
    tree_model.appendRow([appearance_item, QStandardItem("Configured")])
    tree_model.appendRow([widgets_item, QStandardItem("Previewed")])
    tree_view.setModel(tree_model)
    tree_view.expandAll()
    details_layout.addWidget(tree_view, 1)

    details_log = QPlainTextEdit()
    details_log.setPlainText(
        "• Theme applied from JSON\n"
        "• Common defaults merged from _common_.json\n"
        "• Screenshot captured after repaint"
    )
    details_layout.addWidget(details_log, 1)

    tabs.addTab(details_tab, "Details")

    right_layout.addWidget(tabs, 1)

    footer = QFrame()
    footer_layout = QHBoxLayout(footer)
    footer_layout.setContentsMargins(12, 0, 12, 0)
    footer_layout.addWidget(QLabel("Repository: jakerdy/qlementine-themes"))
    footer_layout.addStretch(1)
    footer_layout.addWidget(QLabel("Binding: PySide6-Qlementine"))
    root_layout.addWidget(footer)

    return window, theme_title, theme_caption


def render_gallery(output_dir: Path, themes: Sequence[ThemeId], *, force: bool = False) -> tuple[Path, ...]:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    output_dir.mkdir(parents=True, exist_ok=True)
    pending_jobs = jobs_to_render(output_dir=output_dir, themes=themes, force=force)
    skipped_jobs = tuple(job for job in screenshot_jobs(output_dir=output_dir, themes=themes) if job not in pending_jobs)

    for job in skipped_jobs:
        print(f"Skipped {job.relative_path.as_posix()} (already exists)")

    if not pending_jobs:
        return ()

    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    window, theme_title, theme_caption = build_gallery_window()
    window.show()
    app.processEvents()

    written_files: list[Path] = []
    for job in pending_jobs:
        metadata = load_theme(job.theme_id).get("meta", {})
        theme_name = metadata.get("name", job.theme_id.value.replace("-", " ").title())
        theme_title.setText(f"{theme_name} — controls gallery")
        theme_caption.setText(f"Saved to {job.relative_path.as_posix()}")
        apply_theme(app, job.theme_id, backend=QtBinding.PYSIDE6)
        window.repaint()
        app.processEvents()
        if not window.grab().save(str(job.output_path)):
            raise RuntimeError(f"Could not save screenshot to {job.output_path}")
        print(f"Saved {job.relative_path.as_posix()}")
        written_files.append(job.output_path)

    window.close()
    app.processEvents()
    return tuple(written_files)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        themes = resolve_themes(args.themes)
        render_gallery(args.output_dir, themes, force=args.force)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
