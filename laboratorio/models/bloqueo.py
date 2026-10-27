"""Bloqueo temporal y auditoria de autenticaciones para la cuenta de prueba."""
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


DEMO_ACCOUNT = "admin"
MAX_FAILURES = 3
LOCK_SECONDS = 60


@dataclass(frozen=True)
class AttemptResult:
    status: str
    retry_after: int = 0


class LoginLockModel:
    """Mantiene el contador y los eventos en transacciones SQLite."""

    def __init__(self, database):
        self.database = Path(database)

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.database, timeout=10, isolation_level=None)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def initialize(self):
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS auth_lock_state (
                username TEXT PRIMARY KEY,
                failed_attempts INTEGER NOT NULL DEFAULT 0,
                blocked_until TEXT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS auth_events (
                id INTEGER PRIMARY KEY,
                fecha_utc TEXT NOT NULL,
                usuario TEXT NOT NULL,
                resultado TEXT NOT NULL,
                ip_origen TEXT,
                bloqueo_activo INTEGER NOT NULL CHECK (bloqueo_activo IN (0, 1))
            )""")
            conn.execute(
                "INSERT OR IGNORE INTO auth_lock_state (username) VALUES (?)",
                (DEMO_ACCOUNT,),
            )

    @staticmethod
    def _utc(value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _record(conn, now, result, source_ip, blocked):
        conn.execute(
            """INSERT INTO auth_events
               (fecha_utc, usuario, resultado, ip_origen, bloqueo_activo)
               VALUES (?, ?, ?, ?, ?)""",
            (now.isoformat(), DEMO_ACCOUNT, result, source_ip, int(blocked)),
        )

    def process_attempt(self, credential_check, source_ip=None, now=None):
        """Verifica bloqueo antes de credenciales y actualiza todo atomicamente."""
        now = self._utc(now or datetime.now(timezone.utc))
        with self.connection() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                row = conn.execute(
                    "SELECT failed_attempts, blocked_until FROM auth_lock_state WHERE username = ?",
                    (DEMO_ACCOUNT,),
                ).fetchone()
                blocked_until = (datetime.fromisoformat(row["blocked_until"])
                                 if row["blocked_until"] else None)

                if blocked_until and blocked_until > now:
                    remaining = max(1, int((blocked_until - now).total_seconds() + 0.999))
                    self._record(conn, now, "blocked", source_ip, True)
                    conn.commit()
                    return AttemptResult("blocked", remaining)

                failed_attempts = row["failed_attempts"]
                if blocked_until:
                    # La expiracion tambien reinicia el contador y queda auditada.
                    failed_attempts = 0
                    conn.execute(
                        "UPDATE auth_lock_state SET failed_attempts = 0, blocked_until = NULL "
                        "WHERE username = ?", (DEMO_ACCOUNT,),
                    )
                    self._record(conn, now, "unlocked", source_ip, False)

                if credential_check():
                    conn.execute(
                        "UPDATE auth_lock_state SET failed_attempts = 0, blocked_until = NULL "
                        "WHERE username = ?", (DEMO_ACCOUNT,),
                    )
                    self._record(conn, now, "success", source_ip, False)
                    conn.commit()
                    return AttemptResult("success")

                failed_attempts += 1
                is_locked = failed_attempts == MAX_FAILURES
                until = now + timedelta(seconds=LOCK_SECONDS) if is_locked else None
                conn.execute(
                    "UPDATE auth_lock_state SET failed_attempts = ?, blocked_until = ? "
                    "WHERE username = ?",
                    (failed_attempts, until.isoformat() if until else None, DEMO_ACCOUNT),
                )
                self._record(conn, now, "failure", source_ip, is_locked)
                conn.commit()
                return AttemptResult("locked" if is_locked else "failure", LOCK_SECONDS if is_locked else 0)
            except Exception:
                conn.rollback()
                raise

    def state(self):
        with self.connection() as conn:
            return conn.execute(
                "SELECT failed_attempts, blocked_until FROM auth_lock_state WHERE username = ?",
                (DEMO_ACCOUNT,),
            ).fetchone()
