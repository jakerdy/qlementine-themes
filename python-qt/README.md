# jakerdy.qlementine-themes

Typed Python helpers for using the JSON themes from this repository with
PySide6/PyQt6 Qlementine bindings.

## Installation

```bash
uv add jakerdy.qlementine-themes
```

Install one of the Qlementine binding packages separately, depending on your Qt
binding:

```bash
uv add PySide6-Qlementine
# or
uv add PyQt6-Qlementine
```

## Example

```python
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

# 1) Load shared defaults from _common_.json
common_theme = load_common_theme()

# 2) Merge the selected repository theme (Gruvbox)
gruvbox_theme = load_theme(ThemeId.GRUVBOX)

# 3) Override any values you want for your application
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

# 4) Apply the final theme to the application
apply_theme(app, custom_theme, backend=QtBinding.PYSIDE6)

label = QLabel("Hello from Gruvbox + custom overrides")
label.show()

app.exec()
```
