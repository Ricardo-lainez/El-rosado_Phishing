"""Sesion, contexto de vistas y cabeceras de seguridad HTTP."""
import secrets

from flask import session

from laboratorio.models.participacion import DEMO


def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(32)
    return session["csrf"]


def valid_csrf(value):
    expected = session.get("csrf")
    return bool(expected and secrets.compare_digest(value.encode("utf-8"), expected.encode("utf-8")))


def configure_web(app):
    @app.context_processor
    def context():
        return {"csrf_token": csrf_token, "demo": DEMO,
                "lab_url": app.config["BASE_URL"] + "/s/demo"}

    @app.after_request
    def headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; img-src 'self' data:; "
            "script-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'")
        return response
