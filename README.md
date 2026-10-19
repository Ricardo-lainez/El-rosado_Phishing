# Super Mercado — formulario local con arquitectura MVC

Formulario de contacto con marca propia, interfaz roja y blanca, datos sintéticos editables, registro SQLite, panel local, QR y correo para Mailpit. Se ejecuta en una computadora; los teléfonos pueden acceder por la misma red local.

## Documentación del equipo

- **[Guía completa: instalar, usar en computadora y acceder desde el teléfono](docs/GUIA_EQUIPO.md)**.
- **[Preparación y revisión antes de publicar el repositorio](docs/PUBLICACION.md)**.

La guía incluye las descargas oficiales, clonación o ZIP, instalación, direcciones de acceso, formatos aceptados, ubicación de los registros, configuración de IP/puerto, correo local y solución de problemas.

## Inicio rápido en Windows

Instala [Python 3.14](https://www.python.org/downloads/windows/), descarga el proyecto y abre PowerShell en la carpeta que contiene `app.py`. Ejecuta una vez:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Después, para iniciar:

```powershell
.\.venv\Scripts\python.exe app.py
```

Deja esa terminal abierta y visita:

| Dirección en la computadora servidor | Uso |
| --- | --- |
| http://127.0.0.1:5000 | Formulario |
| http://127.0.0.1:5000/admin | Registros y QR |
| http://127.0.0.1:5000/qr.svg | Imagen del QR |

Detén el servidor con **Ctrl+C**. No necesitas activar el entorno virtual ni instalar un servidor de base de datos. Las versiones de `requirements-lock.txt` fueron verificadas en Windows con Python 3.14.7; `requirements.txt` mantiene los rangos para futuras actualizaciones.

## Acceso desde el teléfono

Conecta computadora y teléfono al mismo Wi-Fi. Ejecuta `ipconfig` en la computadora, identifica la IPv4 del adaptador conectado y sustituye la IP de ejemplo en el comando:

```powershell
.\.venv\Scripts\python.exe app.py --lan --base-url http://192.168.1.20:5000
```

En el teléfono abre `http://192.168.1.20:5000` con la IP real de esa computadora, o escanea el QR mostrado en su panel local. El teléfono solo necesita un navegador. El panel `/admin` se consulta desde la computadora servidor usando `127.0.0.1`.

Si no conecta, consulta el [paso de acceso LAN y los problemas frecuentes](docs/GUIA_EQUIPO.md). `127.0.0.1` en un teléfono apunta al propio teléfono. Publicar el repositorio comparte el código; no hace accesible tu servidor desde Internet.

## Datos que acepta

Los campos son editables dentro de estos formatos sintéticos:

| Campo | Ejemplo y regla |
| --- | --- |
| Nombre | `Ejemplo Cliente Dos`: comienza con `Ejemplo ` |
| Teléfono | `0001234567`: diez dígitos, comenzando con `000` |
| Correo y confirmación | `cliente.dos@example.test`: elige un alias y conserva `@example.test` |
| Consentimiento | Marca la aceptación del registro local |

Al enviar, se muestra una confirmación propia. Los valores válidos se guardan en `data/laboratorio.sqlite3`, disponible en el panel del servidor. La base se crea automáticamente y está excluida de Git. Cada copia ejecutada tiene sus propios registros.

## Correo local opcional

La [guía del equipo](docs/GUIA_EQUIPO.md) explica cómo descargar y abrir Mailpit. Con Mailpit ejecutándose en la computadora servidor:

```powershell
.\.venv\Scripts\python.exe preparar_correo.py --base-url http://192.168.1.20:5000 --mailpit
```

Sustituye la IP por la que usaste al iniciar el servidor. Abre http://127.0.0.1:8025 en esa computadora para ver el correo. El script entrega solo al SMTP local `127.0.0.1:1025`; no envía a cuentas reales de Gmail, Hotmail u Outlook.

Sin `--mailpit`, solo genera el mensaje `.eml` y el QR en `artifacts/`. Esos archivos no se comparten por Git. El envío del formulario no envía correos automáticamente.

## Estructura MVC

```text
app.py                         Inicio del servidor Waitress
preparar_correo.py              Entrada de consola para correo y QR
laboratorio/
  __init__.py                  Fábrica y configuración de la aplicación
  web.py                       Sesiones, CSRF y cabeceras HTTP
  controllers/                 Rutas públicas y panel local
  models/                      Validación de datos sintéticos y SQLite
  services/                    Generación de enlaces, QR y correo local
templates/                     Vistas HTML con Jinja
static/                        CSS y JavaScript
tests/                         Pruebas funcionales y del modelo
docs/                          Guía del equipo y preparación de publicación
requirements.txt               Rangos de dependencias
requirements-lock.txt          Versiones verificadas
```

El controlador recibe la petición y utiliza el modelo para validar y guardar. Después devuelve una vista. El SQL está en el modelo; la construcción del correo y del QR está en servicios reutilizables.

## Verificación

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas usan bases temporales y no envían mensajes. Cubren el envío de datos sintéticos, validaciones, consentimiento, CSRF, acceso local al panel, persistencia, QR y construcción del correo.

Antes de subir el código, revisa [PUBLICACION.md](docs/PUBLICACION.md), especialmente los archivos excluidos y la identidad de los commits existentes. El informe académico queda fuera de esta entrega.
