from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_tasks(path: str) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []

    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []

    tasks: list[dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if "id" not in item or "texto" not in item or "hecho" not in item:
            continue
        tasks.append(
            {
                "id": int(item["id"]),
                "texto": str(item["texto"]),
                "hecho": bool(item["hecho"]),
            }
        )
    tasks.sort(key=lambda t: t["id"])
    return tasks


def save_tasks(path: str, tasks: list[dict[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    tmp.replace(p)

