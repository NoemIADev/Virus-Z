from flask import Flask
from routes import register_routes
from alertedb import init_db
from service import check_and_send_alert
import threading
import time

init_db()
app = Flask(__name__)
register_routes(app)

# Scheduler pour vérifier toutes les 10 minutes
def alert_scheduler():
    while True:
        check_and_send_alert()
        time.sleep(60)  # toutes les 10 minutes

threading.Thread(target=alert_scheduler, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)