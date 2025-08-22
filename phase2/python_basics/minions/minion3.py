"""3. Generadores y comprensión de listas avanzadas
Desarrolla un generador que produzca secuencias de números primos 
hasta un valor máximo dado. Además, genera una lista que contenga sus cuadrados utilizando 
comprensión de listas avanzada."""

maxnum = 13

def generador_primo():
    for i in range(2, maxnum + 1):
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            yield i

'''else puede usarse con for en lugar de if. 
la condicion else solo se ejecuta si no se salio del bucle for mediante un break.'''

primos = [i for i in generador_primo()]
primo_cuadrados = [i**2 for i in generador_primo()]

print(primos)
print(primo_cuadrados)

