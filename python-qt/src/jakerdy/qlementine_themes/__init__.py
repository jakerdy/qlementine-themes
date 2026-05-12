from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from importlib import import_module, resources
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping, Protocol, TypeAlias, TypedDict, cast

__all__ = [
    "QtBinding",
    "ThemeId",
    "ThemeData",
    "ThemeMeta",
    "ThemeValue",
    "add_theme_menu",
    "apply_theme",
    "available_themes",
    "build_theme",
    "create_qlementine_theme",
    "load_common_theme",
    "load_theme",
    "merge_theme_layers",
]


class ThemeMeta(TypedDict, total=False):
    author: str
    name: str
    version: str


ThemeScalar: TypeAlias = bool | int | float | str
ThemeValue: TypeAlias = ThemeScalar | ThemeMeta
ThemeData: TypeAlias = dict[str, ThemeValue]
ThemeLayer: TypeAlias = Mapping[str, ThemeValue]


class ThemeId(str, Enum):
    ALPINE = "alpine"
    COLD_DARK = "cold-dark"
    COLD_LIGHT = "cold-light"
    DARK = "dark"
    DRACULA = "dracula"
    GRAYTABLE = "graytable"
    GRUVBOX = "gruvbox"
    HELLO_KITTY = "hello-kitty"
    KHAKI = "khaki"
    LIGHT = "light"
    MINT_COCKTAIL = "mint-cocktail"
    NEUTRAL_DARK = "neutral-dark"
    NEUTRAL_LIGHT = "neutral-light"
    NIXIE_DAWN = "nixie-dawn"
    NORD = "nord"
    OLD_TERMINAL = "old-terminal"
    SHREK = "shrek"
    SOLARIZED_DARK = "solarized-dark"
    SOLARIZED_LIGHT = "solarized-light"
    TOKYO_NIGHT = "tokyo-night"
    TRON_DARK = "tron-dark"
    TRON_LIGHT = "tron-light"
    WARM_DARK = "warm-dark"
    WARM_LIGHT = "warm-light"


class QtBinding(str, Enum):
    PYQT6 = "pyqt6"
    PYSIDE6 = "pyside6"


class QApplicationProtocol(Protocol):
    def style(self) -> object: ...

    def setStyle(self, style: object) -> None: ...


@dataclass(frozen=True)
class _QlementineRuntime:
    qjson_document: Any
    qlementine_style: type[Any]
    theme_class: type[Any]


if TYPE_CHECKING:
    from collections.abc import Sequence
else:
    Sequence = tuple


def available_themes() -> tuple[ThemeId, ...]:
    return tuple(sorted(ThemeId, key=lambda theme_id: theme_id.value))


def load_common_theme() -> ThemeData:
    return _load_json_file(_theme_path("_common_"))


def load_theme(theme_id: ThemeId | str) -> ThemeData:
    return _load_json_file(_theme_path(_normalize_theme_id(theme_id)))


def merge_theme_layers(*layers: ThemeLayer) -> ThemeData:
    merged: ThemeData = {}
    for layer in layers:
        for key, value in layer.items():
            if key == "meta" and isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
                merged[key] = cast(ThemeMeta, {**cast(Mapping[str, str], merged[key]), **dict(value)})
                continue
            if key == "meta" and isinstance(value, Mapping):
                merged[key] = cast(ThemeMeta, dict(value))
                continue
            merged[key] = cast(ThemeValue, value)
    return merged


def build_theme(theme_id: ThemeId | str, overrides: ThemeLayer | None = None) -> ThemeData:
    layers: list[ThemeLayer] = [load_common_theme(), load_theme(theme_id)]
    if overrides:
        layers.append(overrides)
    return merge_theme_layers(*layers)


def create_qlementine_theme(theme: ThemeLayer, backend: QtBinding | None = None) -> Any:
    runtime = _load_qlementine_runtime(backend)
    json_document = runtime.qjson_document.fromVariant(dict(theme))
    return runtime.theme_class.fromJsonDoc(json_document)


def apply_theme(
    app: QApplicationProtocol,
    theme: ThemeId | str | ThemeLayer,
    *,
    overrides: ThemeLayer | None = None,
    backend: QtBinding | None = None,
) -> Any:
    runtime = _load_qlementine_runtime(backend)
    theme_data = build_theme(theme, overrides) if isinstance(theme, (ThemeId, str)) else merge_theme_layers(theme, overrides or {})
    style = app.style()
    if not isinstance(style, runtime.qlementine_style):
        style = runtime.qlementine_style(app)
        app.setStyle(style)
    style.setTheme(create_qlementine_theme(theme_data, backend=backend))
    return style


def add_theme_menu(
    menu_bar: Any,
    app: QApplicationProtocol,
    *,
    title: str = "Theme",
    initial_theme: ThemeId | str | None = None,
    overrides: ThemeLayer | None = None,
    backend: QtBinding | None = None,
    on_theme_changed: Any | None = None,
) -> Any:
    initial_theme_id = _coerce_theme_id(initial_theme or available_themes()[0])
    qt_gui_module_name, qt_widgets_module_name = _menu_module_names(backend)
    try:
        qt_gui = import_module(qt_gui_module_name)
        qt_widgets = import_module(qt_widgets_module_name)
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Could not import Qt menu classes. Install PySide6 or PyQt6 together with the matching "
            "Qlementine binding."
        ) from exc

    action_group = getattr(qt_gui, "QActionGroup")(menu_bar)
    action_group.setExclusive(True)
    menu = menu_bar.addMenu(title)
    theme_actions: dict[ThemeId, Any] = {}

    for theme_id in available_themes():
        theme_name = _theme_display_name(theme_id)
        action = getattr(qt_gui, "QAction")(theme_name, menu)
        action.setCheckable(True)
        action.setChecked(theme_id is initial_theme_id)
        action_group.addAction(action)
        menu.addAction(action)
        theme_actions[theme_id] = action

        def _handle_triggered(checked: bool, selected_theme: ThemeId = theme_id) -> None:
            if not checked:
                return
            apply_theme(app, selected_theme, overrides=overrides, backend=backend)
            if on_theme_changed is not None:
                on_theme_changed(selected_theme)

        action.triggered.connect(_handle_triggered)

    if not theme_actions[initial_theme_id].isChecked():
        theme_actions[initial_theme_id].setChecked(True)

    apply_theme(app, initial_theme_id, overrides=overrides, backend=backend)
    setattr(menu, "_qlementine_theme_actions", theme_actions)
    setattr(menu, "_qlementine_theme_action_group", action_group)
    return menu


def _load_json_file(path: Path) -> ThemeData:
    with path.open("r", encoding="utf-8") as file_obj:
        return cast(ThemeData, json.load(file_obj))


def _normalize_theme_id(theme_id: ThemeId | str) -> str:
    normalized = theme_id.value if isinstance(theme_id, ThemeId) else theme_id
    if normalized == "_common_":
        return normalized
    try:
        return ThemeId(normalized).value
    except ValueError as exc:
        raise ValueError(f"Unknown theme id: {theme_id}") from exc


def _coerce_theme_id(theme_id: ThemeId | str) -> ThemeId:
    return ThemeId(_normalize_theme_id(theme_id))


def _theme_display_name(theme_id: ThemeId) -> str:
    meta = load_theme(theme_id).get("meta")
    if isinstance(meta, Mapping):
        name = meta.get("name")
        if isinstance(name, str) and name:
            return name
    return theme_id.value.replace("-", " ").title()


def _theme_path(theme_name: str) -> Path:
    filename = f"{theme_name}.json"
    packaged_path = Path(__file__).with_name("themes") / filename
    if packaged_path.is_file():
        return packaged_path

    repo_themes_dir = _find_repo_themes_dir(Path(__file__).resolve())
    if repo_themes_dir is not None:
        repo_path = repo_themes_dir / filename
        if repo_path.is_file():
            return repo_path

    try:
        package_root = resources.files("jakerdy.qlementine_themes")
    except ModuleNotFoundError:
        package_root = None
    else:
        resource_path = package_root / "themes" / filename
        if resource_path.is_file():
            return Path(str(resource_path))

    raise FileNotFoundError(f"Theme file not found: {filename}")


def _find_repo_themes_dir(start_path: Path) -> Path | None:
    for parent in start_path.parents:
        candidate = parent / "themes"
        if (candidate / "_common_.json").is_file():
            return candidate
    return None


def _load_qlementine_runtime(backend: QtBinding | None) -> _QlementineRuntime:
    errors: list[str] = []
    bindings: Sequence[QtBinding] = (backend,) if backend is not None else (QtBinding.PYSIDE6, QtBinding.PYQT6)
    for binding in bindings:
        core_module_name, qlementine_module_name = _module_names(binding)
        try:
            qt_core = import_module(core_module_name)
            qlementine_module = import_module(qlementine_module_name)
        except ModuleNotFoundError as exc:
            errors.append(f"{binding.value}: {exc.name}")
            continue
        return _QlementineRuntime(
            qjson_document=getattr(qt_core, "QJsonDocument"),
            qlementine_style=getattr(qlementine_module, "QlementineStyle"),
            theme_class=getattr(qlementine_module, "Theme"),
        )
    formatted_errors = ", ".join(errors) if errors else "no bindings were tried"
    raise ModuleNotFoundError(
        "Could not import a Qlementine Qt binding. Install PySide6-Qlementine or "
        f"PyQt6-Qlementine first ({formatted_errors})."
    )


def _module_names(binding: QtBinding) -> tuple[str, str]:
    if binding is QtBinding.PYSIDE6:
        return "PySide6.QtCore", "PySide6Qlementine"
    return "PyQt6.QtCore", "PyQt6Qlementine"


def _menu_module_names(binding: QtBinding | None) -> tuple[str, str]:
    resolved_binding = binding or _detect_qt_binding()
    if resolved_binding is QtBinding.PYSIDE6:
        return "PySide6.QtGui", "PySide6.QtWidgets"
    return "PyQt6.QtGui", "PyQt6.QtWidgets"


def _detect_qt_binding() -> QtBinding:
    for candidate in (QtBinding.PYSIDE6, QtBinding.PYQT6):
        core_module_name, _ = _module_names(candidate)
        try:
            import_module(core_module_name)
        except ModuleNotFoundError:
            continue
        return candidate
    raise ModuleNotFoundError("Could not import PySide6 or PyQt6.")
