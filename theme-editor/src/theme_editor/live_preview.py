from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QDate, QStringListModel, Qt, QTime
from PySide6.QtGui import QFont, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QCalendarWidget,
    QCheckBox,
    QComboBox,
    QCommandLinkButton,
    QDateEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QKeySequenceEdit,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollBar,
    QSlider,
    QSpinBox,
    QSplitter,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QTimeEdit,
    QToolBox,
    QToolButton,
    QTreeView,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6Qlementine import Label as ThemeLabel


class LivePreviewWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.theme_title: ThemeLabel
        self.theme_caption: ThemeLabel
        self._build_ui()

    def set_theme_name(self, name: str) -> None:
        self.theme_title.setText(f"{name} - controls gallery")

    def set_caption(self, text: str) -> None:
        self.theme_caption.setText(text)

    def _build_ui(self) -> None:
        self.setMinimumWidth(860)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(4, 4, 15, 4)
        root_layout.setSpacing(16)

        self.theme_title = self._make_heading(
            "Theme preview", 26, QFont.Weight.ExtraBold
        )
        self.theme_caption = self._make_heading(
            "PySide6 controls showcase rendered with qlementine-themes",
            12,
            QFont.Weight.Medium,
        )
        self.theme_caption.setWordWrap(True)

        root_layout.addWidget(self.theme_title)
        root_layout.addWidget(self.theme_caption)

        tabs = QTabWidget(self)
        tabs.addTab(
            self._create_tab_page(
                "Overview",
                "High-level snapshot, shortcuts and branding surfaces.",
                self._build_overview_content,
            ),
            "Overview",
        )
        tabs.addTab(
            self._create_tab_page(
                "Forms",
                "Dense input controls, date and time editing, and typography-sensitive widgets.",
                self._build_forms_content,
            ),
            "Forms",
        )
        tabs.addTab(
            self._create_tab_page(
                "Data",
                "Lists, trees, tables, and model-view heavy widgets.",
                self._build_data_content,
            ),
            "Data",
        )
        tabs.addTab(
            self._create_tab_page(
                "Navigation",
                "Panels, splitters, toolboxes, and scrolling surfaces.",
                self._build_navigation_content,
            ),
            "Navigation",
        )
        tabs.addTab(
            self._create_tab_page(
                "Feedback",
                "Progress, alerts, toggles, and state-driven controls.",
                self._build_feedback_content,
            ),
            "Feedback",
        )
        root_layout.addWidget(tabs, 1)

    def _make_heading(
        self, text: str, point_size: int, weight: QFont.Weight
    ) -> ThemeLabel:
        label = ThemeLabel(text, self)
        font = QFont(label.font())
        font.setPointSize(point_size)
        font.setWeight(weight)
        label.setFont(font)
        return label

    def _create_tab_page(
        self,
        title: str,
        intro: str,
        builder: Callable[[QWidget, QGridLayout], None],
    ) -> QWidget:
        page = QWidget(self)
        layout = QVBoxLayout(page)
        layout.setSpacing(12)
        layout.addWidget(self._make_heading(title, 16, QFont.Weight.Bold))

        intro_label = ThemeLabel(intro, page)
        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

        content = QWidget(page)
        content_layout = QGridLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setHorizontalSpacing(12)
        content_layout.setVerticalSpacing(12)
        builder(content, content_layout)
        layout.addWidget(content, 1)
        return page

    def _build_overview_content(self, parent: QWidget, layout: QGridLayout) -> None:
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

    def _build_forms_content(self, parent: QWidget, layout: QGridLayout) -> None:
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

    def _build_data_content(self, parent: QWidget, layout: QGridLayout) -> None:
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
        table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
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
        appearance_item.appendRow(
            [QStandardItem("Spacing"), QStandardItem("Comfortable")]
        )
        appearance_item.appendRow(
            [QStandardItem("Contrast"), QStandardItem("Balanced")]
        )
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

    def _build_navigation_content(self, parent: QWidget, layout: QGridLayout) -> None:
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
        detail_layout.addWidget(QLabel("Active section"))
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
        scroll_layout.addWidget(QLabel("Horizontal"), 0, 0)
        horizontal_scroll = QScrollBar(Qt.Orientation.Horizontal, scroll_group)
        horizontal_scroll.setValue(40)
        scroll_layout.addWidget(horizontal_scroll, 0, 1)
        scroll_layout.addWidget(QLabel("Vertical"), 1, 0)
        vertical_scroll = QScrollBar(Qt.Orientation.Vertical, scroll_group)
        vertical_scroll.setValue(60)
        scroll_layout.addWidget(vertical_scroll, 1, 1, Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(toolbox_group, 0, 0)
        layout.addWidget(split_group, 0, 1)
        layout.addWidget(scroll_group, 1, 0, 1, 2)
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 3)
        layout.setRowStretch(0, 1)

    def _build_feedback_content(self, parent: QWidget, layout: QGridLayout) -> None:
        status_group = QGroupBox("Progress and intensity", parent)
        status_layout = QGridLayout(status_group)
        status_layout.setContentsMargins(12, 12, 12, 12)
        status_layout.setHorizontalSpacing(10)
        status_layout.setVerticalSpacing(10)
        progress_bar = QProgressBar(status_group)
        progress_bar.setRange(0, 100)
        progress_bar.setValue(72)
        status_layout.addWidget(QLabel("Progress"), 0, 0)
        status_layout.addWidget(progress_bar, 0, 1)
        queued_bar = QProgressBar(status_group)
        queued_bar.setRange(0, 100)
        queued_bar.setValue(38)
        status_layout.addWidget(QLabel("Queue"), 1, 0)
        status_layout.addWidget(queued_bar, 1, 1)
        opacity_slider = QSlider(Qt.Orientation.Horizontal, status_group)
        opacity_slider.setRange(0, 100)
        opacity_slider.setValue(58)
        status_layout.addWidget(QLabel("Opacity"), 2, 0)
        status_layout.addWidget(opacity_slider, 2, 1)
        accent_dial = QDial(status_group)
        accent_dial.setRange(0, 100)
        accent_dial.setValue(33)
        status_layout.addWidget(QLabel("Accent"), 3, 0)
        status_layout.addWidget(accent_dial, 3, 1)

        alerts_group = QGroupBox("Alerts and notes", parent)
        alerts_layout = QVBoxLayout(alerts_group)
        alerts_layout.setContentsMargins(12, 12, 12, 12)
        alerts_layout.setSpacing(10)
        alerts_layout.addWidget(
            QLabel(
                "Success, info, warning and error colors should all stay readable here."
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
        queue_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
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
