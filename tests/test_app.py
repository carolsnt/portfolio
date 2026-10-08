import importlib
import json
import os
import unittest
from unittest.mock import patch

import app
from resend.exceptions import ResendError


class PortfolioAppTests(unittest.TestCase):
    def setUp(self):
        app.app.config.update(TESTING=True)
        self.client = app.app.test_client()
        self.contact_data = {
            "name": "Carol Santos",
            "email": "carol@example.com",
            "subject": "parceria",
            "message": "Olá! Gostaria de conversar sobre uma parceria.",
        }

    def test_homepage_renders_template_and_static_assets(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"/static/styles.css", response.data)
        self.assertIn(b"/static/script.js", response.data)
        self.assertIn(b"/static/i18n.js", response.data)
        self.assertIn(b"/static/tailwind.css", response.data)
        self.assertNotIn(b"cdn.tailwindcss.com", response.data)
        self.assertIn(b'id="languagePicker"', response.data)
        self.assertIn(b'<option value="de">Deutsch</option>', response.data)
        self.assertIn(b'<option value="fr">Fran\xc3\xa7ais</option>', response.data)
        self.assertIn(b"/static/me.jpeg", response.data)
        self.assertIn(b"/static/logo.png", response.data)
        self.assertIn(b"Prosa Tech Cybersec", response.data)
        self.assertIn(b"Dispon\xc3\xadvel para novas oportunidades", response.data)
        self.assertIn(b"Analista de Seguran\xc3\xa7a da Informa\xc3\xa7\xc3\xa3o", response.data)
        self.assertIn(b"Imediatamente \xc2\xb7 estou me candidatando agora", response.data)
        self.assertIn(b"S\xc3\xa3o Paulo, SP \xc2\xb7 Costa Rica", response.data)
        self.assertIn(b"Tempo integral", response.data)
        self.assertIn(b"PagBank", response.data)
        self.assertIn(b"Porto Seguro", response.data)
        self.assertIn(b"Defesa Cibern\xc3\xa9tica", response.data)
        self.assertNotIn(b"carol.santos.acps@gmail.com", response.data)
        self.assertIn(b'href="https://prosa-nfc.vercel.app/" target="_blank"', response.data)
        self.assertNotIn(b"Bora prosear?", response.data)
        self.assertNotIn(b'id="contactForm"', response.data)
        self.assertIn(b"about-copy-panel", response.data)
        self.assertIn(b"about-intro-grid", response.data)
        self.assertIn(b"about-details", response.data)
        self.assertIn(b"Fundadora &amp; Desenvolvedora", response.data)
        self.assertIn(b"Prosa Tech \xc2\xb7 dez. 2023\xe2\x80\x93atual", response.data)
        self.assertIn(b"Landing Page Coritiba", response.data)
        self.assertIn(b"Ensino T\xc3\xa9cnico em Mecatr\xc3\xb4nica", response.data)
        self.assertIn(b"Penetration Testing Professional", response.data)
        self.assertIn(b"Sensibiliza\xc3\xa7\xc3\xa3o para a Seguran\xc3\xa7a Digital", response.data)
        self.assertIn(b"Ingl\xc3\xaas (profissional)", response.data)
        self.assertIn(b'href="https://github.com/carolsnt"', response.data)
        self.assertIn(b"XDR/EDR", response.data)
        self.assertNotIn(b"+10K seguidores no YouTube", response.data)
        self.assertEqual(response.data.count(b'class="certification-list"'), 1)
        self.assertEqual(response.data.count(b'<li>Cyber Academy 2025/2</li>'), 1)
        self.assertIn(b"Threat Modeling", response.data)
        self.assertIn(b"Vault", response.data)
        self.assertNotIn("🎯 Ativa".encode(), response.data)
        self.assertEqual(response.data.count(b'href="https://www.fiap.com.br/"'), 2)
        self.assertIn(b"course-grid", response.data)
        self.assertIn(b"Per\xc3\xadcia Forense Computacional", response.data)
        self.assertIn(b"Febraban / GoHacking", response.data)
        self.assertEqual(response.data.count(b'class="course-card"'), 6)
        self.assertEqual(response.data.count(b'class="testimonial-card fade-in"'), 27)
        self.assertIn(b"27 recomenda\xc3\xa7\xc3\xb5es", response.data)
        self.assertIn(b"https://www.linkedin.com/in/carolsnt/", response.data)
        self.assertIn(
            b"Tenho a oportunidade de estudar com a Carol",
            response.data,
        )
        self.assertIn(
            b"Desaprendida, desembara\xc3\xa7ada, comunica e expressa-se muito bem.",
            response.data,
        )
        self.assertIn(
            b"Profissional dedicada e focada em resultado.",
            response.data,
        )
        self.assertNotIn(
            b"Destaca meu crescimento t\xc3\xa9cnico",
            response.data,
        )
        self.assertEqual(response.data.count(b'class="volunteer-item'), 9)
        self.assertIn(b"Mente Bin\xc3\xa1ria", response.data)
        self.assertIn(b"Supera\xc3\xa7\xc3\xa3o ORC", response.data)
        self.assertIn(b"cerca de 20 pessoas por m\xc3\xaas", response.data)
        self.assertIn(b"https://www.instagram.com/bsidessp/", response.data)
        self.assertIn(b"https://307conf.com/", response.data)
        self.assertIn(b"https://hackerrangers.com/", response.data)
        self.assertIn(b"https://mentebinaria.com.br/", response.data)

    def test_profile_image_is_served(self):
        response = self.client.get("/static/me.jpeg")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/jpeg")
        response.close()

    def test_frontend_script_is_served(self):
        response = self.client.get("/static/script.js")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/javascript")
        response.close()

    def test_localization_script_is_served(self):
        response = self.client.get("/static/i18n.js")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/javascript")
        self.assertIn(b"recommendationTranslations", response.data)
        response.close()

    def test_local_tailwind_stylesheet_is_served(self):
        response = self.client.get("/static/tailwind.css")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/css")
        self.assertIn(b"Tailwind CSS v3.4.17", response.data)
        self.assertIn(b".container{width:100%}", response.data)
        response.close()

    def test_vercel_framework_and_public_assets_are_configured(self):
        with open(
            os.path.join(app.app.root_path, "vercel.json"),
            encoding="utf-8",
        ) as config_file:
            config = json.load(config_file)

        self.assertEqual(config["framework"], "flask")
        public_static = os.path.join(app.app.root_path, "public", "static")
        self.assertTrue(os.path.isfile(os.path.join(public_static, "styles.css")))
        self.assertTrue(os.path.isfile(os.path.join(public_static, "tailwind.css")))

    def test_vercel_build_only_static_endpoint_generates_asset_urls(self):
        try:
            with patch.dict(os.environ, {"VERCEL": "1"}):
                importlib.reload(app)
                deployed_app = app.app

                self.assertIsNone(deployed_app.static_folder)
                with deployed_app.test_request_context():
                    self.assertEqual(
                        app.url_for("static", filename="styles.css"),
                        "/static/styles.css",
                    )
        finally:
            importlib.reload(app)

    def test_site_logo_is_served(self):
        response = self.client.get("/static/logo.png")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/png")
        response.close()

    def test_contact_form_rejects_invalid_data(self):
        response = self.client.post(
            "/contato",
            data={**self.contact_data, "email": "invalido"},
            headers={"Accept": "application/json"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json["success"])

    def test_contact_form_reports_missing_resend_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post(
                "/contato",
                data=self.contact_data,
                headers={"Accept": "application/json"},
            )

        self.assertEqual(response.status_code, 503)
        self.assertFalse(response.json["success"])
        self.assertIn("não está configurado", response.json["message"])

    def test_contact_form_sends_email_when_resend_is_configured(self):
        resend_settings = {
            "RESEND_API_KEY": "re_test_key",
            "RESEND_FROM_EMAIL": "Prosa Tech <onboarding@resend.dev>",
            "CONTACT_RECIPIENT": "inbox@example.com",
        }
        with (
            patch.dict(os.environ, resend_settings, clear=True),
            patch("app.resend.Emails.send") as resend_send,
        ):
            response = self.client.post(
                "/contato",
                data=self.contact_data,
                headers={"Accept": "application/json"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])
        resend_send.assert_called_once()
        payload = resend_send.call_args.args[0]
        self.assertEqual(payload["from"], resend_settings["RESEND_FROM_EMAIL"])
        self.assertEqual(payload["to"], ["inbox@example.com"])
        self.assertEqual(payload["reply_to"], self.contact_data["email"])
        self.assertIn("Nome:</strong> Carol Santos", payload["html"])
        self.assertIn("carol@example.com", payload["html"])
        self.assertIn("conversar sobre uma parceria", payload["html"])

    def test_contact_email_escapes_html_content(self):
        resend_settings = {
            "RESEND_API_KEY": "re_test_key",
            "RESEND_FROM_EMAIL": "Prosa Tech <onboarding@resend.dev>",
            "CONTACT_RECIPIENT": "inbox@example.com",
        }
        with (
            patch.dict(os.environ, resend_settings, clear=True),
            patch("app.resend.Emails.send") as resend_send,
        ):
            response = self.client.post(
                "/contato",
                data={**self.contact_data, "name": "<script>alert(1)</script>"},
                headers={"Accept": "application/json"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("<script>", resend_send.call_args.args[0]["html"])
        self.assertIn("&lt;script&gt;", resend_send.call_args.args[0]["html"])

    def test_contact_form_reports_resend_api_error(self):
        resend_settings = {
            "RESEND_API_KEY": "re_test_key",
            "RESEND_FROM_EMAIL": "Prosa Tech <onboarding@resend.dev>",
            "CONTACT_RECIPIENT": "inbox@example.com",
        }
        with (
            patch.dict(os.environ, resend_settings, clear=True),
            patch(
                "app.resend.Emails.send",
                side_effect=ResendError(
                    code=403,
                    error_type="validation_error",
                    message="Test rejection",
                    suggested_action="Check Resend settings",
                ),
            ),
        ):
            response = self.client.post(
                "/contato",
                data=self.contact_data,
                headers={"Accept": "application/json"},
            )

        self.assertEqual(response.status_code, 502)
        self.assertFalse(response.json["success"])


if __name__ == "__main__":
    unittest.main()
