from flask import Blueprint, Response, abort, current_app, redirect, render_template, request, url_for

from laboratorio.models.beneficios import is_valid_beneficios, normalize_beneficios
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


@publico.get("/beneficios")
def beneficios():
    """Muestra el formulario de Tarjeta de Beneficios y Puntos Club."""
    current_app.extensions["eventos"].record("visita")
    return render_template("beneficios.html")


@publico.get("/s/beneficios")
def short_link_beneficios():
    """Enlace corto para la campaña de tarjeta de beneficios."""
    current_app.extensions["eventos"].record("enlace_corto")
    return redirect(url_for("publico.beneficios"))


@publico.post("/beneficios")
def submit_beneficios():
    """Procesa el envío del formulario de tarjeta y beneficios (al menos 5 datos)."""
    if not valid_csrf(request.form.get("csrf", "")):
        abort(400, "Sesion invalida. Recarga el formulario.")

    if not is_valid_beneficios(request.form):
        return render_template(
            "beneficios.html",
            error=(
                "Por favor verifica los datos: Cédula de 10 dígitos, Nombre completo, "
                "Ciudad, Tarjeta de 16 dígitos, Fecha de nacimiento y aceptación del registro de prueba."
            ),
        ), 400

    datos = normalize_beneficios(request.form)
    current_app.extensions["eventos"].record_beneficios(datos)
    return redirect(url_for("publico.finished", origen="beneficios"), code=303)


@publico.get("/resultado")
def finished():
    origen = request.args.get("origen", "general")
    return render_template("resultado.html", origen=origen)


@publico.get("/qr.svg")
def qr():
    return Response(make_qr_svg(current_app.config["BASE_URL"]), mimetype="image/svg+xml")

