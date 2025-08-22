from file_manager import saving_tasks, tasks
from datetime import datetime

def printed_menu():
    menu = ["---MENU---",
            "1. Ver tareas",
            "2. Añadir tareas",
            "3. Eliminar tarea",
            "4. Salir"
            ]
    for opcion in menu: print(opcion)

def choices():
    opciones = {
        "1": see_task,
        "2": add_task,
        "3": delete_task
    }

    choice = ""
    while choice != "4":
        choice = input("Elige una opción: ")
        accion = opciones.get(choice) #opciones.get(choice) selecciona el elemento del diccionario si este existe
        if choice == "4":
            print("Has salido.")
        elif accion: #si opciones(choice) existe:
            accion() #si por ejemplo accion equivale a opciones("1"), entonces accion = see_task, y accion() = see_task()
            printed_menu()
        else:
            print("Opción no válida. Inténtalo de nuevo.")
 
def see_task():
    if len(tasks) == 0:
        print("-------")
        print("No hay ninguna tarea guardada. selecciona otra opción")       
    print_tasks(tasks)
    print("Selecciona el numero de la tarea a completar. Si no, pulsa enter: ")
    completed_task = input()
    while completed_task != "":
        try: 
            tasks[int(completed_task)-1]["status"] = "Completada"
            saving_tasks()
            print("Tarea completada")
            break
        except (ValueError,IndexError): 
            print("Selecciona una opción válida")
            completed_task = input()
    print("-------")
    filter_tasks()

def filter_tasks():
    completed_tasks = list(filter(lambda x: x["status"] == "Completada", tasks))
    not_completed_tasks = list(filter(lambda x: x["status"] == "No Completada", tasks))
    ordered_tasks = sorted(tasks, key=lambda t: datetime.strptime(t["deadline"], "%d/%m/%Y"))
    print("Filtrar por Completadas:'c', Filtrar por No completadas: 'nc', Ordenar por fecha límite: 'o', Salir a menu: Enter")
    
    opciones = {
        "c": completed_tasks,
        "nc": not_completed_tasks,
        "o": ordered_tasks,
    }
    
    user_filter_choice = "001"
    while user_filter_choice != "":
        user_filter_choice = input("Elige una opción: ")
        accion = opciones.get(user_filter_choice)
        if accion: #si opciones(user_filter choice) existe:
            print_tasks(accion) 
        elif user_filter_choice == "":
            print("volviendo al menú inicial")
        else:
            print("Opción no válida. Inténtalo de nuevo.")

def print_tasks(n):
    for i, task in enumerate(n):
        print (f"{i+1}. {task["title"]} -- {task["description"]} -- A completar antes del {task["deadline"]} --({task["status"]})")

def add_task():
    task_title = input("Escribe una nueva tarea: ")
    task_description = input("Escribe una descripción de la tarea: ")
    while True:
        date_input = input("Escribe la fecha limite para completar esta tarea, en formato dd-mm-aaaa (guiones incluidos): ")
        try: 
            task_deadline = datetime.strptime(date_input, "%d-%m-%Y").strftime("%d/%m/%Y") #strptime toma la fecha del string si esta en el formato indicado. strftime la mostrara en el formato indicado.
            break
        except ValueError:
            print ("Ingrese una fecha válida en formato dd-mm-aaaa (guiones incluidos)")

    tasks.append({"title": task_title, "description": task_description, "deadline": task_deadline, "status": "No Completada"}) #añade bibliotecas a la lista tasks
    saving_tasks()
    print ("Tarea añadida. Volviendo al menú inicial")
    print("-------")
    print ("Selecciona una nueva opción.")

def delete_task():
    while True: #bucle infinito hasta que no se especifique un break que lo haga salir
        if tasks ==[]:
            print("Ninguna tarea disponible para eliminar. volviendo al menú principal")
            break
        try:
            to_delete = input("Selecciona el número de la tarea a eliminar y pulse Enter:")
            try:
                tasks.pop(int(to_delete)-1)
            except ValueError:
                print("Valor inválido. Por favor, seleccione un número válido")
                continue
            saving_tasks()
            print ("Tarea eliminada. Seleccione una nueva opción")
            break #para salir del bucle. solo sale si se selecciona una opcion valida.
        except IndexError:
            print("Valor inválido. Por favor, seleccione un número válido")

if __name__ == "__main__":
    tasks = [{"title": "correr", "description": "correr 100m", "deadline": "02/11/2025", "status": "Completada"}, {"title": "fumar mucho", "description": "fumar mucho mucho", "deadline": "02/03/2026", "status": "No Completada"},{"title": "gritar", "description": "gritR 100m", "deadline": "02/11/2027", "status": "Completada"}]
    printed_menu()
    choices()
    while len(tasks) != 0:
        tasks.pop(len(tasks)-1)
    saving_tasks()
