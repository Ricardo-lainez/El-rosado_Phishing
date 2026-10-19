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
        print("Super Mercado - servidor local", flush=True)
        print(f"En esta computadora: http://127.0.0.1:{args.port}", flush=True)
        print(f"Panel local: http://127.0.0.1:{args.port}/admin", flush=True)
        print(f"Destino del QR y correo: {base}/s/demo", flush=True)
        if args.lan:
            print("Acceso LAN habilitado. Ambas direcciones sirven la misma instancia.", flush=True)
            if not args.base_url:
                print("Para el QR del telefono, usa --base-url http://TU_IP_LAN:PUERTO", flush=True)
        else:
            print("Acceso limitado a esta computadora. Para otros dispositivos, inicia con --lan.", flush=True)
        print("Manten esta terminal abierta. Detener: Ctrl+C.", flush=True)
        serve(application, sockets=[listener])


if __name__ == "__main__":
    main()
