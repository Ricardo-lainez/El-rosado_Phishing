import re
import tempfile
import unittest
from pathlib import Path

from laboratorio import create_app
from laboratorio.models.beneficios import DEMO_BENEFICIOS


class BeneficiosTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / "test.sqlite3"
        self.app = create_app(self.database)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def payload(self):
        html = self.client.get("/beneficios").get_data(as_text=True)
        token = re.search(r'name="csrf" value="([^"]+)"', html).group(1)
        return {
            **DEMO_BENEFICIOS,
            "csrf": token,
            "consentimiento": "si",
        }

    def test_get_beneficios_page(self):
        response = self.client.get("/beneficios")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Tarjeta de Beneficios", html)
        self.assertIn("SUPER MERCADO", html)
        self.assertNotIn("EL ROSADO", html)

    def test_short_link_beneficios_redirects(self):
        response = self.client.get("/s/beneficios")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/beneficios")

    def test_submit_valid_beneficios(self):
        response = self.client.post("/beneficios", data=self.payload(), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Recibimos tu formulario", response.get_data(as_text=True))

        rows, total = self.app.extensions["eventos"].dashboard_beneficios()
        self.assertEqual(total, 1)
        self.assertEqual(rows[0]["cedula"], "0912345678")
        self.assertEqual(rows[0]["tarjeta"], "4509123456789012")
        self.assertEqual(rows[0]["nombre"], "Ejemplo Cliente Beneficios")

    def test_invalid_data_rejected(self):
        # Cédula incorrecta
        data = self.payload()
        data["cedula"] = "123"
        res = self.client.post("/beneficios", data=data)
        self.assertEqual(res.status_code, 400)

        # Tarjeta incorrecta
        data = self.payload()
        data["tarjeta"] = "999"
        res = self.client.post("/beneficios", data=data)
        self.assertEqual(res.status_code, 400)

        # Falta consentimiento
        data = self.payload()
        data["consentimiento"] = "no"
        res = self.client.post("/beneficios", data=data)
        self.assertEqual(res.status_code, 400)

        rows, total = self.app.extensions["eventos"].dashboard_beneficios()
        self.assertEqual(total, 0)


if __name__ == "__main__":
    unittest.main()
