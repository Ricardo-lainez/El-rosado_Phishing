# Guía del equipo: computadora, teléfono y correo local

Esta guía usa Windows y PowerShell. Los comandos se ejecutan en la carpeta que contiene `app.py`, salvo que se indique otra cosa. No hace falta editar el código para instalar o cambiar la IP.

## 1. Elegir cómo va a trabajar el grupo

| Modalidad | Quién instala | Dónde quedan los registros |
| --- | --- | --- |
| Cada compañero ejecuta su copia | Cada computadora instala Python y las dependencias | En la computadora de cada compañero |
| Una computadora sirve para todo el grupo | Solo esa computadora instala y ejecuta el proyecto; los demás usan navegador | Todos los envíos llegan a esa computadora |

En la segunda modalidad, los teléfonos y otras computadoras deben conectarse a la misma red local. El teléfono no necesita Python, Git ni una aplicación especial.

Publicar el repositorio comparte el código. No enciende un servidor ni hace accesible tu computadora desde Internet. Las bases de datos de las distintas copias no se sincronizan mediante Git.

## 2. Qué instalar en la computadora que ejecutará el servidor

| Componente | ¿Es necesario? | Instalación o descarga |
| --- | --- | --- |
| Python 3.14 | Sí | [Descarga oficial para Windows](https://www.python.org/downloads/windows/). Escoge la versión 3.14; el proyecto fue verificado con 3.14.7. |
| Git | Para clonar y actualizar; opcional si descargas ZIP | [Git para Windows](https://git-scm.com/install/windows) |
| Flask, Waitress, qrcode y dependencias | Sí | El comando de instalación del paso 4 las descarga automáticamente. |
| SQLite | Sí, pero ya está incluido | Forma parte de Python; no hay que instalar un servidor de base de datos. |
| Mailpit | Solo para probar la recepción del correo | [Instalación oficial](https://mailpit.axllent.org/docs/install/) |
| Visual Studio Code | Opcional | Cualquier editor sirve; también puedes usar solo PowerShell. |

No necesitas XAMPP, MySQL, Apache, Node.js ni Docker. La primera instalación de dependencias necesita Internet. Después, el formulario puede usarse en la red local sin servicios externos.

Tras instalar Python y Git, cierra y abre PowerShell. Comprueba:

```powershell
python --version
git --version
```

Si `python` no funciona pero `py` sí, usa `py -3.14` en lugar de `python` para crear el entorno del paso 4. Una vez creado, utiliza siempre `.\.venv\Scripts\python.exe`.

## 3. Descargar el proyecto

En la página del repositorio, pulsa **Code** y copia su dirección HTTPS. Sustituye `USUARIO` y `REPOSITORIO` antes de ejecutar:

```powershell
git clone https://github.com/USUARIO/REPOSITORIO.git
cd REPOSITORIO
```

También puedes usar **Code → Download ZIP**, descomprimirlo y abrir PowerShell en la carpeta descomprimida que contiene `app.py`. No lo ejecutes desde dentro del ZIP.

Si abres el proyecto en VS Code, utiliza **Terminal → New Terminal**. Verifica que estás en la carpeta correcta:

```powershell
Get-ChildItem app.py, requirements-lock.txt
```

## 4. Preparar el entorno: una vez por computadora

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

`requirements-lock.txt` fija las versiones verificadas para que el grupo utilice las mismas dependencias. `requirements.txt` contiene los rangos permitidos para futuras actualizaciones deliberadas.

No hace falta activar el entorno virtual ni cambiar la política de ejecución de PowerShell. Cada compañero crea su propia `.venv`; esa carpeta no se comparte por Git.

## 5. Abrirlo solo en la computadora

Ejecuta:

```powershell
.\.venv\Scripts\python.exe app.py
```

Deja esta terminal abierta. Cuando veas las direcciones de inicio, abre un navegador:

| Dirección | Qué muestra |
| --- | --- |
| http://127.0.0.1:5000 | Formulario de Super Mercado |
| http://127.0.0.1:5000/admin | Panel de registros y QR |
| http://127.0.0.1:5000/instructor | Alias del mismo panel |
| http://127.0.0.1:5000/qr.svg | QR del enlace configurado |
| http://127.0.0.1:5000/s/demo | Enlace corto que lleva al formulario |

El servidor es el proceso Python que aparece en esa terminal. El navegador solo muestra su página. Al cerrar la terminal o pulsar **Ctrl+C**, el sitio deja de responder. No se abre automáticamente en el navegador.

## 6. Completar el formulario

Puedes escribir distintos datos sintéticos. El botón **Usar un ejemplo** es opcional.

| Campo | Regla | Ejemplo |
| --- | --- | --- |
| Nombre | Comienza con `Ejemplo `; después admite entre 2 y 65 letras, números, espacios o los signos `_ . ' -` | `Ejemplo Cliente Dos` |
| Teléfono | Exactamente diez dígitos; empieza con `000` | `0001234567` |
| Correo | Alias de hasta 64 caracteres en `@example.test`; empieza y termina en letra o número | `cliente.dos@example.test` |
| Confirmación | Repite el correo; se ignoran diferencias de mayúsculas | `cliente.dos@example.test` |
| Consentimiento | Debe estar marcado | Aceptación del registro local |

El alias del correo admite letras, números y los signos `. _ + -` en su interior. `example.test` se usa como dirección de ejemplo: no es una cuenta que tengas que crear ni un buzón al que este formulario escriba.

Pulsa **Enviar formulario**. Si la entrada es válida, verás **Recibimos tu formulario**. Si falla la validación, aparecerá el formato requerido y no se guardarán los valores rechazados. El formulario no envía automáticamente un correo de confirmación.

## 7. Abrirlo desde uno o varios teléfonos

### A. Encontrar la IP de la computadora servidor

Conecta la computadora y los teléfonos al mismo Wi-Fi. En la computadora ejecuta:

```powershell
ipconfig
```

Busca **Dirección IPv4 / IPv4 Address** en el adaptador Wi-Fi que estés usando. Si usas cable, busca el adaptador Ethernet conectado al router. El adaptador activo suele mostrar una puerta de enlace predeterminada. Evita copiar IP de adaptadores desconectados, VPN o adaptadores virtuales.

En los comandos de abajo, `192.168.1.20` es solo un ejemplo: cámbialo por la IP de la computadora que ejecutará el servidor. No copies la IP de otro compañero. Puede cambiar al conectarte a otra red.

### B. Reiniciar el servidor en modo LAN

Si ya estaba abierto, detén el proceso anterior con **Ctrl+C**. Después inicia:

```powershell
.\.venv\Scripts\python.exe app.py --lan --base-url http://192.168.1.20:5000
```

- `--lan` permite conexiones desde otros dispositivos de la red.
- `--base-url` establece el destino del QR y de los enlaces mostrados en el panel.
- Esta URL no cambia la IP de Windows ni configura el router.

Si Windows solicita permiso del firewall, permite Python/Waitress solo en la red privada de confianza que utilizarán. No desactives el firewall completo.

### C. Abrir en el teléfono

En Chrome, Safari u otro navegador del teléfono escribe la dirección completa:

```text
http://192.168.1.20:5000
```

Usa la IP que encontraste y escribe `http://`. No uses `https://`, `0.0.0.0` ni `127.0.0.1`. En el teléfono, `127.0.0.1` apunta al propio teléfono.

Puedes abrir la misma dirección desde otro teléfono o una computadora del grupo conectada a esa red. Esos dispositivos solo necesitan navegador.

### D. Usar el QR

En la computadora servidor abre http://127.0.0.1:5000/admin. Comprueba que el enlace mostrado usa la IP LAN correcta y escanea el QR con la cámara del teléfono. El QR y el enlace llevan al mismo formulario.

El panel `/admin` y su alias `/instructor` solo se abren desde la computadora servidor usando `127.0.0.1`. Un **403** al intentar abrirlos desde el teléfono es el comportamiento esperado.

## 8. Ver dónde quedaron los envíos

En la computadora servidor abre http://127.0.0.1:5000/admin y recarga después de un envío. El panel no se actualiza automáticamente.

- `visita`: se abrió el formulario.
- `enlace_corto`: se utilizó `/s/demo` por enlace o QR.
- `envio_demo`: se aceptaron y guardaron los datos sintéticos; se conserva este nombre interno por compatibilidad.

La tabla muestra los últimos 200 eventos. Los contadores corresponden a todos los eventos guardados, no a personas únicas. Enlace y QR comparten destino, por lo que no se distingue cuál se usó.

Los datos están en `data/laboratorio.sqlite3`, dentro de esta copia del proyecto. La carpeta y la base se crean automáticamente. Las fechas se guardan en UTC; para Ecuador continental, resta cinco horas.

Los registros permanecen al reiniciar el servidor. No se imprimen los campos del formulario en la terminal ni se crea `datos_capturados.txt`. Cada computadora que ejecute su copia tiene una base independiente.

## 9. Generar correo y QR como archivos

Con el servidor encendido, abre una **segunda terminal** en la carpeta del proyecto:

```powershell
.\.venv\Scripts\python.exe preparar_correo.py --base-url http://192.168.1.20:5000
```

Usa la misma IP y puerto que en el servidor. Para uso exclusivo en la computadora puedes omitir `--base-url`; usará `http://127.0.0.1:5000`.

Archivos generados:

- `artifacts/invitacion-laboratorio.eml`: mensaje con texto, HTML y QR adjunto.
- `artifacts/qr-laboratorio.svg`: imagen del QR.

Generar estos archivos no envía correos. Al volver a ejecutar el comando, se reemplazan con la URL indicada. Si cambia la IP o el puerto, reinicia el servidor con la nueva URL y regenera estos archivos.

## 10. Recibir el correo en Mailpit: opcional

El correo se entrega a un buzón local. No necesitas cuentas de correo, contraseñas ni archivos `.env`.

1. Descarga el archivo de Windows adecuado para tu arquitectura desde la [documentación oficial de Mailpit](https://mailpit.axllent.org/docs/install/).
2. Descomprímelo en una carpeta fuera del repositorio.
3. Abre una terminal en esa carpeta e inicia:

```powershell
.\mailpit.exe --listen 127.0.0.1:8025 --smtp 127.0.0.1:1025
```

Deja Mailpit abierto. En otra terminal situada en el proyecto ejecuta:

```powershell
.\.venv\Scripts\python.exe preparar_correo.py --base-url http://192.168.1.20:5000 --mailpit
```

Abre http://127.0.0.1:8025 **en la computadora servidor**. Verás el mensaje de Super Mercado, su enlace y el QR adjunto. Puedes abrir el enlace desde esa computadora o escanear el adjunto desde el teléfono.

| Puerto | Servicio | Dónde se usa |
| --- | --- | --- |
| 5000 | Sitio web | Computadora y, con `--lan`, dispositivos de la red |
| 8025 | Bandeja web de Mailpit | Navegador de la computadora servidor |
| 1025 | SMTP de Mailpit | Lo utiliza el script; no se abre en el navegador |

Para el flujo completo suelen quedar tres terminales: servidor web, Mailpit y comandos de generación/entrega. El envío se realiza solo cuando ejecutas `preparar_correo.py --mailpit`; completar el formulario no dispara otro correo.

Los destinatarios `@example.test` se ven en Mailpit. No llega ningún mensaje a Gmail, Hotmail u Outlook. La bandeja de Mailpit se mantiene local y no se abre desde el teléfono con esta configuración. Su almacenamiento predeterminado es temporal; guarda las evidencias necesarias antes de cerrarlo. Consulta las [opciones oficiales](https://mailpit.axllent.org/docs/configuration/runtime-options/) para otros ajustes de almacenamiento.

## 11. Qué cambiar y qué dejar tal como está

| Necesidad | Qué hacer |
| --- | --- |
| Usar otra computadora | Descargar y crear su propia `.venv`; no copiar una `.venv` ajena |
| Usar otro Wi-Fi | Obtener su nueva IPv4, reiniciar con `--base-url` y regenerar correo/QR |
| Puerto 5000 ocupado | Detener la otra instancia o elegir otro puerto con `--port` |
| Cambiar el texto de las páginas | Editar `templates/` |
| Cambiar los estilos | Editar `static/styles.css` |
| Cambiar el texto del correo local | Editar `laboratorio/services/correo.py` |
| Ver los formatos aceptados | Consultar `laboratorio/models/participacion.py` |
| Cambiar el dominio del correo para usar Mailpit | No hace falta: conserva `example.test` |

Ejemplo con puerto alternativo; cambia también la URL del navegador y la del correo:

```powershell
.\.venv\Scripts\python.exe app.py --lan --port 5001 --base-url http://192.168.1.20:5001
```

Después de editar Python o plantillas, reinicia el servidor con **Ctrl+C** y el comando correspondiente; el proceso no tiene recarga automática. Si cambias CSS o JavaScript, recarga también el navegador.

## 12. Problemas frecuentes

| Problema | Qué comprobar |
| --- | --- |
| `python` no se reconoce o abre Microsoft Store | Instala Python 3.14, reabre PowerShell o prueba `py -3.14 --version` |
| No existe `.venv\Scripts\python.exe` | Estás en otra carpeta o falta crear el entorno del paso 4 |
| `ModuleNotFoundError` | Instala `requirements-lock.txt` usando el Python de `.venv` |
| No abre ni en la computadora | Comprueba que el servidor siga ejecutándose y que la URL/puerto coincidan |
| Abre en computadora, pero no en teléfono | Revisa `--lan`, IPv4 actual, mismo Wi-Fi, permiso del firewall y aislamiento de clientes/red de invitados |
| `127.0.0.1` muestra una versión y la IP LAN otra | Detén las instancias anteriores con Ctrl+C y deja solo una instancia actual con `--lan`. El inicio ahora reserva el puerto de forma exclusiva en Windows y avisa si está ocupado. Recarga el navegador con Ctrl+F5. |
| El inicio indica que no pudo reservar el puerto | Hay otra instancia o aplicación usando ese puerto, o Windows no permite reservarlo. Cierra la instancia anterior o elige `--port 5001` y actualiza `--base-url` con ese mismo puerto. |
| El teléfono está usando datos móviles | Conéctalo a la misma red local del servidor |
| El QR abre `127.0.0.1` o una IP anterior | Reinicia con el `--base-url` correcto; regenera los archivos del correo |
| `/admin` devuelve 403 | Ábrelo en la computadora servidor mediante `http://127.0.0.1:5000/admin` |
| El formulario rechaza los campos | Respeta los formatos del paso 6, la confirmación y el consentimiento |
| Error de sesión tras reiniciar | Recarga el formulario antes de volver a enviarlo |
| No conecta a Mailpit | Comprueba que `mailpit.exe` esté abierto en la misma computadora y SMTP escuche en `127.0.0.1:1025` |
| El correo no llega a Hotmail | El proyecto utiliza el buzón Mailpit local; abre el puerto 8025 |
| GitHub muestra archivos pero no funciona la página | El repositorio distribuye código; hay que ejecutar Python localmente |

La IP LAN solo funciona dentro de la red que la administra. No abras puertos en el router ni uses túneles públicos para seguir esta guía. En redes universitarias con aislamiento puede ser necesario usar una red de prueba autorizada donde los dispositivos puedan comunicarse.

## 13. Verificación y actualización del proyecto

Antes de la sesión del grupo, ejecuta:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas usan bases temporales y no envían mensajes. Luego comprueba manualmente: formulario en computadora, envío sintético, registro en `/admin`, acceso desde teléfono y correo en Mailpit si lo usarán.

Para actualizar una copia clonada, detén el servidor. Si tienes cambios propios, guárdalos en un commit o resuélvelos antes de actualizar; no los borres para forzar la descarga. Después:

```powershell
git pull --ff-only
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Vuelve a iniciar el servidor. Si descargaste ZIP, utiliza una nueva carpeta para la versión nueva; tus registros permanecen en la copia anterior.
