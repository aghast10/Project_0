'''2. Funciones avanzadas (lambda, map, filter, reduce).
Caso práctico: Escribe un script que tome una lista numérica de precios de productos, 
aplique un impuesto fijo usando funciones lambda y map, 
filtre los precios superiores a 3 con filter, 
y calcule el total usando reduce.'''

products = [
    {"nombre": "manzana", "precio": 1},
    {"nombre": "pan", "precio": 1.5},
    {"nombre": "leche", "precio": 1.2},
    {"nombre": "arroz", "precio": 2.0},
    {"nombre": "huevos", "precio": 2.5},
    {"nombre": "pollo", "precio": 5.5},
    {"nombre": "carne molida", "precio": 6.0},
    {"nombre": "pasta", "precio": 1.3},
    {"nombre": "queso", "precio": 3.2},
    {"nombre": "aceite", "precio": 4.0},
    {"nombre": "azúcar", "precio": 1.8},
    {"nombre": "sal", "precio": 0.8},
    {"nombre": "papel higiénico", "precio": 3.5},
    {"nombre": "detergente", "precio": 4.5},
    {"nombre": "café", "precio": 3.8}
]

precios = list(map(lambda p: p["precio"], products))
precios_con_iva = list(map(lambda p:p+p/10, precios))
precios_filtrados = list(filter(lambda p: p>3,precios_con_iva))
print(precios_filtrados)

from functools import reduce
total_filtrados = reduce(lambda a,b: a+b, precios_filtrados)
print(total_filtrados)

taxed_products=[]
'''actualiza en una lista de diccionario los nuevos precios con IVA'''
for i, product in enumerate(products):
    for j, coniva in enumerate(precios_con_iva):
        if i == j:
            taxed_products.append({"nombre": product["nombre"], "precio": coniva})
            continue
for product in taxed_products:
    print(f"{product["nombre"]} -- precio: {product["precio"]}")
