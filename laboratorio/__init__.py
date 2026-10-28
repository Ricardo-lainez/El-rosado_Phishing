"""Fabrica de aplicacion: conecta modelos, vistas y controladores."""
import secrets
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask

from laboratorio.controllers.auth import auth
from laboratorio.controllers.instructor import instructor
from laboratorio.controllers.publico import publico
from laboratorio.models.bloqueo import LoginLockModel
from laboratorio.models.eventos import EventModel
from laboratorio.services.enlaces import validate_base_url
from laboratorio.web import configure_web

ROOT = Path(__file__).resolve().parent.parent


def create_app(database=None, base_url="http://127.0.0.1:5000", auth_clock=None):
    app = Flask(__name__, template_folder=str(ROOT / "templates"),
                static_folder=str(ROOT / "static"))
    app.config.update(SECRET_KEY=secrets.token_hex(32), MAX_CONTENT_LENGTH=8192,
                      SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                      DATABASE=str(database or ROOT / "data" / "laboratorio.sqlite3"),
                      BASE_URL=validate_base_url(base_url),
                      AUTH_CLOCK=auth_clock or (lambda: datetime.now(timezone.utc)))
    model = EventModel(app.config["DATABASE"])
    model.initialize()
    app.extensions["eventos"] = model
    auth_lock = LoginLockModel(app.config["DATABASE"])
    auth_lock.initialize()
    app.extensions["auth_lock"] = auth_lock
    app.register_blueprint(publico)
    app.register_blueprint(instructor)
    app.register_blueprint(auth)
    configure_web(app)
    return app
