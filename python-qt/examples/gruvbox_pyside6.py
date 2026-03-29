from __future__ import annotations

from PySide6.QtWidgets import QApplication, QLabel

from jakerdy.qlementine_themes import (
    QtBinding,
    ThemeId,
    apply_theme,
    load_common_theme,
    load_theme,
    merge_theme_layers,
)

app = QApplication([])

common_theme = load_common_theme()
gruvbox_theme = load_theme(ThemeId.GRUVBOX)
custom_theme = merge_theme_layers(
    common_theme,
    gruvbox_theme,
    {
        "meta": {"name": "My Gruvbox"},
        "primaryColor": "#83a598",
        "primaryColorHovered": "#93b5a6",
        "borderRadius": 10.0,
    },
)

apply_theme(app, custom_theme, backend=QtBinding.PYSIDE6)

label = QLabel("Hello from Gruvbox + custom overrides")
label.resize(360, 120)
label.show()

app.exec()
