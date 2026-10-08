import html
import json
import os
import re

from flask import Flask, jsonify, redirect, render_template, request, url_for
from dotenv import load_dotenv
import resend
from resend.exceptions import ResendError


load_dotenv()
resend.api_key = os.environ.get("RESEND_API_KEY")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
ALLOWED_SUBJECTS = {
    "",
    "consultoria",
    "parceria",
    "palestra",
    "duvida",
    "outro",
}


@app.get("/")
def index():
    contact_status = request.args.get("contato")
    if contact_status not in {"sent", "error"}:
        contact_status = None
    return render_template("index.html", contact_status=contact_status)


def contact_response(success, message, status_code):
    if request.accept_mimetypes.best == "application/json":
        return jsonify(success=success, message=message), status_code

    status = "sent" if success else "error"
    return redirect(f"{url_for('index', contato=status)}#contato", code=303)


@app.post("/contato")
def contact():
    name = request.form.get("name", "").strip()
    sender = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    body = request.form.get("message", "").strip()

    if (
        not 2 <= len(name) <= 100
        or len(sender) > 254
        or not EMAIL_PATTERN.fullmatch(sender)
        or subject not in ALLOWED_SUBJECTS
        or not 10 <= len(body) <= 5000
    ):
        return contact_response(
            False,
            "Confira seu nome, e-mail e mensagem antes de tentar novamente.",
            400,
        )

    api_key = os.environ.get("RESEND_API_KEY")
    sender_address = os.environ.get("RESEND_FROM_EMAIL")
    recipient = os.environ.get("CONTACT_RECIPIENT")
    if not all((api_key, sender_address, recipient)):
        app.logger.error("Contact form email is unavailable: Resend settings are incomplete")
        return contact_response(
            False,
            "O envio de e-mail ainda não está configurado. Tente novamente mais tarde ou use o WhatsApp.",
            503,
        )

    escaped_name = html.escape(name)
    escaped_sender = html.escape(sender)
    escaped_body = html.escape(body).replace("\n", "<br>")
    email_payload = {
        "from": sender_address,
        "to": [recipient],
        "reply_to": sender,
        "subject": f"Contato do portfólio: {subject or 'Novo contato'}",
        "html": (
            f"<p><strong>Nome:</strong> {escaped_name}</p>"
            f"<p><strong>E-mail:</strong> {escaped_sender}</p>"
            f"<p>{escaped_body}</p>"
        ),
    }

    try:
        resend.api_key = api_key
        resend.Emails.send(email_payload)
    except ResendError:
        app.logger.exception("Unable to deliver contact form email through Resend")
        return contact_response(
            False,
            "Não foi possível enviar sua mensagem agora. Tente novamente ou use o WhatsApp.",
            502,
        )

    return contact_response(
        True,
        "Mensagem enviada com sucesso! Obrigada pelo contato.",
        200,
    )


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
