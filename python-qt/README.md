# jakerdy.qlementine-themes

- Original Qlementine (C++): https://github.com/oclero/qlementine
- Original Python bindings: https://github.com/JerryZhangZZY/PyQlementine

`jakerdy.qlementine-themes` is the Python/Qt integration layer for the JSON theme
set in this repository. It turns the raw theme files into a small typed library
that can be used directly from PySide6 or PyQt6 applications.

## What This Layer Adds

The upstream pieces solve different parts of the problem:

- Qlementine provides the Qt style engine and JSON theme format.
- PyQlementine exposes that engine to PySide6 and PyQt6.
- This package provides the application-facing workflow around those themes.

In practice, this package adds:

- typed Python API for loading repository themes
- composition helpers for `_common_` + selected theme + app overrides
- direct application of the merged theme to a running Qt app
- a ready-made main-menu theme switcher utility, including optional `System` mode wiring
- package data and PyInstaller integration so theme JSON files are bundled automatically

## Installation

Install this package plus the Qlementine binding that matches your Qt stack:

```bash
uv add jakerdy.qlementine-themes
uv add PySide6 PySide6-Qlementine
```

Or, if your app uses PyQt6:

```bash
uv add jakerdy.qlementine-themes
uv add PyQt6 PyQt6-Qlementine
```

## Golden Example

This is the recommended integration pattern for both developers and agents. It
shows the full intended flow: resolve a `System` theme dynamically, add
app-specific overrides, apply the result, and expose runtime switching through
the main menu.

```python
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from jakerdy.qlementine_themes import (
    QtBinding,
    ThemeId,
    add_theme_menu,
    apply_theme,
    build_theme,
)


def resolve_theme(selection: ThemeId | str) -> ThemeId:
    if selection == "system":
        return ThemeId.NEUTRAL_DARK
    return ThemeId(selection)


def main() -> int:
    app = QApplication([])
    window = QMainWindow()

    theme_overrides = {
        "meta": {"name": "VOX Gruvbox"},
        "borderRadius": 10.0,
        "primaryColor": "#83a598",
        "primaryColorHovered": "#93b5a6",
    }

    initial_theme = "system"
    merged_theme = build_theme(resolve_theme(initial_theme), theme_overrides)
    apply_theme(app, merged_theme, backend=QtBinding.PYSIDE6)

    add_theme_menu(
        window.menuBar(),
        app,
        title="Themes",
        include_system_theme=True,
        initial_theme=initial_theme,
        resolve_theme=resolve_theme,
        overrides=theme_overrides,
        backend=QtBinding.PYSIDE6,
    )

    label = QLabel("Qlementine theme is active", window)
    label.move(24, 24)
    window.resize(720, 480)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
```

Use this pattern when you need:

- a stable default theme at startup, including a `System` option
- optional app-level overrides on top of a repository theme
- a menu for runtime switching without rewriting QAction boilerplate

## Utilities

### Theme Loading And Composition

- `available_themes()` returns all built-in theme ids in stable order.
- `load_common_theme()` loads shared defaults from `_common_.json`.
- `load_theme(theme_id)` loads only the selected per-theme layer.
- `merge_theme_layers(*layers)` merges layers with special handling for `meta`.
- `build_theme(theme_id, overrides=None)` produces the final merged theme object.

### Qt Integration

- `create_qlementine_theme(theme, backend=None)` converts a Python mapping into the Qlementine theme object.
- `apply_theme(app, theme, overrides=None, backend=None)` ensures the app has a Qlementine style and applies the final theme.
- `add_theme_menu(menu_bar, app, ...)` creates a ready-to-use menu with checkable actions for all built-in themes and can optionally include a `System` entry.

### Enums And Types

- `ThemeId` is the stable enum of repository themes.
- `QtBinding` selects `PySide6` or `PyQt6` explicitly when autodetection is not enough.
- `ThemeData`, `ThemeMeta`, and `ThemeValue` document the expected shape of composed theme objects.

## PyInstaller

This package is set up so that PyInstaller can discover the theme JSON files
without a manual `datas` stanza in your application spec.

It does that in two ways:

- the wheel includes the packaged JSON theme files
- the package exports a `pyinstaller40` hook entry point that tells PyInstaller to collect them

If your application imports `jakerdy.qlementine_themes`, modern PyInstaller
should bundle the theme files automatically.

## Theme Composition Model

Themes in this repository are intentionally split into layers.

### Layer 1: Shared Defaults

- `themes/_common_.json`
- contains shared non-palette defaults such as numeric sizing, radius, spacing, and other values common to all themes

### Layer 2: Per-Theme Palette

- `themes/<theme>.json`
- contains theme metadata plus the palette and per-theme overrides

### Layer 3: Application Overrides

- optional Python dictionary provided by the consuming application
- use this for product branding or small UI-specific adjustments without forking the repository theme

The final merged theme is:

```text
final_theme = _common_ + selected_theme + application_overrides
```

`meta` is merged as an object. Other keys are overwritten by the last layer that
defines them.

## Adding A New Theme

When adding a new built-in theme to this repository:

1. Create `themes/<new-theme>.json`.
2. Put only `meta` and theme-specific palette values in that file.
3. Keep shared numeric defaults in `themes/_common_.json` instead of copying them.
4. Add the new enum member to `ThemeId`.
5. Regenerate or add gallery output if needed.
6. Run the package tests and rebuild the wheel.

Keep the split clean: if a value is common to every theme, it belongs in
`_common_.json`; if it is part of the identity of one palette, it belongs in the
theme file.

## Repository Packaging Notes

The package is built from `python-qt/`, but its theme data originates from the
repository-level `themes/` directory. Build logic copies those JSON files into the
package artifact so the installed wheel stays self-contained.

That means consumers only need to install the package; they do not need a git
checkout of this repository for runtime theme loading.
