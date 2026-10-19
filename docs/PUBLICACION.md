# Preparar el repositorio público

Esta lista es para quien va a publicar el código. El uso diario está en la [guía del equipo](GUIA_EQUIPO.md).

## Archivos que se comparten

Comparte el código, `templates/`, `static/`, `tests/`, `docs/`, `README.md`, `.gitignore`, `requirements.txt` y `requirements-lock.txt`. Las rutas y direcciones de la documentación son ejemplos; cada compañero utiliza su propia IP LAN.

El proyecto no necesita credenciales SMTP, un `.env`, tu dirección de correo real ni rutas personales de Windows. No copies `.venv` ni `mailpit.exe` al repositorio.

`.gitignore` excluye el entorno virtual, bases de datos, carpetas `data/` y `artifacts/`, archivos `.env`, claves y registros. Git no deja de seguir un archivo ya versionado solo por agregar una regla: [documentación de GitHub](https://docs.github.com/en/get-started/git-basics/ignoring-files).

Comprueba antes de preparar el commit:

```powershell
git status --short --untracked-files=all
git ls-files
git check-ignore -v data/laboratorio.sqlite3 artifacts/invitacion-laboratorio.eml .env
```

Evita `git add -f`, que puede agregar archivos excluidos. No subas capturas con datos de personas, contraseñas o información privada visible.

## Nombre y correo de los commits

El historial de un repositorio público expone la identidad del autor de sus commits. Revisa:

```powershell
git log --all --format="%h %an <%ae>"
```

Si prefieres no publicar tu correo, copia tu dirección `noreply` desde la configuración de correo de GitHub y configúrala para este repositorio. Sustituye el texto de ejemplo:

```powershell
git config user.email "TU_DIRECCION_NOREPLY_DE_GITHUB"
```

Esto afecta a los commits futuros. **No elimina el correo de commits anteriores**. Antes de publicar, resuelve por separado cualquier identidad del historial que no quieras hacer pública. No se reescribe el historial automáticamente ni se hace un push forzado como parte de esta preparación. [Guía oficial sobre el correo de los commits](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address).

## Preparar el commit

Una vez revisada la identidad, prepara solamente los archivos del proyecto:

```powershell
git add .gitignore README.md app.py preparar_correo.py requirements.txt requirements-lock.txt laboratorio templates static tests docs
git diff --cached --stat
git diff --cached
```

Revisa el contenido preparado y comprueba que no aparezcan `data/`, `artifacts/`, `.venv/` ni información privada. Entonces puedes crear el commit y publicarlo en el repositorio de GitHub que el equipo haya elegido. No se ha ejecutado ningún commit ni publicación automáticamente.

Publicar el código no publica el servidor local ni sus registros. Al invitar al grupo, comparte el enlace del repositorio junto con la [guía de uso](GUIA_EQUIPO.md); el enlace LAN se comparte solo cuando esté encendida la computadora que sirve el formulario.
