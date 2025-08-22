#
# 5. Special Methods 
# Task: Smart Book Object
# Create a Book class with title, author, pages.
# Implement:
#   __str__ → represents the book as a string.
#   __len__ → returns number of pages.
#   __eq__ → compares books by title and author.#
# Goal: Customize object behavior with special (magic) methods.
#

class Book:
    def __init__(self, title, author, pages) -> None:
        self.title = title
        self.author = author
        self.pages = pages
    def __str__(self) -> str:
        return f"{self.title}"
    def __len__(self):
        return len(self.pages)
    def __eq__(self, other) -> bool:
        return self.title == other.title and self.author == other.author
        #un objeto sera igual a otro si coinciden en titulo y author simultáneamente.

book1 = Book("Juego de Tronos", "George R.R. Martin", [1,2,3,4,5,6,7,8,9,10])
book2 = Book("Harry Potter", "J.K. Rowling", [1,2,3,4,5,6,7,8,9,10,11])
print (book1)
print(len(book1))
print (book1 == book2)