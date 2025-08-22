#
# Conceptos: HTTP básico (GET/POST, headers, query params), requests, status codes, timeout.
# Misiones:
# Petición GET con params y headers.
# Comprobar status_code y elapsed.
# Añadir timeout y capturar Timeout.
# Entregable: 01_ping_oraculo.py imprime OK si responde < 500 ms y REINTENTAR si no.
#
import requests
import json
import os 


if os.path.exists('phase2/04_api_requests/01_tarea_requests.json'):
    with open('phase2/04_api_requests/01_tarea_requests.json',"r", encoding="utf-8") as f:
            tasks = json.load(f)
else:
     tasks = []

url = " https://api.agify.io"  # endpoint seguro para pruebas
check = ""
name = input("indique nombre: ")
country_id = input("indique código de país: ")
if country_id == "":
     country_id = None
     
while check == "":
    try:
        r = requests.get(url, params={"name": name, "country_id":country_id}, 
                         headers = {"Accept": "application/json"},
                         timeout=0.5)
        check = "ok"
        print("OK")
        print (r.json())
        print(r.status_code)
        print("Remaining:", r.headers.get("X-Rate-Limit-Remaining"))
        if r.json() not in tasks:
            tasks.append(r.json())
            with open("phase2/04_api_requests/01_tarea_requests.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=4, ensure_ascii=False)
    except requests.exceptions.Timeout:
        print("La petición tardó demasiado y fue cancelada")
        print ("REINTENTAR")