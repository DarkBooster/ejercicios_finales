import os
from pathlib import Path

from flask import Flask


def create_app() -> Flask:
    root_dir = Path(__file__).resolve().parents[1]
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(root_dir / "templates"),
        static_folder=str(root_dir / "static"),
    )

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        TASKS_FILE=str(Path(app.instance_path) / "tasks.json"),
    )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from .routes import bp as main_bp

    app.register_blueprint(main_bp)

    return app

