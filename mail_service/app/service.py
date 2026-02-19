import requests
from alertedb import get_last_state, update_state, get_all_subscribers
from mailer import send_mail

ORANGE_SEUIL = 10
ROUGE_SEUIL = 20
FASTAPI_URL = "http://localhost:8000/cases/count"  # ton API FastAPI

def check_and_send_alert():
    try:
        response = requests.get(FASTAPI_URL)
        response.raise_for_status()
        count = response.json().get("count", 0)  # <- c’est le count réel de la table cas
    except Exception as e:
        print("Erreur API FastAPI:", e)
        return

    # Détermination du nouvel état
    if count >= ROUGE_SEUIL:
        new_state = "ROUGE"
    elif count >= ORANGE_SEUIL:
        new_state = "ORANGE"
    else:
        new_state = "NORMAL"

    # Vérifier si l'état a changé
    last_state = get_last_state()
    if new_state != last_state:
        print(f"Changement de statut : {last_state} -> {new_state}")
        update_state(count, new_state)

        # Envoyer un mail à tous les abonnés
        subscribers = get_all_subscribers()
        if subscribers:
            message = f"⚠️ État du virus : {new_state}\nNombre de cas : {count}"
            send_mail(message, subscribers)