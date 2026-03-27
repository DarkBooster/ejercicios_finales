from __future__ import annotations

from flask import Blueprint, abort, current_app, redirect, render_template, request, url_for

from .storage import load_tasks, save_tasks

bp = Blueprint("main", __name__)

def _tasks_file() -> str:
    return str(current_app.config["TASKS_FILE"])


def _get_tasks() -> list[dict]:
    return load_tasks(_tasks_file())


def _next_id(tasks: list[dict]) -> int:
    return (max((t["id"] for t in tasks), default=0)) + 1


@bp.get("/")
def index():
    tareas = _get_tasks()
    return render_template("index.html", tareas=tareas)


@bp.post("/agregar")
def agregar():
    texto = (request.form.get("texto") or "").strip()
    tareas = _get_tasks()
    if texto:
        tareas.append({"id": _next_id(tareas), "texto": texto, "hecho": False})
        save_tasks(_tasks_file(), tareas)

    return redirect(url_for("main.index"))


@bp.post("/completar/<int:tarea_id>")
def completar(tarea_id: int):
    tareas = _get_tasks()
    for t in tareas:
        if t["id"] == tarea_id:
            t["hecho"] = True
            save_tasks(_tasks_file(), tareas)
            return redirect(url_for("main.index"))

    abort(404)


@bp.post("/eliminar/<int:tarea_id>")
def eliminar(tarea_id: int):
    tareas = _get_tasks()
    nuevas = [t for t in tareas if t["id"] != tarea_id]
    if len(nuevas) == len(tareas):
        abort(404)

    save_tasks(_tasks_file(), nuevas)
    return redirect(url_for("main.index"))


@bp.get("/editar/<int:tarea_id>")
def editar_form(tarea_id: int):
    tareas = _get_tasks()
    for t in tareas:
        if t["id"] == tarea_id:
            return render_template("edit.html", tarea=t)
    abort(404)


@bp.post("/editar/<int:tarea_id>")
def editar_guardar(tarea_id: int):
    texto = (request.form.get("texto") or "").strip()
    if not texto:
        return redirect(url_for("main.editar_form", tarea_id=tarea_id))

    tareas = _get_tasks()
    for t in tareas:
        if t["id"] == tarea_id:
            t["texto"] = texto
            save_tasks(_tasks_file(), tareas)
            return redirect(url_for("main.index"))

    abort(404)

