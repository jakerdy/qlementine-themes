from __future__ import annotations

import json
import re
from pathlib import Path

from PySide6.QtCore import QJsonDocument
from PySide6.QtWidgets import QApplication
from PySide6Qlementine import QlementineStyle, Theme

from .constants import THEMES_DIR


def load_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def save_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def built_in_theme_paths() -> list[Path]:
    return sorted(
        path for path in THEMES_DIR.glob("*.json") if path.name != "_common_.json"
    )


def load_repo_theme(theme_id: str) -> Theme:
    common = load_json(THEMES_DIR / "_common_.json")
    theme_layer = load_json(THEMES_DIR / f"{theme_id}.json")
    return Theme.fromJsonDoc(QJsonDocument.fromVariant(common | theme_layer))


def theme_display_name(path: Path) -> str:
    try:
        payload = load_json(path)
    except (OSError, json.JSONDecodeError):
        return path.stem.replace("-", " ").title()
    meta = payload.get("meta")
    if isinstance(meta, dict):
        name = meta.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return path.stem.replace("-", " ").title()


def copy_theme(theme: Theme) -> Theme:
    return Theme.fromJsonDoc(theme.toJson())


def theme_to_bytes(theme: Theme) -> bytes:
    return bytes(theme.toJson().toJson(QJsonDocument.JsonFormat.Indented).data())


def theme_to_dict(theme: Theme) -> dict[str, object]:
    return json.loads(theme_to_bytes(theme).decode("utf-8"))


def preset_payload_from_theme(theme: Theme) -> dict[str, object]:
    payload = theme_to_dict(theme)
    common_keys = set(load_json(THEMES_DIR / "_common_.json"))
    preset_payload = {
        key: value
        for key, value in payload.items()
        if key == "meta" or key not in common_keys
    }
    meta = preset_payload.get("meta")
    if not isinstance(meta, dict):
        preset_payload["meta"] = {
            "name": theme.meta.name,
            "author": theme.meta.author,
            "version": theme.meta.version,
        }
    return preset_payload


def preset_file_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return slug or "new-theme"


def ensure_qlementine_style(app: QApplication) -> QlementineStyle:
    style = app.style()
    if isinstance(style, QlementineStyle):
        return style
    qlementine_style = QlementineStyle(app)
    app.setStyle(qlementine_style)
    return qlementine_style
