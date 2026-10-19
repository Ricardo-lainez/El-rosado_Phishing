import re
import sqlite3
import tempfile
import unittest
from contextlib import closing
from email import policy
from email.parser import BytesParser
from pathlib import Path

from laboratorio import create_app
from laboratorio.models.participacion import DEMO
from laboratorio.services.enlaces import validate_base_url
from laboratorio.services.correo import prepare


class LabTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / "test.sqlite3"
        self.app = create_app(self.database)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def payload(self):
        html = self.client.get("/").get_data(as_text=True)
        token = re.search(r'name="csrf" value="([^"]+)"', html).group(1)
        return {**DEMO, "csrf": token, "confirmacion": DEMO["correo"], "consentimiento": "si"}

    def test_full_flow_and_saved_demo(self):
        self.assertEqual(self.client.get("/s/demo").status_code, 302)
        result = self.client.post("/participar", data=self.payload(), follow_redirects=True)
        self.assertIn("Recibimos tu formulario", result.get_data(as_text=True))
        with closing(sqlite3.connect(self.database)) as conn:
            row = conn.execute("SELECT nombre,telefono,correo FROM eventos WHERE tipo='envio_demo'").fetchone()
        self.assertEqual(row, tuple(DEMO.values()))
        self.assertEqual(self.client.get("/qr.svg").mimetype, "image/svg+xml")
        self.assertEqual(self.client.get("/instructor").status_code, 200)

    def test_personal_data_and_missing_consent_are_not_saved(self):
        for field, value in [("correo", "persona@gmail.com"), ("nombre", "Nombre real"),
                             ("telefono", "0991234567"), ("consentimiento", "no"),
                             ("confirmacion", "otro@example.test")]:
            data = self.payload()
            data[field] = value
            self.assertEqual(self.client.post("/participar", data=data).status_code, 400)
        with closing(sqlite3.connect(self.database)) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM eventos WHERE tipo='envio_demo'").fetchone()[0], 0)

    def test_forgery_and_remote_admin_rejected(self):
        data = self.payload()
        for token in ("invalid", "", "\u00f1"):
            data["csrf"] = token
            self.assertEqual(self.client.post("/participar", data=data).status_code, 400)
        self.assertEqual(self.client.get("/instructor", environ_overrides={"REMOTE_ADDR": "192.168.1.9"}).status_code, 403)
        self.assertEqual(self.client.post("/participar", data="x" * 9000, content_type="application/x-www-form-urlencoded").status_code, 413)

    def test_url_and_generated_email(self):
        for url in ["https://example.com", "http://8.8.8.8", "http://192.168.1.2/otro", "http://localhost@evil.test"]:
            with self.assertRaises(ValueError):
                validate_base_url(url)
        for url in ["http://127.0.0.1:5000", "http://192.168.1.20:5000", "http://10.0.0.1:5000"]:
            self.assertEqual(validate_base_url(url), url)
        _, path = prepare("http://192.168.1.20:5000", Path(self.temp.name) / "artifacts")
        msg = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
        self.assertIn("Super Mercado", msg["Subject"])
        self.assertIn("http://192.168.1.20:5000/s/demo", msg.get_body(preferencelist=("plain",)).get_content())
        self.assertEqual(len(list(msg.iter_attachments())), 1)

    def test_model_can_be_used_without_http_and_database_survives_recreation(self):
        from laboratorio.models.eventos import EventModel

        model = EventModel(self.database)
        model.record("envio_demo", DEMO)
        with self.assertRaises(ValueError):
            model.record("envio_demo", {**DEMO, "correo": "otro@gmail.com"})
        with self.assertRaises(ValueError):
            model.record("visita", DEMO)
        recreated = create_app(self.database)
        rows, totals = recreated.extensions["eventos"].dashboard()
        self.assertEqual(totals, {"envio_demo": 1})
        self.assertEqual(rows[0]["nombre"], DEMO["nombre"])

    def test_editable_synthetic_data_is_normalized_and_saved(self):
        data = self.payload()
        data.update(nombre="  Ejemplo Cliente Dos  ", telefono="0001234567",
                    correo="CLIENTE.DOS@example.test", confirmacion="cliente.dos@example.test")
        response = self.client.post("/participar", data=data)
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["Location"], "/resultado")
        rows, totals = self.app.extensions["eventos"].dashboard()
        submission = next(row for row in rows if row["tipo"] == "envio_demo")
        self.assertEqual((submission["nombre"], submission["telefono"], submission["correo"]),
                         ("Ejemplo Cliente Dos", "0001234567", "cliente.dos@example.test"))
        self.assertEqual(totals["envio_demo"], 1)

    def test_invalid_formats_are_rejected_by_model(self):
        model = self.app.extensions["eventos"]
        for field, value in [("nombre", "Ejemplo <script>"), ("nombre", "Ejemplo " + "x" * 66),
                             ("telefono", "0001234"), ("telefono", "0991234567"),
                             ("correo", "cliente@example.test.evil"),
                             ("correo", "cliente@gmail.com"), ("correo", "a" * 65 + "@example.test")]:
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValueError):
                    model.record("envio_demo", {**DEMO, field: value})
        self.assertEqual(model.dashboard()[0], [])

    def test_public_branding_and_local_admin_alias(self):
        for path in ("/", "/resultado"):
            html = self.client.get(path).get_data(as_text=True)
            self.assertIn("SUPER MERCADO", html)
            self.assertNotIn("EL ROSADO", html)
        self.assertEqual(self.client.get("/admin").status_code, 200)
        self.assertEqual(self.client.get("/admin", environ_overrides={"REMOTE_ADDR": "192.168.1.9"}).status_code, 403)


if __name__ == "__main__":
    unittest.main()
