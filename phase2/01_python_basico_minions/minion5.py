'''5. Manejo avanzado de archivos (archivos binarios, CSV, JSON)
Caso práctico: Implementa un script que guarde información de usuarios (nombre, edad, email) en formato CSV. 
Luego, carga estos datos y guárdalos en formato JSON. 
Finalmente, crea una copia binaria de este archivo JSON para respaldos eficientes y seguros.'''
import csv
import json
import os
import pickle

user_info = []
if os.path.exists("minion5.csv"):
    with open('minion5.csv', newline='') as f:
        reader = csv.DictReader(f)
        user_info = [row for row in reader]

while True:
    name = input("name: ")
    age = input("age: ")
    email = input("email: ")
    user_info.append({"name": name, "age": age, "email": email})
    if email == "":
        user_info.pop()
        break

with open('minion5.csv', 'w', newline='') as f:
    campos = ['name', 'age', 'email']
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    for i in user_info:
        writer.writerow(i)

with open('minion5.csv', newline='') as f:
    reader = csv.DictReader(f)
    loaded_user = [row for row in reader]
    with open("minion5.json", "w", encoding="utf-8") as f:
        json.dump(loaded_user, f, indent=4, ensure_ascii=False)

with open("minion5.dat", "wb") as f:
    pickle.dump(loaded_user, f)

with open("minion5.dat", "rb") as f:
    datos_recuperados = pickle.load(f)
    print(datos_recuperados)