from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # debe coincidir con la variable de Render

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.json
    destinatario = data["email"]
    asunto = data["subject"]
    html = data["html"]

    msg = MIMEText(html, "html")
    msg["Subject"] = asunto
    msg["From"] = SMTP_USER
    msg["To"] = destinatario

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return jsonify({"status": "ok"})
    except Exception as e:
        print("Error SMTP:", e)  # se ve en los logs de Render
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)