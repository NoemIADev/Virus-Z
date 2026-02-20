# # import requests

# def get_server_status(server_id):
#     response = requests.get(f"http://monitoring-api/servers/{server_id}")
#     return response.json()


import requests

def get_cases_count():
    response = requests.get("http://fastapi_service:8000/cases/count")
    return response.json()["count"]

