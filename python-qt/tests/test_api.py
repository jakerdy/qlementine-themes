from __future__ import annotations

import unittest

from jakerdy.qlementine_themes import (
    ThemeId,
    available_themes,
    build_theme,
    load_common_theme,
    load_theme,
    merge_theme_layers,
)


class ThemeApiTests(unittest.TestCase):
    def test_available_themes_matches_enum(self) -> None:
        self.assertEqual(available_themes(), tuple(sorted(ThemeId, key=lambda item: item.value)))

    def test_load_common_theme_exposes_shared_defaults(self) -> None:
        common_theme = load_common_theme()

        self.assertEqual(common_theme["fontSize"], 12)
        self.assertEqual(common_theme["borderRadius"], 6.0)
        self.assertNotIn("primaryColor", common_theme)

    def test_load_theme_returns_palette_without_common_values(self) -> None:
        gruvbox = load_theme(ThemeId.GRUVBOX)

        self.assertEqual(gruvbox["primaryColor"], "#d79921")
        self.assertEqual(gruvbox["meta"], {"author": "Qlementine Themes", "name": "Gruvbox", "version": "1.0.0"})
        self.assertNotIn("fontSize", gruvbox)

    def test_merge_theme_layers_merges_meta_and_custom_overrides(self) -> None:
        merged = merge_theme_layers(
            load_common_theme(),
            load_theme(ThemeId.GRUVBOX),
            {
                "meta": {"name": "Custom Gruvbox"},
                "primaryColor": "#83a598",
                "borderRadius": 10.0,
            },
        )

        self.assertEqual(merged["fontSize"], 12)
        self.assertEqual(merged["primaryColor"], "#83a598")
        self.assertEqual(merged["borderRadius"], 10.0)
        self.assertEqual(
            merged["meta"],
            {"author": "Qlementine Themes", "name": "Custom Gruvbox", "version": "1.0.0"},
        )

    def test_build_theme_starts_from_common_then_theme_then_overrides(self) -> None:
        built = build_theme(
            ThemeId.GRUVBOX,
            {"primaryColor": "#458588", "meta": {"version": "2.0.0"}},
        )

        self.assertEqual(built["fontSize"], 12)
        self.assertEqual(built["primaryColor"], "#458588")
        self.assertEqual(built["meta"], {"author": "Qlementine Themes", "name": "Gruvbox", "version": "2.0.0"})

    def test_unknown_theme_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown theme id"):
            build_theme("missing-theme")


if __name__ == "__main__":
    unittest.main()
