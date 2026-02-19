from flask import request, jsonify
from service import envoyer_alerte

def register_routes(app):

    @app.route("/alerte", methods=["POST"])
    def alerte():
        data = request.json
        envoyer_alerte(data)
        return jsonify({"status": "ok"})