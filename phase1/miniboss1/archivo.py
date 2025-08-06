import os, json
with open("memory.json", "r", encoding="utf-8") as f:
    tasks = json.load(f) #aquí se guardan las tareas que el usuario anote

def saving_tasks():
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f,ensure_ascii=False) #ensure_ascii=False hace que los caracteres especiales se guarden bien en el json

if __name__ == "__main__":#solo se ejecuta si estoy ejecutando el archivo directamente. util para pruebas
    print(tasks)