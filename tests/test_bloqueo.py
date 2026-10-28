import re
import sqlite3
import tempfile
import unittest
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path

from laboratorio import create_app


class FakeClock:
    def __init__(self):
        self.value = datetime(2026, 10, 27, 12, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += timedelta(seconds=seconds)


class LoginLockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / "auth.sqlite3"
        self.clock = FakeClock()
        self.app = create_app(self.database, auth_clock=self.clock)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def login_payload(self, username="admin", password="wrong"):
        page = self.client.get("/login").get_data(as_text=True)
        token = re.search(r'name="csrf" value="([^"]+)"', page).group(1)
        return {"csrf": token, "username": username, "password": password}

    def post_login(self, username="admin", password="wrong"):
        return self.client.post(
            "/login", data=self.login_payload(username, password),
            environ_overrides={"REMOTE_ADDR": "192.0.2.15"},
        )

    def state(self):
        row = self.app.extensions["auth_lock"].state()
        return row["failed_attempts"], row["blocked_until"]

    def test_third_consecutive_failure_locks_for_sixty_seconds(self):
        self.assertEqual(self.post_login().status_code, 303)
        self.assertEqual(self.state(), (1, None))
        self.post_login()
        self.assertEqual(self.state(), (2, None))
        self.post_login()
        count, blocked_until = self.state()
        self.assertEqual(count, 3)
        self.assertEqual(datetime.fromisoformat(blocked_until), self.clock.value + timedelta(seconds=60))
        with self.client.session_transaction() as stored_session:
            message = stored_session["login_error"]
        page = self.client.get("/login").get_data(as_text=True)
        self.assertIn("bloqueada temporalmente", page)
        self.assertNotIn("L4b0rat0r10!", message)

    def test_success_resets_consecutive_failure_count(self):
        self.post_login()
        self.post_login()
        response = self.post_login(password="L4b0rat0r10!")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.state(), (0, None))
        self.post_login()
        self.assertEqual(self.state(), (1, None))

    def test_correct_password_is_rejected_while_locked(self):
        for _ in range(3):
            self.post_login()
        model = self.app.extensions["auth_lock"]
        result = model.process_attempt(
            lambda: self.fail("No se deben validar credenciales durante el bloqueo"),
            source_ip="192.0.2.15", now=self.clock(),
        )
        self.assertEqual(result.status, "blocked")
        response = self.post_login(password="L4b0rat0r10!")
        self.assertEqual(response.status_code, 303)
        self.assertEqual(self.state()[0], 3)
        self.assertIn("bloqueada temporalmente", self.client.get("/login").get_data(as_text=True))

    def test_expiration_resets_counter_and_records_unlock(self):
        for _ in range(3):
            self.post_login()
        self.clock.advance(60)
        self.post_login()
        self.assertEqual(self.state(), (1, None))
        with closing(sqlite3.connect(self.database)) as conn:
            unlocked = conn.execute(
                "SELECT resultado, bloqueo_activo FROM auth_events WHERE resultado='unlocked'"
            ).fetchone()
        self.assertEqual(unlocked, ("unlocked", 0))

    def test_block_persists_across_model_recreation(self):
        for _ in range(3):
            self.post_login()
        recreated = create_app(self.database, auth_clock=self.clock)
        result = recreated.extensions["auth_lock"].process_attempt(
            lambda: True, source_ip="192.0.2.20", now=self.clock(),
        )
        self.assertEqual(result.status, "blocked")
        self.assertEqual(recreated.extensions["auth_lock"].state()["failed_attempts"], 3)

    def test_audit_has_utc_account_result_and_ip_without_secrets(self):
        self.post_login(password="secret-do-not-store")
        with closing(sqlite3.connect(self.database)) as conn:
            columns = {row[1] for row in conn.execute("PRAGMA table_info(auth_events)")}
            record = conn.execute(
                "SELECT fecha_utc, usuario, resultado, ip_origen, bloqueo_activo "
                "FROM auth_events"
            ).fetchone()
            dump = " ".join(str(value) for row in conn.execute("SELECT * FROM auth_events") for value in row)
        self.assertEqual(columns, {"id", "fecha_utc", "usuario", "resultado", "ip_origen", "bloqueo_activo"})
        self.assertEqual(record[1:], ("admin", "failure", "192.0.2.15", 0))
        self.assertTrue(record[0].endswith("+00:00"))
        self.assertNotIn("secret-do-not-store", dump)
        self.assertNotIn("L4b0rat0r10!", dump)

    def test_csrf_error_does_not_count_as_failed_password(self):
        response = self.client.post(
            "/login", data={"csrf": "invalid", "username": "admin", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.state(), (0, None))
        with closing(sqlite3.connect(self.database)) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM auth_events").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
