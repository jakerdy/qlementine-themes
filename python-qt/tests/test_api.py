from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

import jakerdy.qlementine_themes as qlementine_themes
from jakerdy.qlementine_themes.__pyinstaller import get_hook_dirs
from jakerdy.qlementine_themes import (
    ThemeId,
    add_theme_menu,
    available_themes,
    build_theme,
    load_common_theme,
    load_theme,
    merge_theme_layers,
)


class ThemeApiTests(unittest.TestCase):
    def test_repo_theme_directory_is_available_from_source_checkout(self) -> None:
        python_qt_dir = next(
            parent for parent in Path(__file__).resolve().parents if (parent / "pyproject.toml").is_file()
        )
        repo_themes_dir = python_qt_dir.parent / "themes"

        self.assertTrue((repo_themes_dir / "_common_.json").is_file())

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

    def test_pyinstaller_hook_directory_contains_package_hook(self) -> None:
        hook_dirs = get_hook_dirs()

        self.assertEqual(len(hook_dirs), 1)
        hook_path = Path(hook_dirs[0]) / "hook-jakerdy.qlementine_themes.py"
        self.assertTrue(hook_path.is_file())

    def test_add_theme_menu_applies_initial_theme_and_reacts_to_selection(self) -> None:
        changes: list[ThemeId | str] = []
        app = object()
        menu_bar = _FakeMenuBar()

        with (
            mock.patch.object(qlementine_themes, "available_themes", return_value=(ThemeId.GRUVBOX, ThemeId.NORD)),
            mock.patch.object(
                qlementine_themes,
                "load_theme",
                side_effect=[
                    {"meta": {"name": "Gruvbox"}},
                    {"meta": {"name": "Nord"}},
                ],
            ),
            mock.patch.object(qlementine_themes, "_menu_module_names", return_value=("fake.qtgui", "fake.qtwidgets")),
            mock.patch.object(
                qlementine_themes,
                "import_module",
                side_effect=lambda module_name: _FakeQtGui if module_name == "fake.qtgui" else _FakeQtWidgets,
            ),
            mock.patch.object(qlementine_themes, "apply_theme") as apply_theme_mock,
        ):
            menu = add_theme_menu(
                menu_bar,
                app,
                title="Themes",
                initial_theme=ThemeId.NORD,
                on_theme_changed=changes.append,
            )

            self.assertEqual(menu.title, "Themes")
            self.assertEqual([action.text for action in menu.actions], ["Gruvbox", "Nord"])
            self.assertTrue(menu.actions[1].isChecked())
            apply_theme_mock.assert_called_once_with(app, ThemeId.NORD, overrides=None, backend=None)

            menu.actions[0].trigger()

            self.assertEqual(
                apply_theme_mock.call_args_list[-1],
                mock.call(app, ThemeId.GRUVBOX, overrides=None, backend=None),
            )
            self.assertEqual(changes, [ThemeId.GRUVBOX])

    def test_add_theme_menu_rejects_unknown_initial_theme(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown theme id"):
            add_theme_menu(_FakeMenuBar(), object(), initial_theme="missing-theme")

    def test_add_theme_menu_supports_system_selection(self) -> None:
        changes: list[ThemeId | str] = []
        app = object()
        menu_bar = _FakeMenuBar()

        with (
            mock.patch.object(qlementine_themes, "available_themes", return_value=(ThemeId.GRUVBOX, ThemeId.NORD)),
            mock.patch.object(
                qlementine_themes,
                "load_theme",
                side_effect=[
                    {"meta": {"name": "Gruvbox"}},
                    {"meta": {"name": "Nord"}},
                ],
            ),
            mock.patch.object(qlementine_themes, "_menu_module_names", return_value=("fake.qtgui", "fake.qtwidgets")),
            mock.patch.object(
                qlementine_themes,
                "import_module",
                side_effect=lambda module_name: _FakeQtGui if module_name == "fake.qtgui" else _FakeQtWidgets,
            ),
            mock.patch.object(qlementine_themes, "apply_theme") as apply_theme_mock,
        ):
            menu = add_theme_menu(
                menu_bar,
                app,
                title="Themes",
                initial_theme="system",
                include_system_theme=True,
                resolve_theme=lambda selection: ThemeId.NORD if selection == "system" else selection,
                on_theme_changed=changes.append,
            )

            self.assertEqual([action.text for action in menu.actions], ["System", "Gruvbox", "Nord"])
            self.assertTrue(menu.actions[0].isChecked())
            apply_theme_mock.assert_called_once_with(app, ThemeId.NORD, overrides=None, backend=None)

            menu.actions[2].trigger()
            menu.actions[0].trigger()

            self.assertEqual(
                apply_theme_mock.call_args_list,
                [
                    mock.call(app, ThemeId.NORD, overrides=None, backend=None),
                    mock.call(app, ThemeId.NORD, overrides=None, backend=None),
                    mock.call(app, ThemeId.NORD, overrides=None, backend=None),
                ],
            )
            self.assertEqual(changes, [ThemeId.NORD, "system"])


class _FakeSignal:
    def __init__(self) -> None:
        self._callbacks: list[object] = []

    def connect(self, callback: object) -> None:
        self._callbacks.append(callback)

    def emit(self, value: bool) -> None:
        for callback in list(self._callbacks):
            callback(value)


class _FakeAction:
    def __init__(self, text: str, parent: object) -> None:
        self.text = text
        self.parent = parent
        self._checked = False
        self._group: _FakeActionGroup | None = None
        self.triggered = _FakeSignal()

    def setCheckable(self, checkable: bool) -> None:
        self.checkable = checkable

    def setChecked(self, checked: bool) -> None:
        self._checked = checked
        if checked and self._group is not None and self._group.exclusive:
            for action in self._group.actions:
                if action is not self:
                    action._checked = False

    def isChecked(self) -> bool:
        return self._checked

    def trigger(self) -> None:
        self.setChecked(True)
        self.triggered.emit(True)


class _FakeActionGroup:
    def __init__(self, parent: object) -> None:
        self.parent = parent
        self.exclusive = False
        self.actions: list[_FakeAction] = []

    def setExclusive(self, exclusive: bool) -> None:
        self.exclusive = exclusive

    def addAction(self, action: _FakeAction) -> None:
        action._group = self
        self.actions.append(action)


class _FakeMenu:
    def __init__(self, title: str) -> None:
        self.title = title
        self.actions: list[_FakeAction] = []

    def addAction(self, action: _FakeAction) -> None:
        self.actions.append(action)


class _FakeMenuBar:
    def __init__(self) -> None:
        self.menus: list[_FakeMenu] = []

    def addMenu(self, title: str) -> _FakeMenu:
        menu = _FakeMenu(title)
        self.menus.append(menu)
        return menu


class _FakeQtGui:
    QAction = _FakeAction
    QActionGroup = _FakeActionGroup


class _FakeQtWidgets:
    pass


if __name__ == "__main__":
    unittest.main()
