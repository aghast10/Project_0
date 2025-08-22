'''Task: Simple Product Manager
Create a Product class with attributes: name, price, stock.
Add methods:
show_info() → prints name and price.
update_stock(quantity) → adds/subtracts stock.
🎯 Goal: Understand how to define and use classes and objects.'''

class coche:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
    def show_info(self):
        print (f"modelo: {self.nombre}, precio: {self.precio}, unidades en stock: {self.stock}")
    def update_stock(self):
        self.stock -= int(input("indique cuantas unidades añadir o sustraer al stock actual: "))

kia_ceed = coche("kia ceed", 15000, 5)       
kia_ceed.show_info()
kia_ceed.update_stock()
kia_ceed.show_info()