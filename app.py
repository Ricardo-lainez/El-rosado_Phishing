"""Punto de entrada del formulario MVC. Ejecutar: python app.py."""
import argparse

from waitress import serve

from laboratorio import create_app
from laboratorio.server import open_listener
from laboratorio.services.enlaces import validate_base_url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lan", action="store_true", help="Escuchar tambien en la red local")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--base-url", help="URL usada en el QR; ejemplo: http://192.168.1.20:5000")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("El puerto debe estar entre 1 y 65535.")
    try:
        base = validate_base_url(args.base_url or f"http://127.0.0.1:{args.port}")
    except ValueError as error:
        parser.error(str(error))
    try:
        listener = open_listener("0.0.0.0" if args.lan else "127.0.0.1", args.port)
    except OSError as error:
        parser.exit(1, f"No se pudo reservar el puerto {args.port}: {error}\n"
                    "Puede haber otra instancia abierta. Deten el servidor anterior con Ctrl+C "
                    "o elige otro puerto con --port y ajusta --base-url.\n")

    with listener:
        application = create_app(base_url=base)
        _print_banner(port=args.port, base_url=base, is_lan=args.lan, has_custom_base=bool(args.base_url))
        serve(application, sockets=[listener])


def _print_banner(port: int, base_url: str, is_lan: bool, has_custom_base: bool) -> None:
    """Imprime un banner claro y profesional con las rutas y estado del servidor."""
    import os
    import sys

    # Asegura compatibilidad con caracteres UTF-8 en PowerShell/CMD de Windows
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if os.name == "nt":
        # Habilita el soporte de secuencias ANSI de color en la consola de Windows
        try:
            os.system("")
        except Exception:
            pass

    red = "\033[91m"
    green = "\033[92m"
    cyan = "\033[96m"
    yellow = "\033[93m"
    bold = "\033[1m"
    dim = "\033[90m"
    reset = "\033[0m"

    local = f"http://127.0.0.1:{port}"

    print(f"\n{red}{bold}{'=' * 66}{reset}")
    print(f"  {bold}🛒  SUPER MERCADO — Servidor de Pruebas (Seguridad Informática){reset}")
    print(f"{red}{bold}{'=' * 66}{reset}")
    print(f"  {green}● Estado:{reset}        {bold}Servidor activo y escuchando{reset}")
    print(f"  {cyan}● Acceso local:{reset}  {bold}{local}{reset}")
    print()
    print(f"  {bold}📌 Rutas disponibles del proyecto:{reset}")
    print(f"     ├── 📝 Formulario 1 (Registro):   {cyan}{local}/{reset}")
    print(f"     ├── 💳 Formulario 2 (Beneficios): {yellow}{local}/beneficios{reset}")
    print(f"     ├── 🔐 Iniciar sesión:           {green}{local}/login{reset}")
    print(f"     ├── ⚙️  Panel de control:        {cyan}{local}/admin{reset}")
    print(f"     └── 📱 Destino QR / demo:        {cyan}{base_url}/s/demo{reset}")
    print()
    print(f"  {bold}🔑 Credenciales de prueba:{reset}")
    print(f"     └── Usuario: {yellow}admin{reset}   |   Contraseña: {yellow}L4b0rat0r10!{reset}")
    print()
    if is_lan:
        print(f"  {yellow}🌐 Modo de red:{reset}  LAN habilitado (0.0.0.0:{port})")
        if not has_custom_base:
            print(f"     {dim}Tip: Para probar el QR en otro dispositivo:{reset}")
            print(f"     {dim}python app.py --lan --base-url http://TU_IP_LOCAL:{port}{reset}")
    else:
        print(f"  {dim}ℹ️  Modo de red:  Solo local. Para otros dispositivos usa: --lan{reset}")
    print()
    print(f"  {dim}🛑 Para detener el servidor: Presiona Ctrl + C en esta terminal{reset}")
    print(f"{red}{bold}{'=' * 66}{reset}\n", flush=True)


if __name__ == "__main__":
    main()
