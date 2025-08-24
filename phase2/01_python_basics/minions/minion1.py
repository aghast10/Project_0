"""1. Simulador de gestión de estudiantes y calificaciones. 
Crea un programa de consola que permita: Agregar estudiantes con su nombre y un identificador único. 
Registrar múltiples calificaciones por estudiante. Calcular y mostrar el promedio de cada uno. 
Mostrar el ranking de estudiantes por promedio."""

students=[]

student_name = ""
while student_name != "exit":
    student_name = input("ingese el nombre del estudiante, o escriba 'exit' para salir: ")
    if student_name == "exit" or student_name == "":
        break
    try:
        math_score = int(input("escriba del 0 al 10 la calificación de matemáticas: "))
        english_score = int(input("escriba del 0 al 10 la calificación de inglés: "))
        sports_score = int(input("escriba del 0 al 10 la calificación de deportes: "))
        average = float(math_score + english_score + sports_score) / 3
        id = len(students)+1
        if math_score not in range(0,11) or english_score not in range(0,11) or sports_score not in range(0,11):
            print("Valores no válidos. por favor, inserte una calificación entre 0 y 10")
        else:
            students.append({"id": id, "name": student_name, "math score": math_score, "english_score": english_score,"sports score": sports_score, "promedio": average})
            for i, student in enumerate(students):
                print (student["name"])
                print(f"Id: {student["id"]}. -- {student["name"]}. math score: {student['math score']}. english score: {student['english_score']}. sports score: {student["sports score"]}. Calificación promedio: {student["promedio"]}")
        print("----------")
        print("RANKING DE ESTUDIANTES")
        ordered_students = sorted(students, key=lambda g: g["promedio"], reverse = True)
        for i, student in enumerate(ordered_students):
            print(f"Id: {student["id"]}. -- {student["name"]}. math score: {student['math score']}. english score: {student['english_score']}. sports score: {student["sports score"]}. Calificación promedio: {student["promedio"]}")
    except ValueError:
        print("por favor, intentelo de nuevo con un número válido")
