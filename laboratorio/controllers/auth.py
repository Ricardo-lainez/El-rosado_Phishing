"""Controlador de autenticacion de prueba para el laboratorio de seguridad."""
import time


# pyrefly: ignore[missing-import]
from flask import (
    Blueprint, current_app, redirect, render_template, request, session, url_for
)

from laboratorio.web import valid_csrf

auth = Blueprint("auth", __name__)

# ---------------------------------------------------------------------------
# Credenciales ficticias fijas — SOLO para el laboratorio academico.
# No usar contraseñas reales ni datos personales.
# ---------------------------------------------------------------------------
_DEMO_USER = "admin"
_DEMO_PASSWORD = "L4b0rat0r10!"   # noqa: S105 — contraseña ficticia de prueba

# Clave en session donde el integrante de NGINX/ZAP puede leer el estado.
SESSION_LOGIN_KEY = "lab_authenticated"


@auth.get("/login")
def login_form():
    """Muestra el formulario de inicio de sesion."""
    error = session.pop("login_error", None)
    return render_template("login.html", error=error)


@auth.post("/login")
def login_submit():
    """Procesa las credenciales enviadas.

    Consulta el bloqueo temporal antes de comprobar las credenciales.
    """
    if not valid_csrf(request.form.get("csrf", "")):
        session["login_error"] = "Sesión inválida. Recarga el formulario."
        return redirect(url_for("auth.login_form"))

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # SQLite registra el resultado sin guardar la contraseña ni el token CSRF.
    result = current_app.extensions["auth_lock"].process_attempt(
        lambda: username == _DEMO_USER and password == _DEMO_PASSWORD,
        source_ip=request.remote_addr,
        now=current_app.config["AUTH_CLOCK"](),
    )

    if result.status == "blocked":
        session.pop(SESSION_LOGIN_KEY, None)
        session.pop("login_user", None)
        session.pop("login_ts", None)
        session["login_error"] = (
            f"La cuenta está bloqueada temporalmente. Intenta nuevamente en "
            f"{result.retry_after} segundos."
        )
        return redirect(url_for("auth.login_form"), code=303)

    if result.status == "success":
        session[SESSION_LOGIN_KEY] = True
        session["login_user"] = username
        session["login_ts"] = time.time()
        return redirect(url_for("instructor.dashboard"))

    # Intento fallido: limpiar cualquier sesion previa.
    session.pop(SESSION_LOGIN_KEY, None)
    session.pop("login_user", None)
    session.pop("login_ts", None)
    session["login_error"] = (
        "La cuenta está bloqueada temporalmente durante 60 segundos."
        if result.status == "locked"
        else "Usuario o contraseña incorrectos."
    )
    return redirect(url_for("auth.login_form"), code=303)


@auth.get("/logout")
def logout():
    """Cierra la sesion activa."""
    session.pop(SESSION_LOGIN_KEY, None)
    session.pop("login_user", None)
    session.pop("login_ts", None)
    return redirect(url_for("publico.index"))
