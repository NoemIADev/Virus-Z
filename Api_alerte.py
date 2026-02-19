from flask import Flask
from flask_mail import Mail, Message
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_DEFAULT_SENDER'] = 'alert@poc.local'

mail = Mail(app)

@app.route("/")
def send_email():
    msg = Message(
        subject="Hello",
        recipients=["recipient@example.com"],
        body="This is a test email sent from Flask-Mail!"
    )
    mail.send(msg)
    return "Email sent successfully!"

# 👉 Conversion WSGI → ASGI
asgi_app = WsgiToAsgi(app)

