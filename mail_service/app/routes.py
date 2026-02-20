from flask import request, jsonify
from service import check_and_send_alert

def register_routes(app):

    @app.route("/alerte", methods=["POST"])
    def alerte():
        check_and_send_alert()
        return jsonify({"status": "ok"})