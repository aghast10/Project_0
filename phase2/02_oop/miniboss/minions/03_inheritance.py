'''3. Inheritance
Task: Vehicle System
Base class: Vehicle with brand, model, start().
Subclasses:
    Car → method honk()
    Motorcycle → method wheelie()
Create instances and test shared and extended behavior.'''

class Vehicle:
    def __init__(self, brand, model) -> None:
        self.brand = brand
        self.model = model
    def start(self):
        return f"{self.brand} {self.model} ha arrancado."

class Car(Vehicle):
    def honk(self) -> str:
        return "HONK"

class Motorcycle(Vehicle):
    def wheelie(self) -> str:
        return "wheelie!"

car1 = Car("toyota","prius")
motorbike1 = Motorcycle("kawasaki", "ninja")

print(car1.model)
print(car1.honk())
print(motorbike1.wheelie())
print(car1.start())