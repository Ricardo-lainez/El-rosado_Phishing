import io
import ipaddress
from urllib.parse import urlsplit

import qrcode
import qrcode.image.svg


def validate_base_url(value):
    parsed = urlsplit(value)
    try:
        host = parsed.hostname
        ip = ipaddress.ip_address(host) if host else None
        local = host == "localhost" or (
            ip and (ip.is_loopback or
                    ip in ipaddress.ip_network("10.0.0.0/8") or
                    ip in ipaddress.ip_network("172.16.0.0/12") or
                    ip in ipaddress.ip_network("192.168.0.0/16") or
                    ip in ipaddress.ip_network("26.0.0.0/8") or   # Radmin VPN
                    ip in ipaddress.ip_network("25.0.0.0/8") or   # Hamachi
                    ip in ipaddress.ip_network("100.64.0.0/10"))  # Tailscale
        )
        parsed.port
    except ValueError:
        local = False
    if (parsed.scheme != "http" or not local or parsed.username or parsed.password
            or parsed.path not in ("", "/") or parsed.query or parsed.fragment):
        raise ValueError("Usa http://127.0.0.1:5000 o una IP privada de tu LAN, sin ruta.")
    return value.rstrip("/")


def make_qr_svg(base_url):
    stream = io.BytesIO()
    qrcode.make(validate_base_url(base_url) + "/s/demo",
                image_factory=qrcode.image.svg.SvgPathImage, box_size=8, border=4).save(stream)
    return stream.getvalue()
