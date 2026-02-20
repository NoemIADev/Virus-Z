# routes.py
from flask import jsonify
from service import check_and_send_alert
from mailer import send_mail

def register_routes(app):

    @app.route("/alerte", methods=["POST"])
    def alerte():
        check_and_send_alert()
        return jsonify({"status": "ok"})

    @app.route("/test-email", methods=["POST"])
    def test_email():
        send_mail("Coucou, mail OK", ["sakura93100@gmail.com"])
        return jsonify({"sent": True})
