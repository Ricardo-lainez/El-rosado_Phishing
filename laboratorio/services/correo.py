"""Construccion del correo y entrega opcional al buzon local de pruebas."""
import smtplib
from email.message import EmailMessage
from html import escape

from laboratorio.services.enlaces import make_qr_svg, validate_base_url


def prepare(base_url, output):
    base = validate_base_url(base_url)
    url = base + "/s/demo"
    qr_url = base + "/qr.svg"
    output.mkdir(parents=True, exist_ok=True)
    message = EmailMessage()
    message["From"] = "Super Mercado <seguridad@example.test>"
    message["To"] = "Usuario de prueba <cliente@example.test>"
    message["Subject"] = "Super Mercado | Actualización obligatoria de parámetros"
    message.set_content(f"""Estimado usuario de Super Mercado:

Le informamos que se requiere la actualización y verificación inmediata de sus parámetros de contacto y registro en la plataforma.

Para modificar y confirmar sus parámetros, escanee el código QR adjunto a este mensaje o ingrese directamente al siguiente enlace seguro:
{url}

También puede visualizar directamente el código QR de acceso en:
{qr_url}

Instrucciones para la práctica de laboratorio (datos sintéticos):
- Nombre que comience con 'Ejemplo ', como Ejemplo Cliente.
- Teléfono de 10 dígitos que comience con 000, como 0001234567.
- Correo terminado en @example.test, como cliente@example.test.

Aviso educativo: Este es un simulador académico local. No ingrese contraseñas ni datos personales reales.

Atentamente,
Departamento de Seguridad y Cuentas - Super Mercado
""")
    message.add_alternative(f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #1e293b; padding: 20px; }}
    .card {{ max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
    .header {{ border-bottom: 2px solid #ef4444; padding-bottom: 12px; margin-bottom: 20px; }}
    .header h1 {{ color: #dc2626; margin: 0; font-size: 22px; }}
    .alert-box {{ background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 12px 16px; margin: 16px 0; border-radius: 4px; font-size: 14px; color: #991b1b; }}
    .btn {{ display: inline-block; background-color: #dc2626; color: #ffffff !important; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; margin: 16px 0; text-align: center; }}
    .qr-info {{ background: #f1f5f9; padding: 16px; border-radius: 6px; text-align: center; margin-top: 20px; }}
    .footer {{ font-size: 12px; color: #64748b; margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 12px; text-align: center; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1>Super Mercado</h1>
    </div>
    <p>Estimado usuario:</p>
    <div class="alert-box">
      <strong>Aviso de seguridad:</strong> Se ha detectado una solicitud para cambiar o verificar los parámetros de su cuenta. Es necesario que confirme sus datos para mantener el servicio activo.
    </div>
    <p>Puede actualizar sus parámetros accediendo mediante el enlace o escaneando el código QR adjunto:</p>
    <p style="text-align: center;">
      <a class="btn" href="{escape(url)}">Actualizar parámetros ahora</a>
    </p>
    <div class="qr-info">
      <p style="margin: 0 0 8px 0; font-weight: 600;">Acceso rápido mediante Código QR:</p>
      <p style="margin: 0; font-size: 13px;">Abra el archivo adjunto <strong>qr-laboratorio.svg</strong> o consulte el QR en línea:</p>
      <p><a href="{escape(qr_url)}">Ver código QR en el navegador</a></p>
    </div>
    <div class="footer">
      <p>Entorno de prueba académica. Ingrese únicamente datos sintéticos con formato de ejemplo (@example.test). No ingrese contraseñas reales.</p>
      <p>&copy; Super Mercado - Sistema de Verificación</p>
    </div>
  </div>
</body>
</html>""", subtype="html")
    qr_path = output / "qr-laboratorio.svg"
    qr_path.write_bytes(make_qr_svg(base_url))
    message.add_attachment(qr_path.read_bytes(), maintype="image", subtype="svg+xml", filename=qr_path.name)
    path = output / "invitacion-laboratorio.eml"
    path.write_bytes(message.as_bytes())
    return message, path


def deliver_to_mailpit(message):
    with smtplib.SMTP("127.0.0.1", 1025, timeout=5) as smtp:
        smtp.send_message(message)
