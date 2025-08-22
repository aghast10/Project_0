'''4. Gestión de excepciones (try, except, finally, raise)
Caso práctico: Crea una función para leer números enteros introducidos por el usuario, 
gestionando adecuadamente posibles errores (entrada no numérica o valores fuera de rango), 
y obligando al usuario a reintentar hasta proporcionar una entrada válida mediante 
excepciones personalizadas.'''

def int_reader():
    class OutofIndex(Exception):
        pass
    while True:
        try:
            user_number = int(input("Por favor, teclee un número entero de 0 a 100: "))
            if user_number in range(0,101):
                return f"su número es {user_number}"
            raise OutofIndex
        
        except ValueError:
            print ("Error. Sólo se puede introducir números enteros")

        except OutofIndex:
            print ("Error. número fuera de rango")

        finally:
            print("Gracias!")

print(int_reader())