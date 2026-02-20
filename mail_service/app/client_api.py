# # import requests

# def get_server_status(server_id):
#     response = requests.get(f"http://monitoring-api/servers/{server_id}")
#     return response.json()


import requests

def get_cases_count():
    response = requests.get("http://127.0.0.1:8000/cases/count")
    return response.json()["count"]

