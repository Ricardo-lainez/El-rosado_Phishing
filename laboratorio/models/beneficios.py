"""Reglas de dominio y validación para el formulario de Tarjeta de Beneficios y Puntos."""
import re

DEMO_BENEFICIOS = {
    "cedula": "0912345678",
    "nombre": "Ejemplo Cliente Beneficios",
    "ciudad": "Guayaquil",
    "tarjeta": "4509-1234-5678-9012",
    "fecha_nacimiento": "1995-08-15",
    "codigo_seguridad": "789",
}


def normalize_beneficios(form):
    """Limpia y estandariza los campos del formulario de beneficios."""
    cedula = re.sub(r"\D", "", form.get("cedula", "").strip())
    nombre = form.get("nombre", "").strip()
    ciudad = form.get("ciudad", "").strip()
    tarjeta = re.sub(r"[\s\-]", "", form.get("tarjeta", "").strip())
    fecha_nacimiento = form.get("fecha_nacimiento", "").strip()
    codigo_seguridad = re.sub(r"\D", "", form.get("codigo_seguridad", "").strip())

    return {
        "cedula": cedula,
        "nombre": nombre,
        "ciudad": ciudad,
        "tarjeta": tarjeta,
        "fecha_nacimiento": fecha_nacimiento,
        "codigo_seguridad": codigo_seguridad,
    }


def is_valid_beneficios(form):
    """Comprueba que los 5+ datos requeridos y el consentimiento sean válidos."""
    data = normalize_beneficios(form)

    # 1. Cédula: 10 dígitos numéricos
    if not re.fullmatch(r"[0-9]{10}", data["cedula"]):
        return False

    # 2. Nombre: al menos 3 caracteres alfabéticos/espacios
    if not (3 <= len(data["nombre"]) <= 100):
        return False

    # 3. Ciudad: al menos 2 caracteres
    if not (2 <= len(data["ciudad"]) <= 60):
        return False

    # 4. Tarjeta Club: 16 dígitos numéricos
    if not re.fullmatch(r"[0-9]{16}", data["tarjeta"]):
        return False

    # 5. Fecha de nacimiento: formato YYYY-MM-DD o DD/MM/YYYY
    if not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["fecha_nacimiento"]) or
            re.fullmatch(r"\d{2}/\d{2}/\d{4}", data["fecha_nacimiento"])):
        return False

    # 6. Código de seguridad/PIN: 3 o 4 dígitos
    if data["codigo_seguridad"] and not re.fullmatch(r"[0-9]{3,4}", data["codigo_seguridad"]):
        return False

    # Consentimiento explícito de laboratorio
    if form.get("consentimiento") != "si":
        return False

    return True
