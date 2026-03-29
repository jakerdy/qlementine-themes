# qlementine-themes

A set of beautiful and varied [Qlementine](https://github.com/oclero/qlementine) themes in JSON format.

## What is Qlementine?

[Qlementine](https://github.com/oclero/qlementine) is a modern QStyle for desktop Qt6 applications. It supports a theming system based on JSON files that let you customize colors, fonts, spacing, and other visual properties.

## Themes

| Theme | Style | Description |
|-------|-------|-------------|
| [Light](themes/light.json) | Light | Clean, classic light theme — the official Qlementine default |
| [Dark](themes/dark.json) | Dark | Neutral dark theme inspired by VS Code Dark+ |
| [Nord](themes/nord.json) | Dark | Arctic, north-bluish color palette from the [Nord](https://www.nordtheme.com/) project |
| [Solarized Dark](themes/solarized-dark.json) | Dark | Dark variant of Ethan Schoonover's popular [Solarized](https://ethanschoonover.com/solarized/) palette |
| [Solarized Light](themes/solarized-light.json) | Light | Light variant of Ethan Schoonover's popular [Solarized](https://ethanschoonover.com/solarized/) palette |
| [Dracula](themes/dracula.json) | Dark | Dark theme with vivid purple accents from the [Dracula](https://draculatheme.com/) project |
| [Tokyo Night](themes/tokyo-night.json) | Dark | Dark theme inspired by the lights of Tokyo at night, featuring cool blue accents |

## Usage

Copy any `.json` theme file into your project and load it using Qlementine's `ThemeManager`:

```cpp
#include <oclero/qlementine/style/QlementineStyle.hpp>
#include <oclero/qlementine/utils/ThemeUtils.hpp>

auto* style = new oclero::qlementine::QlementineStyle(qApp);
qApp->setStyle(style);
style->setThemeJsonPath(":/path/to/theme.json");
```

## Theme format

Themes are JSON files. All keys are optional — missing keys fall back to the built-in defaults.

- **Colors** are hexadecimal strings: `"#rrggbb"` or `"#rrggbbaa"` (with alpha).
- **Metadata** is a nested object under the `"meta"` key.
- **Booleans**, **integers**, and **doubles** are used for layout and animation properties.

See the [full theme documentation](https://oclero.github.io/qlementine/theme/) for the complete list of available keys.
