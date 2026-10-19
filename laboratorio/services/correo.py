"""Construccion del correo y entrega opcional al buzon local de pruebas."""
import smtplib
from email.message import EmailMessage
from html import escape

from laboratorio.services.enlaces import make_qr_svg, validate_base_url


def prepare(base_url, output):
    url = validate_base_url(base_url) + "/s/demo"
    output.mkdir(parents=True, exist_ok=True)
    message = EmailMessage()
    message["From"] = "Super Mercado <contacto@example.test>"
    message["To"] = "Contacto de ejemplo <cliente@example.test>"
    message["Subject"] = "Super Mercado | Formulario de contacto"
    message.set_content(f"""Hola:

Puedes completar el formulario de Super Mercado desde esta direccion:
{url}

Tambien puedes utilizar el QR adjunto desde un dispositivo conectado a la
misma red del servidor.

Escribe datos de ejemplo elegidos por ti:
- Nombre que comience con 'Ejemplo ', como Ejemplo Cliente.
- Telefono de 10 digitos que comience con 000, como 0001234567.
- Correo con un alias terminado en @example.test, como cliente@example.test.

El formulario guarda estos datos sinteticos en este servidor para comprobar
su funcionamiento. No uses datos personales.

Super Mercado
""")
    message.add_alternative(f"""<!doctype html><html lang="es"><body>
<h1>Super Mercado</h1><p>Hola:</p>
<p>Puedes completar nuestro formulario con datos de ejemplo elegidos por ti.</p>
<p><a href="{escape(url)}">Abrir formulario: {escape(url)}</a></p>
<ul><li>Nombre que comience con <strong>Ejemplo </strong>.</li>
<li>Telefono de 10 digitos que comience con <strong>000</strong>.</li>
<li>Correo terminado en <strong>@example.test</strong>.</li></ul>
<p>Los datos sinteticos se guardan en este servidor para comprobar el formulario.
No uses datos personales.</p>
<p>El QR adjunto abre la misma direccion desde un dispositivo en la misma red.</p>
<p>Super Mercado</p></body></html>""", subtype="html")
    qr_path = output / "qr-laboratorio.svg"
    qr_path.write_bytes(make_qr_svg(base_url))
    message.add_attachment(qr_path.read_bytes(), maintype="image", subtype="svg+xml", filename=qr_path.name)
    path = output / "invitacion-laboratorio.eml"
    path.write_bytes(message.as_bytes())
    return message, path


def deliver_to_mailpit(message):
    with smtplib.SMTP("127.0.0.1", 1025, timeout=5) as smtp:
        smtp.send_message(message)
