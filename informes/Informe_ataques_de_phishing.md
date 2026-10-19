# Ataques de phishing en un entorno local

Informe del proyecto Super Mercado

En este trabajo analizamos cómo un mensaje, un enlace y un formulario pueden intervenir en un ataque de phishing. Para estudiar ese recorrido, desarrollamos una aplicación local con la marca Super Mercado y datos de ejemplo. El resultado principal fue comprobar el funcionamiento del formulario, el registro de envíos y el direccionamiento local. Estas comprobaciones permiten explicar el proceso técnico, pero no demuestran que una persona haya sido engañada.

## 1 Tema

Ataques de phishing y análisis de un flujo de acceso mediante correo, enlace y código QR en una red local.

El proyecto aborda la relación entre la ingeniería social y los formularios web. La implementación utiliza una marca propia, una computadora como servidor y datos sintéticos para representar el ingreso de información sin utilizar datos personales de los participantes.

## 2 Objetivo

### Objetivo general

Analizar cómo funciona el phishing y comprender sus riesgos mediante la implementación de un entorno local que permita revisar el acceso a una página, el envío de datos de ejemplo y su registro en un servidor.

### Objetivos específicos

- Identificar las amenazas, vulnerabilidades y conductas humanas relacionadas con el phishing.
- Configurar un servidor web local y organizar el proyecto mediante la arquitectura Modelo Vista Controlador.
- Preparar un enlace corto local y un código QR como medios de acceso al formulario.
- Comprobar la validación y el almacenamiento de entradas sintéticas, así como la consulta de los registros.
- Proponer medidas para reconocer mensajes sospechosos y reducir la exposición de información personal.

## 3 Antecedentes y fundamentos

### 3 1 Phishing e ingeniería social

El phishing es una forma de engaño que busca que una persona entregue información o realice una acción a partir de un mensaje que aparenta ser confiable. Puede presentarse por correo, mensajes de texto u otros canales. Un caso común es una solicitud inesperada para confirmar datos o resolver un supuesto problema con una cuenta [1].

La ingeniería social aprovecha la manera en que las personas toman decisiones. En lugar de depender únicamente de una falla de un programa, intenta influir en la confianza, la atención o la preocupación de quien recibe el mensaje. Por eso, una página ordenada o un nombre conocido pueden generar confianza sin demostrar quién administra realmente el sitio.

En nuestro proyecto analizamos estas situaciones como antecedentes. La versión desarrollada usa Super Mercado y explica el uso de los datos de ejemplo. Por tanto, sirve para estudiar el recorrido técnico de un formulario y sus puntos de revisión, sin presentarse como un portal oficial de otra empresa.

### 3 2 Amenaza vulnerabilidad y riesgo

Una amenaza es una situación o acción que puede causar daño. Una vulnerabilidad es una debilidad que podría ser aprovechada. El riesgo considera la posibilidad de que ocurra un daño y sus consecuencias. Estas ideas se apoyan en las definiciones del glosario de seguridad del NIST [2].

En un caso de phishing, la amenaza puede ser una solicitud falsa de actualización de datos. La vulnerabilidad puede incluir hábitos de verificación insuficientes o controles de correo mal configurados. El riesgo sería la exposición de información, el uso indebido de una cuenta o una pérdida económica. El hecho de recibir un mensaje sospechoso no significa, por sí solo, que ese daño ya haya ocurrido.

### 3 3 Técnicas y comportamiento humano

Entre las técnicas relacionadas se encuentran la suplantación de remitentes, la imitación visual de páginas, las promesas de premios y la presión para actuar con rapidez. En el phishing mediante QR, también llamado quishing o QRishing, la dirección se presenta dentro de un código que debe leerse antes de conocer su destino. La FTC recomienda revisar esa dirección y comprobar por otro medio las solicitudes inesperadas [3].

Para el análisis del comportamiento humano consideramos la confianza en nombres conocidos, la curiosidad, la expectativa de obtener un beneficio y la tendencia a resolver una tarea rápidamente. No medimos estos factores en los compañeros. Los utilizamos para explicar por qué una persona podría omitir la revisión del remitente o del enlace.

Geisler y Pöhn estudiaron variantes de mensajes con QR y observaron que la presentación profesional podía atraer más atención en su contexto de estudio [4]. Este antecedente ayuda a formular preguntas para nuestra práctica, pero sus resultados no se pueden trasladar directamente a nuestro grupo.

### 3 4 Herramientas y funcionalidad

| Herramienta | Función dentro del proyecto |
| --- | --- |
| Python 3.14 | Ejecuta la aplicación y los scripts del proyecto. |
| Flask | Atiende las rutas, procesa el formulario y genera las respuestas HTML [5]. |
| Waitress | Sirve la aplicación web y permite acceder desde Windows y la red local [6]. |
| HTML CSS y JavaScript | Definen la estructura, los colores y las acciones del formulario en el navegador. |
| SQLite | Guarda los eventos y los datos sintéticos en una base local. |
| Mailpit | Recibe mensajes SMTP de prueba y permite consultarlos en una bandeja web local [7]. |
| qrcode | Genera el código QR a partir de la dirección configurada [8]. |
| Navegador y cámara del teléfono | Permiten abrir el enlace y leer el QR para acceder al formulario. |
| Git y GitHub | Permiten compartir el código y la documentación con el equipo. |

El correo local, el servidor web y la base de datos cumplen funciones distintas. Mailpit recibe el mensaje de prueba; Waitress sirve la página; SQLite conserva los registros del formulario.

## 4 Desarrollo

### 4 1 Preparación del entorno

Trabajamos con Python y un entorno virtual para separar las dependencias del proyecto. Las versiones verificadas quedaron registradas en requirements-lock.txt. La preparación se realiza desde PowerShell, en la carpeta que contiene app.py:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

No fue necesario instalar un servidor independiente de base de datos. SQLite utiliza un archivo que la aplicación crea cuando se inicia. También se preparó una guía para que cada compañero pueda instalar su copia sin utilizar rutas personales de otra computadora.

### 4 2 Organización del sitio mediante MVC

Organizamos el código con la arquitectura Modelo Vista Controlador. El modelo contiene las reglas de validación y las operaciones de SQLite. Las vistas están en templates y presentan el formulario, la confirmación y el panel. Los controladores reciben las peticiones y coordinan las respuestas.

Los servicios de correo y QR se ubicaron aparte para poder utilizarlos desde la aplicación y desde la consola. Esta separación facilita modificar una parte del proyecto sin mezclar el diseño de la página con las consultas a la base de datos.

El sitio de Super Mercado conserva los colores rojo y blanco. Solicita nombre, teléfono, correo y confirmación del correo. También informa que los valores de ejemplo se guardarán en el servidor y pide aceptar ese registro.

### 4 3 Configuración del servidor y direccionamiento

Para utilizar la aplicación únicamente desde la computadora se ejecuta:

```powershell
.\.venv\Scripts\python.exe app.py
```

El formulario se abre en http://127.0.0.1:5000 y el panel en http://127.0.0.1:5000/admin. Esta dirección local apunta al equipo desde el que se abre el navegador. Por ese motivo, escribirla en un teléfono no permite acceder a la computadora.

Para habilitar otros dispositivos se obtiene la IPv4 del adaptador conectado mediante ipconfig y se inicia el modo LAN. En el siguiente comando, 192.168.1.20 es una dirección de ejemplo que cada integrante debe sustituir por la de su computadora:

```powershell
.\.venv\Scripts\python.exe app.py --lan --base-url http://192.168.1.20:5000
```

La computadora y el teléfono deben poder comunicarse en la misma red local. El servidor debe permanecer encendido y el firewall debe permitir la conexión en esa red. En el teléfono se abre http://192.168.1.20:5000, usando la IP real correspondiente. El panel de registros permanece limitado al equipo servidor.

Durante el desarrollo detectamos que una instancia antigua seguía atendiendo la dirección local y mostraba una versión anterior de la página. Se detuvo ese proceso y se modificó el arranque para reservar el puerto de forma exclusiva en Windows. Así, una segunda instancia informa del conflicto en lugar de provocar respuestas diferentes entre direcciones.

### 4 4 Enlace corto y lectura del QR

Implementamos la ruta /s/demo como enlace corto local. Al abrirla, el servidor registra el acceso y redirige a la página principal. No se utilizó un servicio público como Bitly o TinyURL, por lo que el nombre del servidor permanece visible. Este mecanismo representa una redirección local fija, no un acortador público con administración de enlaces.

El QR contiene esa misma dirección. La biblioteca qrcode crea la imagen y la cámara del teléfono actúa como lector. No fue necesario desarrollar un escáner propio. Antes de abrir el enlace leído por la cámara, se puede revisar la dirección que muestra el teléfono.

El parámetro --base-url determina el destino del QR. Si cambia la IP de la computadora, se debe reiniciar con la nueva dirección y regenerar los archivos del correo. Un QR con 127.0.0.1 no sirve para dirigir un teléfono hacia la computadora del servidor.

### 4 5 Preparación del correo y registro de datos

El script preparar_correo.py genera un mensaje con texto, HTML y el QR adjunto. El mensaje utiliza la marca Super Mercado y direcciones del dominio de ejemplo example.test. El archivo se guarda en artifacts/invitacion-laboratorio.eml; crear este archivo no equivale a entregar un correo a una cuenta real.

Para comprobar la recepción se dispone de Mailpit. Su bandeja web se abre en http://127.0.0.1:8025 y el script entrega los mensajes al SMTP local en el puerto 1025. La entrega se solicita de manera independiente:

```powershell
.\.venv\Scripts\python.exe preparar_correo.py --base-url http://192.168.1.20:5000 --mailpit
```

Los datos aceptados por el formulario son sintéticos. El nombre comienza con Ejemplo, el teléfono tiene diez dígitos y comienza con 000, y el correo termina en @example.test. El correo de confirmación debe coincidir y el consentimiento debe estar marcado.

Cuando la validación es correcta, los valores se guardan en data/laboratorio.sqlite3 y aparece una confirmación propia. El panel permite ver el evento envio_demo y los valores enviados. No se realiza una redirección a otra empresa después del registro, ni se envía automáticamente un correo al completar el formulario.

## 5 Resultados

### 5 1 Comprobaciones realizadas

La revisión más reciente de las pruebas automáticas, realizada el 19 de octubre de 2026, terminó con diez pruebas aprobadas. Se verificaron el envío válido, la normalización de valores, el rechazo de entradas fuera del formato, el consentimiento, la protección de sesión, el acceso restringido al panel, la persistencia, el QR, la construcción del mensaje y los conflictos de puerto.

En las comprobaciones HTTP realizadas durante el desarrollo se confirmó que la dirección local y la IP LAN de la computadora servían la misma versión de Super Mercado y el mismo QR. Las capturas del navegador compartidas durante la implementación también permitieron identificar la diferencia de versiones causada por el proceso antiguo y revisar el formulario actualizado.

| Comprobación | Resultado o estado |
| --- | --- |
| Formulario y confirmación | El flujo con datos sintéticos fue validado mediante las pruebas del proyecto. |
| Almacenamiento y consulta | Se comprobó el registro de valores y su lectura desde el panel local. |
| Direcciones local y LAN | En la revisión HTTP ambas respondieron con el mismo formulario actualizado. |
| Código QR | Se verificó su generación y coincidencia entre ambas direcciones. |
| Mensaje de correo | Se verificó la construcción del archivo con texto, HTML y un adjunto. |
| Lectura desde un teléfono | Falta incorporar una captura del teléfono para documentar esta parte. |
| Recepción en Mailpit | Está preparada en el proyecto; falta incorporar evidencia de una entrega ejecutada. |
| Recepción en cuentas reales | No se realizó como parte de la versión implementada. |

### 5 2 Ejemplo de ingreso de datos

Para representar el envío se utilizó una entrada con el nombre Ejemplo Cliente Dos, el teléfono 0001234567 y el correo cliente.dos@example.test. La prueba comprobó que la aplicación guarda los valores aceptados y devuelve la ruta /resultado. También se comprobó que un correo fuera del dominio permitido o un teléfono con otro formato se rechazan.

Los eventos de visita no identifican personas únicas. Una misma persona puede abrir varias veces la página. Además, el enlace y el QR comparten destino. Por tanto, los contadores no permiten calcular cuántos compañeros fueron engañados ni separar automáticamente los accesos por clic de los accesos por cámara.

### 5 3 Evidencias visuales para completar la entrega

Para documentar el recorrido completo se deben adjuntar capturas tomadas durante la ejecución del equipo:

- Captura del servidor iniciado y de la página de Super Mercado, mostrando la dirección de acceso.
- Captura del teléfono con el enlace LAN abierto, o de la lectura del QR y el destino mostrado.
- Captura del formulario con datos de ejemplo y de su confirmación de recepción.
- Captura del panel local con el evento y los valores correspondientes al envío.
- Captura del mensaje recibido en Mailpit, si se incluye la parte de correo en la demostración.

Estas evidencias complementan las pruebas técnicas. Mientras no se añadan las capturas del teléfono y de la bandeja, no corresponde presentar esas dos actividades como resultados visuales ya demostrados.

## 6 Conclusiones

El desarrollo permitió comprender que un correo o un QR pueden dirigir a una página distinta de la que una persona espera. La apariencia del sitio y el texto del mensaje deben revisarse junto con el destino real del enlace. Un diseño conocido, por sí solo, no demuestra la identidad de quien solicita la información.

Comprobamos el recorrido técnico del formulario: acceso al servidor, validación, almacenamiento en SQLite y consulta del registro. La arquitectura MVC permitió mantener separadas las reglas de datos, las rutas y la presentación. También se resolvió un conflicto de instancias que afectaba la consistencia del sitio.

La distinción entre dirección local e IP LAN fue necesaria para explicar el acceso desde otros dispositivos. Cada computadora que ejecute su copia guarda sus propios registros. Cuando varios participantes usan una sola computadora servidor, sus envíos se concentran allí.

Las diez pruebas aprobadas respaldan el funcionamiento de los casos evaluados. No equivalen a una auditoría completa ni demuestran la efectividad de un ataque de ingeniería social. Tampoco contamos con una medición del comportamiento del grupo. Para completar la evidencia del flujo se requieren las capturas indicadas del teléfono y del correo local.

## 7 Recomendaciones

- Revisar el remitente completo y la dirección de los enlaces antes de abrirlos. Si una solicitud resulta inesperada, confirmar por un canal conocido de la organización [1].
- Examinar la dirección que muestra la cámara después de leer un QR. El código facilita abrir un enlace, pero no garantiza que el destino sea confiable [3].
- Activar la autenticación de múltiples factores y mantener actualizados los equipos y teléfonos como medidas adicionales de protección [1].
- En organizaciones con correo propio, configurar SPF, DKIM y DMARC. SPF ayuda a comprobar los servidores autorizados; DKIM permite verificar una firma del mensaje; DMARC establece políticas y reportes relacionados con la autenticación y la alineación del dominio. Estos mecanismos reducen ciertos abusos, pero no garantizan que todo mensaje autenticado sea legítimo [10].
- Mantener el laboratorio en una red de confianza, utilizar datos sintéticos y explicar el propósito antes de invitar participantes. No abrir el panel ni la base de datos al público.
- Evitar subir credenciales, bases de datos o evidencias con información privada a GitHub. Revisar también la identidad registrada en los commits.
- Si una aplicación similar se destinara a usuarios reales, sería necesario revisar HTTPS, autenticación del administrador, protección de datos y controles de acceso. La configuración HTTP local de este ejercicio no representa un despliegue público.
- Planificar la prevención y la respuesta, además de la capacitación. El marco NIST CSF 2.0 propone gobernar, identificar, proteger, detectar, responder y recuperar como funciones de la gestión del riesgo [9].

## 8 Bibliografía

Se presentan referencias institucionales, documentación oficial y un estudio académico. Los recursos web se consultaron el 19 de octubre de 2026.

[1] Federal Trade Commission. (s. f.). Cómo reconocer y evitar las estafas de phishing. https://consumidor.ftc.gov/articulos/como-reconocer-y-evitar-las-estafas-de-phishing

[2] National Institute of Standards and Technology. (s. f.). CSRC Glossary. Entradas threat, vulnerability y risk. https://csrc.nist.gov/glossary

[3] Federal Trade Commission. (2023, 6 de diciembre). Scammers hide harmful links in QR codes to steal your information. https://consumer.ftc.gov/consumer-alerts/2023/12/scammers-hide-harmful-links-qr-codes-steal-your-information

[4] Geisler, M., y Pöhn, D. (2024). Hooked: A Real-World Study on QR Code Phishing. arXiv, 2407.16230. https://doi.org/10.48550/arXiv.2407.16230

[5] Pallets Projects. (s. f.). Flask Documentation. https://flask.palletsprojects.com/en/stable/

[6] Pylons Project. (s. f.). Waitress Documentation. https://docs.pylonsproject.org/projects/waitress/en/stable/

[7] Mailpit. (s. f.). Mailpit Documentation. https://mailpit.axllent.org/docs/

[8] Proyecto qrcode. (s. f.). qrcode en Python Package Index. https://pypi.org/project/qrcode/

[9] National Institute of Standards and Technology. (2024). The NIST Cybersecurity Framework (CSF) 2.0. NIST CSWP 29. https://doi.org/10.6028/NIST.CSWP.29

[10] Nightingale, J. S. (2017). Email Authentication Mechanisms: DMARC, SPF and DKIM. NIST Technical Note 1945. https://doi.org/10.6028/NIST.TN.1945
