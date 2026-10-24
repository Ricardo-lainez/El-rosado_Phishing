# wsgi.py — punto de entrada para mod_wsgi (Apache HTTP Server)
#
# Apache carga este archivo una sola vez al arrancar.
# La variable 'application' es el objeto WSGI que mod_wsgi espera.
#
# USO:
#   En el VirtualHost de Apache:
#       WSGIScriptAlias / "C:/ruta/al/proyecto/wsgi.py"
#       WSGIDaemonProcess supermercado python-home="C:/ruta/al/venv" \
#           python-path="C:/ruta/al/proyecto"
#       WSGIProcessGroup supermercado
#
# NOTA: Ajusta BASE_URL al nombre o IP real con la que Apache sirve el sitio.
# Si Apache escucha en el puerto 80: http://127.0.0.1
# Si escucha en el puerto 8080:     http://127.0.0.1:8080

import sys
from pathlib import Path

# Asegura que Python encuentre el paquete 'laboratorio'
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from laboratorio import create_app  # noqa: E402

application = create_app(base_url="http://127.0.0.1")
