from flask import Blueprint, Response, abort, current_app, redirect, render_template, request, url_for

from laboratorio.models.participacion import is_valid_participation, normalize_identity
from laboratorio.services.enlaces import make_qr_svg
from laboratorio.web import valid_csrf

publico = Blueprint("publico", __name__)


@publico.get("/")
def index():
    current_app.extensions["eventos"].record("visita")
    return render_template("index.html")


@publico.get("/s/demo")
def short_link():
    current_app.extensions["eventos"].record("enlace_corto")
    return redirect(url_for("publico.index"))


@publico.post("/participar")
def participate():
    if not valid_csrf(request.form.get("csrf", "")):
        abort(400, "Sesion invalida. Recarga el formulario.")
    if not is_valid_participation(request.form):
        return render_template("index.html", error=(
            "Escribe un nombre que comience con 'Ejemplo ', un telefono de 10 digitos "
            "que comience con 000 y un correo terminado en @example.test. "
            "Confirma el mismo correo y acepta el registro local. No se guardo esta entrada.")), 400
    current_app.extensions["eventos"].record("envio_demo", normalize_identity(request.form))
    return redirect(url_for("publico.finished"), code=303)


@publico.get("/resultado")
def finished():
    return render_template("resultado.html")


@publico.get("/qr.svg")
def qr():
    return Response(make_qr_svg(current_app.config["BASE_URL"]), mimetype="image/svg+xml")
