from __future__ import annotations

from pathlib import Path
from typing import cast

from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSizePolicy,
    QStyle,
    QVBoxLayout,
    QWidget,
)
from PySide6Qlementine import ColorEditor as QlementineColorEditor
from PySide6Qlementine import ColorMode, Theme

from .constants import DEFAULT_FILE_NAME, PREVIOUS_PATH_SETTINGS_KEY
from .fonts import monospace_font
from .schema import ALPHA_COLOR_FIELDS, COLOR_SECTIONS, METADATA_FIELDS
from .theme_utils import copy_theme, theme_to_bytes


class LabelColumn(QWidget):
    def hasHeightForWidth(self) -> bool:
        layout = self.layout()
        return layout is not None and layout.hasHeightForWidth()

    def heightForWidth(self, width: int) -> int:
        layout = self.layout()
        if layout is None:
            return super().heightForWidth(width)
        return layout.totalHeightForWidth(width)


def create_label_column(title: str, description: str, parent: QWidget) -> QWidget:
    column = LabelColumn(parent)
    column.setMaximumWidth(350)
    column.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
    layout = QVBoxLayout(column)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(
        max(
            2,
            parent.style().pixelMetric(QStyle.PixelMetric.PM_LayoutVerticalSpacing)
            // 4,
        )
    )

    title_label = QLabel(title, column)
    mono_font = monospace_font()
    mono_font.setPixelSize(14)
    title_label.setFont(mono_font)
    title_label.setWordWrap(False)
    title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    title_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    layout.addWidget(title_label)

    if description:
        description_label = QLabel(description, column)
        description_label.setWordWrap(True)
        description_label.setObjectName("captionLabel")
        description_label.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        description_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(description_label)

    return column


class ColorEditor(QlementineColorEditor):
    def __init__(self, color: QColor, parent: QWidget | None = None) -> None:
        super().__init__(color, parent)

        line_edit = self.findChild(QLineEdit)
        if line_edit is None:
            return

        line_edit.setMinimumWidth(120)
        line_edit.setMaximumWidth(16777215)

        size_policy = line_edit.sizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        line_edit.setSizePolicy(size_policy)

        layout = self.layout()
        if isinstance(layout, QHBoxLayout):
            layout.setStretchFactor(line_edit, 1)


class ThemeEditorWidget(QWidget):
    themeChanged = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._theme = Theme()
        self._color_editors: dict[str, ColorEditor] = {}
        self._metadata_editors: dict[str, QLineEdit] = {}
        self._build_ui()

    def theme(self) -> Theme:
        return copy_theme(self._theme)

    def setTheme(self, theme: Theme) -> None:
        if theme == self._theme:
            return
        self._theme = copy_theme(theme)
        self._update_ui()
        self.themeChanged.emit(self._theme)

    def load_theme_from_file(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load JSON theme", self._default_dialog_path(), "JSON Files (*.json)"
        )
        if not file_name:
            return
        try:
            theme = Theme.fromJsonPath(file_name)
        except RuntimeError as exc:
            QMessageBox.critical(
                self, "Load Error", f"Cannot load theme file:\n{file_name}\n\n{exc}"
            )
            return
        self.setTheme(theme)
        self._remember_dialog_path(file_name)

    def save_theme_to_file(self) -> None:
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save JSON theme", self._default_dialog_path(), "JSON Files (*.json)"
        )
        if not file_name:
            return

        json_bytes = theme_to_bytes(self._theme).replace(b"    ", b"  ")
        try:
            Path(file_name).write_bytes(json_bytes)
        except OSError as exc:
            QMessageBox.critical(
                self, "Writing Error", f"Cannot write to file:\n{file_name}\n\n{exc}"
            )
            return
        self._remember_dialog_path(file_name)

    def _build_ui(self) -> None:
        # self.setMinimumWidth(660)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        global_layout = QVBoxLayout(self)
        global_layout.setContentsMargins(0, 0, 0, 0)

        form_layout = QFormLayout()
        h_spacing = self.style().pixelMetric(
            QStyle.PixelMetric.PM_LayoutHorizontalSpacing
        )
        v_spacing = self.style().pixelMetric(
            QStyle.PixelMetric.PM_LayoutVerticalSpacing
        )
        form_layout.setHorizontalSpacing(h_spacing * 2)
        form_layout.setVerticalSpacing(max(v_spacing, 4))
        form_layout.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
        form_layout.setContentsMargins(4, 4, 15, 4)

        self._setup_metadata_editors(form_layout, v_spacing)
        self._setup_color_editors(form_layout, v_spacing)
        global_layout.addLayout(form_layout)
        self._refresh_description_colors()

    def _setup_metadata_editors(self, form_layout: QFormLayout, v_spacing: int) -> None:
        self._add_title(form_layout, "Metadata", v_spacing)
        for field_name, description in METADATA_FIELDS:
            left_column = create_label_column(field_name, description, self)
            editor = QLineEdit(self)
            editor.setPlaceholderText(field_name)
            editor.editingFinished.connect(
                lambda field_name=field_name, editor=editor: self._on_metadata_changed(
                    field_name, editor.text().strip()
                )
            )
            self._metadata_editors[field_name] = editor
            form_layout.addRow(left_column, editor)

    def _setup_color_editors(self, form_layout: QFormLayout, v_spacing: int) -> None:
        for section in COLOR_SECTIONS:
            self._add_title(form_layout, str(section["title"]), v_spacing)
            rows = cast(tuple[tuple[str, ...], ...], section["rows"])
            for row in rows:
                kind = row[0]
                if kind == "subtitle":
                    self._add_subtitle(form_layout, str(row[1]), v_spacing)
                elif kind == "description":
                    self._add_description(form_layout, str(row[1]))
                elif kind == "color":
                    _, field_name, description = row
                    self._add_color_editor(
                        form_layout, str(field_name), str(description)
                    )

    def _add_title(self, form_layout: QFormLayout, text: str, v_spacing: int) -> None:
        if form_layout.rowCount() > 0:
            spacer = QWidget(self)
            spacer.setFixedHeight(max(v_spacing * 2, 16))
            form_layout.addRow(spacer)

        label = QLabel(text, self)
        title_font = label.font()
        title_font.setBold(True)
        title_font.setPointSize(title_font.pointSize() + 2)
        label.setFont(title_font)
        form_layout.addRow(label)

    def _add_subtitle(
        self, form_layout: QFormLayout, text: str, v_spacing: int
    ) -> None:
        spacer = QWidget(self)
        spacer.setFixedHeight(max(v_spacing // 2, 6))
        form_layout.addRow(spacer)

        label = QLabel(text, self)
        subtitle_font = label.font()
        subtitle_font.setBold(True)
        label.setFont(subtitle_font)
        form_layout.addRow(label)

    def _add_description(self, form_layout: QFormLayout, text: str) -> None:
        label = QLabel(text, self)
        label.setWordWrap(True)
        label.setObjectName("captionLabel")
        label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        form_layout.addRow(label)

    def _add_color_editor(
        self, form_layout: QFormLayout, field_name: str, description: str
    ) -> None:
        label = create_label_column(field_name, description, self)

        editor = ColorEditor(getattr(self._theme, field_name), self)
        if field_name in ALPHA_COLOR_FIELDS:
            editor.setColorMode(ColorMode.RGBA)
        editor.colorChanged.connect(
            lambda field_name=field_name, editor=editor: self._on_color_changed(
                field_name, editor.color()
            )
        )
        editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._color_editors[field_name] = editor

        form_layout.addRow(label, editor)

    def _on_color_changed(self, field_name: str, color: QColor) -> None:
        setattr(self._theme, field_name, QColor(color))
        self._refresh_description_colors()
        self.themeChanged.emit(self._theme)

    def _on_metadata_changed(self, field_name: str, value: str) -> None:
        setattr(self._theme.meta, field_name, value)
        self.themeChanged.emit(self._theme)

    def _update_ui(self) -> None:
        for field_name, editor in self._color_editors.items():
            editor.blockSignals(True)
            editor.setColor(getattr(self._theme, field_name))
            editor.blockSignals(False)

        for field_name, editor in self._metadata_editors.items():
            editor.blockSignals(True)
            editor.setText(getattr(self._theme.meta, field_name))
            editor.blockSignals(False)

        self._refresh_description_colors()

    def _refresh_description_colors(self) -> None:
        description_color = self._theme.secondaryAlternativeColor.name(
            QColor.NameFormat.HexArgb
        )
        for label in self.findChildren(QLabel, "captionLabel"):
            label.setStyleSheet(f"color: {description_color};")

    def _default_dialog_path(self) -> str:
        default_dir = Path.home() / "Documents"
        default_path = default_dir / DEFAULT_FILE_NAME
        settings = QSettings()
        return str(settings.value(PREVIOUS_PATH_SETTINGS_KEY, str(default_path)))

    def _remember_dialog_path(self, file_name: str) -> None:
        settings = QSettings()
        settings.setValue(PREVIOUS_PATH_SETTINGS_KEY, file_name)
        settings.sync()
