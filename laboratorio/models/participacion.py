"""Reglas de dominio para entradas sinteticas editables."""
import re

DEMO = {"nombre": "Ejemplo Cliente", "telefono": "0000000000", "correo": "cliente@example.test"}


def normalize_identity(form):
    fields = {key: form.get(key, "").strip() for key in DEMO}
    fields["correo"] = fields["correo"].lower()
    return fields


def is_valid_identity(fields):
    return (isinstance(fields, dict) and set(fields) == set(DEMO)
            and all(isinstance(value, str) for value in fields.values())
            and re.fullmatch(r"Ejemplo [\w .'-]{2,65}", fields["nombre"]) is not None
            and re.fullmatch(r"000[0-9]{7}", fields["telefono"]) is not None
            and re.fullmatch(r"[a-z0-9](?:[a-z0-9._+-]{0,62}[a-z0-9])?@example\.test",
                             fields["correo"]) is not None)


def is_valid_participation(form):
    fields = normalize_identity(form)
    return (is_valid_identity(fields)
            and form.get("confirmacion", "").strip().lower() == fields["correo"]
            and form.get("consentimiento") == "si")
