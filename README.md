# qlementine-themes

A set of beautiful and varied [Qlementine](https://github.com/oclero/qlementine) themes in JSON format.

## What is Qlementine?

[Qlementine](https://github.com/oclero/qlementine) is a modern QStyle for desktop Qt6 applications. It supports a theming system based on JSON files that let you customize colors, fonts, spacing, and other visual properties.

## Themes

| Theme | Style | Description | `<img>` |
|-------|-------|-------------|------------|
| [Light](themes/light.json) | Light | Clean, classic light theme — the official Qlementine default | <img src="galery/img/light.png" alt="Light theme preview" width="320"> |
| [Dark](themes/dark.json) | Dark | Neutral dark theme inspired by VS Code Dark+ | <img src="galery/img/dark.png" alt="Dark theme preview" width="320"> |
| [Nord](themes/nord.json) | Dark | Arctic, north-bluish color palette from the [Nord](https://www.nordtheme.com/) project | <img src="galery/img/nord.png" alt="Nord theme preview" width="320"> |
| [Solarized Dark](themes/solarized-dark.json) | Dark | Dark variant of Ethan Schoonover's popular [Solarized](https://ethanschoonover.com/solarized/) palette | <img src="galery/img/solarized-dark.png" alt="Solarized Dark theme preview" width="320"> |
| [Solarized Light](themes/solarized-light.json) | Light | Light variant of Ethan Schoonover's popular [Solarized](https://ethanschoonover.com/solarized/) palette | <img src="galery/img/solarized-light.png" alt="Solarized Light theme preview" width="320"> |
| [Dracula](themes/dracula.json) | Dark | Dark theme with vivid purple accents from the [Dracula](https://draculatheme.com/) project | <img src="galery/img/dracula.png" alt="Dracula theme preview" width="320"> |
| [Tokyo Night](themes/tokyo-night.json) | Dark | Dark theme inspired by the lights of Tokyo at night, featuring cool blue accents | <img src="galery/img/tokyo-night.png" alt="Tokyo Night theme preview" width="320"> |
| [Gruvbox](themes/gruvbox.json) | Dark | Warm retro groove palette inspired by the [Gruvbox](https://github.com/morhetz/gruvbox) project | <img src="galery/img/gruvbox.png" alt="Gruvbox theme preview" width="320"> |
| [Shrek](themes/shrek.json) | Dark | Playful swamp-green theme with earthy ogre-inspired tones | <img src="galery/img/shrek.png" alt="Shrek theme preview" width="320"> |
| [Alpine](themes/alpine.json) | Light | Crisp high-altitude palette with snowy backgrounds and cool blue accents | <img src="galery/img/alpine.png" alt="Alpine theme preview" width="320"> |
| [Hello Kitty](themes/hello-kitty.json) | Light | Soft pastel pink theme with candy-colored highlights | <img src="galery/img/hello-kitty.png" alt="Hello Kitty theme preview" width="320"> |
| [Nixie Dawn](themes/nixie-dawn.json) | Dark | Warm dark theme inspired by glowing nixie tubes, with deep brown backgrounds and vivid orange accents | <img src="galery/img/nixie-dawn.png" alt="Nixie Dawn theme preview" width="320"> |
| [Khaki](themes/khaki.json) | Dark | Rugged military-style interface palette with muted olive, sand, and khaki tones | <img src="galery/img/khaki.png" alt="Khaki theme preview" width="320"> |
| [Tron Light](themes/tron-light.json) | Light | Bright futuristic palette with icy cyan highlights and warm orange contrasts inspired by Tron Legacy | <img src="galery/img/tron-light.png" alt="Tron Light theme preview" width="320"> |
| [Tron Dark](themes/tron-dark.json) | Dark | Dark companion to Tron Light with neon cyan accents and glowing amber controls | <img src="galery/img/tron-dark.png" alt="Tron Dark theme preview" width="320"> |
| [Mint Cocktail](themes/mint-cocktail.json) | Light | Refreshing mint-based theme balanced by vivid purple accent colors | <img src="galery/img/mint-cocktail.png" alt="Mint Cocktail theme preview" width="320"> |
| [Old Terminal](themes/old-terminal.json) | Dark | High-contrast black-and-green terminal look with enough midtones to stay readable | <img src="galery/img/old-terminal.png" alt="Old Terminal theme preview" width="320"> |
| [Cold Light](themes/cold-light.json) | Light | Cool light variant with blue-tinted neutrals and crisp frosty accents | <img src="galery/img/cold-light.png" alt="Cold Light theme preview" width="320"> |
| [Cold Dark](themes/cold-dark.json) | Dark | Cool dark variant with steel-blue surfaces and icy highlights | <img src="galery/img/cold-dark.png" alt="Cold Dark theme preview" width="320"> |
| [Neutral Light](themes/neutral-light.json) | Light | Balanced low-saturation light palette for understated everyday interfaces | <img src="galery/img/neutral-light.png" alt="Neutral Light theme preview" width="320"> |
| [Neutral Dark](themes/neutral-dark.json) | Dark | Balanced low-saturation dark palette with restrained contrast and slate accents | <img src="galery/img/neutral-dark.png" alt="Neutral Dark theme preview" width="320"> |
| [Warm Light](themes/warm-light.json) | Light | Warm cream and sand palette suited to softer, less clinical light UIs | <img src="galery/img/warm-light.png" alt="Warm Light theme preview" width="320"> |
| [Warm Dark](themes/warm-dark.json) | Dark | Warm brown-leaning dark palette with amber accents and softened contrast | <img src="galery/img/warm-dark.png" alt="Warm Dark theme preview" width="320"> |
| [GrayTable](themes/graytable.json) | Light | Low-contrast gray theme inspired by the classic light 3ds Max interface | <img src="galery/img/graytable.png" alt="GrayTable theme preview" width="320"> |

Gallery screenshots are generated by [`galery/src/generate_gallery.py`](galery/src/generate_gallery.py) and written to [`galery/img/`](galery/img/).

## Usage

Theme files are now split into:

- [`themes/_common_.json`](themes/_common_.json) — shared common defaults (numeric parameters and other non-palette settings that are identical across themes)
- `themes/*.json` — per-theme files that define only `meta` and color palette values

If your application supports merging JSON objects, merge `_common_.json` with the selected theme file into one final theme JSON document. Then save that merged JSON as a file (or embed it as a Qt resource) and pass the path of that merged file to Qlementine. If you only need the palette for a custom workflow, you can read the theme file by itself.

Once you have that merged file, load it using Qlementine:

```cpp
#include <oclero/qlementine/style/QlementineStyle.hpp>

auto* style = new oclero::qlementine::QlementineStyle(qApp);
qApp->setStyle(style);
style->setThemeJsonPath(":/themes/merged-theme.json");
```

## Theme format

Themes are JSON files. All keys are optional — missing keys fall back to the built-in defaults.

- Shared non-palette defaults live in [`themes/_common_.json`](themes/_common_.json).
- Individual theme files intentionally contain only **metadata** and **palette** values.
- **Colors** are hexadecimal strings: `"#rrggbb"` or `"#rrggbbaa"` (with alpha).
- **Metadata** is a nested object under the `"meta"` key.
- **Booleans**, **integers**, and **doubles** are used for layout and animation properties.

When adding a new theme to this repository, define only the `meta` block and the palette entries in the theme file. Put shared common defaults into `_common_.json` instead of copying them into every theme.

See the [full theme documentation](https://oclero.github.io/qlementine/theme/) for the complete list of available keys.

## Python helper package

For PySide6/PyQt6 usage, see [`python-qt/`](python-qt/). It contains a small `uv`-managed package named `jakerdy.qlementine-themes` with typed helpers for loading `_common_`, merging a repository theme, applying custom overrides, and sending the final theme directly to PyQlementine.
