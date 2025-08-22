# 🏭 7. Factory Pattern
# Task: Animal Creator
# Create an AnimalFactory class with a method create_animal(type).
# Return instances of classes like Dog, Cat, Bird based on the requested type.
# Each animal has a different make_sound() method.
# 🎯 Goal: Understand how to dynamically create objects based on input.

class Dog:
    def make_sound(self):
        return "Guau"
class Cat:
    def make_sound(self):
        return "Miau"
class Bird:
    def make_sound(self):
        return "Pio"

class AnimalFactory:
    def create_animal(self, type):
        if type == "dog":
            return Dog()
        elif type == "cat":
            return Cat()
        elif type == "bird":
            return Bird()
        else:
            raise ValueError("Unknown animal")

factory = AnimalFactory()
animal1 = factory.create_animal("dog")
print(animal1.make_sound()) 