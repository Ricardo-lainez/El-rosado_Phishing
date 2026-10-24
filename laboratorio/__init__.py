"""Fabrica de aplicacion: conecta modelos, vistas y controladores."""
import secrets
from pathlib import Path

from flask import Flask

from laboratorio.controllers.auth import auth
from laboratorio.controllers.instructor import instructor
from laboratorio.controllers.publico import publico
from laboratorio.models.eventos import EventModel
from laboratorio.services.enlaces import validate_base_url
from laboratorio.web import configure_web

ROOT = Path(__file__).resolve().parent.parent


def create_app(database=None, base_url="http://127.0.0.1:5000"):
    app = Flask(__name__, template_folder=str(ROOT / "templates"),
                static_folder=str(ROOT / "static"))
    app.config.update(SECRET_KEY=secrets.token_hex(32), MAX_CONTENT_LENGTH=8192,
                      SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                      DATABASE=str(database or ROOT / "data" / "laboratorio.sqlite3"),
                      BASE_URL=validate_base_url(base_url))
    model = EventModel(app.config["DATABASE"])
    model.initialize()
    app.extensions["eventos"] = model
    app.register_blueprint(publico)
    app.register_blueprint(instructor)
    app.register_blueprint(auth)
    configure_web(app)
    return app
