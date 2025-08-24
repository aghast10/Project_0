# 
# Crea una tabla productos con campos id, nombre, precio, stock.
# Inserta al menos 5 registros con datos variados.
# Lista todos los productos.
# Actualiza el precio de uno de ellos y disminuye su stock.
# Elimina un producto cuyo stock sea 0.
#

import sqlite3
import os
# Carpeta donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tienda.db")
# Crea (o abre) la base de datos tienda.db

conn = sqlite3.connect(db_path)

conn.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio INTEGER NOT NULL,
    stock INTEGER NOT NULL
);
""")

conn.close()
