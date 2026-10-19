"""CLI para generar el correo educativo y entregarlo opcionalmente a Mailpit."""
import argparse
from pathlib import Path
from laboratorio.services.correo import deliver_to_mailpit, prepare


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:5000")
    parser.add_argument("--mailpit", action="store_true", help="Entregar solo a SMTP local 127.0.0.1:1025")
    args = parser.parse_args()
    mail, path = prepare(args.base_url, Path(__file__).resolve().parent / "artifacts")
    print(f"Correo generado: {path}")
    print(f"QR generado: {path.parent / 'qr-laboratorio.svg'}")
    if args.mailpit:
        try:
            deliver_to_mailpit(mail)
        except OSError as error:
            parser.exit(1, f"No se pudo conectar a Mailpit local: {error}\nInicia Mailpit y vuelve a ejecutar.\n")
        print("Correo entregado al buzon de pruebas: http://127.0.0.1:8025")


if __name__ == "__main__":
    main()
