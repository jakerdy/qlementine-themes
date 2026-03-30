from __future__ import annotations

from typing import cast

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)
from PySide6Qlementine import AboutDialog, Theme

from .constants import (
    APP_AUTHOR,
    APP_ICON_PATH,
    APP_NAME,
    APP_REPOSITORY_URL,
    APP_VERSION,
    DEFAULT_THEME_ID,
    THEMES_DIR,
)
from .live_preview import LivePreviewWidget
from .theme_editor_widget import ThemeEditorWidget
from .theme_utils import (
    built_in_theme_paths,
    copy_theme,
    ensure_qlementine_style,
    load_repo_theme,
    preset_file_name,
    preset_payload_from_theme,
    save_json,
    theme_display_name,
)


class ThemeEditorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        if APP_ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(APP_ICON_PATH)))
        self.resize(1480, 920)

        app = cast(QApplication | None, QApplication.instance())
        if app is None:
            raise RuntimeError(
                "QApplication must exist before ThemeEditorWindow is created."
            )

        self._style = ensure_qlementine_style(app)
        self._built_in_paths = built_in_theme_paths()
        self._theme_editor = ThemeEditorWidget(self)
        self._preview = LivePreviewWidget(self)
        self._preset_combo = QComboBox(self)
        self._build_ui()
        self._populate_presets()
        self._theme_editor.themeChanged.connect(self._apply_theme)
        self._preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        self._load_initial_theme()

    def _build_ui(self) -> None:
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(18)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)
        toolbar.addWidget(QLabel("Preset", self))
        self._preset_combo.setFixedWidth(300)
        toolbar.addWidget(self._preset_combo)

        new_preset_button = QPushButton("New Preset", self)
        new_preset_button.clicked.connect(self._create_new_preset)
        toolbar.addWidget(new_preset_button)

        load_button = QPushButton(
            QIcon.fromTheme("document-open"), "Load JSON file...", self
        )
        load_button.clicked.connect(self._theme_editor.load_theme_from_file)
        toolbar.addWidget(load_button)

        save_button = QPushButton(
            QIcon.fromTheme("document-save"), "Save JSON file...", self
        )
        save_button.clicked.connect(self._theme_editor.save_theme_to_file)
        toolbar.addWidget(save_button)
        toolbar.addStretch(1)
        layout.addLayout(toolbar)

        splitter = QSplitter(Qt.Orientation.Horizontal, self)
        splitter.setHandleWidth(18)
        splitter.setChildrenCollapsible(False)

        editor_scroll = QScrollArea(splitter)
        editor_scroll.setWidgetResizable(True)
        editor_scroll.setFrameShape(QFrame.Shape.NoFrame)
        editor_scroll.setContentsMargins(0, 0, 16, 0)
        editor_scroll.setMinimumWidth(300)
        editor_scroll.setWidget(self._theme_editor)
        splitter.addWidget(editor_scroll)

        preview_scroll = QScrollArea(splitter)
        preview_scroll.setWidgetResizable(True)
        preview_scroll.setFrameShape(QFrame.Shape.NoFrame)
        preview_scroll.setContentsMargins(0, 0, 16, 0)
        preview_scroll.setMinimumWidth(300)
        preview_scroll.setWidget(self._preview)
        splitter.addWidget(preview_scroll)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([460, 920])
        layout.addWidget(splitter, 1)
        self._build_menu()

    def _build_menu(self) -> None:
        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)

    def _populate_presets(self) -> None:
        self._preset_combo.blockSignals(True)
        self._preset_combo.clear()
        for path in self._built_in_paths:
            self._preset_combo.addItem(theme_display_name(path), path.stem)

        default_index = max(0, self._preset_combo.findData(DEFAULT_THEME_ID))
        self._preset_combo.setCurrentIndex(default_index)
        self._preset_combo.blockSignals(False)

    def _load_initial_theme(self) -> None:
        self._load_selected_preset()

    def _on_preset_changed(self) -> None:
        self._load_selected_preset()

    def _load_selected_preset(self) -> None:
        theme_id = self._preset_combo.currentData()
        if not isinstance(theme_id, str):
            return
        theme = load_repo_theme(theme_id)
        self._theme_editor.setTheme(theme)

    def _apply_theme(self, theme: Theme) -> None:
        theme_copy = copy_theme(theme)
        self._style.setTheme(theme_copy)
        self._preview.set_theme_name(theme.meta.name or "Untitled")
        self._preview.set_caption(
            "PySide6 controls showcase rendered with qlementine-themes"
        )

    def _create_new_preset(self) -> None:
        preset_name, accepted = QInputDialog.getText(self, "New Preset", "Preset name")
        if not accepted:
            return

        preset_name = preset_name.strip()
        if not preset_name:
            QMessageBox.warning(self, "New Preset", "Preset name cannot be empty.")
            return

        file_stem = preset_file_name(preset_name)
        preset_path = THEMES_DIR / f"{file_stem}.json"
        if preset_path.exists():
            QMessageBox.warning(
                self, "New Preset", f"Preset already exists:\n{preset_path.name}"
            )
            return

        theme = load_repo_theme(DEFAULT_THEME_ID)
        theme.meta.name = preset_name
        theme.meta.author = "Qlementine Themes"
        theme.meta.version = "1.0.0"

        save_json(preset_path, preset_payload_from_theme(theme))
        self._built_in_paths = built_in_theme_paths()
        self._populate_presets()
        index = self._preset_combo.findData(file_stem)
        if index >= 0:
            self._preset_combo.setCurrentIndex(index)

    def _show_about_dialog(self) -> None:
        dialog = AboutDialog(self)
        dialog.setApplicationName(APP_NAME)
        dialog.setApplicationVersion(APP_VERSION)
        dialog.setDescription(
            "PySide6 port of the Qlementine theme editor with live preview and repository preset management."
        )
        dialog.setWebsiteUrl(APP_REPOSITORY_URL)
        dialog.setLicense("MIT")
        dialog.setCopyright(APP_AUTHOR)
        dialog.exec()
